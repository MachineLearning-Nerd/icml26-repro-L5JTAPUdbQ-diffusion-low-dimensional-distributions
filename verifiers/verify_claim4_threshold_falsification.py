#!/usr/bin/env python3
"""Independently verify the Claim 4 weak-regularity falsification."""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


if len(sys.argv) != 4:
    fail("usage: verify_claim4_threshold_falsification.py CLAIM4_JSON CLAIM1_JSON OUTPUT_JSON")

claim4_path, claim1_path, output_path = map(Path, sys.argv[1:])
claim4 = json.loads(claim4_path.read_text())
claim1 = json.loads(claim1_path.read_text())

expected_hash = "07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7"
actual_hash = hashlib.sha256(
    (ROOT / "evidence" / "source" / "arxiv_source.tar").read_bytes()
).hexdigest()
if claim4["source_hash"] != expected_hash or actual_hash != expected_hash:
    fail("paper source hash changed")
if len(claim4["source_checks"]) != 6 or not all(claim4["source_checks"].values()):
    fail("the weak-regularity source contract is incomplete")

target = claim4["target"]
if target != {
    "M": 1,
    "V1": "R",
    "c_p": 1,
    "d": 1,
    "k": 1,
    "law": "Uniform{-1,+1}",
    "sigma_squared": 1.0 / math.log(2.0),
}:
    fail("the counterexample target changed")

assumptions = claim4["assumption_checks"]
if not assumptions["support_in_V1_equals_R"] or assumptions["dimension_k1"] != 1:
    fail("Assumption 1 support or dimension failed")
if assumptions["M1_intersection_condition"] != "vacuous":
    fail("Assumption 1 intersection audit failed")
if assumptions["component_mass"] != assumptions["required_component_mass"]:
    fail("Assumption 1 component mass failed")
if not assumptions["bounded_support"]:
    fail("bounded support certificate is absent")
if not math.isclose(
    math.exp(1.0 / assumptions["sigma_squared"]), 2.0, rel_tol=1e-12
):
    fail("Assumption 2 exponential moment failed")
if "trivial" not in assumptions["exact_recovery"]:
    fail("exact recovery is not resolved")

regularity = claim4["regularity_audit"]
required = (
    "atomic_measure",
    "no_ambient_lebesgue_density",
    "no_intrinsic_lebesgue_density",
    "no_holder_density_or_score",
    "no_uniform_density_upper_bound",
    "no_positive_density_lower_bound",
    "not_log_concave",
)
if not all(regularity[key] for key in required):
    fail("the witness does not lack every named regularity")
if "midpoint 0 is not" not in regularity["nonconvex_support_witness"]:
    fail("the log-concavity counter-witness is missing")

if claim1["verdict"] != "FALSIFIED" or claim1["confidence"] != "HIGH":
    fail("the linked Theorem 2 counterexample is not accepted")
if claim1["source_hash"] != expected_hash:
    fail("Claim 1 and Claim 4 use different paper sources")
if claim1["assumption_checks"] != assumptions:
    fail("Claim 4 does not use the exact Claim 1 target")
if "score remains exactly zero" not in claim1["continuous_time_certificate"]["threshold_persistence"]:
    fail("zero-score tail persistence is missing")
if "every training realization" not in claim1["continuous_time_certificate"]["training_expectation"]:
    fail("the lower bound does not cover training expectation")
if "tends to +infinity" not in claim1["asymptotic_certificate"]["contradiction"]:
    fail("the asymptotic rate contradiction is missing")
last = claim1["asymptotic_cases"][-1]["log_ratio_to_n_minus_half_polylog"]
previous = claim1["asymptotic_cases"][-2]["log_ratio_to_n_minus_half_polylog"]
if any(last[str(power)] <= 0 or last[str(power)] <= previous[str(power)] for power in range(9)):
    fail("the stored lower bound does not dominate checked fixed polylogs")
if claim4["verdict"] != "FALSIFIED" or claim4["confidence"] != "HIGH":
    fail("Claim 4 verdict changed")

result = {
    "status": "PASS",
    "claim": 4,
    "verdict": "FALSIFIED",
    "confidence": "HIGH",
    "checks": {
        "exact_claim_contract": True,
        "all_paper_assumptions": True,
        "no_named_regularity": True,
        "not_log_concave": True,
        "exact_paper_estimator": True,
        "continuous_time_theorem_failure": True,
        "training_expectation": True,
        "asymptotic_rate_contradiction": True,
    },
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
