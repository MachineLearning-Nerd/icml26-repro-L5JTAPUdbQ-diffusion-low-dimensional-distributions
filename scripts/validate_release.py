#!/usr/bin/env python3
"""Run the cheap deterministic scientific and structural release gates."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(*arguments: str) -> None:
    subprocess.run([PYTHON, *arguments], cwd=ROOT, check=True)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


run(
    "verifiers/verify_claim1_threshold_escape.py",
    ".openresearch/artifacts/claim1_threshold_escape/raw_results.json",
    ".openresearch/artifacts/claim1_threshold_escape/independent_checker.json",
)
run(
    "verifiers/verify_claim2_intrinsic_score.py",
    ".openresearch/artifacts/claim2_intrinsic_score/raw_results.json",
    ".openresearch/artifacts/claim2_intrinsic_score/independent_checker.json",
)
run(
    "verifiers/verify_claim2_component_scaling.py",
    ".openresearch/artifacts/claim2_component_scaling/raw_results.json",
    ".openresearch/artifacts/claim2_component_scaling/independent_checker.json",
)
run("verifiers/verify_claim3_literal_assumption.py")
run(
    "verifiers/verify_claim4_threshold_falsification.py",
    ".openresearch/artifacts/claim4_threshold_falsification/raw_results.json",
    ".openresearch/artifacts/claim1_threshold_escape/raw_results.json",
    ".openresearch/artifacts/claim4_threshold_falsification/independent_checker.json",
)
run(
    "verifiers/verify_claim5_primary_proof_chain.py",
    ".openresearch/artifacts/claim5_prior_rate/raw_results.json",
    ".openresearch/artifacts/claim5_prior_rate/independent_checker.json",
)

logbook = json.loads((ROOT / "logbook.json").read_text())
root = logbook["root"]
expected = [
    ("index", "pages/index.md"),
    ("executive-summary", "pages/executive-summary/page.md"),
    ("claim-1-intrinsic-dimension-sample-rate", "pages/claim-1-intrinsic-dimension-sample-rate/page.md"),
    ("claim-2-intrinsic-score-error-rate", "pages/claim-2-intrinsic-score-error-rate/page.md"),
    ("claim-3-union-of-subspaces-assumption", "pages/claim-3-union-of-subspaces-assumption/page.md"),
    ("claim-4-weak-regularity-assumptions", "pages/claim-4-weak-regularity-assumptions/page.md"),
    ("claim-5-prior-ambient-dimensional-comparator", "pages/claim-5-prior-ambient-dimensional-comparator/page.md"),
    ("conclusion", "pages/conclusion/page.md"),
]
actual = [(root["slug"], root["file"])] + [
    (page["slug"], page["file"]) for page in root["children"]
]
require(actual == expected, "page order or route changed")
require(all(not page["children"] for page in root["children"]), "nested sidebar page found")
require(all((ROOT / path).is_file() for _, path in expected), "required page missing")

pages = "\n".join((ROOT / path).read_text() for _, path in expected)
require("#/current-" not in pages, "stale quarantined route link found")
require("Appendix B.1" in pages and "outside the literal" in pages, "Claim 3 scope boundary missing")
require((ROOT / "logbook/poster_embed.html").is_file(), "poster_embed.html missing")
poster = (ROOT / "logbook/poster_embed.html").read_text()
require("Score boundary" in poster and "Claim 3" in poster, "poster scope or score boundary missing")

verdicts = json.loads((ROOT / "reproduction_verdicts.json").read_text())
require(verdicts["candidate_only"] is True, "candidate score boundary missing")
require([row["claim"] for row in verdicts["claims"]] == [1, 2, 3, 4, 5], "claim order changed")
require([row["verdict"] for row in verdicts["claims"]] == ["FALSIFIED", "VERIFIED", "VERIFIED", "FALSIFIED", "VERIFIED"], "candidate verdict changed")

print("PASS: six scientific checks, fixed eight-page tree, poster, and score boundary")
