#!/usr/bin/env bash
# Clean CPU-only bootstrap for the tracked reproduction.
set -euo pipefail
uv sync --frozen --python 3.14
uv run python scripts/fetch_sources.py
uv run python scripts/report_environment.py
