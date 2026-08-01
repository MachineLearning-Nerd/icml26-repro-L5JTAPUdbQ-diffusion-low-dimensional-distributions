# Claim 5: prior ambient-dimensional comparator


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_bcf490afbe86", "created_at": "2026-08-01T06:47:50+00:00", "title": "Outcome: scoreable 1-point toy; not theorem verification/falsification"}
-->
## Outcome: scoreable 1-point toy; not theorem verification/falsification

**Exact live claim:** Prior work requiring beta-Holder smooth densities achieves only `epsilon^(-(d+2 beta)/beta)` sample complexity, exhibiting a curse of dimensionality that this paper's bound avoids.

### Independent primary-source route

The pinned primary sources, rather than this paper's Equation (1), agree with the stated exponent and metric qualification:

- Zhang et al. (arXiv:2402.15602, `evidence/claim5_attempt1/prior_sources/zhang_theorem_excerpt.tex`) gives an expected **TV** rate `polylog(n) n^(-beta/(2 beta+d))` for its DDPM construction under its smoothness/class assumptions.
- Cai & Li (arXiv:2503.09583, `evidence/claim5_attempt1/prior_sources/cai_theorem_excerpt.tex`) gives expected **TV** rate `C n^(-beta/(d+2 beta)) polylog(n)` for its probability-flow ODE, with Assumptions 1--2 and `beta <= 2`.

Independently solving `n^(-beta/(d+2 beta)) = epsilon` gives `n = epsilon^(-(d+2 beta)/beta)` (checked exactly in `tests/test_claim5_prior_comparator.py`). Thus no defensible literal mismatch was found: the cited rates support the epsilon exponent only up to logarithms, constants, their stated TV metric, and their respective assumptions.

### Executed reduced comparator

A clean-room, full-dimensional Gaussian-mixture KDE-score diagnostic was executed locally for `d={2,4,6}`, `n={500,1000,2000}`, three seeds, and held-out analytic-score MSE. It is retained as **non-scoreable toy provenance**: it is not either cited paper's end-to-end DDPM/DDIM sampler and cannot verify their universal TV theorems. The implementation has a finite-difference score check and raw per-seed CSV/JSON artifacts. Evidence and hashes: `src/claim5_prior_work_comparator.py`, `outputs/claim5_attempt1/toy_summary.json`, `outputs/claim5_attempt1/SHA256SUMS`.

No full claim verification or falsification is asserted.

### Direct Cai--Li probability-flow toy: scoreable premise-compliant 1-D result

The earlier `K=64` broad grid is retained only as **non-scoreable provenance**: it violated the cited iteration premise and used truncated metrics. The new clean-room toy is a narrow `d=1`, `n=250`, three-seed execution of Cai & Li's actual probability-flow procedure: Gaussian KDE `p_hat`, the paper's `eta_t` soft threshold, forward-score transform, and Algorithm-1/DDIM reverse update. It uses `beta=2`, `tau=n^(-2/5)`, `c0=2`, `c1=12`, and the smallest integer `K=5,990` satisfying the pinned theorem premise `K >= n^(beta/(d+2beta)) (log K)^3`.

Its metric is **not called exact TV**. It is a normalized full-real-line Gaussian-KDE TV-proxy interval computed by overlap with the analytic target on a fixed `[-12,12]` target-tail-certified interval; the omitted target overlap is bounded and resolution sensitivity is retained. Thresholded, unthresholded, and reversed-training-order runs use the identical saved initial `Y_K`; the permutation implementation check is exact. A genuine normalized KDE(target-A)-versus-KDE(target-B) calibration (with a certified KDE-tail bound) and a translated-sample tail-accounting control are retained. The finite result has a near-one TV-proxy interval because the method output escaped the target scale; that finite observation is neither a verification nor a falsification of the asymptotic theorem.

Independent review found this corrected finite direct-method result eligible as a **1-point toy**, while retaining the strict limitation that it is not theorem verification/falsification. See `src/claim5_cai_premise_1d_toy.py`, `outputs/claim5_cai_premise_1d_toy/PROTOCOL.json`, `results.csv`, raw `*.npz`, and `SHA256SUMS`.
