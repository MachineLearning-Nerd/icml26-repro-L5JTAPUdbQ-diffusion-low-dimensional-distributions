# Claim 1 alternate-route derivation

This local CPU diagnostic uses the paper's schedule `T=log(n)`, `tau=n^-2/k` in the special theorem-domain fixture `d=k=M=1`, target `N(0,1)`. This target has one linear subspace and subgaussian tails; it is not a literal-scale rate reproduction.

At reverse time `r`, set forward time `s=T-r`, `c=exp(-s)`, and `h=exp(2s)-1`. The clean-room estimator evaluates the 1-D Gaussian KDE at `u=y/c`; its OU score is `score_Xs(y)=score_h(u)/c`. Therefore the reverse drift used by both integrators is

`b_r(y) = y + 2 score_Xs(y)`.

The hard estimator is `score_h(u)=raw_KDE_score(u)` when `KDE_h(u) >= eta_h`, and zero otherwise, with `eta_h=log(n)/(n sqrt(2 pi h))`, followed by the source-style norm clip. At a surface `KDE_h(u)=eta_h`, the two one-sided values are generally `raw_KDE_score(u)` and zero. Thus the drift is not globally Lipschitz in general. A standard global-Lipschitz Euler--Maruyama strong-error theorem cannot itself be an error certificate here.

Before execution, `PROTOCOL.json` fixed `W1(Euler_256, Euler_2048) <= .15`, `W1(Heun_256, Euler_2048) <= .15`, and `W1(Euler_256, Heun_256) <= .15`, using exact shared Brownian increments. The recorded results fail all three (1.93, 1.03, 2.75). That is a finite numerical instability observation, not a counterexample to the theorem's expected W1 guarantee: it neither quantifies its expectation over training samples nor establishes an unavoidable error at the theorem's asymptotic regime.
