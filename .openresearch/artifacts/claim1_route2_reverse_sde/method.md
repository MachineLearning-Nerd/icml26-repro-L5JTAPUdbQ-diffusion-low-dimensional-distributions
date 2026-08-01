# Claim 1 route 2 method

Training duplicates are aggregated to their exact `+1` and `-1` counts; this
is algebraically identical to summing all KDE kernels. Reverse time is
integrated by Euler-Maruyama on a geometric forward-time grid, resolving the
small-`tau` stiffness. Antithetic initial states and Brownian increments reduce
Monte Carlo noise without changing the simulated marginal law.

The metric is exact one-dimensional empirical W1: sort the 8,192 generated
values and integrate their quantile distance from the target quantile, which is
`-1` on the lower half and `+1` on the upper half. It is not sliced W1.

Sixteen independent training seeds support confidence intervals. A
192/384/768-step calibration checks discretization, and `0.5/1/1.5` multiples
of `log n` check horizon sensitivity. Replacing the learned score with the
standard-normal score is the scientific negative control.
