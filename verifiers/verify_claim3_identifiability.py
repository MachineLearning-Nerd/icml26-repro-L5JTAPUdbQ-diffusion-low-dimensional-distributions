#!/usr/bin/env python3
"""Independently verify the Claim 3 identifiability counterexample."""
from __future__ import annotations

import json
import math
import sys
from itertools import combinations
from pathlib import Path


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def total_variation(left: dict[str, float], right: dict[str, float]) -> float:
    atoms = set(left) | set(right)
    return 0.5 * sum(abs(left.get(atom, 0.0) - right.get(atom, 0.0)) for atom in atoms)


if len(sys.argv) != 3:
    fail("usage: verify_claim3_identifiability.py RAW_JSON OUTPUT_JSON")

raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())
counterexample = raw["counterexample"]
assumptions = raw["assumption_checks"]
control = raw["distinguishable_negative_control"]

if (
    counterexample["d"],
    counterexample["M"],
    counterexample["k"],
    counterexample["c_p"],
) != (4, 2, 2, 1):
    fail("counterexample dimensions or component-mass constant changed")

pmf = counterexample["pmf"]
if not math.isclose(sum(pmf.values()), 1.0, abs_tol=1e-15):
    fail("counterexample PMF is not normalized")
if set(pmf) != {"-1,0,0,0", "0,-1,0,0", "0,1,0,0", "1,0,0,0"}:
    fail("counterexample support changed")


def coordinate_set(basis: list[list[int]]) -> frozenset[int]:
    coordinates = []
    for vector in basis:
        nonzero = [index for index, value in enumerate(vector) if value]
        if len(nonzero) != 1 or vector[nonzero[0]] != 1:
            fail("basis is not a standard orthonormal coordinate basis")
        coordinates.append(nonzero[0])
    return frozenset(coordinates)


def targets(parameterization: dict[str, list[list[int]]]) -> frozenset[frozenset[int]]:
    return frozenset(coordinate_set(basis) for basis in parameterization.values())


target_a = targets(counterexample["parameterization_a"])
target_b = targets(counterexample["parameterization_b"])
for target in (target_a, target_b):
    if len(target) != counterexample["M"]:
        fail("parameterization does not contain M distinct subspaces")
    if any(len(plane) != counterexample["k"] for plane in target):
        fail("a declared subspace does not have dimension k")
    if any(coordinate >= counterexample["d"] for plane in target for coordinate in plane):
        fail("a declared basis coordinate exceeds the ambient dimension")
    if any(left & right for left, right in combinations(target, 2)):
        fail("declared subspaces have nonzero pairwise intersection")
if target_a == target_b:
    fail("the two recovery targets are not distinct")


def atom_coordinate(atom: str) -> int:
    vector = tuple(map(int, atom.split(",")))
    if len(vector) != counterexample["d"]:
        fail("support atom has the wrong ambient dimension")
    nonzero = [index for index, value in enumerate(vector) if value]
    if len(nonzero) != 1 or abs(vector[nonzero[0]]) != 1:
        fail("support atom is not a signed coordinate vector")
    return nonzero[0]


support_coordinates = {atom: atom_coordinate(atom) for atom in pmf}
required_mass = 1.0 / (counterexample["c_p"] * counterexample["M"])
for target in (target_a, target_b):
    if not all(any(coordinate in plane for plane in target) for coordinate in support_coordinates.values()):
        fail("support is not contained in a declared union")
    component_masses = [
        sum(probability for atom, probability in pmf.items() if support_coordinates[atom] in plane)
        for plane in target
    ]
    if any(mass < required_mass - 1e-15 for mass in component_masses):
        fail("independently computed component mass violates Assumption 1")
    if any(not math.isclose(mass, 0.5, abs_tol=1e-15) for mass in component_masses):
        fail("counterexample component masses changed")
if not assumptions["support_contained_in_union_for_both_parameterizations"]:
    fail("support containment failed")
if assumptions["pairwise_intersections"] != "{0} in both parameterizations":
    fail("intersection condition is not established")
if not math.isclose(assumptions["probability_mass_on_each_pairwise_intersection"], 0.0, abs_tol=1e-15):
    fail("pairwise intersection has positive probability")
if not math.isclose(assumptions["required_component_mass"], required_mass, abs_tol=1e-15):
    fail("reported required component mass is inconsistent")
if not math.isclose(assumptions["component_mass"], required_mass, abs_tol=1e-15):
    fail("component-mass lower bound failed")

sigma_squared = assumptions["sigma_squared"]
worst_moment = math.exp(1.0 / sigma_squared)
if worst_moment > 2.0 + 1e-12:
    fail("Assumption 2 failed")
if not math.isclose(worst_moment, assumptions["subgaussian_worst_direction_moment"], rel_tol=1e-12):
    fail("reported subgaussian moment is inconsistent")

observed_tv = total_variation(pmf, pmf)
if not math.isclose(counterexample["observation_total_variation"], observed_tv, abs_tol=1e-15):
    fail("reported observation TV is not exactly zero")
if not counterexample["sample_law_identical_for_every_n0"]:
    fail("all-sample-size indistinguishability is missing")
if not math.isclose(counterexample["maximin_exact_recovery_success"], 0.5, abs_tol=1e-15):
    fail("Le Cam two-point success bound changed")

control_tv = total_variation(control["left_pmf"], control["right_pmf"])
if not math.isclose(control_tv, 1.0, abs_tol=1e-15):
    fail("distinguishable control must have TV one")
if control["indistinguishability_argument_applies"]:
    fail("negative control unexpectedly claims indistinguishability")

result = {
    "status": "PASS",
    "verdict": "FALSIFIED",
    "checks": {
        "assumption_1": True,
        "assumption_2": True,
        "distinct_targets": True,
        "identical_sample_laws": True,
        "maximin_success_at_most_one_half": True,
        "n_minus_10_contradiction_for_sufficiently_large_n": True,
        "distinguishable_control_rejected": True,
    },
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
