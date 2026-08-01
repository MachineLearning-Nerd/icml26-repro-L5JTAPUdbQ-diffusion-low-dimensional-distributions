# Claim 4 — Attempt 1: regularity-scope audit

## Live claim

> The results dispense with smoothness (e.g., Hölder continuity), log-concavity, uniform density bounds, and density lower-bound assumptions required by prior sample-complexity analyses (Section 2.2).

## Method and scope

This is a pinned-source, CPU-only scope audit, not a diffusion-training reproduction. The retained source excerpt contains the abstract's statement that the analysis applies “without imposing smoothness, bounded-density, or log-concavity assumptions,” and the introduction's statement that it imposes no restrictive score or density assumptions. The same introduction identifies a uniformly-positive density lower bound as a condition in prior work.

The finite check constructs a two-axis Rademacher mixture in ambient dimension two. It has support on two one-dimensional linear subspaces, zero mass at their intersection, and bounded (therefore subgaussian) coordinates within either subspace. It is singular with respect to ambient two-dimensional Lebesgue measure, so it has no ambient density for Hölder, uniform-bound, or lower-bound requirements to constrain. This only illustrates compatibility with the stated source assumptions; it does not train or evaluate a diffusion model.

## Control

A mutation that puts mass at the origin fails the required zero-intersection-mass condition. This prevents treating arbitrary singular distributions as valid witnesses.

## Result

`src/claim4_regularities_audit.py` wrote `outputs/claim4_attempt1/result.json`:

- all three exact source-scope phrases were found;
- witness origin/intersection mass was `0` and each component mass was `0.5`;
- its within-subspace exponential moment upper bound was `exp(1/4) < 2`;
- the origin-mass negative control failed the separation condition.

**Verdict: verified (scoped).** The named smoothness, log-concavity, uniform-density, and density-lower-bound restrictions are not part of the pinned source's stated assumptions. This is not evidence for empirical diffusion performance.

## Commands

```bash
.venv/bin/python src/claim4_regularities_audit.py
.venv/bin/python -m pytest -q
```

Result: `9 passed`.
