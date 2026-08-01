#!/usr/bin/env python3
"""Independently verify the atomic weak-regularity experiment."""
from __future__ import annotations

import hashlib
import json
import math
import sys
import tarfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evidence" / "source" / "arxiv_source.tar"


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def member_text(member: str) -> str:
    with tarfile.open(SOURCE) as archive:
        extracted = archive.extractfile(member)
        if extracted is None:
            fail(f"missing {member}")
        return extracted.read().decode()


if len(sys.argv) != 3:
    fail("usage: verify_claim4_atomic_weak_regularity.py RAW_JSON OUTPUT_JSON")
raw_path, output_path = map(Path, sys.argv[1:])
raw = json.loads(raw_path.read_text())
expected_hash = "07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7"
if sha256(SOURCE) != expected_hash or raw.get("source_hash") != expected_hash:
    fail("the pinned paper source hash changed")

abstract = member_text("abstract.tex")
introduction = member_text("introduction.tex")
problem = member_text("problem_formulation.tex")
results_source = member_text("Results.tex")
expected_source_checks = {
    "abstract_named_regularities": "without imposing smoothness, bounded-density, or log-concavity assumptions" in abstract,
    "introduction_no_score_or_density_restrictions": "without imposing any restrictive assumptions on scores or densities" in introduction,
    "bounded_support_is_subgaussian": "subsumes any distribution with bounded support" in problem,
    "both_theorems_only_assumptions_1_and_2": results_source.count(
        "Suppose the target distribution $p^\\star$ satisfies Assumptions~\\ref{assume:multi-modal} and \\ref{assump:sub-gaussian target}."
    )
    == 2,
}
if not all(expected_source_checks.values()) or raw.get("source_checks") != expected_source_checks:
    fail("the source-scope certificate changed")

configuration = raw.get("configuration", {})
expected_configuration = {
    "d": 48,
    "M": 128,
    "k": 3,
    "atoms_per_component": 6,
    "sample_sizes": [6250, 12500, 25000, 50000],
    "seeds": list(range(20264001, 20264021)),
    "evaluation_samples_per_seed": 10000,
    "diffusion_time": 0.25,
    "basis_seed": 260530153,
    "regularization_constant_C_R": 4.0,
}
for key, value in expected_configuration.items():
    if configuration.get(key) != value:
        fail(f"configuration changed: {key}")

assumptions = raw.get("assumption_checks", {})
required_true = (
    "support_in_union",
    "pairwise_intersection_is_zero",
    "zero_intersection_mass",
    "each_component_atoms_span_k",
    "bounded_support",
)
if not all(assumptions.get(key) is True for key in required_true):
    fail("the atomic target fails a paper assumption")
if not math.isclose(assumptions.get("component_mass", -1), 1 / 128, rel_tol=0, abs_tol=1e-15):
    fail("component mass changed")
if not math.isclose(
    assumptions.get("worst_direction_exponential_square_moment", -1),
    2,
    rel_tol=1e-12,
    abs_tol=1e-12,
):
    fail("the exact subgaussian moment certificate changed")
if raw.get("geometry", {}).get("intersection_spectral_gap", 0) <= 0:
    fail("subspace intersections were not excluded")

regularity = raw.get("regularity_failures", {})
required_false = (
    "ambient_lebesgue_density_exists",
    "intrinsic_lebesgue_density_exists",
    "holder_density",
    "log_concave_measure",
    "uniform_density_upper_bound_applicable",
    "positive_density_lower_bound_applicable",
)
if not all(regularity.get(key) is False for key in required_false):
    fail("the target no longer violates every named regularity")

cells = sorted(raw.get("cells", []), key=lambda cell: cell["N"])
if [cell["N"] for cell in cells] != expected_configuration["sample_sizes"]:
    fail("the sample-size sweep is incomplete")
for cell in cells:
    values = np.asarray(cell.get("seed_mse", []), dtype=np.float64)
    controls = np.asarray(cell.get("seed_omitted_normal_mse", []), dtype=np.float64)
    if len(values) != 20 or len(controls) != 20 or np.any(values <= 0):
        fail("a seed result is absent or invalid")
    mean = float(np.mean(values))
    half_width = 2.093 * float(np.std(values, ddof=1)) / math.sqrt(len(values))
    if not math.isclose(cell["mean_mse"], mean, rel_tol=1e-12, abs_tol=1e-14):
        fail("a reported MSE mean changed")
    if not math.isclose(cell["ci95_low"], mean - half_width, rel_tol=1e-12, abs_tol=1e-14):
        fail("a reported confidence interval changed")
    if not math.isclose(cell["ci95_high"], mean + half_width, rel_tol=1e-12, abs_tol=1e-14):
        fail("a reported confidence interval changed")
    if cell.get("minimum_component_count", 0) <= 0:
        fail("the exact-recovery conditional component event failed")

slope = float(
    np.polyfit(
        np.log([cell["N"] for cell in cells]),
        np.log([cell["mean_mse"] for cell in cells]),
        1,
    )[0]
)
control_ratio = float(
    np.mean(cells[-1]["seed_omitted_normal_mse"])
    / np.mean(cells[-1]["seed_mse"])
)
if not math.isclose(raw.get("log_log_N_slope", 0), slope, rel_tol=1e-12, abs_tol=1e-14):
    fail("the N-scaling slope changed")
if not (-1.5 <= slope <= -0.2):
    fail("the N-scaling result missed its precommitted range")
if not math.isclose(
    raw.get("omitted_normal_control_ratio_at_N_50000", 0),
    control_ratio,
    rel_tol=1e-12,
    abs_tol=1e-12,
):
    fail("the omitted-normal control ratio changed")
if control_ratio <= 10:
    fail("the omitted-normal scientific control did not fail strongly")
if raw.get("verdict") != "VERIFIED" or raw.get("confidence") != "MEDIUM":
    fail("the claim verdict or confidence changed")
if not all(raw.get("acceptance", {}).values()):
    fail("an acceptance gate failed")

result = {
    "status": "PASS",
    "verdict": "VERIFIED",
    "confidence": "MEDIUM",
    "claim": 4,
    "checks": {
        "pinned_source_scope": True,
        "paper_scale_configuration": True,
        "all_assumptions": True,
        "no_density_or_named_regularity": True,
        "twenty_seed_complete_sweep": True,
        "independent_uncertainty": True,
        "N_scaling": True,
        "omitted_normal_control": True,
    },
    "log_log_N_slope": slope,
    "omitted_normal_control_ratio": control_ratio,
}
output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps(result, indent=2, sort_keys=True))
