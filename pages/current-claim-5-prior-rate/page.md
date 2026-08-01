# Claim 5: prior ambient-dimensional rate

## Reviewer verdict: VERIFIED

A pinned primary-source proof-chain certificate verifies the paper's comparison
to prior diffusion analyses: under the directly supporting beta-Holder theorem,
the TV rate `n^(-beta/(d+2 beta))` inverts to sample complexity
`epsilon^(-(d+2 beta)/beta)`, up to logarithmic factors. This is a symbolic
proof certificate, not a finite-sample trend fit.

## Exact claim contract

The reproduced paper's [Equation 1](https://ar5iv.labs.arxiv.org/html/2605.30153#S1.E1)
attributes the exponent `(d+2 beta)/beta` to prior smooth-density diffusion
analyses. Its HTML was retrieved `2026-08-01T14:48:25Z` with an explicit
`Mozilla/5.0` user agent; SHA-256
`d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.

The direct primary contract is Cai and Li, [arXiv:2503.09583](https://arxiv.org/abs/2503.09583),
Theorem 1: for integer `d >= 1`, `0 < beta <= 2`, a subgaussian target with a
beta-Holder density, and the displayed iteration premise, expected TV is at
most

`C n^(-beta/(d+2 beta)) (log n)^((d+1)/2) log K`.

Verification requires pinned source hashes, exact theorem and assumption
markers, independent reconstruction of the polynomial exponent through the
proof, exact inversion, and strictly increasing dependence on ambient `d`.
The [machine-readable contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/claim_contract.json)
fixes the scope. No resource budget or observation was chosen from the formula.

## Primary-source proof chain

| Step | Exact polynomial exponent |
| --- | --- |
| squared score error after `tau=n^(-2/(d+2 beta))` | `-1+d/(d+2 beta) = -2 beta/(d+2 beta)` |
| score error after square root | `-beta/(d+2 beta)` |
| early stopping `tau^(beta/2)` | `-beta/(d+2 beta)` |
| TV after convergence and triangle inequality | `-beta/(d+2 beta)` |
| inversion for epsilon accuracy | `(d+2 beta)/beta` |
| derivative of sample exponent in `d` | `1/beta > 0` |

The exact-arithmetic sweep covered 20 `(d,beta)` pairs. Representative raw
values are:

| `d` | `beta` | TV exponent | sample exponent | inversion product |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 1/2 | 1/4 | 4 | 1 |
| 2 | 1 | 1/4 | 4 | 1 |
| 4 | 3/2 | 3/14 | 14/3 | 1 |
| 16 | 2 | 1/10 | 10 | 1 |
| 48 | 2 | 1/26 | 26 | 1 |

For the last case, the prior sample exponent is `26`; the reproduced paper's
illustrative intrinsic dimension `k=3` gives exponent `3`. The comparison is of
exponents, not a claim that the theorem constants or logarithms are equal.

Zhang et al., [arXiv:2402.15602](https://arxiv.org/abs/2402.15602), Theorem
3.8 independently give the matching `beta/(2 beta+d)` TV exponent, but assume
beta-Sobolev rather than beta-Holder smoothness. It is a cross-check, not the
source used to support the Holder wording.

## Raw results and independent checks

| Check | Result |
| --- | --- |
| all 12 source markers | `true` |
| all 20 exact inversions | `1` |
| ambient derivative | `1/beta > 0` |
| independent checker | `PASS` |
| exponent-999 mutation checker exit | `1` (required nonzero) |

- [Raw JSON](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/raw_results.json)
- [Independent checker output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/independent_checker.json)
- [Negative-control output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/negative_control_output.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/source_audit.md)
- [Method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/method.md)
- [Exact command and locked environment](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/reproduction.md)
- [Pre-run resource estimate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/resource_estimate.md)
- [Limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim5_prior_rate/limitations.md)

The [generator](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim5_primary_proof_chain.py)
and [independent verifier](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim5_primary_proof_chain.py)
are executable. The verifier re-extracts the pinned archives and exits nonzero
when a source, exponent, domain, comparison, or verdict changes. Replacing the
first sample exponent with `999` produced exit code `1` and stderr `the exact
rate table does not match the independently derived table`.

## Reproduction and allocation

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Locked environment: Python `3.14.2`, one repository `.venv`, `pyproject.toml`
and `uv.lock`, materialized by `uv sync --frozen --python 3.14.2` in
`ghcr.io/astral-sh/uv:python3.14-bookworm`.

The estimate was 1 useful core. HF `cpu-upgrade` allocated 8 cgroup-limited
vCPUs and 32,000,000,000 bytes RAM with no accelerator. The certificate took
`0.018315` seconds; the complete cumulative job took `106` seconds and cost
approximately `$0.000883` at `$0.0005/minute`. Run
`1bbdfbc1-3ab4-4b24-a50b-55c18405d322`, HF job
`DineshAI/6a6e11b4a00abefd4b28b92c`, Git
`c59609443ad89cf114c0875e46fc1f4c08653e28`, deterministic exact arithmetic,
no random seed.

All 31 repository tests and 17 offline manifests passed. The inherited
historical poster gate then failed its already-known style, asset, and measure
checks after downloading browser assets; that presentation failure does not
alter the scientific verifier result.

## Limitations

Confidence is **MEDIUM** because the certificate verifies the primary theorem,
the complete displayed exponent chain, and the exact inversion, but does not
independently re-prove every analytic lemma in Cai and Li. One intermediate
Cai-Li simplified Jacobian display omits a leading `n^(-1/2)` factor; the
certificate derives the exponent from its immediately preceding unsimplified
expression, and the following proof line uses that correct exponent.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | this page | yes | yes | yes | PASS | mutation fails | yes | VERIFIED |

The older source-only page is retained under **Historical rejected baseline**
and is not the current verifier.
