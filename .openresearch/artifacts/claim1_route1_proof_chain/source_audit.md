# Claim 1 route 1 source audit

Primary paper HTML: `https://ar5iv.labs.arxiv.org/html/2605.30153`, retrieved
2026-08-01 with `Mozilla/5.0`, SHA-256
`d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.
Theorem 2 is `#Thmtheorem2`; its proof is Appendix A.2. The theorem quantifies
over targets satisfying Assumptions 1 and 2 and sufficiently large `n`, fixes
`n0=C_sc M^2 k log n`, `T=log n`, and `tau=n^(-2/k)`, averages W1 over the
training sample, and states a constant independent of `n,d,M`.

Pinned paper source tar SHA-256:
`07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`.
Audited files: `Results.tex` and `pf-of-theorems.tex`.

External bridge: Azangulov et al., arXiv:2409.18804, equation label
`thm:from_score_matching_to_wasserstein`. HTML SHA-256
`ef2e562ba4a531c5579e8727c1a64f3b8e4cb8ef78de9520920ec01df5545054`;
source-response SHA-256
`ee0f36028e13fe450eda9e6dd5bcc5dbc8b4fedf3af699222bc3fa00ba85be2a`.
It gives the square-root interval score-loss bridge used by the paper and cites
Oko et al. Eq. (90)/Lemma D.7 for its proof.

The paper proof invokes its Appendix B.1 exact-subspace-recovery lemma before
removing the conditioning event. The accepted Claim 3 certificate falsifies
that lemma under the stated assumptions.
