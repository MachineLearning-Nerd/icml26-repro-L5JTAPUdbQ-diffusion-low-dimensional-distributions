import json
from pathlib import Path
from src.claim3_literal_uos_estimator import run
ROOT=Path(__file__).parents[1]

def test_literal_low_dimensional_clipping_and_controls():
 r, arrays, rows=run(seed=7,n=900,ne=64)
 a=r['assumption_checks']; e=r['estimator']
 assert a['union_support'] and a['intersection_mass_zero_by_construction']
 assert e['all_component_masses_pass'] and e['regularized_mse'] >= 0
 assert e['C_R']==1 and len(r['C_R_sweep']['nominal'])==3
 assert [x['C_R'] for x in r['C_R_sweep']['nominal']]==[.5,1.,2.]
 assert r['C_R_sweep']['intersection_atom'][1]['intersection_atom_executed']
 assert not r['C_R_sweep']['low_mass'][1]['all_component_masses_pass']
 assert arrays['nominal_C_R_1']['pointwise_sqerr_regularized'].shape==(64,)
 assert len(rows)==9

def test_saved_result_is_honest_and_raw_present():
 r=json.loads((ROOT/'outputs/claim3_literal_uos_estimator/summary.json').read_text())
 assert r['verdict']=='inconclusive' and 'low-dimensional clipping' in r['scope']
 assert r['config']['C_R_sweep']==[.5,1.,2.]
 assert (ROOT/'outputs/claim3_literal_uos_estimator/raw_arrays.npz').exists()
 assert 'unregularized_mse' in r['estimator']
