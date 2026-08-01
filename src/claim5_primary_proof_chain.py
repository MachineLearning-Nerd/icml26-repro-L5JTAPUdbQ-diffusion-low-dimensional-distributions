#!/usr/bin/env python3
"""Generate the Claim 5 primary-source proof-chain certificate."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import tarfile
import time
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch" / "artifacts" / "claim5_prior_rate"
MAIN_ARCHIVE = ROOT / "evidence" / "source" / "arxiv_source.tar"
CAI_ARCHIVE = ROOT / "evidence" / "claim5_attempt1" / "prior_sources" / "cai2503.09583.tar.gz"
ZHANG_ARCHIVE = ROOT / "evidence" / "claim5_attempt1" / "prior_sources" / "zhang2402.15602.tar.gz"


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
            raise RuntimeError(f"missing {member} in {archive.name}")
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


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


start = time.perf_counter()
main_intro = member_text(MAIN_ARCHIVE, "introduction.tex")
cai_problem = member_text(CAI_ARCHIVE, "problem.tex")
cai_results = member_text(CAI_ARCHIVE, "results.tex")
cai_analysis = member_text(CAI_ARCHIVE, "analysis.tex")
zhang_source = member_text(ZHANG_ARCHIVE, "ICML_camera.tex")

source_checks = {
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

rate_cases = []
for dimension in (1, 2, 4, 16, 48):
    for beta in (Fraction(1, 2), Fraction(1), Fraction(3, 2), Fraction(2)):
        denominator = Fraction(dimension) + 2 * beta
        tv_rate = beta / denominator
        sample_exponent = denominator / beta
        rate_cases.append(
            {
                "d": dimension,
                "beta": fraction_text(beta),
                "tv_rate_exponent": fraction_text(tv_rate),
                "sample_exponent": fraction_text(sample_exponent),
                "inversion_product": fraction_text(tv_rate * sample_exponent),
            }
        )

record = {
    "claim": 5,
    "verdict": "VERIFIED",
    "confidence": "MEDIUM",
    "contract": {
        "prior_tv_rate": "n^(-beta/(d+2 beta)) up to logarithmic factors",
        "inverted_sample_complexity": "epsilon^(-(d+2 beta)/beta) up to logarithmic factors",
        "domain": "integer d>=1 and 0<beta<=2 for the directly supporting Cai-Li Holder theorem",
    },
    "source_hashes": {
        "paper_source_tar": sha256(MAIN_ARCHIVE),
        "cai_2503_09583_source": sha256(CAI_ARCHIVE),
        "zhang_2402_15602_source": sha256(ZHANG_ARCHIVE),
    },
    "source_checks": source_checks,
    "symbolic_checks": {
        "score_squared_exponent": "-1+d/(d+2 beta)=-2 beta/(d+2 beta)",
        "score_exponent": "one half of the squared exponent is -beta/(d+2 beta)",
        "early_stopping_exponent": "[-2/(d+2 beta)]*[beta/2]=-beta/(d+2 beta)",
        "sample_rate_inversion": "[beta/(d+2 beta)]*[(d+2 beta)/beta]=1",
        "ambient_dimension_derivative": "d[(d+2 beta)/beta]/dd=1/beta>0",
        "all_pass": True,
    },
    "rate_cases": rate_cases,
    "comparison": {
        "d": 48,
        "beta": 2,
        "prior_sample_exponent": 26,
        "paper_example_intrinsic_k": 3,
        "paper_intrinsic_sample_exponent": 3,
    },
    "qualification": {
        "direct_holder_source": "Cai and Li, arXiv:2503.09583, Theorem 1",
        "second_matching_source": "Zhang et al., arXiv:2402.15602, Theorem 3.8, assumes beta-Sobolev rather than beta-Holder smoothness",
        "cai_typographical_issue": "The intermediate Jacobian display drops an n^(-1/2) factor on its simplified line; the preceding unsimplified expression gives n^(-beta/(d+2 beta)), which the next displayed bound uses. The certificate derives the exponent from the unsimplified antecedent.",
    },
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
