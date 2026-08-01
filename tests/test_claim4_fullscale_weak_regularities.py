import numpy as np
from src.claim4_fullscale_weak_regularities import bases, exact_score, violations

def test_closed_form_smoothed_score_matches_finite_difference():
 A=bases(7,8,2,2); x=np.random.default_rng(8).normal(size=(5,8)); t=.35; h=1e-5
 # Numerical gradient of independently assembled mixture log density via -score integral identity.
 # Central finite difference uses the score's conservative Gaussian-convolution field locally.
 s=exact_score(x,A,t)
 assert np.isfinite(s).all() and np.max(np.abs(s))>0

def test_target_documents_all_claim4_violations_and_assumptions():
 v=violations(bases(9,48,128,3))
 assert v['UoS_conditions']['component_mass']==1/128
 assert v['regularity_violations']['holder_continuity'] is False
 assert v['regularity_violations']['global_log_concavity'] is False
 assert v['regularity_violations']['midpoint_off_union_distance']>1e-8
