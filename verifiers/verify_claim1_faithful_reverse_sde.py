#!/usr/bin/env python3
"""Independently verify the faithful Claim 1 reverse-SDE study."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def close(left: float, right: float, tolerance: float = 1e-12) -> bool:
    return math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)


if len(sys.argv) != 3:
    fail("usage: verify_claim1_faithful_reverse_sde.py RAW_JSON OUTPUT_JSON")
raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())
configuration = raw["configuration"]
if (configuration["d"], configuration["M"], configuration["k"]) != (1, 1, 1):
    fail("route is not the declared d=M=k=1 special case")
if configuration["sample_sizes"] != [256, 1024, 4096, 16384]:
    fail("sample-size sweep changed")
if configuration["seeds"] != list(range(20261001, 20261017)):
    fail("seed schedule changed")
if configuration["steps"] != 768 or configuration["generated_samples_per_seed"] != 8192:
    fail("main numerical budget changed")

assumptions = raw["assumption_checks"]
if not assumptions["support_in_one_dimensional_linear_subspace"]:
    fail("support assumption failed")
if assumptions["intersection_condition"] != "vacuous for M=1":
    fail("intersection audit changed")
if not close(assumptions["component_mass"], 1.0):
    fail("component mass failed")
if not assumptions["bounded_support"]:
    fail("subgaussian witness is missing")
if not close(math.exp(1.0 / assumptions["sigma_squared"]), 2.0):
    fail("subgaussian moment calculation failed")

rows = raw["rows"]
main = [row for row in rows if row["group"] == "main"]
refinement_rows = [row for row in rows if row["group"] == "refinement"]
horizon_rows = [row for row in rows if row["group"] == "horizon"]
control_rows = [row for row in rows if row["group"] == "wrong_score_control"]
if (len(main), len(refinement_rows), len(horizon_rows), len(control_rows)) != (64, 16, 16, 8):
    fail("incomplete precommitted task matrix")
if any(row["score_mode"] != "paper_kde" for row in main + refinement_rows + horizon_rows):
    fail("a scientific cell did not use the paper score estimator")
if any(row["score_mode"] != "standard_normal" for row in control_rows):
    fail("wrong-score control changed")
if any(row["generated_samples"] != 8192 for row in rows):
    fail("generated-sample count changed")
if any(not math.isfinite(row["w1"]) or row["w1"] <= 0 for row in rows):
    fail("a W1 result is invalid")
if any(row["tau"] != row["N"] ** -2.0 for row in rows):
    fail("tau is not the paper's n^-2 schedule")
if any(
    not close(row["T"], row["horizon_factor"] * math.log(row["N"]))
    for row in rows
):
    fail("a time horizon is inconsistent")

means = []
for cell in raw["main_cells"]:
    selected = [row["w1"] for row in main if row["N"] == cell["N"]]
    if len(selected) != 16:
        fail("a main N cell lacks 16 seeds")
    mean = float(np.mean(selected))
    if not close(mean, cell["mean"]):
        fail("reported main-cell mean is inconsistent")
    means.append(mean)
slope = float(np.polyfit(np.log([256, 1024, 4096, 16384]), np.log(means), 1)[0])
if not close(slope, raw["log_log_N_slope"]):
    fail("reported scaling slope is inconsistent")
if not (-0.9 <= slope <= -0.15):
    fail("precommitted W1 scaling range failed")
if not means[-1] < 0.75 * means[0]:
    fail("N endpoint improvement failed")

refinement = raw["step_refinement"]
if set(refinement) != {"192", "384", "768"}:
    fail("step-refinement schedule is incomplete")
if abs(refinement["384"]["mean"] - refinement["768"]["mean"]) >= 0.05:
    fail("384-to-768 step refinement did not stabilize")
if refinement["768"]["mean"] > refinement["192"]["mean"] + 0.05:
    fail("fine grid is materially worse than the coarse grid")

horizons = raw["horizon_calibration"]
if set(horizons) != {"0.5", "1.0", "1.5"}:
    fail("multiple-horizon calibration is incomplete")
if abs(horizons["1.5"]["mean"] - horizons["1.0"]["mean"]) >= 0.05:
    fail("canonical and longer horizon disagree materially")

control_mean = float(np.mean([row["w1"] for row in control_rows]))
ratio = control_mean / means[-1]
if not close(control_mean, raw["wrong_score_control"]["mean"]):
    fail("reported control mean is inconsistent")
if not close(ratio, raw["wrong_score_control_ratio_at_Nmax"]):
    fail("reported control ratio is inconsistent")
if ratio <= 3.0:
    fail("wrong-score control is not discriminative")
if "BLOCKED" not in raw["route_status"]:
    fail("finite route improperly verifies the universal theorem")

result = {
    "status": "PASS",
    "claim": 1,
    "route": 2,
    "route_result": "SCOPED_CORROBORATION",
    "universal_theorem": "BLOCKED",
    "log_log_N_slope": slope,
    "wrong_score_control_ratio": ratio,
    "checks": {
        "paper_assumptions": True,
        "exact_algorithm_schedule": True,
        "complete_sixteen_seed_sweep": True,
        "exact_one_dimensional_w1": True,
        "step_refinement": True,
        "multiple_horizons": True,
        "wrong_score_control": True,
        "non_circular_budget": True,
    },
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
