---
title: "Reproduction: Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions"
emoji: 🎯
colorFrom: yellow
colorTo: red
sdk: static
pinned: false
tags:
 - trackio
 - trackio-logbook
 - open-experiment
 - icml2026-repro
 - paper-L5JTAPUdbQ
---

# Reproduction: Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions

The canonical evaluator entrypoint is [`logbook.json`](logbook.json). Its root
opens the current cumulative reproduction first; the exact judged 0/10 pages
remain reachable under **Historical rejected baseline**.

| Claim | Candidate verdict | Confidence | Current page |
| --- | --- | --- | --- |
| 1 | FALSIFIED | HIGH | [threshold escape](#/current-claim-1-threshold-escape) |
| 2 | VERIFIED | MEDIUM | [intrinsic score structure](#/current-claim-2-intrinsic-score) |
| 3 | FALSIFIED | HIGH | [recovery non-identifiability](#/current-claim-3-identifiability-counterexample) |
| 4 | FALSIFIED | HIGH | [weak-domain theorem failure](#/current-claim-4-threshold-falsification) |
| 5 | VERIFIED | MEDIUM | [prior-rate proof chain](#/current-claim-5-prior-rate) |

These are candidate reproduction verdicts, not awarded points. The previous
live judge result remains **0/10** at Space revision
`fe1fd273934cf8568fbcc1187d857e7662313648` until the judge evaluates a new
published revision.

## Fixed reproduction command

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The environment is pinned by [`pyproject.toml`](pyproject.toml) and
[`uv.lock`](uv.lock). Every scientific and release-gate run used Hugging Face
`cpu-upgrade` with no accelerator.

## Release audit

- [Release report](release/RELEASE_REPORT.md)
- [Evaluator-blind review](release/EVALUATOR_RED_TEAM.md)
- [Visibility matrix](release/VISIBILITY_MATRIX.md)
- [Exact text allowlist](release/HF_TEXT_ALLOWLIST.txt)
- [SHA-256 manifest](release/HF_TEXT_MANIFEST.sha256)
