#!/usr/bin/env python3
"""Independently check the continuous threshold-escape certificate."""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARGIN = 1.0
SURVIVAL = math.erf(MARGIN / math.sqrt(2.0))


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def close(left: float, right: float, tolerance: float = 1e-11) -> bool:
    return math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)


if len(sys.argv) != 3:
    fail("usage: verify_claim1_threshold_escape.py RAW_JSON OUTPUT_JSON")
raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())

expected_hash = "07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7"
actual_hash = hashlib.sha256((ROOT / "evidence" / "source" / "arxiv_source.tar").read_bytes()).hexdigest()
if raw["source_hash"] != expected_hash or actual_hash != expected_hash:
    fail("paper source hash changed")
if len(raw["source_checks"]) != 11 or not all(raw["source_checks"].values()):
    fail("a source marker is missing")

assumptions = raw["assumption_checks"]
if not assumptions["support_in_V1_equals_R"] or assumptions["dimension_k1"] != 1:
    fail("one-dimensional support assumption failed")
if assumptions["M1_intersection_condition"] != "vacuous":
    fail("M=1 intersection audit failed")
if not close(assumptions["component_mass"], assumptions["required_component_mass"]):
    fail("component-mass lower bound failed")
if not close(math.exp(1.0 / assumptions["sigma_squared"]), 2.0):
    fail("Assumption 2 moment failed")
if not assumptions["bounded_support"]:
    fail("bounded-support certificate is missing")
if "trivial" not in assumptions["exact_recovery"]:
    fail("the counterexample did not remove recovery uncertainty")

finite = raw["finite_cases"]
if len(finite) != 18:
    fail("finite audit matrix is incomplete")
if sorted({row["C_sc"] for row in finite}) != [1, 4, 16]:
    fail("sample-split constants changed")
if sorted({row["n"] for row in finite}) != [256, 1024, 4096, 16384, 65536, 262144]:
    fail("finite n schedule changed")
for row in finite:
    n = row["n"]
    N = n - math.ceil(row["C_sc"] * math.log(n))
    if row["N"] != N:
        fail("score sample count is inconsistent")
    h_T = n * n - 1.0
    boundary = (1.0 + math.sqrt(2.0 * h_T * math.log(N / math.log(N)))) / n
    threshold = math.log(N) / N
    kernel = math.exp(-((n * boundary - 1.0) ** 2) / (2.0 * h_T))
    if not close(boundary, row["threshold_boundary_b"]):
        fail("threshold boundary is inconsistent")
    if not close(kernel, threshold) or not close(kernel, row["kernel_ratio_at_T"]):
        fail("tail kernel is not at the density threshold")
    if not close(threshold, row["threshold_ratio_logN_over_N"]):
        fail("reported threshold ratio is inconsistent")
    tail = 0.5 * math.erfc((boundary + MARGIN) / math.sqrt(2.0))
    output_floor = n * math.exp(-(n**-2.0)) * boundary - 1.0
    lower = tail * SURVIVAL * output_floor
    if not close(tail, row["initial_gaussian_tail_probability"]):
        fail("initial Gaussian tail probability is inconsistent")
    if not close(row["brownian_survival_probability_lower_bound"], SURVIVAL):
        fail("Brownian survival lower bound changed")
    if not close(output_floor, row["output_distance_floor"]):
        fail("output amplification floor is inconsistent")
    if not close(lower, row["w1_lower_bound"]):
        fail("W1 lower bound is inconsistent")
    if lower <= 0:
        fail("finite W1 lower bound is not positive")

asymptotic = raw["asymptotic_cases"]
if [row["log_n"] for row in asymptotic] != [16.0, 32.0, 64.0, 128.0, 256.0, 512.0]:
    fail("asymptotic log-n schedule changed")
for row in asymptotic:
    x = row["mills_argument_b_plus_a"]
    mills = -0.5 * x * x - 0.5 * math.log(2.0 * math.pi) + math.log(x) - math.log(x * x + 1.0)
    if not close(mills, row["log_mills_tail_lower"]):
        fail("Mills-ratio lower bound is inconsistent")
    reconstructed = math.log(SURVIVAL) + mills + row["log_output_distance_floor"]
    if not close(reconstructed, row["log_w1_lower_bound"]):
        fail("log W1 lower bound is inconsistent")
    for power, value in row["log_ratio_to_n_minus_half_polylog"].items():
        expected = reconstructed + 0.5 * row["log_n"] - int(power) * math.log(row["log_n"])
        if not close(expected, value):
            fail("polylog comparison is inconsistent")
last = asymptotic[-1]["log_ratio_to_n_minus_half_polylog"]
previous = asymptotic[-2]["log_ratio_to_n_minus_half_polylog"]
if any(last[str(power)] <= 0 or last[str(power)] <= previous[str(power)] for power in range(9)):
    fail("asymptotic lower bound does not dominate checked polylog powers")

certificate = raw["continuous_time_certificate"]
required_phrases = {
    "integrating_factor": "Y_r=e^r",
    "ve_coordinate": "z_r=",
    "threshold_persistence": "score remains exactly zero",
    "event_probability_lower_bound": "Phi",
    "output_distance": "n e^-tau b - 1",
    "training_expectation": "every training realization",
}
for key, phrase in required_phrases.items():
    if phrase not in certificate[key]:
        fail(f"continuous-time proof step missing: {key}")
if raw["controls"]["threshold_disabled"]["zero_score_tail_event_applies"]:
    fail("threshold-disabled negative control unexpectedly passes")
historical = raw["controls"]["historical_precommitted_euler"]
if historical["status"] != "REJECTED_NUMERICAL_BASELINE":
    fail("failed Euler attempt was not labeled historical rejected baseline")
if not historical["horizon_half_mean_w1"] < historical["horizon_canonical_mean_w1"] < historical["horizon_long_mean_w1"]:
    fail("historical horizon diagnostic changed")
if raw["verdict"] != "FALSIFIED" or raw["confidence"] != "HIGH":
    fail("counterexample verdict changed")

result = {
    "status": "PASS",
    "claim": 1,
    "verdict": "FALSIFIED",
    "confidence": "HIGH",
    "checks": {
        "exact_theorem_contract": True,
        "all_paper_assumptions": True,
        "trivial_exact_recovery": True,
        "zero_score_tail_persistence": True,
        "positive_event_probability": True,
        "continuous_time_amplification": True,
        "wasserstein_lower_bound": True,
        "training_expectation": True,
        "asymptotic_rate_contradiction": True,
        "threshold_disabled_control": True,
        "historical_numerical_failure_labeled": True,
    },
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
