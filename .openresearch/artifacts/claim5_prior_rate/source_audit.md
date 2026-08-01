# Claim 5 source audit

## Reproduced paper

- Primary HTML: https://ar5iv.labs.arxiv.org/html/2605.30153
- Retrieved: `2026-08-01T14:48:25Z` with explicit `Mozilla/5.0` user agent
- HTML SHA-256: `d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`
- Section 1 Equation 1 source: `introduction.tex`, label
  `eq:sample complexity general`
- Pinned source archive SHA-256:
  `07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`

Equation 1 attributes the sample exponent `(d+2 beta)/beta`, up to logarithmic
factors, to prior DDPM and DDIM analyses for general smooth-density classes.

## Direct beta-Holder primary source

- Cai and Li, *Minimax Optimality of the Probability Flow ODE for Diffusion
  Models*: https://arxiv.org/abs/2503.09583
- Pinned source archive SHA-256:
  `fc462d3046091f2d050bfa2fac0d2e1905a7e144dff4379f4b921afb0f64d211`
- Assumption: `problem.tex`, `assume:smooth`
- Theorem: `results.tex`, `thm:TV`
- Proof: `analysis.tex`, `sub:proof_of_theorem_ref_thm_tv`

The theorem assumes a subgaussian target with a beta-Holder density for
`0<beta<=2` and bounds expected TV by
`C n^(-beta/(d+2 beta)) (log n)^((d+1)/2) log K`, subject to its displayed
iteration premise.

## Independent matching-rate primary source

- Zhang et al., *Minimax Optimality of Score-based Diffusion Models: Beyond the
  Density Lower Bound Assumptions*: https://arxiv.org/abs/2402.15602
- Pinned source archive SHA-256:
  `76ad896b273e22ead0ee136bd80422a3498a5950b237a5e867ed7a304c891650`
- Assumption and theorem: `ICML_camera.tex`, Assumption 3.4 and Theorem 3.8

Zhang et al. independently obtain the matching TV exponent
`beta/(2 beta+d)`, but their smoothness assumption is beta-Sobolev rather than
beta-Holder. Cai and Li are therefore the direct support for the Holder wording;
Zhang et al. are only a matching-rate cross-check.
