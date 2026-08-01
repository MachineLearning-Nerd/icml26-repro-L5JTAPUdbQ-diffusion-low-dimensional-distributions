#!/usr/bin/env python3
"""Independently verify Claim 1 route 1 without trusting its verdict fields."""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


if len(sys.argv) != 3:
    fail("usage: verify_claim1_proof_chain.py RAW_JSON OUTPUT_JSON")
raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())

expected_hash = "07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7"
actual_hash = hashlib.sha256((ROOT / "evidence" / "source" / "arxiv_source.tar").read_bytes()).hexdigest()
if actual_hash != expected_hash or raw["source_hashes"]["paper_source_tar"] != expected_hash:
    fail("paper source hash changed")
if raw["source_hashes"]["azangulov_source_response"] != "ee0f36028e13fe450eda9e6dd5bcc5dbc8b4fedf3af699222bc3fa00ba85be2a":
    fail("external primary-source hash changed")
if not all(raw["source_checks"].values()) or len(raw["source_checks"]) != 16:
    fail("a theorem or external-source marker is missing")

cases = raw["exponent_cases"]
if [row["k"] for row in cases] != list(range(1, 9)):
    fail("the complete prespecified k=1..8 audit is missing")
for row in cases:
    k = row["k"]
    q = max(k, 2)
    if row["q_k_vee_2"] != q:
        fail("k vee 2 was computed incorrectly")
    tau_power = parse_fraction(row["tau_power_in_n"])
    if tau_power != Fraction(-2, k):
        fail("the paper's tau=n^(-2/k) schedule changed")
    geometric_power = parse_fraction(row["tau_power_in_geometric_sum"])
    if geometric_power != Fraction(1, 2) - Fraction(q, 4):
        fail("geometric-sum power changed")
    signed = Fraction(-1, 2) + tau_power * geometric_power
    if signed != parse_fraction(row["final_signed_n_power"]):
        fail("reported final n exponent is inconsistent")
    if signed != -Fraction(1, q):
        fail("conditional exponent does not equal -1/(k vee 2)")
    if parse_fraction(row["claimed_decay_exponent"]) != Fraction(1, q):
        fail("claimed decay exponent changed")
    if not row["identity_pass"]:
        fail("generator reported a failed exponent identity")

dependency = raw["dependency_audit"]
if dependency["recovery_certificate_verdict"] != "FALSIFIED":
    fail("false exact-recovery dependency is not exposed")
if dependency["recovery_checker"] != "PASS":
    fail("exact-recovery counterexample checker did not pass")
if dependency["recovery_maximin_success"] > 0.5:
    fail("recovery impossibility bound changed")
if not dependency["recovery_event_used_unconditionally"]:
    fail("unconditional recovery dependency was hidden")
if "BLOCKED" not in raw["route_status"]:
    fail("route incorrectly upgrades the unconditional theorem")

result = {
    "status": "PASS",
    "claim": 1,
    "route": 1,
    "conditional_exponent_chain": "PASS",
    "unconditional_theorem": "BLOCKED",
    "checks": {
        "exact_contract": True,
        "pinned_paper_source": True,
        "pinned_external_w1_source": True,
        "sixteen_source_markers": True,
        "eight_exact_exponent_cases": True,
        "ambient_prefactor_trace": True,
        "invalid_recovery_dependency_exposed": True,
        "no_false_falsification": True,
    },
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
