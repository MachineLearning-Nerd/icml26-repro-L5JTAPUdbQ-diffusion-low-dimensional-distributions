# Claim 5 score-bearing recovery plan (pre-execution)

## Why the prior attempt is non-scoreable
The retained `outputs/claim5_attempt1/` experiment measures KDE **score MSE**, not the live claim's cited-method **TV** sampling rate. Its `toy` label is provenance only and is now reported as `inconclusive`.

## Source-faithful viable route
Cai & Li, arXiv:2503.09583, is the implementable local route. Its retained source text specifies: Algorithm 1's deterministic probability-flow update (`cai.txt:775-830`); the Gaussian-kernel density/soft-threshold score construction in equations (18)--(20) (`cai.txt:820-865`); and a TV guarantee in Theorem 1 (`cai.txt:892-915`). Unlike the earlier generic KDE diagnostic, this route directly exercises one cited sampler and the claimed metric.

No author implementation was located in the pinned archive, so this will be a clean-room reproduction. Zhang et al.'s Brownian DDPM Algorithm 1 is retained as a secondary cross-check, not mixed into this result.

## Fixed reduced-scale toy protocol
The committed pre-execution config is `configs/claim5_cai_probability_flow_toy.json`:

- smooth two-component Gaussian-mixture targets, `beta=2`, dimensions `d={1,2,3}`;
- train sizes `{250,500,1000,2000}`, five fixed data/seeding replicates per cell;
- implement Cai & Li equations (18)--(20) and Algorithm 1, including the equation (19) threshold—not an oracle score and not the previous standalone KDE score-MSE code;
- evaluate generated-versus-analytic-target **TV** by deterministic quadrature for d=1/2. The d=3 density estimator must be a separately labeled common-random-number Monte-Carlo L1 proxy, never called exact TV;
- controls: unthresholded plug-in score, permuted training set, and target-vs-target TV floor;
- fit a within-dimension log TV/log n slope and report CIs/raw rows. Compare dimension trends but do not identify finite slopes with the universal asymptotic theorem.

## Score boundary and decision
This directly resolves the review's method/metric mismatch and is worth executing. It can at most support an honestly labelled **toy** result (one point), not a verified/falsified theorem outcome. A 2-point Claim 5 result would require a complete independent theorem derivation/proof validation, not this experiment.

The next worker must first reproduce the equation (18)--(20) estimator on an analytic Gaussian target with finite-difference and normalization tests, then run the pre-registered config. If those source-defined equations cannot be recovered unambiguously from the pinned archive, it must checkpoint that literal blocker rather than substitute a generic KDE.
