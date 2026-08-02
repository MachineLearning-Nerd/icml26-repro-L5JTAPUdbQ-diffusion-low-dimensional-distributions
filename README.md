# Reproduction: Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions

ICML 2026 reproduction for OpenReview `L5JTAPUdbQ`.

## Scope and verdict provenance

`contract/live_claims.json` is an immutable official challenge input. Its `status: unverified` fields are source metadata, not this repository's results. Our separate scoped CPU audit verdicts are in `reproduction_verdicts.json`. They are source/theorem/finite-construction audits, **not** end-to-end diffusion-model training.

## Clean CPU bootstrap

```bash
./scripts/bootstrap_reproduction.sh
./.venv/bin/python scripts/validate_release.py
./scripts/run_full_poster_gates.sh
```

The source archive and PDF are pinned under `evidence/source/`; hashes are in `evidence/source/SHA256SUMS`.

## Poster gates and trace

`scripts/run_full_poster_gates.sh` pins Posterly at `94d374d72afdc372af226eb745e82af00f07e43f` and runs all style rules plus the real-figure area/provenance gate without disabled rules or a waiver. `logbook/GATE_REPORT.json` is the retained result. No public agent trace is declared or attached in this release; private local traces are intentionally excluded.

## Official validator

See `outputs/official_validator_transcript.log` for the exact downloaded validator URL, target, timestamp, command, and exit status. Re-run the documented command after installing Trackio and configuring an authenticated HF target.
