# Claim 4 evaluation

- Verdict: **VERIFIED**
- Confidence: **MEDIUM**
- Scale: `d=48, M=128, k=3, N_max=50000, E=10000, 20 seeds`
- Target: bounded atomic UoS distribution with no ambient or intrinsic density
- Log-log N slope: `-0.648950`
- MSE at `N=6250`: `0.175599` (95% CI `0.166304, 0.184893`)
- MSE at `N=50000`: `0.045451` (95% CI `0.039838, 0.051064`)
- Omitted-normal control ratio at `N=50000`: `3470.951`
- Independent checker: `PASS`
- Assumption-mutation checker exit: `1` (nonzero required)
- Git SHA: `f23684773489717e1550b61f375ccfd4f8d10193`
- Scientific runtime: `227.529138` seconds
- Complete cumulative job runtime: `287` seconds
- Allocation: `8.0` vCPU, `32000000000` bytes RAM, no accelerator
- Estimated/actual HF cost: `$0.002392` at `$0.0005/minute`

The exact target satisfies both stated assumptions while having no density,
nonconvex support, and no Holder, log-concavity, uniform-density, or positive
density-lower-bound property. The faithful score estimator improves across the
precommitted N sweep; omitting the known normal score fails strongly.

This is direct full-scale corroboration plus a source dependency certificate.
It does not repair the separate exact-recovery failure, and the paper leaves
the regularization constant unspecified; confidence is therefore MEDIUM.
