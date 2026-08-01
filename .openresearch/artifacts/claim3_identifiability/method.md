# Method

Use `M=2`, `d=4`, `k=2`, and the bounded distribution assigning probability
one quarter to each of `-e1`, `e1`, `-e2`, and `e2`. In parameterization A,
declare the subspaces as `span(e1,e3)` and `span(e2,e4)`. In parameterization
B, declare them as `span(e1,e4)` and `span(e2,e3)`. Both unions contain the
support; each component has mass one half; and each non-vacuous pairwise
intersection is `{0}`, which has probability zero. Both parameterizations
satisfy Assumption 2 with `sigma^2=1/log(2)` because the worst-direction
exponential-square moment of every normalized component is exactly two.

The observations have total variation zero under the two parameterizations for
every sample size, while the exact recovery targets are distinct. The two
success events are disjoint, so their probabilities sum to at most one. Thus
at least one valid parameterization has exact-recovery probability at most one
half for every sample size. This contradicts the lemma's asymptotically
vanishing universal failure probability.

`src/claim3_identifiability_counterexample.py` generates the raw record.
`verifiers/verify_claim3_identifiability.py` separately recomputes normalization,
support, subgaussian moment, total variation, and the two-point lower bound. The
runner mutates observation TV from zero to 0.25 and requires the checker to exit
nonzero. A second control uses disjoint atom laws with TV one, for which the
indistinguishability argument correctly does not apply.
