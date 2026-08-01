# Claim 2 component-study reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

`scripts/validate_release.py` invokes the cumulative research runner, which
runs this study after every prior accepted check. Environment: one repository
`.venv`, Python `3.14.2`, NumPy `2.5.1`, pinned `uv.lock`,
`ghcr.io/astral-sh/uv:python3.14-bookworm`, HF `cpu-upgrade`, no GPU.
