# Claim 5 Cai--Li probability-flow TV toy: executed protocol

This clean-room **toy** implements Cai & Li, arXiv:2503.09583, Algorithm 1 / `results.tex`: Eq. `p_hat` Gaussian KDE; Eq. `score-estimate` with the literal `eta_t=log(n)/(n(2*pi*t)^(d/2))` soft threshold; Eq. `score-estimator-X`; and the Algorithm-1/DDIM deterministic reverse update. The source archive is checksum-pinned at `../../evidence/claim5_attempt1/prior_sources/cai2503.09583.tar.gz`.

Smooth two-component unit-covariance Gaussian mixtures (beta=2 toy) were run on local CPU: five fixed seeds, d=1/2/3, n=250/500/1000/2000, K=64, 1,024 generated samples/cell, and `tau=n^(-2/(d+4))`. d=1/2 use deterministic target-vs-generated Gaussian-KDE grid-quadrature TV and a shifted-grid crosscheck. d=3 is separately reported with a held-out histogram-TV proxy. Controls are the unthresholded plug-in score, IID-order permutation invariance, and target-vs-target floor.

Deviations: finite K=64 and tiny dimensions/sample sizes replace the theorem's asymptotic schedule; the metric estimators are finite empirical proxies. Result: the finite toy was numerically unstable (TV near 0.5 and generated samples escape target scale). It does not verify or falsify the cited asymptotic TV-rate theorem; independent review must decide scoreability.

Independent executable crosscheck: `scripts/crosscheck_claim5_cai_toy.py` recomputes fixed-bin histogram TV directly from every raw generated/target NPZ. Its separate result is `independent_histogram_crosscheck.json`; all 60 cells have generated samples outside the target [-5,5] grid.
