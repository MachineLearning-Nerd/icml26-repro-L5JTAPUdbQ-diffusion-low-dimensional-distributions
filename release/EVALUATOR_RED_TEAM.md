# Evaluator-blind pre-publication review

The reviewer began only at `README.md` and `logbook.json`, downloaded the
protected revision afresh, traversed the candidate page tree and direct links,
and did not use unpublished repository knowledge. The exact files opened and
all release-gate reads are recorded in
[`EVALUATOR_RED_TEAM.json`](EVALUATOR_RED_TEAM.json).

## Round 1 — FAIL before fixes

- Run: `0bf1fc1d-4741-4654-a8ee-9b68e66d69c2`
- HF job: `DineshAI/6a6e3877a00abefd4b28bd46` (`cpu-upgrade`, no accelerator)
- Git SHA: `d825d66e84b0a416ed735d27e920e490b5dc4187`
- Reviewer status: **FAIL**
- Files opened through evaluator traversal: `77`
- Findings: `16`

- `entrypoint.readme` — README does not identify logbook.json as the canonical evaluator entrypoint
- `history.page_tree` — protected page-tree nodes are not a subset of the candidate
- `claim.link` — Claim 1: EVAL.md is not directly linked
- `claim.git` — Claim 2: 'Git SHA' not visible
- `claim.link` — Claim 2: EVAL.md is not directly linked
- `claim.link` — Claim 2: reproduction.md is not directly linked
- `claim.link` — Claim 2: resource_estimate.md is not directly linked
- `claim.confidence` — Claim 3: confidence missing
- `claim.git` — Claim 3: 'Git SHA' not visible
- `claim.link` — Claim 3: EVAL.md is not directly linked
- `claim.link` — Claim 4: EVAL.md is not directly linked
- `claim.link` — Claim 4: reproduction.md is not directly linked
- `claim.link` — Claim 4: resource_estimate.md is not directly linked
- `claim.git` — Claim 5: 'Git SHA' not visible
- `claim.link` — Claim 5: EVAL.md is not directly linked
- `release.allowlist` — exact HF text allowlist is missing

## Round 2 — PASS after fixes

- Run: `9ec85de3-636f-4ecb-ab7b-d2ffc70b6316`
- HF job: `DineshAI/6a6e3ad0a00abefd4b28bd76` (`cpu-upgrade`, no accelerator)
- Git SHA: `214ef5e8fea680f32be066e40f31bd3bfd6ebaea`
- Reviewer status: **PASS**
- Files opened through evaluator traversal: `90`
- Findings: `0`
- Protected file subset: `true`
- Protected page-tree subset: `true`
- Visibility rows complete: `true`

The packaged release adds this record after Round 2, so a final third HF run
must pass before publication.
