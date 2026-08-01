#!/usr/bin/env bash
# Clean CPU-only bootstrap for the tracked reproduction.
set -euo pipefail
uv sync --frozen --python 3.14
uv run python --version
getconf _NPROCESSORS_ONLN
uv run playwright install chromium
uv run pytest -q
