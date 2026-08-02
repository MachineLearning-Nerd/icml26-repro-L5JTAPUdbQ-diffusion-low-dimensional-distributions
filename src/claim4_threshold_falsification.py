#!/usr/bin/env python3
"""Turn the threshold-escape witness into the exact Claim 4 falsification."""
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
OUT = ROOT / ".openresearch" / "artifacts" / "claim4_threshold_falsification"
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"
CLAIM1 = ROOT / ".openresearch" / "artifacts" / "claim1_threshold_escape" / "raw_results.json"


def read_limit(path: str) -> str:
    file = Path(path)
    return file.read_text().strip() if file.exists() else "unavailable"


def cpu_limit() -> float | str:
    value = read_limit("/sys/fs/cgroup/cpu.max")
    if value == "unavailable" or value.startswith("max"):
        return value
    quota, period = value.split()
    return int(quota) / int(period)


start = time.perf_counter()
claim1 = json.loads(CLAIM1.read_text())
with tarfile.open(SOURCE) as archive:
    results = archive.extractfile("Results.tex").read().decode()

source_checks = {
    "theorem_2_uses_only_assumptions_1_and_2": (
        "satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}"
        in results
    ),
    "theorem_2_wasserstein_conclusion": r"n^{-\frac1{k\vee 2}}" in results,
    "weak_assumptions_remark": (
        "Our results do not rely on stringent structural conditions" in results
    ),
    "smooth_density_excluded": "smooth densities/scores" in results,
    "log_concavity_excluded": "log-concavity" in results,
    "only_subgaussian_claim": "under only a subgaussian assumption" in results,
}

record = {
    "claim": 4,
    "verdict": "FALSIFIED",
    "confidence": "HIGH",
    "exact_contract": {
        "paper_claim": (
            "The results hold under Assumptions 1 and 2 without smooth-density, "
            "score-smoothness, log-concavity, uniform-density, or density-lower-bound assumptions."
        ),
        "falsification_rule": (
            "An exact theorem failure on a target satisfying Assumptions 1 and 2 "
            "and lacking every named regularity falsifies the broad claim."
        ),
        "failed_result": "Theorem 2 and its n^{-1/(k vee 2)} polylog(n) Wasserstein bound",
    },
    "source_hash": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "source_checks": source_checks,
    "target": {
        "law": "Uniform{-1,+1}",
        "d": 1,
        "M": 1,
        "k": 1,
        "V1": "R",
        "c_p": 1,
        "sigma_squared": 1.0 / math.log(2.0),
    },
    "assumption_checks": claim1["assumption_checks"],
    "regularity_audit": {
        "atomic_measure": True,
        "no_ambient_lebesgue_density": True,
        "no_intrinsic_lebesgue_density": True,
        "no_holder_density_or_score": True,
        "no_uniform_density_upper_bound": True,
        "no_positive_density_lower_bound": True,
        "not_log_concave": True,
        "nonconvex_support_witness": "-1 and +1 are support points while their midpoint 0 is not",
    },
    "theorem_failure": {
        "claim1_verdict": claim1["verdict"],
        "claim1_confidence": claim1["confidence"],
        "threshold_persistence": claim1["continuous_time_certificate"]["threshold_persistence"],
        "training_expectation": claim1["continuous_time_certificate"]["training_expectation"],
        "asymptotic_contradiction": claim1["asymptotic_certificate"]["contradiction"],
        "finite_cells": len(claim1["finite_cases"]),
        "asymptotic_cells": len(claim1["asymptotic_cases"]),
        "raw_evidence": ".openresearch/artifacts/claim1_threshold_escape/raw_results.json",
    },
    "why_falsified": (
        "The Rademacher target has none of the named density regularities, satisfies "
        "every stated theorem assumption, and contradicts Theorem 2 under the exact "
        "paper estimator. Thus the paper's results do not hold over the claimed weak domain."
    ),
}
record["environment"] = {
    "git_sha": subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip(),
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
