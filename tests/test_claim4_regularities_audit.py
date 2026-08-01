import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import claim4_regularities_audit

def test_claim4_source_scope_and_witness():
    claim4_regularities_audit.main()
    data=json.loads((Path(__file__).resolve().parents[1] / 'outputs/claim4_attempt1/result.json').read_text())
    assert data['verdict'] == 'verified_scoped'
    assert all(data['source_phrase_hits'].values())
    assert data['witness']['ambient_density_exists'] is False
    assert data['witness']['intersection_origin_mass'] == 0.0
    assert data['witness']['within_subspace_bound_less_than_2'] is True

def test_claim4_negative_control_fails_required_condition():
    data=json.loads((Path(__file__).resolve().parents[1] / 'outputs/claim4_attempt1/result.json').read_text())
    assert data['negative_control']['origin_mass_after_mutation'] > 0
    assert data['negative_control']['zero_intersection_mass_passes'] is False
