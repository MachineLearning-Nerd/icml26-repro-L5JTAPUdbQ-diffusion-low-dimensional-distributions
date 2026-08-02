# Claim 3: union-of-subspaces and tail assumptions

## Reviewer verdict: VERIFIED

The literal claim is descriptive: the analysis assumes support on a union of
`M` low-dimensional linear subspaces, zero probability mass on their pairwise
intersections, and subgaussian tails within each subspace. A pinned-source
certificate verifies every part at **HIGH** confidence.

## Exact claim contract

[Assumption 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption1)
states

`supp(p*) subset union_(i=1)^M V_i`, `dim(V_i)=k_i`,
`p*(V_i intersect V_j)=0` for every `i != j`, and
`p*(V_i) >= 1/(c_p M)`.

[Assumption 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmassumption2)
is titled “Subgaussian within each subspace” and bounds the conditional
exponential-square moment in every unit direction by `2`. In the tail-
regularity sense used by the live claim, this is the only tail condition; it
is not a statement that the theorems have no other premises.

[Theorem 1](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmtheorem1) and
[Theorem 2](https://ar5iv.labs.arxiv.org/html/2605.30153#Thmtheorem2) each
explicitly invoke both assumptions. The source archive is pinned at SHA-256
`07430c702d35e6dc7d6e34a79d32881a8f08cf48b1d855bf9cfb99c8a6981dc7`.

## Independent witness

To ensure the conditions are jointly satisfiable rather than merely copied,
the certificate constructs `d=4`, `V1=span(e1)`, `V2=span(e2)`, and the equal
atomic law on `{-e1,+e1,-e2,+e2}`.

| Requirement | Exact result |
| --- | --- |
| low-dimensional linear subspaces | dimensions `[1,1]` in `R^4` |
| support in union | all four atoms lie in `V1 union V2` |
| pairwise intersection | `V1 intersect V2={0}` |
| intersection mass | `0` |
| component masses | `[1/2,1/2]`, exactly `1/(c_p M)` for `c_p=1` |
| subgaussian parameter | `sigma^2=1/log 2` |
| worst exponential-square moment | `exp(1/sigma^2)=2`, exactly the bound |

The independent verifier repeats nine source checks and twelve witness checks.
It reports `PASS`. Adding `0.1` mass to the intersection and deleting the
subgaussian bound are separate negative controls; both are rejected.

- [Machine-readable contract](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/claim_contract.json)
- [Raw certificate](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/raw_results.json)
- [Independent checker](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/independent_checker.json)
- [Negative controls](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/negative_control_output.json)
- [Source audit](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/source_audit.md)
- [Method](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/method.md)
- [Exact rerun](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/reproduction.md)
- [Limitations](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim3_literal_assumption/limitations.md)

The executable [generator](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim3_literal_assumption.py)
and [independent verifier](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim3_literal_assumption.py)
use only the Python standard library and exit nonzero on a failed check.

## Scope boundary

Appendix B.1's exact-recovery argument is a separate proof issue and is not
part of the literal live Claim 3. This page neither uses that issue to falsify
the assumption statement nor presents the source audit as proof of recovery or
of either main theorem.

## Evaluator visibility

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | this page | yes | yes | yes | PASS | two invalid witnesses rejected | yes | VERIFIED |
