# Reproduction

Fixed inherited experiment command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The bootstrap runs every accepted claim check through:

```sh
uv run python scripts/run_research_checks.py
```

The single repository `.venv` is locked by `pyproject.toml`, `uv.lock`, and
`.python-version` (`3.14.2`) and materialized with
`uv sync --frozen --python 3.14.2`. The HF job uses
`ghcr.io/astral-sh/uv:python3.14-bookworm`, `cpu-upgrade`, and no accelerator.

Generated Claim 5 evidence:

- `raw_results.json`
- `independent_checker.json`
- `mutated_evidence.json`
- `negative_control_output.json`
- `EVAL.md`
