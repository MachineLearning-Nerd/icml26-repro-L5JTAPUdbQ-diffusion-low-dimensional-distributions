# Claim 2 reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The command materializes the single repository `.venv` with
`uv sync --frozen --python 3.14.2`, then `scripts/validate_release.py` invokes
`scripts/run_research_checks.py`. That cumulative runner executes the Claim 2
generator, independent checker, and mutation control after all accepted prior
claim checks.

Environment: `ghcr.io/astral-sh/uv:python3.14-bookworm`, `.python-version`
`3.14.2`, pinned `pyproject.toml` and `uv.lock`, HF `cpu-upgrade`, no GPU.
