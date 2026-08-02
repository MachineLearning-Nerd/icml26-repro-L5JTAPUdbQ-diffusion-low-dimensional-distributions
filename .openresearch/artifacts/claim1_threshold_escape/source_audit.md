# Claim 1 threshold-escape source audit

Primary HTML: `https://ar5iv.labs.arxiv.org/html/2605.30153`, retrieved
2026-08-01 with `Mozilla/5.0`, SHA-256
`d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.
Pinned source tar SHA-256:
`07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`.

Audited anchors and quantifiers:

- Assumptions 1 and 2: `#Thmassumption1`, `#Thmassumption2`;
- Algorithm 1 reverse drift and standard-normal initialization;
- estimator equations (8)--(14), especially the KDE threshold
  `eta=log N/[N(2 pi h)^(k/2)]` and `psi(g;eta)=1{g>=eta}`;
- VE-to-OU score transform;
- Theorem 2 `#Thmtheorem2`: `T=log n`, `tau=n^(-2/k)`, expectation over
  training data, and `n^(-1/(k vee 2)) polylog n` W1 conclusion.

The counterexample uses the theorem's exact universally quantified domain. It
does not change the algorithm or appeal to the separate recovery flaw.
