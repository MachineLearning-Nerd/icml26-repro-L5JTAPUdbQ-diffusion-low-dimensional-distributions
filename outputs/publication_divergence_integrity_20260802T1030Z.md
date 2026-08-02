# L5 publication divergence integrity checkpoint

- Checked UTC: 2026-08-02T10:30:42Z
- Prior reviewed C5-only local HEAD before fetch: `5da9f5694d785e18097cddbe44bfc17a260154c5`
- Concurrent candidate fetched from public GitHub: `1e411431b3d967272fd31147c65c41f71f2aab97`
- Existing public Space SHA before any retry: `223123ff67da24f79fcc1da6293b4108f2e60cd2`
- Supervisor-directed hold: do not publish, reconstruct, overwrite, or claim points. Fresh independent scientific and compliance reviews are required for all changed C1--C5 verdicts.

## Integrity results

- `git fsck --no-reflogs`: exit 0; reports only pre-existing dangling blobs/one dangling commit, no object corruption.
- `sha256sum -c evidence/source/SHA256SUMS`: exit 0; source archive and PDF match.
- `git diff --check 5da9f5694d785e18097cddbe44bfc17a260154c5..1e411431b3d967272fd31147c65c41f71f2aab97`: exit 2. Nine new JSON artifacts have a blank line at EOF, including Claim 2 component-scaling/intrinsic-score and Claim 4 atomic-weak-regularity files. This is a release-review finding, not silently repaired here.

No publication command was run. Candidate content remains unmodified; this report and local durable state are intentionally uncommitted pending review ownership.
