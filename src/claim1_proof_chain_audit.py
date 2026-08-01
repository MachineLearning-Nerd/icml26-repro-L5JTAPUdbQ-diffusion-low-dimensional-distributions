#!/usr/bin/env python3
"""Audit Theorem 2's conditional exponent chain and recovery dependency."""
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
OUT = ROOT / ".openresearch" / "artifacts" / "claim1_route1_proof_chain"
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"
EXTERNAL = ROOT / "evidence" / "source" / "azangulov_2409_18804_w1_excerpt.tex"


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
with tarfile.open(SOURCE) as archive:
    results = archive.extractfile("Results.tex").read().decode()
    proof = archive.extractfile("pf-of-theorems.tex").read().decode()
external = EXTERNAL.read_text()

source_checks = {
    "theorem_anchor": r"\label{thm:high prob TV}" in results,
    "assumptions_1_and_2": "satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}" in results,
    "subspace_budget": r"n_0 = C_{\mathsf{sc}}M^2 k \log n" in results,
    "algorithm_schedule": r"T=\log n" in results and r"\tau = n^{-2/k}" in results,
    "w1_conclusion": r"n^{-\frac1{k\vee 2}}" in results,
    "constant_scope": "independent of $n$, $d$ and $M$" in results,
    "recovery_lemma_invoked": r"From Lemma \ref{lem:subspace clustering}" in proof,
    "recovery_failure_probability": r"\bP [\mathcal{E}^c] \lesssim Mn^{-10}" in proof,
    "paper_w1_bridge": r"\label{eq:W_1 convergence rate}" in proof,
    "external_equation_cited": r"(8) in \citet{azangulov" in proof,
    "geometric_time_partition": r"T_{j+1} = 2T_j" in proof,
    "delta_choice": r"\delta = n^{-1}" in proof,
    "external_w1_anchor": r"\label{thm:from_score_matching_to_wasserstein}" in external,
    "external_sqrt_dimension": r"\sqrt{D}" in external,
    "external_score_integral": r"\int_{T_k}^{T_{k+1}}" in external,
    "external_oko_provenance": "Eq. (90)" in external and "Lemma D.7" in external,
}

cases = []
for k in range(1, 9):
    q = max(k, 2)
    tau_power = Fraction(-2, k)
    pre_tau_power = Fraction(1, 2) - Fraction(q, 4)
    signed_n_power = Fraction(-1, 2) + tau_power * pre_tau_power
    cases.append(
        {
            "k": k,
            "q_k_vee_2": q,
            "base_score_root_n_power": "-1/2",
            "tau_power_in_n": fraction_text(tau_power),
            "tau_power_in_geometric_sum": fraction_text(pre_tau_power),
            "final_signed_n_power": fraction_text(signed_n_power),
            "claimed_decay_exponent": fraction_text(Fraction(1, q)),
            "identity_pass": signed_n_power == -Fraction(1, q),
        }
    )

claim3 = json.loads(
    (ROOT / ".openresearch" / "artifacts" / "claim3_identifiability" / "raw_results.json").read_text()
)
claim3_checker = json.loads(
    (ROOT / ".openresearch" / "artifacts" / "claim3_identifiability" / "independent_checker.json").read_text()
)

record = {
    "claim": 1,
    "route": 1,
    "route_status": "CONDITIONAL_PROOF_CHAIN_PASS_UNCONDITIONAL_CLAIM_BLOCKED",
    "exact_contract": {
        "domain": "Every target satisfying Assumptions 1 and 2, for sufficiently large n",
        "algorithm": "Algorithm 1 with the paper score estimator, n0=C_sc M^2 k log n, N=n-n0, T=log n, tau=n^(-2/k)",
        "quantifier": "Expected W1 over the n training samples",
        "conclusion": "E W1 <= C d M^(3/2) n^(-1/(k vee 2)) polylog(n), with C independent of n,d,M",
    },
    "source_hashes": {
        "paper_source_tar": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        "paper_ar5iv_html": "d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4",
        "azangulov_ar5iv_html": "ef2e562ba4a531c5579e8727c1a64f3b8e4cb8ef78de9520920ec01df5545054",
        "azangulov_source_response": "ee0f36028e13fe450eda9e6dd5bcc5dbc8b4fedf3af699222bc3fa00ba85be2a",
    },
    "source_checks": source_checks,
    "exponent_cases": cases,
    "dependency_audit": {
        "conditional_score_bound": "d M^3 n^-1 times the intrinsic-time singularity",
        "external_w1_bridge": "sqrt(d) times square roots of interval score integrals",
        "prefactor_result": "sqrt(d) * sqrt(d M^3/n) = d M^(3/2) n^-1/2",
        "geometric_sum": "For k>2, dominated by tau^(1/2-k/4); for k<=2, only logarithmic growth",
        "recovery_event_used_unconditionally": True,
        "recovery_certificate_verdict": claim3["verdict"],
        "recovery_checker": claim3_checker["status"],
        "recovery_maximin_success": claim3["counterexample"]["maximin_exact_recovery_success"],
        "paper_claimed_recovery_failure": "O(M n^-10)",
    },
    "interpretation": {
        "established": "The displayed exponent and d,M prefactor follow from the paper's conditional score bound plus the independently pinned external W1 inequality.",
        "not_established": "The unconditional theorem does not follow under only the stated assumptions because its exact-recovery lemma is false.",
        "falsification_status": "No W1 counterexample is supplied by this route; a broken proof dependency is not itself a contradiction of the theorem conclusion.",
    },
    "non_circularity": "All k=1..8 exponent identities are derived symbolically. No n, tolerance, time horizon, or first-hit result is fitted to the claimed rate.",
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
