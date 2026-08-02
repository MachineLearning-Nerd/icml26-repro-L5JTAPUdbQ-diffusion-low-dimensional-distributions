import json
from pathlib import Path
from src.claim3_literal_uos_estimator import run
ROOT=Path(__file__).parents[1]
def test_literal_regularization_and_executed_controls():
 r, arrays=run(seed=7,n=900,ne=64)
 a=r['assumption_checks']; e=r['estimator']
 assert a['union_support'] and a['intersection_mass_zero_by_construction']
 assert e['all_component_masses_pass'] and e['regularized_mse'] >= 0
 assert len(e['psi_pass_rates'])==3 and len(e['gate_pass_rates'])==3
 assert r['controls']['intersection_atom']['intersection_atom_executed']
 assert not r['controls']['low_mass']['all_component_masses_pass']
 assert arrays['nominal']['pointwise_sqerr_regularized'].shape==(64,)
def test_saved_result_is_honest_and_raw_present():
 r=json.loads((ROOT/'outputs/claim3_literal_uos_estimator/summary.json').read_text())
 assert r['verdict']=='inconclusive' and 'neither proves' in r['scope']
 assert (ROOT/'outputs/claim3_literal_uos_estimator/raw_arrays.npz').exists()
 assert 'unregularized_mse' in r['estimator']
