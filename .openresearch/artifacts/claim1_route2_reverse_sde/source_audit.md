# Claim 1 route 2 source audit

The source and exact Theorem 2 contract are pinned by route 1. This route uses
Algorithm 1 exactly in the `d=M=k=1` special case:

- forward OU: `dX_t=-X_t dt+sqrt(2)dB_t`;
- reverse drift: `Y+2 s_hat_X`;
- initialization: standard normal;
- `T=log n`, `tau=n^-2`;
- VE-to-OU score transform `s_X(x)=s_Z(x/c_t)/c_t`;
- the paper's Gaussian KDE, density threshold, and tangent clip.

The target is uniform on `{-1,+1}`. It is bounded, supported on the single
one-dimensional linear subspace, has component mass one, and has no pairwise
intersection condition when `M=1`. With `sigma^2=1/log 2`, the exponential
square moment is exactly two.
