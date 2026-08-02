# Claim 1 threshold-escape reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The bootstrap fetches all three public arXiv inputs only when absent and
requires their pinned SHA-256 hashes. `scripts/validate_release.py` then runs
the independent continuous-time verifier and every other accepted claim
check. Python 3.14.x and dependencies are locked by `uv.lock`.
