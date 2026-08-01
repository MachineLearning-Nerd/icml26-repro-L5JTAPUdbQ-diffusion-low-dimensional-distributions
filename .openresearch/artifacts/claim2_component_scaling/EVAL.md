# Claim 2 component-study evaluation

- Status: **SCOPED_CORROBORATION_PASS**
- Scope: faithful `M=1` component estimator, conditional on exact recovery
- Complete cells: `15`
- Seeds per cell: `12`
- Held-out queries per seed: `1024`
- Log-log MSE slopes for `k=1,2,3`: `-0.864391`, `-0.668297`, `-0.516232`
- Broken-projector `d=48/d=4` ratios: `15.5975`, `22.7805`, `38.9466`
- Independent checker: `PASS`
- Mutated-control checker exit: `1` (nonzero required)
- Git SHA: `355d19192868f7540a7169b17728349b0478e5af`
- Scientific runtime: `8.878270` seconds
- Complete cumulative job runtime: `58` seconds
- Allocation: `8.0` vCPU, `32000000000` bytes RAM, no accelerator
- Estimated/actual HF cost: `$0.000483` at `$0.0005/minute`

The paper's executable low-dimensional KDE estimator shows the precommitted
decreasing `N` scaling with uncertainty for every intrinsic dimension. Its
correct normal score cancels ambient error for every scheduled `d`; the
omitted-normal control exposes strong ambient growth.

This finite route is scoped corroboration, not a proof of Theorem 1. It is
combined with the independent proof-level structural certificate.
