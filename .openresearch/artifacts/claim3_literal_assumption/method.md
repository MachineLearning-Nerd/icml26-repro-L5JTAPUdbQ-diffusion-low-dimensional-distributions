# Method

The generator extracts `problem_formulation.tex` and `Results.tex` from the
pinned arXiv source archive. It checks exact markers for the support union,
linear and low-dimensional subspaces, zero intersection mass, component mass,
the within-subspace exponential-square moment, and invocation of both
assumptions by Theorems 1 and 2.

An independent finite witness uses two coordinate lines in `R^4` and equal
mass on `±e1, ±e2`. Exact arithmetic checks support, intersection mass,
component mass, and the boundary value of the subgaussian moment. A separate
verifier repeats the source extraction and witness checks without importing
the generator.
