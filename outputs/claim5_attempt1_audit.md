# Claim 5 — Attempt 1: prior-work rate audit

## Scope

This CPU-only clean-room audit checks the pinned paper's Equation (1) transcription and finite exponent arithmetic. It is **not** diffusion-model training and does not independently reproduce the cited prior-work theorems.

## Primary-source evidence

The retained `introduction.tex` excerpt states that for broad `d`-dimensional distributions with `β`-Hölder smooth densities, prior DDPM/DDIM theory requires, up to logarithmic factors,

\[
\varepsilon^{-(d+2\beta)/\beta}
\]

training samples, and calls its ambient-`d` dependence a curse of dimensionality.

## CPU check and control

For `d=4, β=2`, the displayed exponent is `(4+4)/2 = 4`. The denominator-mutation control drops division by `β` and yields `8`; it fails. At `β=1`, the exponent rises from 4 to 12 to 102 as `d` changes from 2 to 10 to 100.

## Outcome

**Verified (scoped):** the live claim's comparator formula and curse-of-dimensionality interpretation match the pinned paper's displayed Equation (1), with independently checked finite arithmetic. This does not establish the external cited theorems or a trained diffusion-model result.

## Reproduction

```bash
.venv/bin/python src/claim5_prior_rate_audit.py
.venv/bin/python -m pytest -q
sha256sum -c evidence/claim5_attempt1/SHA256SUMS
```
