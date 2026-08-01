#!/usr/bin/env python3
"""Paper-scale atomic-target test of the claimed weak regularity scope."""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import subprocess
import tarfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch" / "artifacts" / "claim4_atomic_weak_regularity"
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"
D = 48
M = 128
K = 3
ATOMS_PER_COMPONENT = 2 * K
SAMPLE_SIZES = (6250, 12500, 25000, 50000)
SEEDS = tuple(range(20264001, 20264021))
EVALUATION_SAMPLES = 10000
DIFFUSION_TIME = 0.25
BASIS_SEED = 260530153
REGULARIZATION_CONSTANT = 4.0
T_CRITICAL_95 = 2.093


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def member_text(member: str) -> str:
    with tarfile.open(SOURCE) as archive:
        extracted = archive.extractfile(member)
        if extracted is None:
            raise RuntimeError(f"missing {member}")
        return extracted.read().decode()


def read_limit(path: str) -> str:
    file = Path(path)
    return file.read_text().strip() if file.exists() else "unavailable"


def cpu_limit() -> float | str:
    value = read_limit("/sys/fs/cgroup/cpu.max")
    if value == "unavailable" or value.startswith("max"):
        return value
    quota, period = value.split()
    return int(quota) / int(period)


def interval(values: list[float]) -> tuple[float, float, float]:
    array = np.asarray(values, dtype=np.float64)
    mean = float(np.mean(array))
    half_width = T_CRITICAL_95 * float(np.std(array, ddof=1)) / math.sqrt(len(array))
    return mean, mean - half_width, mean + half_width


def make_geometry() -> tuple[np.ndarray, np.ndarray, np.ndarray, float]:
    rng = np.random.default_rng(BASIS_SEED)
    bases = np.stack(
        [np.linalg.qr(rng.normal(size=(D, K)))[0] for _ in range(M)]
    )
    latent_atoms = np.zeros((ATOMS_PER_COMPONENT, K), dtype=np.float64)
    for coordinate in range(K):
        latent_atoms[2 * coordinate, coordinate] = 1
        latent_atoms[2 * coordinate + 1, coordinate] = -1
    atoms = np.einsum("mdk,rk->mrd", bases, latent_atoms)
    maximum_overlap = 0.0
    for first in range(M):
        for second in range(first + 1, M):
            maximum_overlap = max(
                maximum_overlap,
                float(np.linalg.svd(bases[first].T @ bases[second], compute_uv=False)[0]),
            )
    return bases, latent_atoms, atoms, maximum_overlap


def evaluate_seed(
    seed: int,
    bases: np.ndarray,
    latent_atoms: np.ndarray,
    atoms: np.ndarray,
) -> dict[int, dict[str, float]]:
    rng = np.random.default_rng(seed)
    training_atoms = rng.integers(M * ATOMS_PER_COMPONENT, size=max(SAMPLE_SIZES))
    counts = {
        sample_count: np.bincount(
            training_atoms[:sample_count], minlength=M * ATOMS_PER_COMPONENT
        ).reshape(M, ATOMS_PER_COMPONENT)
        for sample_count in SAMPLE_SIZES
    }
    query_atoms = rng.integers(M * ATOMS_PER_COMPONENT, size=EVALUATION_SAMPLES)
    flat_atoms = atoms.reshape(M * ATOMS_PER_COMPONENT, D)
    queries = flat_atoms[query_atoms] + math.sqrt(DIFFUSION_TIME) * rng.normal(
        size=(EVALUATION_SAMPLES, D)
    )
    totals = {
        sample_count: {
            "error": 0.0,
            "broken_error": 0.0,
            "thresholded": 0.0,
            "excluded": 0.0,
            "min_component_count": float(np.min(np.sum(counts[sample_count], axis=1))),
        }
        for sample_count in SAMPLE_SIZES
    }
    atom_norm = np.sum(flat_atoms * flat_atoms, axis=1)
    for start in range(0, EVALUATION_SAMPLES, 128):
        query = queries[start : start + 128]
        distances = (
            np.sum(query * query, axis=1)[:, None]
            + atom_norm[None, :]
            - 2 * query @ flat_atoms.T
        )
        log_kernel = -np.maximum(distances, 0) / (2 * DIFFUSION_TIME)
        maximum = np.max(log_kernel, axis=1, keepdims=True)
        ambient_kernel = np.exp(log_kernel - maximum).reshape(
            len(query), M, ATOMS_PER_COMPONENT
        )
        truth_denominator = np.sum(ambient_kernel, axis=(1, 2))
        truth_mean = (
            ambient_kernel.reshape(len(query), -1) @ flat_atoms
        ) / truth_denominator[:, None]
        truth = (truth_mean - query) / DIFFUSION_TIME

        tangent_query = np.einsum("bd,mdk->bmk", query, bases)
        tangent_distances = (
            np.sum(tangent_query * tangent_query, axis=2)[:, :, None]
            + 1
            - 2 * np.einsum("bmk,rk->bmr", tangent_query, latent_atoms)
        )
        tangent_kernel = np.exp(
            -np.maximum(tangent_distances, 0) / (2 * DIFFUSION_TIME)
        )
        projection = np.einsum("bmk,mdk->bmd", tangent_query, bases)
        normal = query[:, None, :] - projection

        for sample_count in SAMPLE_SIZES:
            atom_counts = counts[sample_count]
            component_counts = np.sum(atom_counts, axis=1)
            weighted_tangent = tangent_kernel * atom_counts[None, :, :]
            tangent_denominator = np.sum(weighted_tangent, axis=2)
            tangent_mean = np.einsum(
                "bmr,rk->bmk", weighted_tangent, latent_atoms
            ) / tangent_denominator[:, :, None]
            low_score = (tangent_mean - tangent_query) / DIFFUSION_TIME
            density = (
                tangent_denominator
                / component_counts[None, :]
                / (2 * math.pi * DIFFUSION_TIME) ** (K / 2)
            )
            threshold = math.log(sample_count) / (
                sample_count * (2 * math.pi * DIFFUSION_TIME) ** (K / 2)
            )
            below = density < threshold
            low_score[below] = 0
            clipping_radius = math.sqrt(2 * math.log(sample_count) / DIFFUSION_TIME)
            low_norm = np.linalg.norm(low_score, axis=2)
            clip_scale = np.minimum(
                1, clipping_radius / np.maximum(low_norm, np.finfo(float).tiny)
            )
            low_score *= clip_scale[:, :, None]
            low_lift = np.einsum("bmk,mdk->bmd", low_score, bases)
            component_score = -normal / DIFFUSION_TIME + low_lift

            radius = REGULARIZATION_CONSTANT * math.sqrt(
                DIFFUSION_TIME
                * D
                * math.log(sample_count * D * DIFFUSION_TIME ** (K / 2))
            )
            regular = np.linalg.norm(normal, axis=2) <= radius
            weighted_ambient = ambient_kernel * atom_counts[None, :, :]
            component_weight = np.sum(weighted_ambient, axis=2)
            component_weight /= np.sum(component_weight, axis=1)[:, None]
            component_weight *= regular
            estimate = np.einsum("bm,bmd->bd", component_weight, component_score)
            broken = np.einsum("bm,bmd->bd", component_weight, low_lift)
            totals[sample_count]["error"] += float(
                np.sum(np.sum((estimate - truth) ** 2, axis=1))
            )
            totals[sample_count]["broken_error"] += float(
                np.sum(np.sum((broken - truth) ** 2, axis=1))
            )
            totals[sample_count]["thresholded"] += float(np.sum(below))
            totals[sample_count]["excluded"] += float(np.sum(~regular))

    return {
        sample_count: {
            "mse": totals[sample_count]["error"] / EVALUATION_SAMPLES,
            "omitted_normal_mse": totals[sample_count]["broken_error"]
            / EVALUATION_SAMPLES,
            "threshold_fraction": totals[sample_count]["thresholded"]
            / (EVALUATION_SAMPLES * M),
            "regularization_exclusion_fraction": totals[sample_count]["excluded"]
            / (EVALUATION_SAMPLES * M),
            "min_component_count": int(totals[sample_count]["min_component_count"]),
        }
        for sample_count in SAMPLE_SIZES
    }


start = time.perf_counter()
abstract = member_text("abstract.tex")
introduction = member_text("introduction.tex")
problem = member_text("problem_formulation.tex")
results_source = member_text("Results.tex")
source_checks = {
    "abstract_named_regularities": "without imposing smoothness, bounded-density, or log-concavity assumptions" in abstract,
    "introduction_no_score_or_density_restrictions": "without imposing any restrictive assumptions on scores or densities" in introduction,
    "bounded_support_is_subgaussian": "subsumes any distribution with bounded support" in problem,
    "both_theorems_only_assumptions_1_and_2": results_source.count(
        "Suppose the target distribution $p^\\star$ satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}."
    )
    == 2,
}
bases, latent_atoms, atoms, maximum_overlap = make_geometry()
seed_results = {str(seed): evaluate_seed(seed, bases, latent_atoms, atoms) for seed in SEEDS}

cells = []
for sample_count in SAMPLE_SIZES:
    values = [seed_results[str(seed)][sample_count]["mse"] for seed in SEEDS]
    controls = [
        seed_results[str(seed)][sample_count]["omitted_normal_mse"] for seed in SEEDS
    ]
    mean_mse, ci_low, ci_high = interval(values)
    cells.append(
        {
            "N": sample_count,
            "seed_mse": values,
            "seed_omitted_normal_mse": controls,
            "mean_mse": mean_mse,
            "ci95_low": ci_low,
            "ci95_high": ci_high,
            "mean_omitted_normal_mse": float(np.mean(controls)),
            "mean_threshold_fraction": float(
                np.mean(
                    [
                        seed_results[str(seed)][sample_count]["threshold_fraction"]
                        for seed in SEEDS
                    ]
                )
            ),
            "mean_regularization_exclusion_fraction": float(
                np.mean(
                    [
                        seed_results[str(seed)][sample_count][
                            "regularization_exclusion_fraction"
                        ]
                        for seed in SEEDS
                    ]
                )
            ),
            "minimum_component_count": min(
                seed_results[str(seed)][sample_count]["min_component_count"]
                for seed in SEEDS
            ),
        }
    )

slope = float(
    np.polyfit(
        np.log([cell["N"] for cell in cells]),
        np.log([cell["mean_mse"] for cell in cells]),
        1,
    )[0]
)
control_ratio = cells[-1]["mean_omitted_normal_mse"] / cells[-1]["mean_mse"]
sigma_squared = 1 / math.log(K + 1)
assumption_checks = {
    "support_in_union": True,
    "pairwise_intersection_is_zero": maximum_overlap < 1,
    "zero_intersection_mass": True,
    "component_mass": 1 / M,
    "required_component_mass_with_cp_1": 1 / M,
    "each_component_atoms_span_k": int(np.linalg.matrix_rank(latent_atoms)) == K,
    "bounded_support": True,
    "subgaussian_sigma_squared": sigma_squared,
    "worst_direction_exponential_square_moment": (
        math.exp(1 / sigma_squared) + K - 1
    )
    / K,
}
regularity_failures = {
    "ambient_lebesgue_density_exists": False,
    "intrinsic_lebesgue_density_exists": False,
    "holder_density": False,
    "log_concave_measure": False,
    "uniform_density_upper_bound_applicable": False,
    "positive_density_lower_bound_applicable": False,
    "nonconvex_support_witness": "e_1 and -e_1 are atoms while their midpoint 0 has zero mass",
}
acceptance = {
    "all_source_checks": all(source_checks.values()),
    "all_assumption_checks": all(
        assumption_checks[key] is True
        for key in (
            "support_in_union",
            "pairwise_intersection_is_zero",
            "zero_intersection_mass",
            "each_component_atoms_span_k",
            "bounded_support",
        )
    )
    and assumption_checks["component_mass"]
    == assumption_checks["required_component_mass_with_cp_1"]
    and abs(assumption_checks["worst_direction_exponential_square_moment"] - 2)
    < 1e-12,
    "complete_twenty_seed_sweep": all(len(cell["seed_mse"]) == 20 for cell in cells),
    "positive_mse": all(value > 0 for cell in cells for value in cell["seed_mse"]),
    "endpoint_mse_decreases": cells[-1]["mean_mse"] < cells[0]["mean_mse"],
    "slope_between_minus_1_5_and_minus_0_2": -1.5 <= slope <= -0.2,
    "omitted_normal_control_ratio_above_10": control_ratio > 10,
    "all_components_observed": all(cell["minimum_component_count"] > 0 for cell in cells),
    "target_fails_every_named_regularity": not any(
        value for key, value in regularity_failures.items() if key != "nonconvex_support_witness"
    ),
}

record = {
    "claim": 4,
    "verdict": "VERIFIED" if all(acceptance.values()) else "FAIL",
    "confidence": "MEDIUM",
    "configuration": {
        "d": D,
        "M": M,
        "k": K,
        "atoms_per_component": ATOMS_PER_COMPONENT,
        "sample_sizes": SAMPLE_SIZES,
        "seeds": SEEDS,
        "evaluation_samples_per_seed": EVALUATION_SAMPLES,
        "diffusion_time": DIFFUSION_TIME,
        "basis_seed": BASIS_SEED,
        "regularization_constant_C_R": REGULARIZATION_CONSTANT,
        "estimator": "paper KDE/threshold/tangent-clip/exact-normal/mixture-weight estimator with duplicate atoms aggregated exactly",
    },
    "source_hash": sha256(SOURCE),
    "source_checks": source_checks,
    "assumption_checks": assumption_checks,
    "geometry": {
        "maximum_pairwise_basis_overlap": maximum_overlap,
        "intersection_spectral_gap": 1 - maximum_overlap,
    },
    "regularity_failures": regularity_failures,
    "cells": cells,
    "log_log_N_slope": slope,
    "omitted_normal_control_ratio_at_N_50000": control_ratio,
    "acceptance": acceptance,
    "non_circularity": "The geometric N sweep, t, seeds, target, and acceptance criteria were committed before the run and were not selected from the theorem formula or observed first hits.",
    "qualification": "The target is full paper scale and exactly outside every named density regularity class. The finite study corroborates the score result; the source dependency audit covers theorem scope but is not a fully formal re-proof of all lemmas.",
    "environment": {
        "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "selected_flavor": "cpu-upgrade",
        "cpu_limit": cpu_limit(),
        "cpu_affinity_count": len(os.sched_getaffinity(0)),
        "memory_limit_bytes": read_limit("/sys/fs/cgroup/memory.max"),
        "accelerator": None,
        "runtime_seconds": time.perf_counter() - start,
    },
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "raw_results.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
print(json.dumps(record, indent=2, sort_keys=True))
