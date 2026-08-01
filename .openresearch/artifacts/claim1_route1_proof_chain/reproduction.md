# Claim 1 route 1 reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The fixed command invokes `scripts/run_research_checks.py`, which runs the
generator, independent checker, and deliberately corrupted-evidence control.
Python 3.14.2 and all dependencies are pinned by `pyproject.toml` and
`uv.lock`; `uv sync --frozen` creates the one repository `.venv`.
