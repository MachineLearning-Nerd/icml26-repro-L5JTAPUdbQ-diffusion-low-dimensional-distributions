#!/usr/bin/env python3
"""Continuous-time threshold-escape counterexample to Theorem 2."""
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch" / "artifacts" / "claim1_threshold_escape"
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"
REJECTED = ROOT / ".openresearch" / "artifacts" / "claim1_route2_reverse_sde" / "rejected_raw_results.json"
MARGIN = 1.0
SURVIVAL_LOWER = math.erf(MARGIN / math.sqrt(2.0))


def read_limit(path: str) -> str:
    file = Path(path)
    return file.read_text().strip() if file.exists() else "unavailable"


def cpu_limit() -> float | str:
    value = read_limit("/sys/fs/cgroup/cpu.max")
    if value == "unavailable" or value.startswith("max"):
        return value
    quota, period = value.split()
    return int(quota) / int(period)


def finite_case(n: int, c_sc: int) -> dict:
    n0 = math.ceil(c_sc * math.log(n))
    score_samples = n - n0
    if score_samples <= math.e:
        raise ValueError("score sample count too small")
    threshold_ratio = math.log(score_samples) / score_samples
    h_T = n * n - 1.0
    boundary = (1.0 + math.sqrt(2.0 * h_T * math.log(score_samples / math.log(score_samples)))) / n
    kernel_ratio = math.exp(-((n * boundary - 1.0) ** 2) / (2.0 * h_T))
    initial_tail = 0.5 * math.erfc((boundary + MARGIN) / math.sqrt(2.0))
    tau = n**-2.0
    output_distance_floor = n * math.exp(-tau) * boundary - 1.0
    w1_lower_bound = initial_tail * SURVIVAL_LOWER * output_distance_floor
    return {
        "n": n,
        "C_sc": c_sc,
        "n0": n0,
        "N": score_samples,
        "T": math.log(n),
        "tau": tau,
        "h_T": h_T,
        "threshold_boundary_b": boundary,
        "kernel_ratio_at_T": kernel_ratio,
        "threshold_ratio_logN_over_N": threshold_ratio,
        "initial_gaussian_tail_probability": initial_tail,
        "brownian_survival_probability_lower_bound": SURVIVAL_LOWER,
        "output_distance_floor": output_distance_floor,
        "w1_lower_bound": w1_lower_bound,
        "n_half_scaled_lower_bound": math.sqrt(n) * w1_lower_bound,
    }


def asymptotic_case(log_n: float, c_sc: int = 16) -> dict:
    n = math.exp(log_n)
    score_samples = n - math.ceil(c_sc * log_n)
    log_score_samples = math.log(score_samples)
    log_threshold_inverse = math.log(score_samples / log_score_samples)
    boundary = math.exp(-log_n) + math.sqrt(
        2.0 * (1.0 - math.exp(-2.0 * log_n)) * log_threshold_inverse
    )
    x = boundary + MARGIN
    log_mills_tail_lower = (
        -0.5 * x * x
        - 0.5 * math.log(2.0 * math.pi)
        + math.log(x)
        - math.log(x * x + 1.0)
    )
    tau = math.exp(-2.0 * log_n)
    log_output_floor = math.log(math.exp(log_n - tau) * boundary - 1.0)
    log_w1_lower = math.log(SURVIVAL_LOWER) + log_mills_tail_lower + log_output_floor
    return {
        "log_n": log_n,
        "C_sc": c_sc,
        "threshold_boundary_b": boundary,
        "mills_argument_b_plus_a": x,
        "log_mills_tail_lower": log_mills_tail_lower,
        "log_output_distance_floor": log_output_floor,
        "log_w1_lower_bound": log_w1_lower,
        "log_ratio_to_n_minus_half_polylog": {
            str(power): log_w1_lower + 0.5 * log_n - power * math.log(log_n)
            for power in range(9)
        },
    }


start = time.perf_counter()
with tarfile.open(SOURCE) as archive:
    results = archive.extractfile("Results.tex").read().decode()
    problem = archive.extractfile("problem_formulation.tex").read().decode()

source_checks = {
    "theorem_anchor": r"\label{thm:high prob TV}" in results,
    "theorem_assumptions": "satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}" in results,
    "theorem_horizon": r"T=\log n" in results,
    "theorem_early_stop": r"\tau = n^{-2/k}" in results,
    "theorem_w1_rate": r"n^{-\frac1{k\vee 2}}" in results,
    "kde_density": r"\widehat{g}_t(i,x)" in results,
    "density_threshold": r"\frac{\log N}{N(2\pi t)^{k_i/2}}" in results,
    "threshold_indicator": r"\psi(x;\eta) \defn \ind\{x \geq \eta\}" in results,
    "reverse_drift": r"\widehat{Y}_t + 2\widehat{s}_{X_{T-t}}" in problem,
    "gaussian_initialization": r"Sample $ y \sim \mathcal{N}(0,I_d)$" in problem,
    "ve_ou_transform": r"\widehat{s}_{X_t}(x)\defn \frac{1}{c_t}" in problem,
}

finite_cases = [
    finite_case(n, c_sc)
    for c_sc in (1, 4, 16)
    for n in (256, 1024, 4096, 16384, 65536, 262144)
]
asymptotic_cases = [asymptotic_case(log_n) for log_n in (16.0, 32.0, 64.0, 128.0, 256.0, 512.0)]
rejected = json.loads(REJECTED.read_text())

record = {
    "claim": 1,
    "route": "2b",
    "verdict": "FALSIFIED",
    "confidence": "HIGH",
    "exact_contract": {
        "target": "p*=Uniform{-1,+1} in R with d=M=k=1 and c_p=1",
        "sample_split": "n0=ceil(C_sc log n), N=n-n0 for any fixed C_sc",
        "algorithm": "Algorithm 1 with the paper KDE/threshold/clip score, T=log n, tau=n^-2",
        "paper_conclusion": "E W1 <= C n^-1/2 polylog(n) for sufficiently large n",
        "counter_conclusion": "An explicit zero-score tail event gives a W1 lower bound that decays more slowly than n^-1/2 (log n)^A for every fixed A and constant C",
    },
    "assumption_checks": {
        "support_in_V1_equals_R": True,
        "dimension_k1": 1,
        "M1_intersection_condition": "vacuous",
        "component_mass": 1.0,
        "required_component_mass": 1.0,
        "bounded_support": True,
        "sigma_squared": 1.0 / math.log(2.0),
        "worst_direction_exponential_square_moment": 2.0,
        "exact_recovery": "trivial because the only one-dimensional subspace of R is R",
    },
    "source_hash": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "source_checks": source_checks,
    "continuous_time_certificate": {
        "threshold_boundary": "b=(1+sqrt(2(n^2-1) log(N/log N)))/n",
        "initial_event": "Y0>b+a and min_{0<=r<=T-tau} M_r>=-a, with a=1",
        "integrating_factor": "While the score is zero, Y_r=e^r(Y0+M_r), M_r=sqrt(2) integral_0^r e^-u dB_u",
        "ve_coordinate": "z_r=Y_r/c_(T-r)=n(Y0+M_r)",
        "threshold_persistence": "On the event z_r>nb, while h(T-r)<=h(T)=n^2-1, every KDE kernel is below eta_h for every training realization; hence the estimated score remains exactly zero",
        "event_probability_lower_bound": "P(Z>b+a) * (2 Phi(a)-1)",
        "output_distance": "dist(Y_(T-tau),{-1,+1}) >= n e^-tau b - 1",
        "wasserstein_lower_bound": "W1 >= E dist(Y,{-1,+1}) >= event_probability * output_distance",
        "training_expectation": "The lower bound holds for every training realization, so it also holds after expectation over training data",
    },
    "asymptotic_certificate": {
        "eventual_sample_split": "For every fixed C_sc, N>=n/2 eventually",
        "boundary_upper_bound": "b<=1+sqrt(2 log n)",
        "mills_ratio": "P(Z>x)>=phi(x) x/(x^2+1) for x>0",
        "log_lower_bound": "log W1 >= -2 sqrt(2 log n) - O(log log n)",
        "contradiction": "For every fixed A, log[W1/(n^-1/2 (log n)^A)] >= 0.5 log n-2 sqrt(2 log n)-O_A(log log n), which tends to +infinity",
    },
    "finite_cases": finite_cases,
    "asymptotic_cases": asymptotic_cases,
    "controls": {
        "threshold_disabled": {
            "zero_score_tail_event_applies": False,
            "reason": "Without psi(g;eta), the KDE score is nonzero on the constructed tail, so the escape proof cannot start."
        },
        "historical_precommitted_euler": {
            "status": rejected["historical_status"],
            "N_slope": rejected["log_log_N_slope"],
            "main_N4096_mean_w1": rejected["main_cells"][2]["mean"],
            "horizon_half_mean_w1": rejected["horizon_calibration"]["0.5"]["mean"],
            "horizon_canonical_mean_w1": rejected["horizon_calibration"]["1.0"]["mean"],
            "horizon_long_mean_w1": rejected["horizon_calibration"]["1.5"]["mean"],
            "standard_normal_score_control_mean_w1": rejected["wrong_score_control"]["mean"],
            "interpretation": "The unstable Euler route failed its own gates and is not the falsification proof; its horizon amplification is a qualitative diagnostic predicted by the independent continuous-time certificate."
        }
    },
    "non_circularity": "The counterexample is analytic and asymptotic. It does not select n, a first hit, a tolerance, a discretization, or a theorem-derived Monte Carlo budget as proof.",
}
record["environment"] = {
    "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
    "python": platform.python_version(),
    "selected_flavor": "cpu-upgrade",
    "cpu_limit": cpu_limit(),
    "cpu_affinity_count": len(os.sched_getaffinity(0)),
    "memory_limit_bytes": read_limit("/sys/fs/cgroup/memory.max"),
    "accelerator": None,
    "seed": None,
    "deterministic": True,
    "runtime_seconds": time.perf_counter() - start,
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "raw_results.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
print(json.dumps(record, indent=2, sort_keys=True))
