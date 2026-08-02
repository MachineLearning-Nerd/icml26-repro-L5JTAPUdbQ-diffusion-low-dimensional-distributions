# Claim 2 component-study reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

`scripts/validate_release.py` runs the statistical checker directly after the
proof-structure checker and before the later claim checks. Environment: one
repository `.venv`, Python `3.14.x`, NumPy `2.5.1`, pinned `uv.lock`,
`ghcr.io/astral-sh/uv:python3.14-bookworm`, HF `cpu-upgrade`, no GPU.
