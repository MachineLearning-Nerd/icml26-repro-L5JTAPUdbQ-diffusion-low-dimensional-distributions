Previous live judged score: `0/10`

Conservative projected score range after the proposed change: **6–10/10**.

Best-supported possible new score: **10/10 forecast only; not a judge result**.

# Final pre-publication release report

The current total remains **0/10**. The protected Space head and judge head are
both `fe1fd273934cf8568fbcc1187d857e7662313648`. Only the live judge can award
points after publication.

| Claim | Current points | Possible points | Confidence | Evidence status | Basis and remaining risk |
| --- | ---: | ---: | --- | --- | --- |
| 1 | 0 | 2 | HIGH | FALSIFIED | Exact continuous-time threshold-escape counterexample satisfies every assumption and defeats every fixed polylog; risk is evaluator interpretation of the paper's threshold convention. |
| 2 | 0 | 2 | MEDIUM | VERIFIED | Proof-structure certificate plus a faithful 12-seed KDE sweep verify intrinsic dependence conditional on exact recovery; not every concentration lemma is independently reproved. |
| 3 | 0 | 2 | HIGH | FALSIFIED | Identical observation laws with different declared subspace targets give an exact maximin success ceiling of 1/2; risk is whether the evaluator treats the recovery lemma as part of this claim. |
| 4 | 0 | 2 | HIGH | FALSIFIED | The atomic Rademacher target lacks all named regularities, meets the stated assumptions, and triggers the exact Theorem 2 failure. |
| 5 | 0 | 2 | MEDIUM | VERIFIED | Pinned Cai-Li primary-source proof chain yields the exact exponent and inversion, with Zhang et al. as a Sobolev cross-check; underlying analytic lemmas are not fully reproved. |

## Claim changes and blocked work

All five claims changed from the judge's source-only **INCONCLUSIVE** baseline:
Claims 1, 3, and 4 are candidate **FALSIFIED** verdicts; Claims 2 and 5 are
candidate **VERIFIED** verdicts. No claim is BLOCKED, and no claim has LOW
confidence, so the mandated three-plus-one LOW-confidence route sequence is
not triggered.

## Experiment tree and winning evidence

The immutable baseline was frozen first. The stacked tree then proceeded
through exact-recovery non-identifiability, the prior-rate proof chain,
conditional intrinsic-score proof and KDE scaling, a paper-scale atomic
weak-regularity study, Claim 1 proof/numerical routes, the exact threshold
counterexample, the linked Claim 4 falsification, cumulative page construction,
zero-warning poster repair, and two evaluator-blind review rounds.

The Round-2 validated evidence/navigation branch is
`orx/evaluator-visible-candidate-fixes` at
`214ef5e8fea680f32be066e40f31bd3bfd6ebaea`. This final packaging child adds
only reviewer records, release ledgers, exact-published-revision review support,
and their manifest entries; it does not change a scientific verdict.

## Reproduction and compute

Every experiment inherited the same command:

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

Every research and release-gate run used HF `cpu-upgrade`: 8 cgroup-limited
vCPUs, 32 GB RAM, no accelerator, the pinned `uv.lock`, and the same
repository-level `.venv` inside each ephemeral job. Through the successful
Round-2 candidate review, 27 HF jobs consumed `6,581` seconds (`1.8281` job
hours), approximately `$0.05484` at `$0.0005/minute`. The final packaging-run
runtime and cost are reported after it reaches a terminal state.

## Release gates

- Every claim has an exact candidate verdict and confidence.
- All current generators, verifiers, independent checkers, and negative
  controls rerun cumulatively; mutations exit nonzero.
- The complete suite reports 31 tests passing and 17 existing evidence/source
  manifests passing.
- Posterly preflight, style, asset, measure, and strict polish pass with zero
  warnings at pinned revision `94d374d72afdc372af226eb745e82af00f07e43f`.
- Round 1 recorded 16 evaluator-visible gaps; Round 2 recorded zero gaps.
- The protected 21-file tree is a subset of the candidate, and protected page
  nodes are a subset of the candidate logbook tree.
- `release/HF_TEXT_ALLOWLIST.txt` is sorted and unique; its companion manifest
  hashes every allowlisted path except the manifest itself.
- The candidate contains no recognized token, private-key, or cloud-key pattern.

## Exact publication action

After the final packaged review passes, create one additive text-only commit on
the existing Space
`DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions`, guarded by
the current protected parent revision. Upload exactly the paths in
`release/HF_TEXT_ALLOWLIST.txt`; perform no deletions and create no second
Space. Download and hash-verify the exact resulting revision, rerun the
canonical traversal on HF `cpu-upgrade`, mark the paper awaiting judge, then
mirror the exact published text paths to GitHub `main` and confirm the remote
SHA with `git ls-remote`.
