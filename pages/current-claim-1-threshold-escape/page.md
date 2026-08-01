# Claim 1: threshold-escape counterexample to Theorem 2

## Reviewer verdict: FALSIFIED

An exact continuous-time counterexample falsifies Theorem 2 at **HIGH**
confidence. This is not the earlier unstable Euler experiment: the result is a
deterministic proof certificate, holds for every training realization, and
uses the paper's stated estimator and sampler without a recovery failure.

## Exact claim contract and source

The primary source is
[Theorem 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmtheorem2), retrieved
`2026-08-01T14:48:25Z` with explicit `Mozilla/5.0` user agent; HTML
SHA-256 `d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.
The pinned source archive has SHA-256
`07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`.

For every target satisfying
[Assumption 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption1) and
[Assumption 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption2),
Theorem 2 takes
`n0=C_sc M^2 k log n`, `N=n-n0`, `T=log n`, and `tau=n^(-2/k)`.
It claims, for sufficiently large `n`,

`E_training W1(p*, Law(Y_(T-tau))) <= C d M^(3/2) n^(-1/(k vee 2)) polylog(n)`,

where `C` is independent of `n,d,M`. The
[machine-readable contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/claim_contract.json)
requires a counterexample satisfying every assumption, using the exact
thresholded estimator, and contradicting every fixed polylogarithmic factor.

## Assumption audit

Take `p*=Uniform{-1,+1}` in `R), with `d=M=k=1`, `V1=R`,
`c_p=1`, and `sigma^2=1/log 2`.

| Requirement | Exact audit |
| --- | --- |
| support in the declared union | `{-1,+1} subset R` |
| component mass | `1=c_p/M` |
| intersection mass | vacuous because `M=1` |
| subgaussian-square moment | `exp(1/sigma^2)=2`, exactly the limit |
| tail condition | bounded support |
| exact subspace recovery | trivial: the only one-dimensional subspace of `R` is `R` |

Thus the witness removes the separate Claim 3 recovery ambiguity.

## Exact continuous-time contradiction

For every fixed `C_sc`, set `n0=ceil(C_sc log n)` and `N=n-n0`. At the
paper's forward horizon `T=log n`, let

`b_n = [1 + sqrt(2(n^2-1) log(N/log N))]/n`.

The certificate checks five exact steps:

1. **Threshold persistence.** If the VE coordinate `z>n b_n`, then every
   Gaussian kernel centered at either training value `-1` or `+1` is
   strictly below the paper's threshold
   `log N/[N(2 pi h)^(1/2)]`. Therefore the estimated low-dimensional score
   is exactly zero, for every possible training dataset.
2. **Positive-probability path event.** Let
   `M_r=sqrt(2) integral_0^r exp(-u)dB_u`. On
   `Y0>b_n+1` and `min_r M_r>=-1`, the zero-score solution is
   `Y_r=exp(r)(Y0+M_r)`, so its VE coordinate is
   `z_r=n(Y0+M_r)>n b_n`. Since the smoothing variance decreases, Step 1
   remains true throughout the reverse path.
3. **Event probability.** Independence and the reflection principle give the
   positive lower bound
   `P(Z>b_n+1) [2 Phi(1)-1]`.
4. **Wasserstein lower bound.** The output is at least
   `n exp(-tau)b_n` on that event. Because the target is supported on
   `{-1,+1}`,
   `W1 >= P(event) [n exp(-tau)b_n-1]`.
   This holds for every training realization, hence also after the theorem's
   expectation over training data.
5. **Rate contradiction.** Mills' ratio gives
   `log W1 >= -2 sqrt(2 log n)-O(log log n)`. Therefore, for every fixed
   `A,C`,
   `W1/[C n^(-1/2)(log n)^A] -> infinity`.

This contradicts the exact universal Theorem 2 conclusion for `k=1`.

## Raw numerical audit

The finite values audit the formulas; the asymptotic derivation above, not a
fit to these rows, establishes falsification. Representative rows use the
largest checked split constant, `C_sc=16`.

| `n` | `N` | threshold boundary `b_n` | W1 lower bound | `sqrt(n) * lower bound` |
| ---: | ---: | ---: | ---: | ---: |
| 256 | 167 | 2.644049 | 0.0619166 | 0.990666 |
| 1,024 | 913 | 3.130625 | 0.0395759 | 1.266428 |
| 4,096 | 3,962 | 3.513111 | 0.0313765 | 2.008093 |
| 16,384 | 16,228 | 3.853095 | 0.0261920 | 3.352578 |
| 65,536 | 65,358 | 4.166982 | 0.0221766 | 5.677222 |
| 262,144 | 261,944 | 4.461414 | 0.0188572 | 9.654877 |

The complete raw file contains 18 finite cells over
`C_sc in {1,4,16}` and six log-scale asymptotic cells. At `log n=128`,
the certified log-ratio even against `n^-1/2(log n)^8` is already
`12.47596`; it rises to `178.69473` at `log n=512`.

- [Raw JSON](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/raw_results.json)
- [Independent checker output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/independent_checker.json)
- [Mutation-control output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/negative_control_output.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/source_audit.md)
- [Method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/method.md)
- [Exact command and environment](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/reproduction.md)
- [Pre-run resource estimate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/resource_estimate.md)
- [Limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/limitations.md)

The executable
[certificate generator](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim1_threshold_escape_counterexample.py)
and
[independent verifier](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim1_threshold_escape.py)
exit nonzero if any source marker, assumption, threshold identity, Brownian
event, Wasserstein bound, or asymptotic comparison fails.

## Controls and non-circularity

Disabling the density threshold makes the zero-score event unavailable, so the
counterexample correctly does not apply to that altered estimator. Separately,
doubling the first stored tail-kernel ratio made the verifier exit `1` with
`tail kernel is not at the density threshold`.

No sample size, tolerance, discretization, first-hit point, or Monte Carlo
budget was chosen from the claimed formula. The result is analytic and covers
all sufficiently large `n` for every fixed `C_sc`.

The precommitted Euler route failed its own checker and is preserved as
[Historical rejected baseline](#/historical-claim-1-euler). It is not used as
falsification evidence.

## Reproduction and allocation

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Locked environment: Python `3.14.2`, NumPy `2.5.1`, one repository
`.venv`, `pyproject.toml` and `uv.lock`, materialized with
`uv sync --frozen` in `ghcr.io/astral-sh/uv:python3.14-bookworm`.

The estimate was 1 useful core. HF `cpu-upgrade` allocated 8 cgroup-limited
vCPUs, 32,000,000,000 bytes RAM, and no accelerator. The certificate took
`0.012820` seconds; job `DineshAI/6a6e23526b79c09949c1e72b` took
`367` seconds total (`361` running) and cost approximately `$0.0031` at
`$0.0005/minute`. Scientific Git SHA:
`1d43a6597a1f15ac19fccd6ef080877a9cfd0870`. The calculation is
deterministic and uses no random seed.

All 31 repository tests and 17 manifests passed. The later poster style,
asset, and measure gates failed; that presentation issue is being repaired
separately and does not alter the scientific checker.

## Limitations

This falsifies Theorem 2 for the paper's thresholded estimator. It does not
claim every diffusion estimator fails on the target. The asymptotic statement
uses the standard meaning of `polylog n`: a fixed finite log power and
`n`-independent constant.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | this page | yes | yes | yes | PASS | threshold disabled plus mutation exit 1 | yes | FALSIFIED |
