# Limitations and deviations

- The certificate verifies the exact theorem assumptions, proof-chain rate
  substitutions, sample-complexity inversion, and ambient-dimension dependence.
- It does not independently re-prove every analytic concentration, score-error,
  Jacobian-error, or early-stopping lemma in the two primary papers. Confidence
  is therefore `MEDIUM`, not `HIGH`.
- The direct beta-Holder support is Cai and Li. Zhang et al. use beta-Sobolev
  smoothness and are retained only as an independent matching-rate source.
- The result is in expected total variation and suppresses logarithmic factors;
  it is not an empirical runtime guarantee.
- One Cai-Li intermediate display omits `n^(-1/2)` on a simplified line. The
  correct exponent follows from the preceding expression and is used later;
  the certificate makes that correction explicit rather than hiding it.
