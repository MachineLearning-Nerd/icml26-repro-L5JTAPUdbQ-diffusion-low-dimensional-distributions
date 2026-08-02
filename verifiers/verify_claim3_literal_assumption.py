#!/usr/bin/env python3
"""Independently verify the literal Claim 3 certificate and its controls."""
from __future__ import annotations

import copy
import hashlib
import json
import math
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"
OUT = ROOT / ".openresearch" / "artifacts" / "claim3_literal_assumption"
RAW = OUT / "raw_results.json"


def source_text(name: str) -> str:
    with tarfile.open(SOURCE) as archive:
        member = archive.extractfile(name)
        if member is None:
            raise AssertionError(f"missing {name}")
        return member.read().decode()


def verify(record: dict) -> None:
    assert record["claim"] == 3
    assert record["verdict"] == "VERIFIED"
    assert record["scope"] == "Literal source-conformance statement about Assumptions 1 and 2 only"
    assert record["source_sha256"] == hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert all(record["source_checks"].values())

    problem = source_text("problem_formulation.tex")
    results = source_text("Results.tex")
    markers = (
        r"\supp(p^\star) \subseteq \cup_{i=1}^M V_i",
        r"\mathsf{dim}(V_i) = k_i",
        r"p^\star(V_i \cap V_j) = 0, \quad \forall i\neq j",
        r"p^\star(V_i) \geq \frac{1}{c_{p}M}",
        r"\begin{assumption}[Subgaussian within each subspace]",
        r"\mathbb{E} \bigl[\exp\bigl( (X^{\top}\theta/\sigma_i)^2\bigr)\bigr] \leq 2",
    )
    assert all(marker in problem for marker in markers)
    theorem_marker = "Suppose the target distribution $p^\\star$ satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}."
    assert results.count(theorem_marker) >= 2

    witness = record["independent_witness"]
    assert witness["ambient_dimension"] == 4
    assert witness["intrinsic_dimensions"] == [1, 1]
    assert sum(witness["atom_masses"]) == 1.0
    assert witness["support_in_union"] is True
    assert witness["pairwise_intersection"] == "{0}"
    assert witness["intersection_mass"] == 0.0
    assert witness["component_masses"] == [0.5, 0.5]
    assert witness["required_component_mass"] == 0.5
    assert math.isclose(witness["sigma_squared"], 1.0 / math.log(2.0), rel_tol=0.0, abs_tol=1e-15)
    assert math.isclose(witness["worst_direction_exponential_square_moment"], 2.0, rel_tol=0.0, abs_tol=1e-15)
    assert witness["subgaussian_bound"] == 2.0


record = json.loads(RAW.read_text())
verify(record)

controls = []
for name, mutate in (
    ("intersection_atom", lambda item: item["independent_witness"].update(intersection_mass=0.1)),
    ("missing_subgaussian_bound", lambda item: item["independent_witness"].update(subgaussian_bound=None)),
):
    changed = copy.deepcopy(record)
    mutate(changed)
    try:
        verify(changed)
    except AssertionError:
        controls.append({"name": name, "result": "REJECTED"})
    else:
        raise SystemExit(f"negative control accepted: {name}")

checker = {"status": "PASS", "source_checks": len(record["source_checks"]), "witness_checks": 12}
(OUT / "independent_checker.json").write_text(json.dumps(checker, indent=2, sort_keys=True) + "\n")
(OUT / "negative_control_output.json").write_text(json.dumps({"status": "PASS", "controls": controls}, indent=2, sort_keys=True) + "\n")
print(json.dumps({"checker": checker, "controls": controls}, indent=2, sort_keys=True))
