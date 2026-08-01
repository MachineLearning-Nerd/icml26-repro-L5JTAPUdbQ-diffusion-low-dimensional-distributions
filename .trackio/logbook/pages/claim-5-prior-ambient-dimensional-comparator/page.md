# Claim 5: prior ambient-dimensional comparator


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_bcf490afbe86", "created_at": "2026-08-01T06:47:50+00:00", "title": "Outcome: toy (independent prior-theorem rate check plus reduced empirical comparator)"}
-->
## Outcome: toy (independent prior-theorem rate check plus reduced empirical comparator)

**Exact live claim:** Prior work requiring beta-Holder smooth densities achieves only `epsilon^(-(d+2 beta)/beta)` sample complexity, exhibiting a curse of dimensionality that this paper's bound avoids.

### Independent primary-source route

The pinned primary sources, rather than this paper's Equation (1), agree with the stated exponent and metric qualification:

- Zhang et al. (arXiv:2402.15602, `evidence/claim5_attempt1/prior_sources/zhang_theorem_excerpt.tex`) gives an expected **TV** rate `polylog(n) n^(-beta/(2 beta+d))` for its DDPM construction under its smoothness/class assumptions.
- Cai & Li (arXiv:2503.09583, `evidence/claim5_attempt1/prior_sources/cai_theorem_excerpt.tex`) gives expected **TV** rate `C n^(-beta/(d+2 beta)) polylog(n)` for its probability-flow ODE, with Assumptions 1--2 and `beta <= 2`.

Independently solving `n^(-beta/(d+2 beta)) = epsilon` gives `n = epsilon^(-(d+2 beta)/beta)` (checked exactly in `tests/test_claim5_prior_comparator.py`). Thus no defensible literal mismatch was found: the cited rates support the epsilon exponent only up to logarithms, constants, their stated TV metric, and their respective assumptions.

### Executed reduced comparator

A clean-room, full-dimensional Gaussian-mixture KDE-score diagnostic was executed locally for `d={2,4,6}`, `n={500,1000,2000}`, three seeds, and held-out analytic-score MSE. It is **toy** evidence: it is not either cited paper's end-to-end DDPM/DDIM sampler and cannot verify their universal TV theorems. The implementation has a finite-difference score check and raw per-seed CSV/JSON artifacts. Evidence and hashes: `src/claim5_prior_work_comparator.py`, `outputs/claim5_attempt1/toy_summary.json`, `outputs/claim5_attempt1/SHA256SUMS`.

No full claim verification or falsification is asserted.
