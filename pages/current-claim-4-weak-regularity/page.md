# Prior finite corroboration (superseded): Claim 4

## Route verdict: VERIFIED; not the current Claim 4 verdict

This finite paper-scale experiment corroborated the estimator on one atomic
target at **MEDIUM** confidence. It is preserved, but it is not the current
Claim 4 verifier. The exact
[threshold-escape counterexample](#/current-claim-4-threshold-falsification)
supersedes it and gives the current **FALSIFIED, HIGH** verdict.

## Exact claim contract

The primary source is ar5iv HTML for
[arXiv:2605.30153](https://ar5iv.labs.arxiv.org/html/2605.30153), retrieved
`2026-08-01T14:48:25Z` with explicit `Mozilla/5.0` user agent; SHA-256
`d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.

The abstract says the analysis does not impose smoothness, bounded-density, or
log-concavity assumptions. Section 1 says there are no restrictive assumptions
on scores or densities. Both [Theorem 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmtheorem1)
and [Theorem 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmtheorem2) cite
only [Assumption 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption1)
and [Assumption 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption2).

Verification requires a target that satisfies every stated assumption while
failing every named regularity, exact smoothed-score ground truth, the paper's
estimator, a pre-result resource and acceptance contract, uncertainty, a
scientific control, and an independent checker. The
[machine-readable contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/claim_contract.json)
fixes these requirements.

## Assumption-satisfying target

The deterministic experiment uses the paper's numerical scale `d=48, M=128,
k=3`. Each component is uniform over the six atoms `+/- A_i e_j`. Those atoms
span their declared subspace. The 128 orthonormal bases are fixed by seed
`260530153`.

| Assumption audit | Exact result |
| --- | --- |
| support in union of 128 subspaces | yes |
| maximum pairwise basis overlap | `0.7354733` |
| certified intersection spectral gap | `0.2645267 > 0` |
| mass on pairwise intersections | `0` |
| component mass | `1/128`, equal to the `c_p=1` lower bound |
| each component spans `k=3` | yes |
| bounded support | norm exactly `1` |
| Assumption 2 `sigma^2` | `1/log(4)` |
| worst-direction exponential-square moment | exactly `2` |

For the last row, a conditional atom is uniform over `+/-e_1,+/-e_2,+/-e_3`.
Convexity on the squared-coordinate simplex puts the worst direction on a
coordinate axis, giving `(exp(1/sigma^2)+k-1)/k=2`.

The target is a finite atomic measure, so neither an ambient nor an intrinsic
Lebesgue density exists. It therefore has no Holder density, density upper
bound, or positive density lower bound. It is not log-concave: `e_1` and
`-e_1` are support atoms while their midpoint has zero mass.

## Faithful paper-scale experiment

The implementation uses the paper's Gaussian KDE, density threshold,
tangent-only clipping, exact normal score, plug-in mixture weights, and
regularization set. Duplicate observations are aggregated by exact counts,
algebraically identical to summing all `N` samples. The true score of `p_t` is
the independently computed posterior average over all 768 Gaussian-smoothed
atoms.

Before seeing results, the route fixed `t=0.25`, `N=6250,12500,25000,50000`,
20 independent training datasets, 10,000 independent queries per seed, and
`C_R=4`. All 80 `(N,seed)` results are reported. No sample size, tolerance, or
first hit came from the theorem formula.

| `N` | mean squared L2 error | 95% CI | min samples in any component | thresholded fraction |
| ---: | ---: | ---: | ---: | ---: |
| 6,250 | 0.175599 | (0.166304, 0.184893) | 23 | 0.0004150 |
| 12,500 | 0.115141 | (0.106996, 0.123285) | 61 | 0.0001838 |
| 25,000 | 0.073898 | (0.067129, 0.080668) | 144 | 0.0000848 |
| 50,000 | 0.045451 | (0.039838, 0.051064) | 320 | 0.0000403 |

The log-log slope is `-0.648950`; every prespecified acceptance gate passed.
No component was absent, and `C_R=4` excluded zero evaluated component-query
pairs.

Omitting the analytically known normal score is the scientific negative
control. At `N=50000` its mean error was `157.757250`, or `3470.951` times the
accepted estimator error. Separately changing the required zero-intersection
mass from true to false made the independent checker exit `1` with `the atomic
target fails a paper assumption`.

- [Raw JSON with every seed](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/raw_results.json)
- [Independent checker output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/independent_checker.json)
- [Assumption-mutation output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/negative_control_output.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/source_audit.md)
- [Method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/method.md)
- [Exact command and environment](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/reproduction.md)
- [Pre-run resource estimate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/resource_estimate.md)
- [Limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_atomic_weak_regularity/limitations.md)

The [generator](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim4_atomic_weak_regularity.py)
and [independent verifier](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim4_atomic_weak_regularity.py)
are executable and exit nonzero when evidence fails.

## Reproduction and allocation

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Locked environment: Python `3.14.2`, NumPy `2.5.1`, one repository `.venv`,
`pyproject.toml` and `uv.lock`, materialized with `uv sync --frozen` in
`ghcr.io/astral-sh/uv:python3.14-bookworm`.

The pre-run estimate was 8 useful cores and 5-20 minutes. HF `cpu-upgrade`
allocated 8 cgroup-limited vCPUs, 32,000,000,000 bytes RAM, and no accelerator.
Scientific runtime was `227.529138` seconds; the cumulative job took `287`
seconds and cost approximately `$0.002392` at `$0.0005/minute`. Run
`e1002fce-0e85-44fd-9dd5-0dfc5ca3ca3e`, HF job
`DineshAI/6a6e183ba00abefd4b28b9cf`, Git
`f23684773489717e1550b61f375ccfd4f8d10193`.

All 31 repository tests and 17 offline manifests passed. The inherited
historical poster then failed its known style, asset, and measure gates; that
presentation failure does not alter the scientific result.

## Limitations

The finite experiment directly corroborates the exact-recovery-conditional
score mechanism, not the universal continuous-time sampling theorem. The paper
does not specify the numerical `C_R`; this route precommits `C_R=4` and reports
that it excluded nothing. The result does not repair Claim 3's recovery
failure. These limits cap confidence at MEDIUM.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | this page | yes | yes | yes | PASS | omitted normal plus assumption mutation | yes | VERIFIED |

The older source-only page is retained under **Historical rejected baseline**
and is not the current verifier.
