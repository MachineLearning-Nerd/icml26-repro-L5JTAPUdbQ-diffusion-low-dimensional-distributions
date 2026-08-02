# Claim 3: union-of-subspaces assumption


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_cf89b262e2bb", "created_at": "2026-08-01T06:47:49+00:00", "title": "Outcome: inconclusive after independent d=48 proof-dependency tests"}
-->
## Outcome: inconclusive after independent d=48 proof-dependency tests

The original source audit is superseded for scoring by an independent local-CPU dependency experiment (`src/claim3_non_toy_dependency_audit.py`). It derives the component-count event independently: for `N_i~Bin(N,p_i)` and `p_i >= 1/(c_p M)`, Chernoff plus a union bound gives `P[min_i N_i < N/(2c_pM)] <= M exp(-N/(8c_pM))`. In 100,000 allocation draws per cell, the event did not fail for `(M,N)=(8,800),(32,6400),(128,51200)`; a vanishing-mass control failed in 100% of draws (mean minimum count 4.99 versus threshold 195.31).

For a clean-room `d=48,M=128,k=3` Gaussian union-of-subspaces mixture, the independently assembled analytic mixture score and normal/tangent decomposition agree on 4,096 held-out smoothed points to maximum norm error `1.13e-14`. The audit maps count, separation, tail, and decomposition uses to the pinned proof files. Positive intersection mass produces 10,112 ambiguous labels in 100,000 samples; a Student-t(3) tail control has an empirical exponential-square diagnostic `6.27e220` versus `1.22` for a Gaussian reference.

This is substantive evidence about necessary proof dependencies, but it does **not** independently prove the complete theorem or diffusion-learning guarantee. Verdict remains **inconclusive**, not verified.

A remediated literal-assumption route runs a finite non-toy clean-room `d=12,M=3,k=2` union of three orthogonal 2-planes. It checks support, zero intersection mass, component mass, and a bounded-support subgaussian certificate before executing the **literal regularized** source estimator: hard density threshold `psi`, `clip_R`, ambient KDE `q/p` weights, and `G_t(i)` distance gates. The nominal regularized score MSE is `0.04248` versus an explicitly non-source unregularized control `0.001314`; raw train/evaluation arrays and pointwise squared errors are retained. Executed intersection-atom and low-mass controls violate their relevant assumptions and are limitations/diagnostics only, never a falsification of literal C3. The finite audit cannot establish a theorem rate or expectation, so the verdict remains **inconclusive**. Evidence: `outputs/claim3_literal_uos_estimator/`, including `raw_arrays.npz` and SHA-256 manifest. Evidence: `outputs/claim3_fullscale/result.json`, `outputs/claim3_fullscale/allocation_raw_min_counts.npz`, `outputs/claim3_fullscale/run.log`, and SHA-256 manifest.
