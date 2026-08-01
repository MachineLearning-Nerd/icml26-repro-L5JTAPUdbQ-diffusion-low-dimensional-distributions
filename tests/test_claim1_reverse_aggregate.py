import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from aggregate_claim1_reverse import build

def test_checked_summary_is_rebuilt_from_raw_json():
    expected=build(ROOT/'outputs/claim1_reverse_full')
    actual=json.loads((ROOT/'outputs/claim1_reverse_full/summary.json').read_text())
    assert actual==expected

def test_aggregate_is_deterministic_without_rewriting_artifacts(tmp_path):
    got=subprocess.check_output([sys.executable,'src/aggregate_claim1_reverse.py','--out','outputs/claim1_reverse_full'],cwd=ROOT,text=True)
    assert json.loads(got)==build(ROOT/'outputs/claim1_reverse_full')
