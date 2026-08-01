# Claim 1 route 2 reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The route is called cumulatively from `scripts/run_research_checks.py`. Python
3.14.2, NumPy 2.5.1, and the full environment are pinned by `uv.lock`; one
repository `.venv` is created by `uv sync --frozen`.
