import json
from pathlib import Path

from src.claim3_non_toy_dependency_audit import allocation_grid, score_identity


def test_48d_128_component_normal_tangent_identity_is_numerically_exact():
    r = score_identity(7, n_eval=128)
    assert r['d'] == 48 and r['M'] == 128 and r['k'] == 3
    assert r['generic_subspace_intersection_dimension_upper_bound'] == 0
    assert r['max_abs_score_identity_error'] < 1e-10
    assert r['posterior_row_sum_max_error'] < 1e-10


def test_allocation_event_and_vanishing_mass_control():
    rows, _ = allocation_grid(9, trials=2000)
    clean = rows[:3]
    assert all(row['observed_event_failure_rate'] <= row['chernoff_union_upper_bound'] for row in clean)
    weak = rows[3]
    assert weak['control'] == 'vanishing_component_mass'
    assert weak['observed_event_failure_rate'] > .99


def test_retained_fullscale_result_has_required_controls():
    p = Path(__file__).parents[1] / 'outputs/claim3_fullscale/result.json'
    d = json.loads(p.read_text())
    assert len(d['allocation_grid']) == 4
    assert d['allocation_grid'][0]['trials'] == 100000
    assert d['score_identity']['d'] == 48
    assert d['score_identity']['M'] == 128
    assert d['assumption_removal_controls']['positive_intersection_atom_control']['zero_intersection_condition'] is False
    assert d['assumption_removal_controls']['heavy_tail_control']['subgaussian_condition_certified'] is False
