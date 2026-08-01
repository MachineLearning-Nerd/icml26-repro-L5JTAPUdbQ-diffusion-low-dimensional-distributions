# Claim 1 threshold-escape evaluation

- Verdict: **FALSIFIED**
- Confidence: **HIGH**
- Scientific Git SHA: `1d43a6597a1f15ac19fccd6ef080877a9cfd0870`
- HF Job: `DineshAI/6a6e23526b79c09949c1e72b`
- Selected flavor: `cpu-upgrade`
- Estimated need: 1 CPU core; allocated: 8 vCPU, 32 GB RAM, no accelerator
- Scientific runtime: `0.012820` seconds
- Full job runtime: `367` seconds (`361` running, `6` scheduling)
- Estimated cost: `$0.0031` at `$0.0005/min`
- Fixed command: `./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh`
- Independent checker: **PASS**
- Negative-control checker exit: `1` (nonzero required)
- Cumulative regression: 31 tests and 17 evidence/release manifests passed
- Cumulative release gate: 31 tests, 17 manifests, and all five Posterly gates passed with zero warnings in HF run `4b29d0fe-6893-436c-95bb-e9f93fad89cb`.

The target is `Uniform{-1,+1}` with `d=M=k=1`, so exact subspace recovery is trivial. Every paper assumption is satisfied. On an explicit positive-probability Gaussian-tail event, the paper's density threshold keeps its KDE score exactly zero for the full continuous reverse trajectory. The remaining linear drift multiplies the output by `e^T=n`. The resulting analytic Wasserstein lower bound asymptotically dominates `n^{-1/2}` times every fixed polylogarithm, contradicting Theorem 2.

The rejected Euler attempt is retained as **Historical rejected baseline** and is not used as falsification evidence.
