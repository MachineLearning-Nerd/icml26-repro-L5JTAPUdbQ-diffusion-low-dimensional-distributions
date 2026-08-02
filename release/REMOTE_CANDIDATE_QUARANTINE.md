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
