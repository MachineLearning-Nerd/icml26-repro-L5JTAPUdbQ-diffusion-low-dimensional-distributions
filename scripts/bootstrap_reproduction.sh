#!/usr/bin/env bash
# Clean CPU-only bootstrap for the tracked theorem/source audits.
set -euo pipefail
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m playwright install chromium
.venv/bin/python -m pytest -q
