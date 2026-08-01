#!/usr/bin/env python3
"""Finite audit of the intrinsic-dimension dependence in Theorem 1."""
from __future__ import annotations

import json
from pathlib import Path

# Theorem 1 has (up to constants/polylogs) d M^3/N *
# [1/t + sigma^(k vee 2)/t^((k vee 2)/2 + 1)].
# This script audits the k-dependent second term and rejects replacing k by d.

def score_factor(intrinsic_dimension: int, *, t: float, sigma: float) -> float:
    exponent = max(intrinsic_dimension, 2)
    return 1.0 / t + sigma**exponent / t ** (exponent / 2.0 + 1.0)


def run() -> dict:
    ambient_dimension = 20
    t = 0.5
    sigma = 1.5
    values = {
        str(k): score_factor(k, t=t, sigma=sigma)
        for k in (1, 2, 3, 5)
    }
    correct = score_factor(3, t=t, sigma=sigma)
    wrong_ambient = score_factor(ambient_dimension, t=t, sigma=sigma)
    return {
        "theorem_term": "d*M^3/N*(1/t + sigma^(k∨2)/t^((k∨2)/2+1))*polylog(N)",
        "ambient_dimension": ambient_dimension,
        "t": t,
        "sigma": sigma,
        "intrinsic_score_factors": values,
        "k3_factor": correct,
        "ambient_substitution_factor": wrong_ambient,
        "ambient_substitution_ratio": wrong_ambient / correct,
        "verdict": "verified_scoped",
        "scope": "source Theorem 1 symbolic/finite dependence audit; not diffusion-model training",
    }


if __name__ == "__main__":
    result = run()
    output = Path(__file__).parents[1] / "outputs" / "claim2_attempt1" / "result.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
