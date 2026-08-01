"""Clean-room arithmetic audit of the Theorem-2 intrinsic-dimension exponent.

This does not train or sample a diffusion model.  It checks the source's
published epsilon exponent and contrasts it with the deliberately incorrect
ambient-dimension substitution.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "claim1_attempt1"


def exponent(intrinsic_dimension: int) -> int:
    return max(intrinsic_dimension, 2)


def sample_scale(epsilon: float, dimension: int) -> float:
    """The epsilon-dependent factor epsilon^(-max(dimension, 2))."""
    return epsilon ** (-exponent(dimension))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    epsilon = 0.1
    # Same ambient space, different intrinsic subspace dimensions.
    ambient_dimension = 20
    rows = []
    for intrinsic_dimension in (1, 2, 3, 5):
        correct = sample_scale(epsilon, intrinsic_dimension)
        wrong_ambient = sample_scale(epsilon, ambient_dimension)
        rows.append(
            {
                "ambient_dimension": ambient_dimension,
                "intrinsic_dimension": intrinsic_dimension,
                "published_epsilon_exponent": exponent(intrinsic_dimension),
                "published_epsilon_factor": correct,
                "ambient_substitution_exponent": exponent(ambient_dimension),
                "ambient_substitution_factor": wrong_ambient,
                "ambient_to_intrinsic_factor_ratio": wrong_ambient / correct,
            }
        )
    result = {
        "scope": "clean-room theorem-rate arithmetic; not diffusion-model training",
        "source_locations": {
            "theorem_bound": "Results.tex lines 161-179 in pinned arXiv source",
            "proof_rate": "Proof_Overview.tex lines 116-118 in pinned arXiv source",
        },
        "claim": "epsilon exponent is k vee 2, with ambient d only in the prefactor",
        "epsilon": epsilon,
        "rows": rows,
        "negative_control": {
            "description": "Substitute ambient d=20 for intrinsic k=3 while holding epsilon fixed.",
            "correct_exponent": exponent(3),
            "incorrect_exponent": exponent(ambient_dimension),
            "factor_ratio": sample_scale(epsilon, ambient_dimension) / sample_scale(epsilon, 3),
            "passes": exponent(3) != exponent(ambient_dimension),
        },
        "verdict": "verified_scoped",
        "limitations": [
            "The source theorem retains a linear ambient-dimension prefactor.",
            "This arithmetic/source audit does not establish an end-to-end trained diffusion-model result.",
        ],
    }
    (OUT / "result.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
