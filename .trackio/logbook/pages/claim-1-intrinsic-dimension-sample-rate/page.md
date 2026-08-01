# Claim 1: intrinsic-dimension sample rate

## Outcome: inconclusive after end-to-end full-scale local sampling

**Live claim.** Theorem 2 states an approximately `epsilon^-(k vee 2)` sample requirement for 1-Wasserstein accuracy, using intrinsic subspace dimension rather than an ambient-dimensional exponent.

**Pre-registered empirical protocol.** This clean-room implementation executes Algorithm 1's reverse OU SDE with Euler--Maruyama, the repository's streaming Eq. (8)--(14) KDE score estimator, exact source labels/bases (the theorem's exact-recovery event), `T=log(N)`, and `tau=N^(-2/k)`. It uses the literal source geometry `d=48, M=128, k=3`, sample budgets `N={6,250,12,500,25,000,50,000}`, and a 64-projection sliced-W1 estimator with a held-out target-versus-target split as its Monte-Carlo floor. This is real end-to-end diffusion sampling, not a formula audit.

**Commands and evidence.** `src/claim1_reverse_diffusion.py` generated 128 reverse samples per cell, raw NPZ samples, exact configurations, logs, checksums, and results in `outputs/claim1_reverse_full/`. At `N=50,000`, three independently generated training/sampling seeds with 16 Euler steps yielded sliced W1 values 1792.61, 1843.83, and 1817.92; their target-split W1 floors were 0.071, 0.084, and 0.075. A step sweep (4, 16, 64) yielded 78.41, 1792.61, and 10312.53 respectively. The wrong-basis control at the same 16-step cell yielded 1790.78, so this practical implementation does not show the expected separation. See `outputs/claim1_reverse_full/summary.json` and `SHA256SUMS`.

**Verdict and limitation.** **Inconclusive.** The finite Euler sampler is extremely poor/unstable under this direct implementation, so it does not verify the claimed empirical rate. It also does **not** falsify Theorem 2: the paper analyzes an idealized continuous-time reverse process and explicitly leaves numerical-discretization error unresolved. The prior pinned-source exponent audit is retained only as provenance, not as a score-bearing result. Implementation: https://github.com/MachineLearning-Nerd/icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions.
