#!/usr/bin/env bash
# Clean CPU-only bootstrap for the tracked reproduction.
set -euo pipefail
uv sync --frozen --python 3.14.2
uv run python scripts/report_environment.py
uv run python scripts/run_research_checks.py
uv run playwright install chromium
uv run python -m pytest -q
