# Claim 4 threshold-falsification source audit

Primary HTML: `https://ar5iv.labs.arxiv.org/html/2605.30153`, retrieved
2026-08-01 with `Mozilla/5.0`, SHA-256
`d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.
Pinned source tar SHA-256:
`07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`.

Audited source statements:

- Theorem 2, `#Thmtheorem2`, invokes only Assumptions 1 and 2.
- Section 3.2 says the results do not rely on smooth densities or scores,
  log-concavity, or exactly Gaussian components.
- The same paragraph claims a near-optimal rate under only a subgaussian
  assumption, without extra assumptions on the score or density.
- The judge's Claim 4 additionally names uniform density bounds and positive
  density lower bounds; an atomic target has no Lebesgue density, so neither
  type of density bound is available.

The exact counterexample is shared with the Claim 1 Theorem 2 falsification.
