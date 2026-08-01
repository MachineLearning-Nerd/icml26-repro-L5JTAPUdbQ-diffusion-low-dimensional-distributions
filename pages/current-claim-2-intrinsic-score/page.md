# Claim 2: intrinsic score-estimation dependence

## Reviewer verdict: VERIFIED

Two independent routes verify the claim's stated dimension dependence,
conditional on Theorem 1's explicit exact-subspace-recovery event: a
machine-checkable proof-structure certificate and a faithful executable KDE
study. Confidence is **MEDIUM**, because the certificate does not independently
re-prove every concentration and tail lemma.

## Exact claim contract

The primary source is [Theorem 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmtheorem1),
retrieved `2026-08-01T14:48:25Z` with explicit `Mozilla/5.0` user agent; HTML
SHA-256 `d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`.

For targets satisfying [Assumption 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption1)
and [Assumption 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption2),
under exact subspace recovery and `t <= N^{O(1)}`, the theorem bounds

`E ||s_hat_t(X)-s*_t(X)||^2`

by

`C_score d M^3/N [1/t + sigma^(k vee 2)/t^((k vee 2)/2+1)] polylog(N)`,

where `C_score` is independent of `N,d,M,t`. The expectation is over the `N`
training samples and `X~p_t`. Verification requires the exact source contract,
an independent proof of the ambient normal-score cancellation, a complete
dependency trace, a faithful estimator run, uncertainty, and controls that
reject ambient substitution and a broken normal projector. The
[machine-readable contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/claim_contract.json)
fixes this scope.

This verdict does not erase Claim 3: the theorem is verified only under its
stated recovery event; Appendix B.1 does not validly guarantee that event from
Assumption 1 alone.

## Route 1: proof-level structural certificate

The checker extracted 13 exact markers from the pinned source archive spanning
the theorem statement, true and estimated component scores, low-dimensional
lemma, weight-error proof, aggregation, and final bound.

| Proof dependency | Independently checked consequence |
| --- | --- |
| true and estimated component normal term | the same `-(I-P_i)x/t`; error is exactly zero |
| tangent lift through orthonormal `A_i` | ambient squared component error equals `k_i`-dimensional squared error |
| low-dimensional KDE lemma | factor `(4/sqrt(pi))^k_i/N`, not an ambient-dimensional factor |
| normal Gaussian integration | integrates to one; remaining bounded box is `k_i`-dimensional |
| mixture aggregation | explicit polynomial `d M^3` prefactor |
| theorem constant | stated independent of `d` |

Exact rational arithmetic reconstructed the normal/tangent identity for 12
precommitted pairs: `d=4,8,16,48` and `k=1,2,3`. Every ambient squared error
equaled its intrinsic squared error and every normal-component error was
exactly zero. Replacing the first `k vee 2` exponent by ambient `d` made the
independent checker exit `1`.

- [Proof-certificate raw JSON](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/raw_results.json)
- [Proof independent checker](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/independent_checker.json)
- [Ambient-substitution control](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/negative_control_output.json)
- [Proof method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/method.md)
- [Proof source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/source_audit.md)
- [Proof limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/limitations.md)
- [Proof command and environment](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/reproduction.md)
- [Proof resource estimate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/resource_estimate.md)
- [Proof evaluation summary](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_intrinsic_score/EVAL.md)

## Route 2: faithful component-estimator study

The target is a Gaussian supported on a known `k`-dimensional coordinate
subspace, the valid `M=1` case of both assumptions. The executable
implementation uses the paper's Gaussian KDE at bandwidth `t`, density
threshold, tangent clipping, orthonormal lift, and exact normal score. Ground
truth is derived independently for the smoothed Gaussian.

The pre-result sweep fixed `t=0.5`, `N=128,256,512,1024,2048`, `k=1,2,3`,
ambient `d=4,8,16,48`, 12 paired seeds, and 1,024 held-out queries per seed.
It reports all 15 `(k,N)` cells and two-sided 95% t intervals; neither sample
sizes nor acceptance thresholds were selected from the theorem formula or an
observed first hit.

| `k` | MSE at `N=128` (95% CI) | MSE at `N=2048` (95% CI) | log-log slope |
| ---: | ---: | ---: | ---: |
| 1 | 0.103974 (0.088206, 0.119741) | 0.008585 (0.005214, 0.011955) | -0.864391 |
| 2 | 0.522764 (0.491560, 0.553969) | 0.081529 (0.068253, 0.094804) | -0.668297 |
| 3 | 1.356593 (1.320002, 1.393184) | 0.326754 (0.300929, 0.352579) | -0.516232 |

The error decreased across the complete geometric sweep for every `k`. With
the correct projector it is identical for all scheduled ambient dimensions,
as the proof certificate predicts. Omitting the known normal score is the
scientific negative control; its `d=48/d=4` error ratios were `15.5975`,
`22.7805`, and `38.9466` for `k=1,2,3`. Removing this ambient error from the
stored control made the checker exit `1`.

- [Scaling raw JSON with every seed](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/raw_results.json)
- [Scaling independent checker](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/independent_checker.json)
- [Broken-projector mutation output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/negative_control_output.json)
- [Numerical method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/method.md)
- [Numerical source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/source_audit.md)
- [Numerical limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/limitations.md)
- [Numerical claim contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/claim_contract.json)
- [Numerical command and environment](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/reproduction.md)
- [Numerical resource estimate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/resource_estimate.md)
- [Numerical evaluation summary](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim2_component_scaling/EVAL.md)

The executable [proof generator](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim2_intrinsic_score_certificate.py),
[proof checker](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim2_intrinsic_score.py),
[KDE study](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim2_faithful_component_scaling.py),
and [statistical checker](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim2_component_scaling.py)
all exit nonzero on failed evidence.

## Reproduction and allocation

Fixed inherited command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Locked environment: Python `3.14.2`, NumPy `2.5.1`, one repository `.venv`,
`pyproject.toml` and `uv.lock`, materialized with `uv sync --frozen` in
`ghcr.io/astral-sh/uv:python3.14-bookworm`.

The proof route estimated 1 useful core; the KDE route estimated 8. HF
`cpu-upgrade` allocated 8 cgroup-limited vCPUs, 32,000,000,000 bytes RAM, and
no accelerator. Proof checking took `0.012764` seconds and the KDE study
`8.878270` seconds. The cumulative job took `58` seconds, approximately
`$0.000483` at `$0.0005/minute`: run
`c8c463cd-93c4-4c0a-b4bb-6ef86f02fddb`, HF job
`DineshAI/6a6e157d6b79c09949c1e687`, scientific Git SHA
`355d19192868f7540a7169b17728349b0478e5af`.

The cumulative release parent passed all 31 repository tests, 17 manifests,
and all five Posterly gates with zero warnings on HF `cpu-upgrade` (run
`4b29d0fe-6893-436c-95bb-e9f93fad89cb`).

## Limitations

The numerical route is finite `M=1` corroboration and does not test mixture
weights. The proof certificate audits their dimension dependence but does not
independently re-prove every analytical lemma, limiting confidence to MEDIUM.
The result is conditional on exact recovery and therefore does not contradict
or repair the Claim 3 falsification.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2 | this page | yes | yes | yes | two PASS | two mutations plus broken projector | yes, conditional scope | VERIFIED |

The older source-only page is retained under **Historical rejected baseline**
and is not the current verifier.
