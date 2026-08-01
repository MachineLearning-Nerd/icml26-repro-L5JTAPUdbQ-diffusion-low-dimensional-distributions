# Status

- OpenReview ID: `L5JTAPUdbQ`
- Submission number: 2510
- Live claims / maximum points: 5 / 10
- Paper: https://arxiv.org/abs/2605.30153
- Source pin: `evidence/source/arxiv_source.tar` (see SHA256SUMS)
- Official executable: none found in initial arXiv source audit
- Compute policy: local CPU/local GTX 1050 only; no HF cpu-upgrade/Jobs/paid compute
- Current phase: claim_2_fullscale_cleanroom_inconclusive
- Claim 1: verified as a scoped pinned-source theorem-rate audit; the epsilon exponent is `k vee 2`, while ambient `d` remains in a linear prefactor. Evidence: `outputs/claim1_attempt1_audit.md`.
- Claim 2: inconclusive pending t-grid/controls. Clean-room Eq. (8)–(14) implementation completed 21 full paper-scale datasets at d=48, M=128, k=3, N=50,000 and 10,000 held-out samples at t=0.25: MSE 3.69597 (95% CI [3.67692, 3.71501]). Evidence: `outputs/claim2_fullscale/summary.json`.
- Claim 3: scoped pinned-source Assumption-1 audit plus finite CPU union-of-subspaces check; it includes support, zero-intersection mass, non-trivial per-subspace mass, and subgaussian-tail conditions. The origin-mass control fails separation. Evidence: `outputs/claim3_attempt1_audit.md`.
- Claim 4: verified as a scoped pinned-source regularity-scope audit plus finite CPU singular union-of-subspaces witness; no diffusion training was run. Evidence: `outputs/claim4_attempt1_audit.md`.
- Claim 5: verified as a scoped pinned-source Equation-1 comparator-rate audit plus finite CPU exponent arithmetic; this is not an independent prior-work theorem reproduction or diffusion training. Evidence: `outputs/claim5_attempt1_audit.md`.
- Next action: monitor official judge/leaderboard status; do not rerun terminal scoped claim audits.
- Publication: published through Trackio at `2026-08-01T07:36:33Z`. Space: https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions. Rendered logbook: https://dineshai-repro-l5jtapudbq-diffusion-low-dimensio-bc85f6d.static.hf.space/. Space revision: `1785569789803468494`; Space git SHA: `fe1fd273934cf8568fbcc1187d857e7662313648`.
- Logbook: fixed-order Trackio pages, pinned executive summary and official validator are complete; no public trace is declared. Posterly full non-waived gate suite passes at `Chenruishuo/posterly@94d374d72afdc372af226eb745e82af00f07e43f`: all style rules including 4/5 are enabled, real-figure provenance passes, total paper-image area is 12%+ without a waiver, measure passes, and strict polish has zero warnings. Reproduce it with `scripts/run_full_poster_gates.sh`; see `logbook/GATE_REPORT.json` and `outputs/posterly_full_gates.log`. Delivered-poster and trace-consistency remediation plus final independent scientific/compliance reviews are complete. Anonymous public readback at `2026-08-01T07:37:52Z` confirmed public access, `paper-L5JTAPUdbQ`, fixed page order and all claim pages, the embedded delivered poster, GitHub/arXiv links, and no trace declaration; see `outputs/public_readback_final_20260801T0737Z.log`. Official judge/leaderboard status is not yet confirmed. `contract/live_claims.json` remains immutable official metadata; scoped reproduction verdicts live in `reproduction_verdicts.json`.
