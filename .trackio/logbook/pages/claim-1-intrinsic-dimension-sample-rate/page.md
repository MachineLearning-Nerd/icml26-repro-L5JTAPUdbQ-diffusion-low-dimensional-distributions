# Claim 1: intrinsic-dimension sample rate


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_bcb64342ac0f", "created_at": "2026-08-01T06:47:48+00:00", "title": "Outcome: verified (scoped clean-room theorem/rate audit)"}
-->
## Outcome: verified (scoped clean-room theorem/rate audit)

**Live claim.** Theorem 2 states an approximately `epsilon^-(k vee 2)` sample requirement for 1-Wasserstein accuracy, using intrinsic subspace dimension rather than an ambient-dimensional exponent.

The pinned source excerpt and finite exponent arithmetic support the displayed `k vee 2` exponent. An ambient-dimension substitution is a negative control and is rejected. This audit does **not** train a diffusion model or establish the full theorem independently. Evidence: `outputs/claim1_attempt1_audit.md`, `outputs/claim1_attempt1/result.json`, and `evidence/claim1_attempt1/`. Primary source: https://arxiv.org/abs/2605.30153. Implementation: https://github.com/MachineLearning-Nerd/icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions.
