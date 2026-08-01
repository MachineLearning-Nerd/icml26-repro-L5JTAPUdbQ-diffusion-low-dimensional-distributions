# Claim 1 threshold-escape reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The cumulative research runner first reproduces and explicitly rejects the
historical Euler attempt, then generates and independently checks the
continuous-time certificate. Python 3.14.2 and dependencies are locked by
`uv.lock` in the single repository `.venv`.
