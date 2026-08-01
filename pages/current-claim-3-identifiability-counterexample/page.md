# Claim 3: exact-recovery identifiability counterexample

## Reviewer verdict: FALSIFIED

This proof-level counterexample falsifies Appendix B.1 Lemma 3's claim that
Assumption 1 suffices for data-only exact recovery of all declared subspaces.
That recovery step is used in the paper's Theorem 2 analysis. This is not a
finite-sample proxy and does not select a sample size from the claimed rate.
Confidence is **HIGH** because the two valid parameterizations have exactly
the same observation law and disjoint exact-recovery targets for every sample
size.

## Exact claim contract

Primary source: ar5iv HTML at
`https://ar5iv.labs.arxiv.org/html/2605.30153`, retrieved
`2026-08-01T14:48:25Z` with an explicit `Mozilla/5.0` user agent, SHA-256
`d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.

[Lemma 3](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmlemma3) claims that,
under [Assumption 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption1),
there is a data-only algorithm using upper bounds on `M` and `k` that exactly
recovers every `V_i` from
`n0 = O(c_p^2 M^2 (k+1) log n)` observations with failure probability bounded
by a universal constant times `M n^-10`.

The domain is every distribution satisfying Assumption 1. The witness also
satisfies [Assumption 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption2),
so it remains within the downstream theorem domain. Falsification requires two
valid parameterizations with identical observation laws and different exact
recovery targets. The full machine-readable
[claim contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/claim_contract.json)
fixes this criterion.

## Assumptions and witness

Let `d=4`, `M=2`, `k=2`, `c_p=1`, and put probability `1/4` on each of
`-e1`, `e1`, `-e2`, and `e2`.

| Check | Parameterization A | Parameterization B |
| --- | --- | --- |
| `V1` | `span(e1,e3)` | `span(e1,e4)` |
| `V2` | `span(e2,e4)` | `span(e2,e3)` |
| support in `V1 ∪ V2` | yes | yes |
| `V1 ∩ V2` | `{0}` | `{0}` |
| probability on intersection | `0` | `0` |
| component masses | `1/2, 1/2` | `1/2, 1/2` |

The intersection condition is non-vacuous because `M=2`. With
`sigma^2=1/log(2)`, every conditional component has worst-direction
`E exp(<u,X>^2/sigma^2)=2`, exactly the Assumption 2 limit.

## Contradiction

Both parameterizations generate the same distribution, hence the same law for
every sample size `n0`, but their unordered exact-subspace targets differ. The
two exact-success events are disjoint under that common observation law, so
their success probabilities sum to at most `1`. At least one valid
parameterization therefore has success probability at most `1/2` for every
`n`. For any universal hidden constant, `C M n^-10 < 1/2` for sufficiently
large `n`, contradicting the lemma's quantified recovery guarantee.

The missing condition is identifiability: for example, a requirement that each
conditional distribution minimally span its declared subspace.

## Raw results and independent checks

| Quantity | Result |
| --- | ---: |
| observation total variation, A vs B | `0.0` |
| maximin exact-recovery success upper bound | `0.5` |
| Assumption 2 worst moment | `2.0` |
| distinguishable-law control TV | `1.0` |
| independent checker | `PASS` |
| corrupted-evidence checker exit | `1` (required nonzero) |

- [Raw JSON](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/raw_results.json)
- [Independent checker output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/independent_checker.json)
- [Negative-control output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/negative_control_output.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/source_audit.md)
- [Method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/method.md)
- [Exact command and locked environment](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/reproduction.md)
- [Pre-run resource estimate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/resource_estimate.md)
- [Limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/limitations.md)
- [Evaluation summary](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_identifiability/EVAL.md)

The [generator](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim3_identifiability_counterexample.py)
and [independent verifier](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim3_identifiability.py)
are executable source. The verifier exits nonzero on any failed premise. A
mutation replacing the required TV `0` with `0.25` produced exit code `1` and
stderr `reported observation TV is not exactly zero`. A second negative
control uses disjoint observation laws with TV `1`; the indistinguishability
argument correctly does not apply.

## Reproduction and allocation

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Locked environment: Python `3.14.2`, one repository `.venv`, `pyproject.toml`
and `uv.lock`, materialized by `uv sync --frozen --python 3.14.2` in
`ghcr.io/astral-sh/uv:python3.14-bookworm`.

The estimate was 1 useful core. HF `cpu-upgrade` allocated 8 cgroup-limited
vCPUs and 32,000,000,000 bytes RAM with no accelerator. The scientific check
took `0.002452` seconds; the whole cumulative job took `42` seconds, costing
approximately `$0.00035` at `$0.0005/minute`. Run
`71e51c0f-2023-4b18-bffb-10ed53c8d160`, HF job
`DineshAI/6a6e0e7d6b79c09949c1e636`, scientific Git SHA
`1d40b18820f2da1c593101f7156e9e01dc3d1ef8`, deterministic exact arithmetic,
no random seed.

The cumulative release parent passed all 31 repository tests, 17 manifests,
and all five Posterly gates with zero warnings on HF `cpu-upgrade` (run
`4b29d0fe-6893-436c-95bb-e9f93fad89cb`).

## Limitations

This result falsifies the stated sufficiency of Assumption 1 for the exact
recovery step. It does not independently falsify Theorem 1 conditional on an
oracle recovery event, and it does not lower-bound the Wasserstein error of an
oracle sampler supplied with the minimal support subspace.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | this page | yes | yes | yes | PASS | two controls | yes | FALSIFIED |

The older source-only page is retained under **Historical rejected baseline**
and is not the current verifier.
