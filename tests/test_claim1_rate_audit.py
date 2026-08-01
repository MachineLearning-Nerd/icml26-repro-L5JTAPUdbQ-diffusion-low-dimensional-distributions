import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_rate_audit_and_ambient_negative_control():
    subprocess.run([sys.executable, "src/claim1_rate_audit.py"], cwd=ROOT, check=True)
    result = json.loads((ROOT / "outputs/claim1_attempt1/result.json").read_text())
    assert result["verdict"] == "verified_scoped"
    assert [row["published_epsilon_exponent"] for row in result["rows"]] == [2, 2, 3, 5]
    control = result["negative_control"]
    assert control["passes"] is True
    assert control["correct_exponent"] == 3
    assert control["incorrect_exponent"] == 20
    assert control["factor_ratio"] == pytest.approx(10**17)
