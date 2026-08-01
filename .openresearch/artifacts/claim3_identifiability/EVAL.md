# Claim 3 evaluation

- Verdict: **FALSIFIED**
- Confidence: **HIGH**
- Scope: Appendix B.1 exact-subspace-recovery lemma used by Theorem 2
- Counterexample observation TV: `0.0`
- Best simultaneous exact-recovery success probability: `0.5`
- Assumption 2 worst-direction exponential-square moment: `2.0` (limit `2`)
- Independent checker: `PASS`
- Mutated-evidence checker exit: `1` (nonzero required)
- Git SHA: `1d40b18820f2da1c593101f7156e9e01dc3d1ef8`
- Scientific-check runtime: `0.002452` seconds
- Whole HF job runtime: `42` seconds
- Allocation: `8.0` vCPU, `32000000000` bytes RAM, no accelerator
- HF job: `DineshAI/6a6e0e7d6b79c09949c1e636`

The same bounded distribution satisfies the paper's stated assumptions under
two distinct declared two-dimensional subspaces. Its entire sample law is
identical in both parameterizations. No data-only algorithm can recover both
subspaces with probability above one half, contradicting the lemma's uniform
failure probability of order `n^-10` for sufficiently large `n`.

This falsifies the claimed sufficiency of Assumption 1 for the recovery step. It
does not by itself falsify conditional Theorem 1 or prove a numerical lower
bound for an oracle supplied with the true subspace.
