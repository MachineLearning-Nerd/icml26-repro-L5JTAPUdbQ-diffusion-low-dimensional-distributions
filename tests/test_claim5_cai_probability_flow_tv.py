import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
import numpy as np
from claim5_cai_probability_flow_tv_toy import schedule, soft_threshold, kde_score, gaussian_density


def test_paper_schedule_is_valid_and_decreasing():
    abar, alpha = schedule(64)
    assert np.all((abar > 0) & (abar < 1))
    assert np.all(np.diff(abar) < 0)
    assert np.all((alpha > 0) & (alpha < 1))


def test_soft_threshold_endpoints():
    eta = 0.1
    vals = soft_threshold(np.array([0.0, eta/2, .075, eta, .2]), eta)
    assert vals[0] == vals[1] == 0
    assert 0 < vals[2] < 1
    assert vals[3] == vals[4] == 1


def test_kde_score_matches_single_gaussian_analytic_score():
    # Many draws from N(0,1): at x=0 the KDE score should be close to 0.
    rng=np.random.default_rng(7); train=rng.normal(size=(4000,1))
    got=kde_score(train,np.zeros((1,1)),t=1.0,thresholded=True)[0,0]
    assert abs(got) < .08


def test_target_density_is_positive_and_symmetric():
    x=np.array([[-1.2],[0.0],[1.2]])
    p=gaussian_density(x)
    assert np.all(p > 0)
    assert abs(p[0]-p[2]) < 1e-12
