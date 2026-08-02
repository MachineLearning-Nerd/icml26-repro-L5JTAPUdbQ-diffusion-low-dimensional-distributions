# Reproduction

From the repository root, either run `scripts/fetch_sources.py` to download the
pinned public archive or place it at `evidence/source/arxiv_source.tar`. Its
required SHA-256 is
`07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`.
Then run:

```sh
python3 src/claim3_literal_assumption.py
python3 verifiers/verify_claim3_literal_assumption.py
```

Both programs are deterministic, use only the Python standard library, and
must exit zero. The verifier regenerates `independent_checker.json` and
`negative_control_output.json`.
