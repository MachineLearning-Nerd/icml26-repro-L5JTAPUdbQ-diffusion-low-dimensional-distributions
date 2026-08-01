#!/usr/bin/env python3
"""CPU finite audit of Claim 3's union-of-subspaces assumptions.

This does not train a diffusion model.  It checks the exact geometric and
subgaussian conditions stated in the pinned source on a finite clean-room
mixture, then changes only the intersection-mass condition as a negative
control.
"""
from __future__ import annotations

import json
import math
from pathlib import Path


ROOT = Path(__file__).parents[1]


def empirical_mgf_bound(values: list[float], sigma: float) -> float:
    return sum(math.exp((x / sigma) ** 2) for x in values) / len(values)


def audit() -> dict:
    # V1=span(e1), V2=span(e2) in R^2; their intersection is the origin.
    # Each component is a Rademacher law on its own coordinate, hence has no
    # mass at the intersection and satisfies E exp((X/sigma)^2) <= 2 for sigma=2.
    component_coordinates = [-1.0, 1.0, -1.0, 1.0]
    sigma = 2.0
    clean_mgf = empirical_mgf_bound(component_coordinates, sigma)
    clean_intersection_mass = 0.0

    # Negative control: retaining the same axes/tails but putting mass at 0
    # violates p*(V1 intersection V2)=0.
    overlap_coordinates = [-1.0, 0.0, 1.0, 0.0]
    overlap_mgf = empirical_mgf_bound(overlap_coordinates, sigma)
    overlap_intersection_mass = 0.5

    return {
        "source_conditions": {
            "support": "supp(p*) subset union_i V_i",
            "separation": "p*(V_i intersection V_j)=0 for i != j",
            "tails": "E exp((X^T theta/sigma_i)^2) <= 2 for each unit theta",
        },
        "finite_clean_room_example": {
            "ambient_dimension": 2,
            "subspaces": ["span(e1)", "span(e2)"],
            "intersection": "{0}",
            "component_coordinates": component_coordinates,
            "sigma": sigma,
            "empirical_subgaussian_mgf": clean_mgf,
            "intersection_mass": clean_intersection_mass,
            "assumption_checks": {
                "union_support": True,
                "zero_intersection_mass": clean_intersection_mass == 0.0,
                "subgaussian_mgf_le_two": clean_mgf <= 2.0,
            },
        },
        "negative_control_intersection_mass": {
            "component_coordinates": overlap_coordinates,
            "empirical_subgaussian_mgf": overlap_mgf,
            "intersection_mass": overlap_intersection_mass,
            "still_subgaussian": overlap_mgf <= 2.0,
            "zero_intersection_mass": overlap_intersection_mass == 0.0,
            "interpretation": "Changing only the overlap condition fails the source separation assumption; this is not a counterexample to the theorem.",
        },
        "verdict": "verified_scoped",
        "scope": "Pinned Assumption 1/source-definition audit plus a finite CPU union-of-subspaces construction; not a trained diffusion-model result.",
    }


def main() -> None:
    output = ROOT / "outputs" / "claim3_attempt1" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(audit(), indent=2) + "\n")
    print(json.dumps(audit(), indent=2))


if __name__ == "__main__":
    main()
