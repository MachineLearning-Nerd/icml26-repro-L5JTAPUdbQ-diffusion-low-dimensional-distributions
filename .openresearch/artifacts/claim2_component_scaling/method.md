# Claim 2 faithful component study

The target is a Gaussian supported on a known `k`-dimensional coordinate
subspace. It satisfies the paper's assumptions with `M=1`. Independent queries
come from its Gaussian-smoothed law `p_t` at the precommitted `t=0.5`.

The implementation follows the paper's component estimator: Gaussian KDE at
bandwidth `t`, density threshold `log(N)/(N(2 pi t)^(k/2))`, clipping of the
low-dimensional score at `sqrt(2 log(N)/t)`, lift through the exact basis, and
the closed-form normal score. Ground truth is derived independently from the
smoothed Gaussian.

The sweep uses `N=128,256,512,1024,2048`, `k=1,2,3`, ambient
`d=4,8,16,48`, 12 paired seeds, and 1,024 held-out queries per seed. Means and
two-sided 95% t intervals are reported. Omitting the known normal score is the
negative scientific control; it should expose error increasing with ambient
dimension.
