# Reproduction: Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions

ICML 2026 reproduction for OpenReview `L5JTAPUdbQ`.

- Paper: https://arxiv.org/abs/2605.30153
- Live contract: 5 claims / 10 points maximum
- Compute policy: CPU-only. GPU-required full experiments will be documented as CPU-infeasible and replaced only by clearly labeled toy evidence.

## Reproduce setup

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -U pip pytest
.venv/bin/python -m pytest -q
```

The source archive and PDF are pinned under `evidence/source/`; their hashes are in `evidence/source/SHA256SUMS`. No author executable was found during the initial source audit, so all future numerical/theorem checks will be explicitly labeled clean-room unless a release is recovered.
