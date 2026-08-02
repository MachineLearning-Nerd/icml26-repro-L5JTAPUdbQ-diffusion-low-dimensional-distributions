import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from claim1_threshold_stability_1d import kde_score_hard, integrate

def test_hard_threshold_zeroes_low_density_and_keeps_high_density_finite():
    train=np.array([-.1,0.,.1])
    scores,g,eta=kde_score_hard(np.array([0.,100.]),train,1.)
    assert g[0] >= eta and np.isfinite(scores[0])
    assert g[1] < eta and scores[1] == 0.

def test_coupled_integrators_return_finite_paths():
    train=np.array([-.5,0.,.5]); y=np.array([-.2,.3]); inc=np.zeros((4,2))
    for method in ('euler','heun'):
        out,diag=integrate(train,y,inc,T=1.,tau=.1,method=method)
        assert np.isfinite(out).all()
        assert diag['dt'] > 0
