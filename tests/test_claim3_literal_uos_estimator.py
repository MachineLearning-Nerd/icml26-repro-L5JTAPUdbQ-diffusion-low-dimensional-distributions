import json
from pathlib import Path
from src.claim3_literal_uos_estimator import run
ROOT=Path(__file__).parents[1]
def test_literal_conditions_and_estimator():
 r=run(seed=7,n=900,ne=64)
 a=r['assumption_checks']
 assert a['union_support'] and a['intersection_mass_zero_by_construction']
 assert a['all_component_masses_pass'] and a['subgaussian_mgf_le_2']
 assert r['estimator']['exact_smoothed_mixture_score_vs_empirical_component_kde_score_mse'] >= 0
 assert r['controls']['intersection_atom']['separation_passes'] is False
def test_saved_result_is_honest():
 r=json.loads((ROOT/'outputs/claim3_literal_uos_estimator/summary.json').read_text())
 assert r['verdict']=='inconclusive'
 assert 'cannot verify' in r['scope']
 assert set(r['proof_dependency_map'])=={'union_support_and_zero_intersection','per_component_mass','subgaussian_within_subspace','orthogonal_basis'}
