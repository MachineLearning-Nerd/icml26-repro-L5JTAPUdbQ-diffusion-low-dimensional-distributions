# Reproduction

Fixed inherited experiment command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The single repository `.venv` is locked by `pyproject.toml`, `uv.lock`, and
`.python-version` (`3.14`) and materialized with
`uv sync --frozen --python 3.14`. The bootstrap downloads the paper, Cai–Li,
and Zhang source archives only when missing and rejects any hash mismatch.
The HF job uses
`ghcr.io/astral-sh/uv:python3.14-bookworm`, `cpu-upgrade`, and no accelerator.

Generated Claim 5 evidence:

- `raw_results.json`
- `independent_checker.json`
- `negative_control_output.json`
- `EVAL.md`
