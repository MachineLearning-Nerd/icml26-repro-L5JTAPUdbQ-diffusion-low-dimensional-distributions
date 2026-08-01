# Claim 3 — Attempt 1: source-assumption and finite CPU audit

**Live claim.** The target support is a union of low-dimensional linear subspaces, has zero probability mass on intersections, and is subgaussian within each subspace.

## Pinned-source audit

The retained excerpt from `problem_formulation.tex` records support, zero-intersection mass, the non-trivial per-subspace mass lower bound `p*(V_i) >= 1/(c_p M)`, and per-subspace subgaussian MGF conditions. See `evidence/claim3_attempt1/problem_formulation_excerpt.tex` and its SHA-256 manifest.

## Clean-room CPU check

`src/claim3_assumption_audit.py` constructs two coordinate-axis subspaces in ambient dimension 2. Each component is a Rademacher law on its own axis with mixture mass 1/2; for `M=2,c_p=1`, this meets the required lower bound 1/(c_p M)=1/2. With `sigma=2`, the finite MGF check is `exp(1/4) < 2`; the intersection mass is zero.

## Negative control

The control retains the axes and subgaussian coordinates but assigns mass to the origin, the intersection of the two subspaces. Its MGF condition still passes while the zero-intersection condition fails. This demonstrates that the separation assumption is independently checked; it is **not** a counterexample to the paper's theorem.

## Verdict

**Verified (scoped):** the pinned-source support, separation, per-subspace mass, and tail conditions are represented in the finite CPU construction. This is not diffusion-model training or an empirical verification of the paper's end-to-end performance.
