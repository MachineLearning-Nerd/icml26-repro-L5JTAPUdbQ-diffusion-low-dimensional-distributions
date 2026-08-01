# Claim 4 atomic-target method

The target uses the paper's numerical scale `d=48,M=128,k=3`. Each component
is uniform on the six atoms `+/- A_i e_j`, which span its subspace. Random
orthonormal bases are fixed by seed; pairwise principal-angle checks certify
zero intersections. The target is bounded and its exact worst-direction
exponential-square moment is 2 for `sigma^2=1/log(4)`.

The target has no ambient or intrinsic Lebesgue density, so it cannot satisfy a
Holder-density, density-bound, or density-lower-bound premise. Its nonconvex
finite support is not log-concave.

The generator runs the paper's Gaussian KDE, density threshold, tangent-only
clipping, exact normal score, plug-in mixture weights, and regularization set.
Repeated atoms are aggregated by exact counts, which is algebraically
identical to summing all `N` samples. The true Gaussian-smoothed score is the
closed-form posterior average over all 768 atoms. Results use four geometric
sample sizes, 20 independent training datasets, and 10,000 independent `p_t`
queries per seed, with two-sided 95% t intervals.

Omitting the exact normal score is the scientific negative control. A separate
mutation changes the required zero-intersection-mass check; the independent
verifier must exit nonzero.
