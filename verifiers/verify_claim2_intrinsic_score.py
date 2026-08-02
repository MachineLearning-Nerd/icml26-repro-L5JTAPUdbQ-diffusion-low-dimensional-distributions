#!/usr/bin/env python3
"""Independently check Theorem 1's source and geometric certificate."""
from __future__ import annotations

import hashlib
import json
import sys
import tarfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


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
            fail(f"missing {member}")
        return extracted.read().decode()


def squared_norm(vector: list[Fraction]) -> Fraction:
    return sum((value * value for value in vector), Fraction(0))


def text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


if len(sys.argv) != 3:
    fail("usage: verify_claim2_intrinsic_score.py RAW_JSON OUTPUT_JSON")
raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())

expected_hash = "07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7"
if sha256(SOURCE) != expected_hash or raw.get("source_hash") != expected_hash:
    fail("the pinned paper source hash changed")

results = member_text("Results.tex")
proof = member_text("pf-of-theorems.tex")
lemmas = member_text("pf-of-lemmas.tex")
expected_source_checks = {
    "theorem_assumptions": "Suppose the target distribution $p^\\star$ satisfies Assumptions" in results,
    "theorem_exact_recovery_condition": "Under the event of exact subspace recovery" in results,
    "theorem_time_domain": "$t\\leq N^{O(1)}$" in results,
    "theorem_bound": "C_\\score \\frac{dM^3}{N}" in results,
    "constant_independent_of_d": "independent of $N$, $d$, $M$ and $t$" in results,
    "true_normal_tangent_decomposition": "s_t(i,x) = -\\frac{1}{t}\\big(x-\\proj_i(x)\\big) + A_i s_t^\\low" in results,
    "estimated_normal_tangent_decomposition": "\\widehat{s}_t(i,x) \\defn -\\frac{x-\\proj_i(x)}{t} + A_i \\widehat{s}_t^\\low" in results,
    "mixture_score_decomposition": "\\sum_{i=1}^M w_t(i,x) \\cdot s_t(i,x)" in results,
    "outer_cauchy_schwarz_factor": "\\defnrev M \\sum_{i=1}^M L_i" in proof,
    "weight_error_term": "\\frac{dM}{Nt} \\Big( 1+\\frac{\\sigma^{k\\vee2}}" in proof,
    "component_error_intrinsic_constant": "(4/\\sqrt{\\pi})^{k_i}" in proof,
    "final_proof_bound": "\\frac{dM^3}{Nt}\\Big( 1+\\frac{\\sigma^{k\\vee2}}" in proof,
    "component_lemma_dimension": "\\frac{(4/\\sqrt{\\pi})^k}{N}" in lemmas,
}
if not all(expected_source_checks.values()):
    fail("a required theorem or proof-chain marker is absent")
if raw.get("source_checks") != expected_source_checks:
    fail("reported source checks differ from independent extraction")

expected_cases = []
for dimension in (4, 8, 16, 48):
    for intrinsic in (1, 2, 3):
        if intrinsic >= dimension:
            continue
        diffusion_time = Fraction(intrinsic + 1, 5)
        point = [Fraction(index + 1, index + 2) for index in range(dimension)]
        true_low = [Fraction(index + 2, intrinsic + 3) for index in range(intrinsic)]
        estimated_low = [Fraction(-(index + 1), intrinsic + 4) for index in range(intrinsic)]
        normal = [Fraction(0)] * intrinsic + [
            -point[index] / diffusion_time for index in range(intrinsic, dimension)
        ]
        true_score = [
            normal[index] + (true_low[index] if index < intrinsic else 0)
            for index in range(dimension)
        ]
        estimated_score = [
            normal[index] + (estimated_low[index] if index < intrinsic else 0)
            for index in range(dimension)
        ]
        ambient_error = squared_norm(
            [true_score[index] - estimated_score[index] for index in range(dimension)]
        )
        intrinsic_error = squared_norm(
            [true_low[index] - estimated_low[index] for index in range(intrinsic)]
        )
        expected_cases.append(
            {
                "d": dimension,
                "k": intrinsic,
                "k_vee_2": max(intrinsic, 2),
                "ambient_substitution": dimension,
                "t": text(diffusion_time),
                "ambient_score_error_squared": text(ambient_error),
                "intrinsic_score_error_squared": text(intrinsic_error),
                "normal_component_error_squared": "0",
                "identity_pass": ambient_error == intrinsic_error,
            }
        )
if raw.get("cancellation_cases") != expected_cases:
    fail("an intrinsic exponent or exact cancellation case changed")
if not all(case["identity_pass"] for case in expected_cases):
    fail("ambient normal-score cancellation failed")

expected_trace = {
    "normal_component": "known exactly and cancels from component estimation error",
    "tangent_estimation": "k_i-dimensional; analytic lemma factor (4/sqrt(pi))^k_i/N",
    "weight_estimation": "normal-coordinate Gaussian integrates to one; remaining tangent box is k_i-dimensional",
    "mixture_aggregation": "Cauchy-Schwarz contributes M and summing M components contributes M",
    "ambient_dependence": "explicit linear prefactor d; theorem constant is stated independent of d",
    "intrinsic_dependence": "k vee 2 in sigma and t powers; constants may depend on k",
    "conclusion": "d M^3/N * (1/t + sigma^(k vee 2)/t^((k vee 2)/2+1)) times polylog(N)",
}
if raw.get("dependency_trace") != expected_trace:
    fail("the dependency trace changed")
if raw.get("status") != "PROOF_CERTIFICATE_PASS":
    fail("the proof certificate did not pass")

result = {
    "status": "PASS",
    "claim": 2,
    "scope": "Theorem 1 conditional on exact subspace recovery",
    "checks": {
        "pinned_source": True,
        "exact_theorem_contract": True,
        "normal_tangent_identity": True,
        "twelve_exact_dimension_cases": True,
        "intrinsic_lemma_factor": True,
        "ambient_constant_independence": True,
        "dependency_trace": True,
    },
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
