# Claim 4 threshold-falsification reproduction

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The validator checks the exact Claim 1 raw certificate first and then invokes
the independent Claim 4 verifier against that shared input. Python 3.14.x and
all dependencies are pinned by `uv.lock`.
