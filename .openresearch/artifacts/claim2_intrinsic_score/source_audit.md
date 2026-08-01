# Claim 2 source audit

- HTML: https://ar5iv.labs.arxiv.org/html/2605.30153
- Retrieved: `2026-08-01T14:48:25Z` with explicit `Mozilla/5.0` user agent
- HTML SHA-256: `d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`
- Theorem anchor: `#Thmtheorem1`
- Assumption anchors: `#Thmassumption1`, `#Thmassumption2`
- Pinned source archive SHA-256: `07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`
- Statement source: `Results.tex`, label `thm:score estimation error`
- Proof source: `pf-of-theorems.tex`, label `pf-of-thm:thm:score estimation error`
- Component lemma source: `pf-of-lemmas.tex`

The statement is explicitly conditional on exact subspace recovery. It covers
targets satisfying Assumptions 1 and 2 and `t<=N^{O(1)}`. The expectation is
over `N` training samples and `X~p_t`. The displayed constant is independent of
`N,d,M,t`, but may depend on intrinsic `k` and fixed assumption constants.
