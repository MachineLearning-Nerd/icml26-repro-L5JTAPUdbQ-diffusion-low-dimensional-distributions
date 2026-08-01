import importlib.util
from pathlib import Path
import numpy as np
p=Path(__file__).parents[1]/'src'/'claim5_prior_work_comparator.py'
s=importlib.util.spec_from_file_location('c5',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
def test_exact_mixture_score_matches_finite_difference_direction():
 x=np.array([[.2,-.3],[1.1,.4]])
 eps=1e-6; direction=np.array([.4,-.7])
 def logp(z):
  means=np.stack([-np.ones(2),np.ones(2)])
  return np.log(np.exp(-.5*((z[None,:]-means)**2).sum(1)).mean())
 fd=np.array([(logp(z+eps*direction)-logp(z-eps*direction))/(2*eps) for z in x])
 assert np.max(np.abs(fd-(m.posterior_score(x)*direction).sum(1))) < 1e-6
def test_rate_inversion_identity():
 for d in (2,6,48):
  for beta in (1,2):
   rate=beta/(d+2*beta); inv=(d+2*beta)/beta
   eps=1e-3
   assert abs((eps**(-inv))**(-rate)-eps) < 1e-14
