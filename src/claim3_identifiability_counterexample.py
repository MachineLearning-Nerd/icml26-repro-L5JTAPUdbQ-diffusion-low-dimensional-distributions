#!/usr/bin/env python3
"""Generate an information-theoretic counterexample to Appendix B.1."""
from __future__ import annotations

import json
import math
import os
import platform
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".openresearch" / "artifacts" / "claim3_identifiability"


def total_variation(left: dict[str, float], right: dict[str, float]) -> float:
    atoms = set(left) | set(right)
    return 0.5 * sum(abs(left.get(atom, 0.0) - right.get(atom, 0.0)) for atom in atoms)


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
observed_pmf = {
    "-1,0,0,0": 0.25,
    "0,-1,0,0": 0.25,
    "0,1,0,0": 0.25,
    "1,0,0,0": 0.25,
}
distinguishable_pmf = {
    "0,0,-1,0": 0.25,
    "0,0,0,-1": 0.25,
    "0,0,0,1": 0.25,
    "0,0,1,0": 0.25,
}
sigma_squared = 1.0 / math.log(2.0)

record = {
    "claim": 3,
    "verdict": "FALSIFIED",
    "paper_statement": {
        "anchor": "Appendix B.1, Lemma 3 / #Thmlemma3",
        "quantifier": "Under Assumption 1 there exists a data-only algorithm using upper bounds on M and k that exactly recovers every V_i with failure probability bounded by a universal constant times M n^-10 from n0=O(c_p^2 M^2 (k+1) log n) samples.",
    },
    "counterexample": {
        "d": 4,
        "M": 2,
        "k": 2,
        "c_p": 1,
        "pmf": observed_pmf,
        "parameterization_a": {
            "V1_basis": [[1, 0, 0, 0], [0, 0, 1, 0]],
            "V2_basis": [[0, 1, 0, 0], [0, 0, 0, 1]]
        },
        "parameterization_b": {
            "V1_basis": [[1, 0, 0, 0], [0, 0, 0, 1]],
            "V2_basis": [[0, 1, 0, 0], [0, 0, 1, 0]]
        },
        "distinct_recovery_targets": True,
        "observation_total_variation": total_variation(observed_pmf, observed_pmf),
        "sample_law_identical_for_every_n0": True,
        "sum_of_success_probabilities_upper_bound": 1.0,
        "maximin_exact_recovery_success": 0.5,
    },
    "assumption_checks": {
        "support_contained_in_union_for_both_parameterizations": True,
        "pairwise_intersections": "{0} in both parameterizations",
        "probability_mass_on_each_pairwise_intersection": 0.0,
        "component_mass": 0.5,
        "required_component_mass": 0.5,
        "sigma_squared": sigma_squared,
        "subgaussian_worst_direction_moment": math.exp(1.0 / sigma_squared),
        "subgaussian_limit": 2.0,
    },
    "distinguishable_negative_control": {
        "left_pmf": observed_pmf,
        "right_pmf": distinguishable_pmf,
        "observation_total_variation": total_variation(observed_pmf, distinguishable_pmf),
        "indistinguishability_argument_applies": False,
    },
    "logic": {
        "reason": "The observation distribution is identical under two different exact-recovery targets, so the two disjoint success-event probabilities sum to at most one. At least one valid parameterization has success probability at most one half for every sample size. A universal O(n^-10) failure bound is eventually below one half, a contradiction.",
        "missing_condition": "A minimal-span or non-degeneracy/identifiability condition on each component distribution.",
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
