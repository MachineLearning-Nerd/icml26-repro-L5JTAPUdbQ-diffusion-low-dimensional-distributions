#!/usr/bin/env python3
"""Offline release checks reproducible from a clean clone."""
from __future__ import annotations
import json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
expected=['executive-summary','claim-1-intrinsic-dimension-sample-rate','claim-2-intrinsic-score-error-rate','claim-3-union-of-subspaces-assumption','claim-4-weak-regularity-assumptions','claim-5-prior-ambient-dimensional-comparator','conclusion']
book=json.loads((ROOT/'.trackio/logbook/logbook.json').read_text())
actual=[x['slug'] for x in book['root']['children']]
assert actual==expected,(actual,expected)
assert book['traces']==[],'public clone must not advertise an untracked trace'
# Every evidence manifest is checked from the working directory encoded by its paths.
manifests=sorted((ROOT/'evidence').rglob('SHA256SUMS'))+sorted((ROOT/'outputs').rglob('SHA256SUMS'))+[ROOT/'logbook/release_artifacts/SHA256SUMS']
for manifest in manifests:
    rel=manifest.relative_to(ROOT)
    # Existing output manifests use paths relative to repository root; source manifest does too.
    # Claim1's manifest is bundle-relative and is therefore checked inside its bundle.
    first=next(line.split(maxsplit=1)[1] for line in manifest.read_text().splitlines() if line.strip())
    cwd=ROOT if '/' in first else manifest.parent
    subprocess.run(['sha256sum','-c',str(manifest if cwd==ROOT else manifest.name)],cwd=cwd,check=True,stdout=subprocess.DEVNULL)
print(f'offline release checks passed; {len(manifests)} source/evidence/release manifests verified; posterly full-gate and official-validator commands require documented external tools')
