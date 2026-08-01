# Claim 2: intrinsic score-error rate


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_bd00f42e3885", "created_at": "2026-08-01T06:47:49+00:00", "title": "Outcome: verified (scoped clean-room theorem audit)"}
-->
## Outcome: inconclusive — full-scale clean-room numerical evidence started

The prior source audit is not treated as a scoreable reproduction. A clean-room implementation of Equations (8)–(14), using the paper's literal `d=48`, `M=128`, `k=3`, `N=50,000`, 10,000 held-out `p_t` samples and independently derived analytic Gaussian-mixture-smoothed score, completed 21 independent training datasets at `t=0.25`. Mean score MSE is **3.69597** (normal 95% CI **[3.67692, 3.71501]**). It streams kernels through `||x||²+||y||²−2x·y` and never materializes a query×training×48 tensor. This is genuine full-scale evidence for one time cell, but remains **inconclusive**: the pre-registered t-grid and required wrong-subspace/reduced-N/ambient controls have not yet run, so it cannot support or refute Theorem 1. Evidence: `src/claim2_fullscale_cleanroom.py`, `outputs/claim2_fullscale/results.csv`, `summary.json`, `run_20seeds.log`, and `SHA256SUMS`.
