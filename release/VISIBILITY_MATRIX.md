# Evaluator-visible evidence matrix

Round 2 traversed the candidate from `README.md` and `logbook.json` with no
repository hints and reported every row complete.

| Claim | Canonical page | Code visible | Data inline | Raw link | Checker | Control | Exact claim tested | Reviewer verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pages/current-claim-1-threshold-escape/page.md` | yes | yes | yes | PASS | threshold-disabled and mutation exit 1 | yes | FALSIFIED |
| 2 | `pages/current-claim-2-intrinsic-score/page.md` | yes | yes | yes | two PASS | ambient substitution and broken projector | yes, conditional scope | VERIFIED |
| 3 | `pages/current-claim-3-identifiability-counterexample/page.md` | yes | yes | yes | PASS | mutation and distinguishable-law control | yes | FALSIFIED |
| 4 | `pages/current-claim-4-threshold-falsification/page.md` | yes | yes | yes | PASS | regularity mutation exit 1 | yes | FALSIFIED |
| 5 | `pages/current-claim-5-prior-rate/page.md` | yes | yes | yes | PASS | exponent mutation exit 1 | yes | VERIFIED |

All canonical pages directly expose the claim contract, source anchors and
quantifiers, assumptions, executable generator and verifier, raw numbers,
downloadable JSON, checker and control output, command, lockfiles, CPU/runtime
record, limitations, and evaluation summary. Exact opened-file lists are in
`release/EVALUATOR_RED_TEAM.json`.
