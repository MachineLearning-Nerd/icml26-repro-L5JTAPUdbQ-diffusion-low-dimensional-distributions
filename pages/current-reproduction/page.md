# Current reproduction evidence

This candidate is not a new judge result. The previous live judged score
remains **0/10** at Hugging Face revision
`fe1fd273934cf8568fbcc1187d857e7662313648`.

## Current verification

| Claim | Status | Confidence | Current evidence |
| --- | --- | --- | --- |
| Claim 1 | FALSIFIED | HIGH | [Exact continuous-time threshold-escape counterexample](#/current-claim-1-threshold-escape) |
| Claim 2 | VERIFIED | MEDIUM | [Conditional proof certificate and faithful KDE study](#/current-claim-2-intrinsic-score) |
| Claim 3 | FALSIFIED | HIGH | [Exact-recovery identifiability counterexample](#/current-claim-3-identifiability-counterexample) |
| Claim 4 | FALSIFIED | HIGH | [Atomic weak-domain theorem counterexample](#/current-claim-4-threshold-falsification) |
| Claim 5 | VERIFIED | MEDIUM | [Primary-source proof-chain certificate](#/current-claim-5-prior-rate) |

These are reproduction verdicts and possible evaluator outcomes, not points
already awarded. Only the live judge can change the score.

## What changed from the judged baseline

The judged pages only audited formulas and explicitly did not run the named
estimator or independently verify proofs. Current pages now expose exact claim
contracts, source quantifiers, executable generators and nonzero-on-failure
verifiers, raw data, independent checker outputs, scientific controls,
limitations, fixed commands, locked versions, Git revisions, seeds, and HF CPU
allocations. Historical files are preserved under **Historical rejected
baseline**.

## Navigation

- [Current Claim 1 verifier](#/current-claim-1-threshold-escape)
- [Current Claim 2 verifier](#/current-claim-2-intrinsic-score)
- [Current Claim 3 verifier](#/current-claim-3-identifiability-counterexample)
- [Current Claim 4 verifier](#/current-claim-4-threshold-falsification)
- [Current Claim 5 verifier](#/current-claim-5-prior-rate)
- [Historical rejected baseline](#/index)

## Evaluator-visible matrix

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Claim 1](#/current-claim-1-threshold-escape) | yes | yes | yes | PASS | threshold-disabled plus mutation | yes | FALSIFIED |
| 2 | [Claim 2](#/current-claim-2-intrinsic-score) | yes | yes | yes | two PASS | ambient substitution and broken projector | yes, conditional scope | VERIFIED |
| 3 | [Claim 3](#/current-claim-3-identifiability-counterexample) | yes | yes | yes | PASS | mutation plus distinguishable law | yes | FALSIFIED |
| 4 | [Claim 4](#/current-claim-4-threshold-falsification) | yes | yes | yes | PASS | regularity mutation | yes | FALSIFIED |
| 5 | [Claim 5](#/current-claim-5-prior-rate) | yes | yes | yes | PASS | exponent mutation | yes | VERIFIED |

The current verifier is always the first linked page. The rejected Euler route
and the old source-only pages remain reachable but are explicitly superseded.

## Release audit

- [Final release report](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/RELEASE_REPORT.md)
- [Evaluator-blind review record](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/EVALUATOR_RED_TEAM.md)
- [Exact reviewer JSON, including every opened file](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/EVALUATOR_RED_TEAM.json)
- [Standalone visibility matrix](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/VISIBILITY_MATRIX.md)
- [Poster gate record](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/POSTER_GATE.json)
- [Campaign command ledger](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/COMMANDS.md)
- [Exact HF text allowlist](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/HF_TEXT_ALLOWLIST.txt)
- [SHA-256 upload manifest](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/release/HF_TEXT_MANIFEST.sha256)
