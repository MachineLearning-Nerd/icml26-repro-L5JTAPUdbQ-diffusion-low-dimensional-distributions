#!/usr/bin/env bash
set -euo pipefail
# Recreates only the checked summary from retained raw JSON; it never reruns expensive sampling.
.venv/bin/python src/aggregate_claim1_reverse.py --out outputs/claim1_reverse_full --write
(cd outputs/claim1_reverse_full && sha256sum -c SHA256SUMS)
