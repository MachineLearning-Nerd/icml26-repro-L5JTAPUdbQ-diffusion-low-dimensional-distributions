# Claim 4 threshold-falsification evaluation

- Verdict: **FALSIFIED**
- Confidence: **HIGH**
- Scientific Git SHA: `7075b338d13fd488ec0a556e05fd0954f4e5f712`
- OpenResearch run: `70f5d228-5ef0-45d6-8938-f6c442eba1d4`
- HF Job: `DineshAI/6a6e278e6b79c09949c1e76b`
- Selected flavor: `cpu-upgrade`
- Estimated need: 1 CPU core; allocated: 8 vCPU, 32 GB RAM, no accelerator
- Scientific route runtime: `0.009269` seconds
- Full cumulative job runtime: `382` seconds (`376` running, `5` scheduling)
- Estimated cost: `$0.0032` at `$0.0005/min`
- Fixed command: `./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh`
- Independent checker: **PASS**
- Negative-control checker exit: `1` (nonzero required)
- Cumulative regression: 31 tests and 17 evidence/release manifests passed
- Cumulative release gate: 31 tests, 17 manifests, and all five Posterly gates passed with zero warnings in HF run `4b29d0fe-6893-436c-95bb-e9f93fad89cb`.

The target has no ambient or intrinsic density and is not log-concave, yet it
satisfies Assumptions 1 and 2. The exact threshold-escape certificate
contradicts Theorem 2 on this target. Therefore the broad claim that the
paper's results hold throughout the stated weak-regularity domain is false as
stated.

The earlier paper-scale atomic experiment remains prior finite corroboration
and is not the current verifier.
