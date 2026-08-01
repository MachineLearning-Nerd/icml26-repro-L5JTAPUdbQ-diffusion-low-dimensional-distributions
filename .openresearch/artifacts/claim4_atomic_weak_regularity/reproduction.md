# Claim 4 reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The cumulative research runner executes the generator, independent checker,
assumption mutation, and all previously accepted claims. Environment: one
repository `.venv`, Python `3.14.2`, NumPy `2.5.1`, pinned `uv.lock`,
`ghcr.io/astral-sh/uv:python3.14-bookworm`, HF `cpu-upgrade`, no GPU.
