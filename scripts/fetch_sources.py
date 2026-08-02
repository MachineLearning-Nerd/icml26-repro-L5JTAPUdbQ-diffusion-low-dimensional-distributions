#!/usr/bin/env python3
"""Fetch the three pinned public arXiv inputs when they are absent."""
from __future__ import annotations

import hashlib
import os
import tempfile
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    (
        "https://export.arxiv.org/e-print/2605.30153",
        ROOT / "evidence/source/arxiv_source.tar",
        "07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7",
    ),
    (
        "https://export.arxiv.org/e-print/2503.09583",
        ROOT / "evidence/claim5_attempt1/prior_sources/cai2503.09583.tar.gz",
        "fc462d3046091f2d050bfa2fac0d2e1905a7e144dff4379f4b921afb0f64d211",
    ),
    (
        "https://export.arxiv.org/e-print/2402.15602",
        ROOT / "evidence/claim5_attempt1/prior_sources/zhang2402.15602.tar.gz",
        "76ad896b273e22ead0ee136bd80422a3498a5950b237a5e867ed7a304c891650",
    ),
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


for url, path, expected in SOURCES:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if digest(path) != expected:
            raise SystemExit(f"existing source has wrong SHA-256: {path}")
        print(f"PASS existing {path.relative_to(ROOT)}")
        continue
    with urllib.request.urlopen(url, timeout=60) as response:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            for block in iter(lambda: response.read(1024 * 1024), b""):
                handle.write(block)
    if digest(temporary) != expected:
        temporary.unlink()
        raise SystemExit(f"downloaded source has wrong SHA-256: {url}")
    os.replace(temporary, path)
    print(f"PASS downloaded {path.relative_to(ROOT)}")
