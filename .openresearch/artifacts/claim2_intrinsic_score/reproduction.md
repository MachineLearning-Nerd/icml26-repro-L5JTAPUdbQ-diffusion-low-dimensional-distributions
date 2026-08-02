# Claim 2 reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The command materializes the single repository `.venv` with
`uv sync --frozen --python 3.14`, downloads only missing public arXiv inputs
after enforcing pinned hashes, and runs both Claim 2 independent checkers from
`scripts/validate_release.py`.

Environment: `ghcr.io/astral-sh/uv:python3.14-bookworm`, `.python-version`
`3.14`, pinned `pyproject.toml` and `uv.lock`, HF `cpu-upgrade`, no GPU.
