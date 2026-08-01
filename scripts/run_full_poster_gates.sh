#!/usr/bin/env bash
# Rebuild the pinned Posterly toolchain and run every poster gate without waivers.
set -euo pipefail

POSTERLY_REV="94d374d72afdc372af226eb745e82af00f07e43f"
POSTERLY_DIR=".tools/posterly"
PYTHON=".venv/bin/python"

if [[ ! -d "${POSTERLY_DIR}/.git" ]]; then
  mkdir -p .tools
  git clone https://github.com/Chenruishuo/posterly.git "${POSTERLY_DIR}"
fi
git -C "${POSTERLY_DIR}" fetch --depth 1 origin "${POSTERLY_REV}"
git -C "${POSTERLY_DIR}" checkout --detach "${POSTERLY_REV}"
[[ "$(git -C "${POSTERLY_DIR}" rev-parse HEAD)" == "${POSTERLY_REV}" ]]

set +e
"${PYTHON}" "${POSTERLY_DIR}/tools/run_gates.py" logbook/poster.html \
  --report logbook/GATE_REPORT.json \
  --manifest logbook/FIGURE_MANIFEST.json \
  --style-disable '' \
  --strict-polish \
  --reset-measure-budget
gate_status=$?
set -e

"${PYTHON}" - <<'PY'
import json
from pathlib import Path

report = json.loads(Path("logbook/GATE_REPORT.json").read_text())
print("# Complete Posterly gate diagnostics")
print(json.dumps(report, indent=2, sort_keys=True))
PY

exit "${gate_status}"
