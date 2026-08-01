# Claim 4: weak-regularity claim fails on an atomic target

## Reviewer verdict: FALSIFIED

The same exact target that falsifies Theorem 2 satisfies every paper assumption
while lacking every regularity named by Claim 4. Therefore the broad statement
that the paper's results hold over this weak domain is false as stated.
Confidence is **HIGH**.

## Exact claim contract and source

The primary source is
[Section 3.2](https://ar5iv.labs.arxiv.org/html/2605.30153#S3.SS2), retrieved
`2026-08-01T14:48:25Z` with explicit `Mozilla/5.0` user agent; HTML
SHA-256 `d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.
The pinned source archive has SHA-256
`07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`.

The paper says its results do not rely on smooth densities or scores,
log-concavity, or exactly Gaussian components, and claims a near-optimal rate
under only a subgaussian assumption. Theorem 2 explicitly invokes only
[Assumption 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption1) and
[Assumption 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption2).
The judge's exact Claim 4 also names uniform density bounds and positive
density lower bounds.

The
[machine-readable contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/claim_contract.json)
requires an exact paper-result failure on a target satisfying both assumptions
and lacking every named regularity.

## Complete target-property audit

Use `p*=Uniform{-1,+1}` with `d=M=k=1`, `V1=R`, `c_p=1`, and
`sigma^2=1/log 2`.

| Paper assumption or excluded regularity | Exact result |
| --- | --- |
| support, component mass, intersections | Assumption 1 passes |
| worst exponential-square moment | `2`, so Assumption 2 passes |
| exact subspace recovery | trivial |
| ambient Lebesgue density | none: the law is atomic |
| intrinsic Lebesgue density | none: the law is atomic |
| Holder density or score | unavailable because no density exists |
| uniform density upper bound | unavailable because no density exists |
| positive density lower bound | unavailable because no density exists |
| log-concavity | false: `-1,+1` are support points but midpoint `0` is not |

All seven machine-checkable regularity flags are true: the target is atomic,
has neither density, has no Holder density/score or density bounds, and is not
log-concave.

## Exact result failure

On this target, the paper's density threshold makes the estimated score exactly
zero on an explicit positive-probability tail event for the whole continuous
reverse path. The remaining drift amplifies the output by `e^T=n`. The exact
lower bound

`W1 >= P(Z>b_n+1) [2 Phi(1)-1] [n exp(-n^-2)b_n-1]`

holds for every training realization, while Mills' ratio proves that it
asymptotically exceeds `C n^-1/2(log n)^A` for every fixed `A,C`. This is
the [full Claim 1 proof](#/current-claim-1-threshold-escape), including raw
values and the exact quantifiers.

Because Theorem 2 fails inside the claimed weak-regularity domain, Claim 4 is
FALSIFIED. This does not argue that smoothness is necessary for every other
estimator; it refutes the paper's broad claim about its stated results.

## Raw evidence and independent checks

| Check | Result |
| --- | --- |
| exact weak-regularity source markers | `6/6` |
| paper assumptions | all pass |
| named regularity absences | `7/7` |
| linked Theorem 2 certificate | FALSIFIED, HIGH |
| independent Claim 4 checker | PASS |
| log-concavity mutation checker | exit `1` (nonzero required) |

- [Claim 4 raw JSON](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/raw_results.json)
- [Claim 4 independent checker](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/independent_checker.json)
- [Claim 4 mutation-control output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/negative_control_output.json)
- [Claim 4 source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/source_audit.md)
- [Claim 4 method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/method.md)
- [Claim 4 limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/limitations.md)
- [Claim 4 command and environment](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/reproduction.md)
- [Claim 4 resource estimate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/resource_estimate.md)
- [Claim 4 evaluation summary](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim4_threshold_falsification/EVAL.md)
- [Shared theorem raw JSON](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_threshold_escape/raw_results.json)

The executable
[Claim 4 generator](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim4_threshold_falsification.py)
and
[independent verifier](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim4_threshold_falsification.py)
exit nonzero if the target, source, assumption audit, regularity audit, or linked
continuous-time contradiction changes. Marking the witness log-concave is the
negative mutation and must produce exit `1`.

## Reproduction and allocation

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Locked environment: Python `3.14.2`, NumPy `2.5.1`, one repository
`.venv`, `pyproject.toml` and `uv.lock`, materialized with
`uv sync --frozen` in `ghcr.io/astral-sh/uv:python3.14-bookworm`.

The estimate was 1 useful core. HF `cpu-upgrade` allocated 8 cgroup-limited
vCPUs, 32,000,000,000 bytes RAM, and no accelerator. The Claim 4 route took
`0.009269` seconds; OpenResearch run
`70f5d228-5ef0-45d6-8938-f6c442eba1d4`, HF job
`DineshAI/6a6e278e6b79c09949c1e76b`, took `382` seconds total
(`376` running) and cost approximately `$0.0032` at
`$0.0005/minute`. Scientific Git SHA:
`7075b338d13fd488ec0a556e05fd0954f4e5f712`. The route is deterministic
and uses no random seed.

The cumulative release parent passed all 31 repository tests, 17 manifests,
and all five Posterly gates with zero warnings on HF `cpu-upgrade` (run
`4b29d0fe-6893-436c-95bb-e9f93fad89cb`).

## Limitations

The falsification targets Theorem 2 and the paper's thresholded estimator. It
does not invalidate the separately assessed conditional score structure in
Claim 2 or establish that all weakly regular diffusion estimators fail.

The earlier `d=48,M=128,k=3` study remains reachable as
[Prior finite corroboration (superseded)](#/current-claim-4-weak-regularity).
It is not the current verifier.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | this page | yes | yes | yes | PASS | regularity mutation exit 1 | yes | FALSIFIED |
