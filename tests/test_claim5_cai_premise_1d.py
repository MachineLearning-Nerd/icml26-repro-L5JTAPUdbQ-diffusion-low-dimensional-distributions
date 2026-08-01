import importlib.util
from pathlib import Path
import numpy as np
p=Path(__file__).parents[1]/'src'/'claim5_cai_premise_1d_toy.py'; s=importlib.util.spec_from_file_location('c',p); c=importlib.util.module_from_spec(s);s.loader.exec_module(c)

def test_k_premise_and_schedule():
 k=c.k_min(250); assert k >= 250**.4*np.log(k)**3; assert k>=5990
 a,b=c.schedule(k); assert np.all((a>0)&(a<1)); assert np.all((b>0)&(b<1))

def test_tail_certified_proxy_normalization_and_escape():
 rng=np.random.default_rng(4); x=c.sample_target(rng,128)
 r=c.tv_proxy_interval(x,2049); assert 0<=r['tv_proxy_lower']<=r['tv_proxy_upper']<=1.000001; assert r['target_tail']<1e-10
 escaped=c.tv_proxy_interval(x+100,2049); assert escaped['tv_proxy_lower']>.99

def test_paired_order_invariance():
 rng=np.random.default_rng(9); train=c.sample_target(rng,25); init=rng.normal(size=8)
 # shorter K here is solely an order-invariance unit test; production uses k_min.
 a=c.flow(train,init,100,True); b=c.flow(train[::-1],init,100,True)
 assert np.allclose(a,b,rtol=1e-11,atol=1e-11)
