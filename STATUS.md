# Status

- OpenReview ID: `L5JTAPUdbQ`
- Submission number: 2510
- Live claims / maximum points: 5 / 10
- Paper: https://arxiv.org/abs/2605.30153
- Source pin: `evidence/source/arxiv_source.tar` (see SHA256SUMS)
- Official executable: none found in initial arXiv source audit
- Compute policy: CPU-only
- Current phase: claim_5_verified_scoped
- Claim 1: verified as a scoped pinned-source theorem-rate audit; the epsilon exponent is `k vee 2`, while ambient `d` remains in a linear prefactor. Evidence: `outputs/claim1_attempt1_audit.md`.
- Claim 2: verified as a scoped Theorem-1 score-error audit; the displayed nonparametric exponent uses `k vee 2`, while `d` remains linear. An ambient-substitution negative control is rejected. Evidence: `outputs/claim2_attempt1_audit.md`.
- Claim 3: verified as a scoped pinned-source Assumption-1 audit plus finite CPU union-of-subspaces check; the origin-mass control fails only the required separation condition. Evidence: `outputs/claim3_attempt1_audit.md`.
- Claim 4: verified as a scoped pinned-source regularity-scope audit plus finite CPU singular union-of-subspaces witness; no diffusion training was run. Evidence: `outputs/claim4_attempt1_audit.md`.
- Claim 5: verified as a scoped pinned-source Equation-1 comparator-rate audit plus finite CPU exponent arithmetic; this is not an independent prior-work theorem reproduction or diffusion training. Evidence: `outputs/claim5_attempt1_audit.md`.
- Next action: assemble logbook and run local validation.
- Publication: not started
- Logbook: fixed-order Trackio pages, pinned executive summary, trace attachment, and official validator are complete. Publication remains blocked: posterly asset/measure/strict-polish gates fail (`logbook/GATE_REPORT.json`); a simple poster draft must be repaired/rebuilt with two source figures and passing layout gates before `poster_embed.html` can be considered release-ready.
- Poster remediation: PASS. Two source-pinned 600-DPI paper excerpts are manifested in `logbook/FIGURE_MANIFEST.json`; strict posterly preflight/style/asset/measure/polish gates have zero failures/warnings. `poster_embed.html`, local trace readback, 10 tests, evidence manifests, and the official validator all pass. State is `independent_review_ready`; publication remains blocked pending fresh independent review.
