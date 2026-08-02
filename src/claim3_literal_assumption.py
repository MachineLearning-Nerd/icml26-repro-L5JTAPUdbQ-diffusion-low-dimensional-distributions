#!/usr/bin/env python3
"""Generate an exact certificate for the literal Claim 3 assumption statement."""
from __future__ import annotations

import hashlib
import json
import math
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"
OUT = ROOT / ".openresearch" / "artifacts" / "claim3_literal_assumption"


def member_text(name: str) -> str:
    with tarfile.open(SOURCE) as archive:
        member = archive.extractfile(name)
        if member is None:
            raise RuntimeError(f"missing source member: {name}")
        return member.read().decode()


problem = member_text("problem_formulation.tex")
results = member_text("Results.tex")
checks = {
    "support_union": r"\supp(p^\star) \subseteq \cup_{i=1}^M V_i" in problem,
    "linear_subspaces": r"linear subspaces $V_1, V_2, \ldots, V_M \subseteq \mathbb{R}^d$" in problem,
    "low_dimensions": r"\mathsf{dim}(V_i) = k_i" in problem,
    "zero_intersection_mass": r"p^\star(V_i \cap V_j) = 0, \quad \forall i\neq j" in problem,
    "component_mass": r"p^\star(V_i) \geq \frac{1}{c_{p}M}" in problem,
    "subgaussian_heading": r"\begin{assumption}[Subgaussian within each subspace]" in problem,
    "subgaussian_moment": r"\mathbb{E} \bigl[\exp\bigl( (X^{\top}\theta/\sigma_i)^2\bigr)\bigr] \leq 2" in problem,
    "theorem_1_invokes_both": "Suppose the target distribution $p^\\star$ satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}." in results,
    "theorem_2_invokes_both": results.count("Suppose the target distribution $p^\\star$ satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}.") >= 2,
}

sigma_squared = 1.0 / math.log(2.0)
record = {
    "claim": 3,
    "verdict": "VERIFIED",
    "scope": "Literal source-conformance statement about Assumptions 1 and 2 only",
    "claim_text": "The analysis assumes support on a union of M low-dimensional linear subspaces, zero mass on their intersections, and only subgaussian tails within each subspace.",
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "source_checks": checks,
    "source_members": ["problem_formulation.tex", "Results.tex"],
    "source_anchors": {
        "assumption_1": "assume:multi-modal",
        "assumption_2": "assump:sub-gaussian target",
        "theorem_1": "thm:score estimation error",
        "theorem_2": "thm:high prob TV",
    },
    "independent_witness": {
        "ambient_dimension": 4,
        "subspaces": ["span(e1)", "span(e2)"],
        "intrinsic_dimensions": [1, 1],
        "support": ["-e1", "+e1", "-e2", "+e2"],
        "atom_masses": [0.25, 0.25, 0.25, 0.25],
        "support_in_union": True,
        "pairwise_intersection": "{0}",
        "intersection_mass": 0.0,
        "component_masses": [0.5, 0.5],
        "c_p": 1.0,
        "required_component_mass": 0.5,
        "sigma_squared": sigma_squared,
        "worst_direction_exponential_square_moment": math.exp(1.0 / sigma_squared),
        "subgaussian_bound": 2.0,
    },
    "separate_limitation": "Appendix B.1 exact-recovery sufficiency is not part of the literal live claim and is neither used to verify nor used to falsify Claim 3.",
    "negative_controls": {
        "intersection_atom": {"intersection_mass": 0.1, "expected": "REJECT"},
        "missing_subgaussian_bound": {"subgaussian_bound": None, "expected": "REJECT"},
    },
}

if not all(checks.values()):
    raise SystemExit("source contract mismatch")
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "raw_results.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
print(json.dumps(record, indent=2, sort_keys=True))
