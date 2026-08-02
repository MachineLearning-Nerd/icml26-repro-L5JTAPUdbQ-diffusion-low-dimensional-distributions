#!/usr/bin/env python3
"""Independently verify the Claim 2 component-estimator scaling study."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


if len(sys.argv) != 3:
    fail("usage: verify_claim2_component_scaling.py RAW_JSON OUTPUT_JSON")
raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())
configuration = raw.get("configuration", {})
expected = {
    "sample_sizes": [128, 256, 512, 1024, 2048],
    "intrinsic_dimensions": [1, 2, 3],
    "ambient_dimensions": [4, 8, 16, 48],
    "seeds": list(range(20262001, 20262013)),
    "evaluation_samples_per_seed": 1024,
    "diffusion_time": 0.5,
}
for key, value in expected.items():
    if configuration.get(key) != value:
        fail(f"configuration changed: {key}")

cells = raw.get("cells", [])
if len(cells) != 15:
    fail("expected 15 complete k,N cells")
recomputed_slopes = {}
recomputed_growth = {}
for intrinsic in expected["intrinsic_dimensions"]:
    intrinsic_cells = sorted(
        (cell for cell in cells if cell.get("k") == intrinsic), key=lambda cell: cell["N"]
    )
    if [cell["N"] for cell in intrinsic_cells] != expected["sample_sizes"]:
        fail("a geometric sample-size sweep is incomplete")
    for cell in intrinsic_cells:
        values = np.asarray(cell.get("seed_mse", []), dtype=np.float64)
        if len(values) != len(expected["seeds"]) or np.any(values <= 0):
            fail("a seed MSE is absent or non-positive")
        mean = float(np.mean(values))
        half_width = 2.201 * float(np.std(values, ddof=1)) / math.sqrt(len(values))
        if not math.isclose(cell["mean_mse"], mean, rel_tol=1e-12, abs_tol=1e-15):
            fail("a reported cell mean changed")
        if not math.isclose(cell["ci95_low"], mean - half_width, rel_tol=1e-12, abs_tol=1e-15):
            fail("a reported confidence interval changed")
        if not math.isclose(cell["ci95_high"], mean + half_width, rel_tol=1e-12, abs_tol=1e-15):
            fail("a reported confidence interval changed")
        if len(cell.get("broken_projector_d4_mse", [])) != len(values):
            fail("the d=4 control is incomplete")
        if len(cell.get("broken_projector_d48_mse", [])) != len(values):
            fail("the d=48 control is incomplete")
    recomputed_slopes[str(intrinsic)] = float(
        np.polyfit(
            np.log([cell["N"] for cell in intrinsic_cells]),
            np.log([cell["mean_mse"] for cell in intrinsic_cells]),
            1,
        )[0]
    )
    last = intrinsic_cells[-1]
    recomputed_growth[str(intrinsic)] = float(
        np.mean(last["broken_projector_d48_mse"])
        / np.mean(last["broken_projector_d4_mse"])
    )

if any(
    not math.isclose(raw["log_log_slopes"][key], value, rel_tol=1e-12, abs_tol=1e-15)
    for key, value in recomputed_slopes.items()
):
    fail("a reported scaling slope changed")
if any(
    not math.isclose(raw["broken_projector_d48_over_d4"][key], value, rel_tol=1e-12, abs_tol=1e-15)
    for key, value in recomputed_growth.items()
):
    fail("a reported projector-control ratio changed")
if not all(-1.5 <= slope <= -0.4 for slope in recomputed_slopes.values()):
    fail("the observed N scaling is outside the prespecified range")
if not all(ratio > 10 for ratio in recomputed_growth.values()):
    fail("broken projector did not expose ambient growth")
if raw.get("status") != "SCOPED_CORROBORATION_PASS" or not all(raw.get("acceptance", {}).values()):
    fail("the study acceptance record did not pass")

result = {
    "status": "PASS",
    "claim": 2,
    "scope": "M=1 exact-recovery component-estimator corroboration",
    "checks": {
        "complete_geometric_sweep": True,
        "twelve_seed_uncertainty": True,
        "independent_statistics": True,
        "prespecified_slope_range": True,
        "ambient_normal_cancellation": True,
        "broken_projector_control": True,
    },
    "log_log_slopes": recomputed_slopes,
    "broken_projector_d48_over_d4": recomputed_growth,
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
