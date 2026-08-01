# Status

- OpenReview ID: `L5JTAPUdbQ`
- Submission number: 2510
- Live claims / maximum points: 5 / 10
- Paper: https://arxiv.org/abs/2605.30153
- Source pin: `evidence/source/arxiv_source.tar` (see SHA256SUMS)
- Official executable: none found in initial arXiv source audit
- Compute policy: CPU-only
- Current phase: publication_ready_for_independent_review
- Claim 1: verified as a scoped pinned-source theorem-rate audit; the epsilon exponent is `k vee 2`, while ambient `d` remains in a linear prefactor. Evidence: `outputs/claim1_attempt1_audit.md`.
- Claim 2: verified as a scoped Theorem-1 score-error audit; the displayed nonparametric exponent uses `k vee 2`, while `d` remains linear. An ambient-substitution negative control is rejected. Evidence: `outputs/claim2_attempt1_audit.md`.
- Claim 3: scoped pinned-source Assumption-1 audit plus finite CPU union-of-subspaces check; it includes support, zero-intersection mass, non-trivial per-subspace mass, and subgaussian-tail conditions. The origin-mass control fails separation. Evidence: `outputs/claim3_attempt1_audit.md`.
- Claim 4: verified as a scoped pinned-source regularity-scope audit plus finite CPU singular union-of-subspaces witness; no diffusion training was run. Evidence: `outputs/claim4_attempt1_audit.md`.
- Claim 5: verified as a scoped pinned-source Equation-1 comparator-rate audit plus finite CPU exponent arithmetic; this is not an independent prior-work theorem reproduction or diffusion training. Evidence: `outputs/claim5_attempt1_audit.md`.
- Next action: assemble logbook and run local validation.
- Publication: not started
- Logbook: fixed-order Trackio pages, pinned executive summary and official validator are complete; no public trace is declared. Posterly full non-waived gate suite passes at `Chenruishuo/posterly@94d374d72afdc372af226eb745e82af00f07e43f`: all style rules including 4/5 are enabled, real-figure provenance passes, total paper-image area is 12%+ without a waiver, measure passes, and strict polish has zero warnings. Reproduce it with `scripts/run_full_poster_gates.sh`; see `logbook/GATE_REPORT.json` and `outputs/posterly_full_gates.log`. Delivered-poster and trace-consistency remediation is complete; fresh independent review is the remaining pre-publication gate. `contract/live_claims.json` remains immutable official metadata; scoped reproduction verdicts live in `reproduction_verdicts.json`.
