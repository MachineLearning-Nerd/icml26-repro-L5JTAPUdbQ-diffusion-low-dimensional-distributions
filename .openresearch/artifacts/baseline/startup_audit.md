# Frozen baseline startup audit

- Paper: arXiv `2605.30153`, OpenReview `L5JTAPUdbQ`
- Repository: `MachineLearning-Nerd/icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions`
- Validated baseline branch: `main`
- Frozen starting Git SHA: `5da9f5694d785e18097cddbe44bfc17a260154c5`
- Existing Space: `DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions`
- Protected judged HF revision: `fe1fd273934cf8568fbcc1187d857e7662313648`
- Live verdict selection: exact `space_id` match, not OpenReview ID alone
- Judged score at that revision: `0/10`
- Judge time: `2026-08-01T07:51:30+00:00`
- Protected Space file count: 21
- Protected manifest: `.openresearch/artifacts/baseline/judged_space_manifest.sha256`
- Disk available at startup: 47 GiB
- Unrelated protected HF job observed: `6a6dff1d6b79c09949c1e5cd` (`RUNNING`, `cpu-upgrade`); it is outside this project and will not be modified.

## Fixed command

This command was selected from the repository's existing documented release
workflow before the baseline run. Every child inherits it unchanged:

```bash
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Variants must be encoded in committed code or configuration, never an alternate
run command or environment variable.

## Environment and compute policy

The campaign uses the single repository-level `.venv` resolved by `uv.lock`
for Python 3.14.6, the available Python 3.14 patch release at lock generation.
Historical baseline artifacts reported Python 3.14.5; no authoritative Python
pin existed in the repository, so the new environment records this patch-level
deviation explicitly. All scientific computation, tests, verifiers, benchmarks,
and data generation run on Hugging Face `cpu-upgrade`; local activity is
limited to inspection, editing, dependency resolution, and orchestration. The
selected flavor exposes 8 vCPU, 32 GB RAM, 50 GB storage, no accelerator, at
the observed price of $0.0005/minute ($0.03/hour). GPU hardware is prohibited.

## Baseline evaluator-visible audit

The protected Space is navigable from `README.md` through `logbook.json`, but
its five claim pages are source/formula audits. They do not expose executable
claim code, raw numerical data, an independent checker, a failing negative
control, a pinned executable environment, or per-run CPU/runtime metadata.
This matches the live judge's `0/10` assessment. Historical files must remain
unchanged and reachable, but must be labeled `Historical rejected baseline`
and placed behind the current verification in candidate navigation.
