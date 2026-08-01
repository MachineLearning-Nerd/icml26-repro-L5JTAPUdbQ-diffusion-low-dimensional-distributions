# Claim 2 proof-certificate method

The generator extracts the theorem, proof, and component lemma from the pinned
source archive. It checks 13 exact markers spanning the statement, the true and
estimated score decompositions, the component lemma, mixture aggregation, and
the final bound.

Independently, exact rational arithmetic instantiates coordinate subspaces for
12 `(d,k)` pairs up to the paper's `d=48,k=3` example. For arbitrary distinct
tangent scores it constructs both lifted ambient scores and proves their
squared difference equals the tangent-space squared difference. The shared
normal score cancels exactly. A separate checker reconstructs every case and
the dependency trace without importing the generator.

The mutation control replaces a `k vee 2` exponent by ambient `d`; the checker
must exit nonzero.
