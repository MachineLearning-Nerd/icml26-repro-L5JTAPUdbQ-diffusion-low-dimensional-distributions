# Claim 2 proof-certificate evaluation

- Status: **PROOF_CERTIFICATE_PASS**
- Scope: Theorem 1 conditional on exact subspace recovery
- Exact normal/tangent cases: `12`
- Source/proof markers: `13` of `13`
- Independent checker: `PASS`
- Ambient-substitution checker exit: `1` (nonzero required)
- Git SHA: `355d19192868f7540a7169b17728349b0478e5af`
- Runtime in the cumulative accepted run: `0.012764` seconds
- Allocation: `8.0` vCPU, `32000000000` bytes RAM, no accelerator

Exact rational arithmetic verifies that the known normal score cancels from
the component estimation error for every tested ambient/intrinsic pair. The
pinned proof trace places the nonparametric factor in `k_i`, retains only an
explicit linear `d` prefactor, and states a theorem constant independent of
`d`. This is proof-level structural evidence, not a finite scaling fit.

The route does not independently re-prove every concentration and tail lemma.
The separate faithful numerical route supplies executable corroboration.
