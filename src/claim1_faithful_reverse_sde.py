#!/usr/bin/env python3
"""Faithful one-dimensional numerical approximation to Algorithm 1."""
from __future__ import annotations

import json
import math
import multiprocessing as mp
import os
import platform
import subprocess
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch" / "artifacts" / "claim1_route2_reverse_sde"
N_VALUES = [256, 1024, 4096, 16384]
SEEDS = list(range(20261001, 20261017))
CALIBRATION_SEEDS = SEEDS[:8]
MAIN_STEPS = 768
GENERATED = 8192


def read_limit(path: str) -> str:
    file = Path(path)
    return file.read_text().strip() if file.exists() else "unavailable"


def cpu_limit() -> float | str:
    value = read_limit("/sys/fs/cgroup/cpu.max")
    if value == "unavailable" or value.startswith("max"):
        return value
    quota, period = value.split()
    return int(quota) / int(period)


def exact_empirical_w1(samples: np.ndarray) -> float:
    ordered = np.sort(samples)
    target_quantiles = np.ones(len(ordered))
    target_quantiles[: len(ordered) // 2] = -1.0
    return float(np.mean(np.abs(ordered - target_quantiles)))


def simulate(task: tuple[str, int, int, int, float, str]) -> dict:
    group, n, seed, steps, horizon_factor, score_mode = task
    training_rng = np.random.default_rng(seed)
    plus_count = int(training_rng.binomial(n, 0.5))
    minus_count = n - plus_count

    path_rng = np.random.default_rng(seed + 10_000_019 * n)
    half = GENERATED // 2
    initial = path_rng.normal(size=half)
    y = np.concatenate([initial, -initial])

    end_time = horizon_factor * math.log(n)
    early_stop = n**-2.0
    forward_times = np.geomspace(end_time, early_stop, steps + 1)
    thresholded = 0
    clipped = 0
    observations = steps * GENERATED

    log_plus = math.log(plus_count / n) if plus_count else -math.inf
    log_minus = math.log(minus_count / n) if minus_count else -math.inf
    for index in range(steps):
        forward_time = float(forward_times[index])
        delta = forward_time - float(forward_times[index + 1])
        c = math.exp(-forward_time)
        variance = -math.expm1(-2.0 * forward_time)

        if score_mode == "paper_kde":
            h = variance / (c * c)
            z = y / c
            plus_logit = log_plus - (z - 1.0) ** 2 / (2.0 * h)
            minus_logit = log_minus - (z + 1.0) ** 2 / (2.0 * h)
            maximum = np.maximum(plus_logit, minus_logit)
            plus_weight = np.exp(plus_logit - maximum)
            minus_weight = np.exp(minus_logit - maximum)
            denominator = plus_weight + minus_weight
            posterior_mean = (plus_weight - minus_weight) / denominator
            low_score = -(z - posterior_mean) / h

            log_density = maximum + np.log(denominator) - 0.5 * math.log(2.0 * math.pi * h)
            log_threshold = math.log(math.log(n)) - math.log(n) - 0.5 * math.log(2.0 * math.pi * h)
            active = log_density >= log_threshold
            thresholded += int(np.count_nonzero(~active))
            low_score = np.where(active, low_score, 0.0)

            clipping_radius = math.sqrt(2.0 * math.log(n) / h)
            needs_clip = np.abs(low_score) > clipping_radius
            clipped += int(np.count_nonzero(needs_clip))
            low_score = np.clip(low_score, -clipping_radius, clipping_radius)
            score = low_score / c
        elif score_mode == "standard_normal":
            score = -y
        else:
            raise ValueError(score_mode)

        noise_half = path_rng.normal(size=half)
        noise = np.concatenate([noise_half, -noise_half])
        y += (y + 2.0 * score) * delta + math.sqrt(2.0 * delta) * noise
        if not np.isfinite(y).all():
            raise FloatingPointError("nonfinite reverse-SDE path")

    return {
        "group": group,
        "N": n,
        "seed": seed,
        "steps": steps,
        "horizon_factor": horizon_factor,
        "score_mode": score_mode,
        "generated_samples": GENERATED,
        "plus_count": plus_count,
        "empirical_plus_weight": plus_count / n,
        "T": end_time,
        "tau": early_stop,
        "w1": exact_empirical_w1(y),
        "generated_mean": float(np.mean(y)),
        "thresholded_fraction": thresholded / observations if score_mode == "paper_kde" else None,
        "clipped_fraction": clipped / observations if score_mode == "paper_kde" else None,
    }


def mean_ci(values: list[float], critical: float) -> dict:
    array = np.asarray(values, dtype=float)
    standard_error = float(array.std(ddof=1) / math.sqrt(len(array)))
    mean = float(array.mean())
    return {
        "mean": mean,
        "sd": float(array.std(ddof=1)),
        "ci95_low": mean - critical * standard_error,
        "ci95_high": mean + critical * standard_error,
        "values": list(map(float, array)),
    }


start = time.perf_counter()
tasks: list[tuple[str, int, int, int, float, str]] = []
for n in N_VALUES:
    tasks.extend(("main", n, seed, MAIN_STEPS, 1.0, "paper_kde") for seed in SEEDS)
for steps in (192, 384):
    tasks.extend(("refinement", 4096, seed, steps, 1.0, "paper_kde") for seed in CALIBRATION_SEEDS)
for factor in (0.5, 1.5):
    tasks.extend(("horizon", 4096, seed, MAIN_STEPS, factor, "paper_kde") for seed in CALIBRATION_SEEDS)
tasks.extend(
    ("wrong_score_control", 16384, seed, MAIN_STEPS, 1.0, "standard_normal")
    for seed in CALIBRATION_SEEDS
)

with mp.get_context("fork").Pool(processes=8) as pool:
    rows = pool.map(simulate, tasks)

main_cells = []
for n in N_VALUES:
    selected = [row["w1"] for row in rows if row["group"] == "main" and row["N"] == n]
    main_cells.append({"N": n, **mean_ci(selected, 2.131)})

refinement = {}
for steps in (192, 384):
    selected = [row["w1"] for row in rows if row["group"] == "refinement" and row["steps"] == steps]
    refinement[str(steps)] = mean_ci(selected, 2.365)
selected = [
    row["w1"]
    for row in rows
    if row["group"] == "main" and row["N"] == 4096 and row["seed"] in CALIBRATION_SEEDS
]
refinement[str(MAIN_STEPS)] = mean_ci(selected, 2.365)

horizons = {}
for factor in (0.5, 1.5):
    selected = [row["w1"] for row in rows if row["group"] == "horizon" and row["horizon_factor"] == factor]
    horizons[str(factor)] = mean_ci(selected, 2.365)
horizons["1.0"] = refinement[str(MAIN_STEPS)]

control_values = [row["w1"] for row in rows if row["group"] == "wrong_score_control"]
control = mean_ci(control_values, 2.365)
nmax_mean = main_cells[-1]["mean"]
slope = float(
    np.polyfit(
        np.log([cell["N"] for cell in main_cells]),
        np.log([cell["mean"] for cell in main_cells]),
        1,
    )[0]
)

record = {
    "claim": 1,
    "route": 2,
    "route_status": "SCOPED_CORROBORATION_UNIVERSAL_THEOREM_BLOCKED",
    "configuration": {
        "target": "Rademacher distribution, uniform on {-1,+1}",
        "d": 1,
        "M": 1,
        "k": 1,
        "sample_sizes": N_VALUES,
        "seeds": SEEDS,
        "steps": MAIN_STEPS,
        "generated_samples_per_seed": GENERATED,
        "score_estimator": "paper one-dimensional Gaussian KDE, density threshold, and tangent clipping, with duplicate samples aggregated exactly",
        "sampler": "Algorithm 1 reverse OU SDE approximated on a geometric forward-time grid",
        "metric": "exact one-dimensional W1 between each generated empirical measure and the target law",
    },
    "assumption_checks": {
        "support_in_one_dimensional_linear_subspace": True,
        "intersection_condition": "vacuous for M=1",
        "component_mass": 1.0,
        "bounded_support": True,
        "sigma_squared": 1.0 / math.log(2.0),
        "worst_direction_exponential_square_moment": 2.0,
        "exact_recovery": "trivial supplied V=R special case",
    },
    "main_cells": main_cells,
    "log_log_N_slope": slope,
    "step_refinement": refinement,
    "horizon_calibration": horizons,
    "wrong_score_control": control,
    "wrong_score_control_ratio_at_Nmax": control["mean"] / nmax_mean,
    "rows": rows,
    "non_circularity": "The geometric N sweep, 16 seeds, sample budget, 768-step main grid, refinement levels, and horizon factors were committed before results. T and tau follow the named algorithm rather than a first-hit search.",
    "limitation": "This is a faithful d=M=k=1 numerical approximation with trivial recovery. Finite Euler evidence cannot verify the universally quantified idealized continuous-time theorem.",
}
record["environment"] = {
    "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "python": platform.python_version(),
    "numpy": np.__version__,
    "selected_flavor": "cpu-upgrade",
    "cpu_limit": cpu_limit(),
    "cpu_affinity_count": len(os.sched_getaffinity(0)),
    "workers": 8,
    "memory_limit_bytes": read_limit("/sys/fs/cgroup/memory.max"),
    "accelerator": None,
    "runtime_seconds": time.perf_counter() - start,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "raw_results.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
print(json.dumps(record, indent=2, sort_keys=True))
