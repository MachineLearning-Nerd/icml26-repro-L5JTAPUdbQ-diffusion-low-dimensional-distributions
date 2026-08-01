# Claim 1 — Attempt 1: Theorem-2 rate audit

## Claim

The live claim states that Theorem 2 gives a near-logarithmic-factor sample requirement of `epsilon^-(k vee 2)` for `epsilon`-accurate 1-Wasserstein sampling, governed by intrinsic dimension `k` rather than ambient dimension `d`.

## Pinned-source evidence

The retained excerpt `evidence/claim1_attempt1/theorem_rate_excerpts.tex` is extracted from the pinned arXiv source archive:

- `Results.tex`, lines 161–179: `E[W_1] <= C d M^(3/2) n^(-1/(k vee 2)) polylog(n)` and the corresponding epsilon sample exponent;
- `Proof_Overview.tex`, lines 116–118: the same `n^(-1/(k vee 2))` rate.

Thus the claim is correct about the epsilon exponent, with the important qualification that `d` remains as a linear prefactor.

## CPU clean-room calculation

`src/claim1_rate_audit.py` evaluates the published epsilon-dependent factor at `epsilon=0.1`, holding ambient dimension at `d=20` and varying intrinsic dimension `k in {1,2,3,5}`. The observed published exponents are `[2,2,3,5]`.

The negative control deliberately substitutes ambient `d=20` for `k=3`. It changes the exponent from `3` to `20` and inflates the epsilon factor by approximately `1e17`; it therefore rejects the incorrect ambient-exponent interpretation.

Commands:

```bash
.venv/bin/python src/claim1_rate_audit.py
.venv/bin/python -m pytest -q
sha256sum -c evidence/claim1_attempt1/SHA256SUMS
```

Results: 3 tests passed; both retained source excerpt and JSON result hashes verify.

## Verdict

**Verified (scoped).** This verifies the source theorem's stated epsilon exponent and intrinsic-vs-ambient exponent distinction. It is a clean-room symbolic/finite CPU audit, not an end-to-end diffusion-model training or sampling reproduction.
