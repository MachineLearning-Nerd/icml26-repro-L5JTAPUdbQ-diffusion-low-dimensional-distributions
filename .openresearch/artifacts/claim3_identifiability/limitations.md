# Limitations and deviations

- This is a proof-level counterexample, not a finite empirical approximation.
- It uses `M=2` with a non-vacuous, exactly checked zero-mass intersection.
- It falsifies Appendix B.1's exact-recovery lemma and the claim that the listed
  assumptions suffice for that step of the analysis.
- It does not falsify Theorem 1 conditional on an oracle exact-recovery event.
- It does not independently lower-bound the Wasserstein error of an oracle
  sampler that is given a minimal support subspace.
- No author code exists in the paper source; the checker is a clean-room
  implementation of the exact finite witness.
