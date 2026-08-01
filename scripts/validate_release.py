#!/usr/bin/env python3
"""Offline release checks reproducible from a clean clone.

This checks tracked page order, source manifests, and deliberately refuses to
call posterly strict gates when its vendored challenge toolchain is absent.
"""
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
expected = ["executive-summary", "claim-1-intrinsic-dimension-sample-rate", "claim-2-intrinsic-score-error-rate", "claim-3-union-of-subspaces-assumption", "claim-4-weak-regularity-assumptions", "claim-5-prior-ambient-dimensional-comparator", "conclusion"]
book = json.loads((ROOT / ".trackio/logbook/logbook.json").read_text())
actual = [x["slug"] for x in book["root"]["children"]]
assert actual == expected, (actual, expected)
assert book["traces"] == [], "public clone must not advertise an untracked trace"
for manifest in [ROOT / "evidence/source/SHA256SUMS", *sorted((ROOT / "evidence").glob("claim*_attempt1/SHA256SUMS"))]:
    subprocess.run(["sha256sum", "-c", str(manifest)], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
print("offline release checks passed; posterly full-gate and official-validator commands require documented external tools")
