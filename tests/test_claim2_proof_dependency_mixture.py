import importlib.util
from pathlib import Path
import numpy as np
P=Path(__file__).resolve().parents[1]/'src/claim2_proof_dependency_mixture.py'
s=importlib.util.spec_from_file_location('c2mix',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_theorem_time_factor_identity_and_intrinsic_exponent():
 c=m.proof_checks(1800,3,2,.6,1.)
 assert c['checks_pass'] and c['algebra_abs_error'] < 1e-13 and c['k_vee_2']==2
 assert c['source_A_complement_upper_bound_cp_1'] > 0
def test_analytic_mixture_score_and_estimator_are_finite():
 r=np.random.default_rng(9); A=m.bases(); train,lab=m.sample(r,A,150);x,_=m.sample(r,A,19,.6)
 truth=m.exact_score(x,A,.6); est=m.estimate(x,train,lab,A,.6)
 assert truth.shape==est.shape==(19,6)
 assert np.isfinite(truth).all() and np.isfinite(est).all()
def test_wrong_basis_is_a_distinct_control():
 A=m.bases(); assert not np.array_equal(A,np.roll(A,1,axis=0))
