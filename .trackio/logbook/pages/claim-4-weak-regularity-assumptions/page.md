# Claim 4: weak regularity assumptions

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_903e3b3159be", "created_at": "2026-08-01T06:47:50+00:00", "title": "Outcome: inconclusive after full-scale weak-regularity experiment"}
-->
## Outcome: inconclusive after full-scale weak-regularity experiment

A clean-room, literal-scale local CPU experiment tested the paper-style streaming tangent-KDE score estimator on a `d=48, M=128, k=3, N=50,000` union-of-subspaces target with 10,000 independently smoothed held-out points at `t=0.25`. The target is an equal-mass mixture of intrinsic uniform cubes: it has bounded (therefore subgaussian) within-subspace tails, generic zero-dimensional subspace intersections, and mass `1/M`, while deliberately violating the cited comparator regularities. Its unsmoothed ambient law is singular (no ambient density/lower bound), has a density gap, discontinuous intrinsic cube-boundary density (not Hölder), and is globally non-log-concave; the retained midpoint witness is distance `0.2263` from every support subspace.

The independently derived closed-form score of the Gaussian-smoothed uniform-cube mixture gave score MSE `1.86113` for the actual estimator. This is non-toy finite numerical evidence that the estimator is executable on a target outside those regularity classes, but it cannot establish the universal theorem or the complete proof chain. It is therefore deliberately **inconclusive**, not a self-awarded verification.

- Code: `src/claim4_fullscale_weak_regularities.py`
- Raw score arrays / result / configuration / run log: `outputs/claim4_fullscale/`
- Integrity: `sha256sum -c outputs/claim4_fullscale/SHA256SUMS`
- Tests: `tests/test_claim4_fullscale_weak_regularities.py`
- Resources: local CPU NumPy float32 streaming; 32.83 seconds estimator time; no HF compute.
