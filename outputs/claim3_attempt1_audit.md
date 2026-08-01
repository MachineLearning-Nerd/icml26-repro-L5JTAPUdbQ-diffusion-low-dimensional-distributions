# Claim 3 — Attempt 1: source-assumption and finite CPU audit

**Live claim.** The target support is a union of low-dimensional linear subspaces, has zero probability mass on intersections, and is subgaussian within each subspace.

## Pinned-source audit

The retained excerpt from `problem_formulation.tex` records the source support condition, zero-intersection condition, non-trivial component mass, and per-subspace subgaussian MGF condition. See `evidence/claim3_attempt1/problem_formulation_excerpt.tex` and its SHA-256 manifest.

## Clean-room CPU check

`src/claim3_assumption_audit.py` constructs two coordinate-axis subspaces in ambient dimension 2. Each component is a Rademacher law on its own axis. With `sigma=2`, the finite MGF check is `exp(1/4) < 2`; the intersection mass is zero.

## Negative control

The control retains the axes and subgaussian coordinates but assigns mass to the origin, the intersection of the two subspaces. Its MGF condition still passes while the zero-intersection condition fails. This demonstrates that the separation assumption is independently checked; it is **not** a counterexample to the paper's theorem.

## Verdict

**Verified (scoped):** the exact pinned-source assumptions and their finite CPU geometry/tail conditions are correctly represented. This is not diffusion-model training or an empirical verification of the paper's end-to-end performance.
