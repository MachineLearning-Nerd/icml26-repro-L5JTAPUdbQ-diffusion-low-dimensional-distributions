import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('claim5', ROOT / 'src' / 'claim5_prior_rate_audit.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_prior_rate_audit_and_negative_control():
    module.main()
    result = json.loads((ROOT / 'outputs' / 'claim5_attempt1' / 'result.json').read_text())
    assert all(result['source_phrase_hits'].values())
    assert result['rate']['example']['correct_exponent'] == 4.0
    assert result['rate']['strictly_increases_with_d']
    assert result['negative_control']['equals_displayed_exponent'] is False
