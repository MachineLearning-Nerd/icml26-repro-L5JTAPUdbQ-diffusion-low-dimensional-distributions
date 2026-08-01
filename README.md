# Reproduction: Diffusion Models Are Statistically Optimal for Learning Low-Dimensional Multi-Modal Distributions

ICML 2026 reproduction for OpenReview `L5JTAPUdbQ`.

## Scope and verdict provenance

`contract/live_claims.json` is an immutable official challenge input. Its `status: unverified` fields are source metadata, not this repository's results. Our separate scoped CPU audit verdicts are in `reproduction_verdicts.json`. They are source/theorem/finite-construction audits, **not** end-to-end diffusion-model training.

## Clean CPU bootstrap

```bash
./scripts/bootstrap_reproduction.sh
./.venv/bin/python scripts/validate_release.py
```

The source archive and PDF are pinned under `evidence/source/`; hashes are in `evidence/source/SHA256SUMS`.

## Release limitation

The tracked poster gate report used disabled style rules and an image-area waiver. It is retained for provenance but is **not** represented as a full strict release gate. Publication remains blocked until a full non-waived posterly toolchain run is retained. The redacted Pi trace is not committed to the public Git clone; any hosted trace attachment is separately controlled by Trackio.

## Official validator

See `outputs/official_validator_transcript.log` for the exact downloaded validator URL, target, timestamp, command, and exit status. Re-run the documented command after installing Trackio and configuring an authenticated HF target.
