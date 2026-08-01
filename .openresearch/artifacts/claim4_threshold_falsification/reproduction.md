# Claim 4 threshold-falsification reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The cumulative runner regenerates the exact Claim 1 certificate first, then
derives and independently verifies the Claim 4 contract. Python 3.14.2 and all
dependencies are pinned by `uv.lock` in the single repository `.venv`.
