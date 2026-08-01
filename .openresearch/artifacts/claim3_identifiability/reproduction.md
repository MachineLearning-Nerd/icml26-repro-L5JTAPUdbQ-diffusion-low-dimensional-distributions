# Reproduction

The experiment node inherits this fixed command unchanged:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

`scripts/bootstrap_reproduction.sh` executes the scientific check with:

```sh
uv run python scripts/run_research_checks.py
```

The runner invokes the generator and independent verifier using the interpreter
from the single repository-level `.venv`. It also corrupts one result and
requires the verifier to exit nonzero.

The environment is locked by `pyproject.toml`, `uv.lock`, and
`.python-version` (`3.14.2`) and materialized with:

```sh
uv sync --frozen --python 3.14.2
```

The Hugging Face job uses image
`ghcr.io/astral-sh/uv:python3.14-bookworm`, flavor `cpu-upgrade`, and no GPU.
The raw record captures the committed Git SHA, resolved Python version, cgroup
CPU quota, CPU affinity, memory limit, runtime, accelerator status, and seed.

Generated evidence:

- `raw_results.json`
- `independent_checker.json`
- `mutated_evidence.json`
- `negative_control_output.json`
- `EVAL.md`
