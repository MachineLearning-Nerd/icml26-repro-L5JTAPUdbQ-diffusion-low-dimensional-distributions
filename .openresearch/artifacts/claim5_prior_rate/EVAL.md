# Claim 5 evaluation

- Verdict: **VERIFIED**
- Confidence: **MEDIUM**
- Direct primary source: Cai and Li, arXiv:2503.09583, Theorem 1
- Prior TV exponent: `beta/(d+2 beta)`
- Inverted sample exponent: `(d+2 beta)/beta`
- `d=48, beta=2` sample exponent: `26`
- Independent checker: `PASS`
- Mutated-evidence checker exit: `1` (nonzero required)
- Git SHA: `c59609443ad89cf114c0875e46fc1f4c08653e28`
- Scientific runtime: `0.018315` seconds
- Full cumulative job runtime: `106` seconds
- Allocation: `8.0` vCPU, `32000000000` bytes RAM, no accelerator
- Estimated/actual HF cost: `$0.000883` at `$0.0005/minute`

The pinned Cai-Li source states a beta-Holder assumption and derives the TV
rate through score-error, convergence, early-stopping, and triangle-inequality
steps. Exact exponent arithmetic independently yields the displayed sample
complexity and its increasing ambient-dimension exponent. Zhang et al. provide
an independent matching TV rate under beta-Sobolev, not beta-Holder, smoothness.

The certificate corrects one transparent missing `n^(-1/2)` factor in a
Cai-Li intermediate simplified display by deriving the exponent from its
immediately preceding unsimplified expression. It does not independently
re-prove every analytic lemma in either primary paper, which limits confidence
to MEDIUM.
