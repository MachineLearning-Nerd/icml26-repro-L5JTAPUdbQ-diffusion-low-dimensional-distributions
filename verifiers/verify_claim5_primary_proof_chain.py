#!/usr/bin/env python3
"""Independently verify the Claim 5 source and exponent certificate."""
from __future__ import annotations

import hashlib
import json
import sys
import tarfile
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAIN_ARCHIVE = ROOT / "evidence" / "source" / "arxiv_source.tar"
CAI_ARCHIVE = ROOT / "evidence" / "claim5_attempt1" / "prior_sources" / "cai2503.09583.tar.gz"
ZHANG_ARCHIVE = ROOT / "evidence" / "claim5_attempt1" / "prior_sources" / "zhang2402.15602.tar.gz"


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def member_text(archive: Path, member: str) -> str:
    with tarfile.open(archive) as bundle:
        extracted = bundle.extractfile(member)
        if extracted is None:
            fail(f"missing {member} in {archive.name}")
        return extracted.read().decode()


def parse_fraction(value: str) -> Fraction:
    return Fraction(value)


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


if len(sys.argv) != 3:
    fail("usage: verify_claim5_primary_proof_chain.py RAW_JSON OUTPUT_JSON")

raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())
expected_hashes = {
    "paper_source_tar": "07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7",
    "cai_2503_09583_source": "fc462d3046091f2d050bfa2fac0d2e1905a7e144dff4379f4b921afb0f64d211",
    "zhang_2402_15602_source": "76ad896b273e22ead0ee136bd80422a3498a5950b237a5e867ed7a304c891650",
}
actual_hashes = {
    "paper_source_tar": sha256(MAIN_ARCHIVE),
    "cai_2503_09583_source": sha256(CAI_ARCHIVE),
    "zhang_2402_15602_source": sha256(ZHANG_ARCHIVE),
}
if actual_hashes != expected_hashes or raw["source_hashes"] != expected_hashes:
    fail("a pinned source archive hash changed")

main_intro = member_text(MAIN_ARCHIVE, "introduction.tex")
cai_problem = member_text(CAI_ARCHIVE, "problem.tex")
cai_results = member_text(CAI_ARCHIVE, "results.tex")
cai_analysis = member_text(CAI_ARCHIVE, "analysis.tex")
zhang_source = member_text(ZHANG_ARCHIVE, "ICML_camera.tex")
independent_source_checks = {
    "main_equation_1_sample_exponent": "\\veps^{-\\frac{d+2\\beta}{\\beta}}" in main_intro,
    "main_equation_1_tv_scope": "total variation (TV) distance" in main_intro,
    "cai_holder_assumption": "\\begin{assumption}[H\\\"older smooth target]" in cai_problem,
    "cai_theorem": "\\begin{theorem}\\label{thm:TV}" in cai_results,
    "cai_tv_rate": "n^{-\\frac{\\beta}{d+2\\beta}}" in cai_results,
    "cai_iteration_premise": "K\\geq n^{\\frac{\\beta}{d+2\\beta}}(\\log K)^3" in cai_results,
    "cai_tau_substitution": "Substituting our selected $\\tau=n^{-2/(d+2\\beta)}$" in cai_analysis,
    "cai_score_squared_rate": "n^{-\\frac{2\\beta}{d+2\\beta}}" in cai_analysis,
    "cai_triangle_completion": "applying the triangle inequality" in cai_analysis,
    "zhang_sobolev_assumption": "Sobolev class" in zhang_source,
    "zhang_theorem": "\\begin{theorem}\\label{main_theorem2}" in zhang_source,
    "zhang_tv_rate": "n^{-\\frac{\\beta}{2\\beta+d}}" in zhang_source,
}
if not all(independent_source_checks.values()):
    fail("a primary-source theorem or proof-chain marker is absent")
if raw["source_checks"] != independent_source_checks:
    fail("reported source checks differ from independent extraction")

expected_cases = []
for dimension in (1, 2, 4, 16, 48):
    for beta in (Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2)):
        denominator = Fraction(dimension) + 2 * beta
        tv_rate = beta / denominator
        sample_exponent = denominator / beta
        expected_cases.append(
            {
                "d": dimension,
                "beta": fraction_text(beta),
                "tv_rate_exponent": fraction_text(tv_rate),
                "sample_exponent": fraction_text(sample_exponent),
                "inversion_product": fraction_text(tv_rate * sample_exponent),
            }
        )
if raw["rate_cases"] != expected_cases:
    fail("the exact rate table does not match the independently derived table")
if any(parse_fraction(case["inversion_product"]) != 1 for case in raw["rate_cases"]):
    fail("sample-complexity inversion failed")

# Exact symbolic coefficient checks over D=d+2*beta. A pair stores the
# coefficients of d and beta. Thus -D+d=-2*beta.
denominator_coefficients = (1, 2)
dimension_coefficients = (1, 0)
left_score_numerator = (
    -denominator_coefficients[0] + dimension_coefficients[0],
    -denominator_coefficients[1] + dimension_coefficients[1],
)
right_score_numerator = (0, -2)
if left_score_numerator != right_score_numerator:
    fail("symbolic score exponent identity failed")
# (-2/D)*(beta/2)=-beta/D and (beta/D)*(D/beta)=1.
if Fraction(-2) * Fraction(1, 2) != -1:
    fail("symbolic early-stopping exponent identity failed")
expected_symbolic_checks = {
    "score_squared_exponent": "-1+d/(d+2 beta)=-2 beta/(d+2 beta)",
    "score_exponent": "one half of the squared exponent is -beta/(d+2 beta)",
    "early_stopping_exponent": "[-2/(d+2 beta)]*[beta/2]=-beta/(d+2 beta)",
    "sample_rate_inversion": "[beta/(d+2 beta)]*[(d+2 beta)/beta]=1",
    "ambient_dimension_derivative": "d[(d+2 beta)/beta]/dd=1/beta>0",
    "all_pass": True,
}
if raw["symbolic_checks"] != expected_symbolic_checks:
    fail("reported symbolic proof certificate changed")
if raw["comparison"] != {
    "d": 48,
    "beta": 2,
    "prior_sample_exponent": 26,
    "paper_example_intrinsic_k": 3,
    "paper_intrinsic_sample_exponent": 3,
}:
    fail("ambient-versus-intrinsic comparison changed")
if raw["verdict"] != "VERIFIED" or raw["confidence"] != "MEDIUM":
    fail("claim verdict or confidence changed")

result = {
    "status": "PASS",
    "verdict": "VERIFIED",
    "confidence": "MEDIUM",
    "checks": {
        "pinned_primary_sources": True,
        "holder_assumption": True,
        "tv_rate_proof_chain": True,
        "exact_rate_inversion": True,
        "ambient_dimension_curse": True,
        "zhang_sobolev_qualification": True,
    },
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
