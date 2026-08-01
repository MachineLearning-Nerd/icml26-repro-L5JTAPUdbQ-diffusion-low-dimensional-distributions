# Claim 2 — Attempt 1: Theorem-1 intrinsic score-error audit

## Claim

The live claim states that Theorem 1 bounds score-estimation `L2` error through the intrinsic subspace dimension `k`, avoiding exponential ambient-dimension `d` dependence.

## Pinned source

The retained excerpt `evidence/claim2_attempt1/theorem1_excerpt.tex` reproduces `Results.tex` lines 135–150 from the pinned arXiv source. Theorem 1 states, conditional on exact subspace recovery and for `t <= N^{O(1)}`:

```text
d M^3 / N * (1/t + sigma^(k vee 2) / t^((k vee 2)/2 + 1)) * polylog(N)
```

Thus `d` remains a linear prefactor, while the nonparametric time/scale exponent is controlled by `k vee 2`, rather than ambient `d`.

## CPU audit and negative control

`src/claim2_score_error_audit.py` evaluates the displayed theorem term at `t=0.5`, `sigma=1.5`, and ambient `d=20` for intrinsic dimensions `k={1,2,3,5}`. It separately substitutes `d=20` for `k=3` as a negative control. That incorrect substitution inflates the finite score factor by more than 1,000x, rejecting the ambient-exponent interpretation.

Commands:

```bash
.venv/bin/python src/claim2_score_error_audit.py
.venv/bin/python -m pytest -q
sha256sum -c evidence/claim2_attempt1/SHA256SUMS
```

Results: 5 tests passed and both source/result hashes verify.

## Verdict

**Verified (scoped).** This is a clean-room source-theorem and finite arithmetic audit of the claimed intrinsic-versus-ambient dependence. It does not constitute a trained diffusion-model reproduction.
