# Quarantine: remote candidate `1e411431b3d967272fd31147c65c41f71f2aab97`

**Status: rejected for publication.** This branch/tag is preserved as
`quarantine/remote-1e41143`; it is not release evidence and must not be
published, mirrored to Trackio, or used to claim points.

## Reason

Independent reviews retained outside this repository found two release blockers:

1. `outputs/L5-remote-10pt-scientific-review.md` shows that the candidate's
   Claim 3 `FALSIFIED` verdict tests an uncontracted Appendix B.1 recovery
   lemma rather than the literal live Claim 3. The literal-contract forecast is
   at most 8/10, not 10/10.
2. `outputs/L5-remote-10pt-compliance-review.md` found stale Space-parent and
   missing final HF readback gates, as well as material conflicts between its
   claimed verdicts/paid-HF-compute provenance and the local-only reviewed
   `STATUS.md` policy.

The user-authorized policy is local CPU/local GPU only. The reviewed lineage at
`5da9f5694d785e18097cddbe44bfc17a260154c5` keeps Claims 1--4 inconclusive
and Claim 5 as the independently reviewed one-point toy. This reconciliation
reverts candidate changes after that trusted ancestor while preserving the
candidate immutable ref for forensic inspection.

## Required next step

Do not retry or publish until a clean local-only candidate is independently
reviewed, validated, and explicitly authorized. The existing HF queue is not
an authorization to publish a different revision.

---

# Quarantine: remote candidate `57cc883d036d3e4af64898f61545be65c60a043a`

**Status: rejected for publication.** This remote tip (chain
`dd175f4 -> 28c2b95 -> 57cc883`) is preserved at both branch and tag
`quarantine/remote-57cc883`. It is forensic-only and must never be mirrored to
Trackio or used for a score claim.

## Reason

It replaces the authoritative local `reproduction_verdicts.json` with
`candidate_only` VERIFIED/FALSIFIED assertions and its Claim-2 public page
explicitly states HF `cpu-upgrade` execution. That conflicts with the
user-authorized local CPU/local GTX 1050-only policy and with the reviewed
local-only official-2/10 lineage. Its content was not independently reviewed
or validated as an exact Space revision. The trusted restoration target is the
local-only chain `0756e0d -> 1ad27bb -> 522a14f`; the latter is a new,
honestly inconclusive C2 proof-dependency diagnostic. No Space action is
permitted as part of this Git reconciliation.
