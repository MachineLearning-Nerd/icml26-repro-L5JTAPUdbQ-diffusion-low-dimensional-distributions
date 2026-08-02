# Executive summary

---
<!-- trackio-cell
{"type": "markdown", "id": "cell_campaign_20260802_summary", "created_at": "2026-08-02T14:30:00+00:00", "title": "Executive summary", "pinned": true, "pinned_at": "2026-08-02T14:30:00+00:00"}
-->
The exact live judge baseline is **2/10** at Hugging Face revision
`47dad2b9bfe645cb59775632bc894efa9d65a546`. The evidence below is a new
candidate, not an earned score; only the live judge can change the baseline.

## Candidate evidence

| Claim | Evidence verdict | Confidence | Exact route |
| --- | --- | --- | --- |
| 1 | FALSIFIED | HIGH | exact continuous-time threshold-escape counterexample |
| 2 | VERIFIED | MEDIUM | conditional proof certificate plus faithful KDE study |
| 3 | VERIFIED | HIGH | literal assumption source-conformance certificate |
| 4 | FALSIFIED | HIGH | same atomic target violates the broad weak-domain result |
| 5 | VERIFIED | MEDIUM | pinned primary-source rate proof chain |

Claim 3 is deliberately corrected from the quarantined candidate: its live
wording is a descriptive statement about Assumptions 1 and 2. Appendix B.1's
separate recovery issue is disclosed as a limitation, not used as evidence.

## Scope and cost

| Route | Scope | Compute |
| --- | --- | --- |
| Claim 1 | analytic counterexample to literal Theorem 2 | deterministic CPU certificate |
| Claim 2 | Theorem 1 conditional on exact recovery; `M=1` executable corroboration | deterministic proof audit plus 12-seed local CPU sweep |
| Claim 3 | literal source-conformance claim only | deterministic local CPU, <1 second |
| Claim 4 | exact Theorem 2 failure within the named weak domain | shared Claim 1 certificate |
| Claim 5 | Cai–Li primary theorem and exponent inversion | deterministic exact arithmetic |

The inherited evidence jobs used only HF `cpu-upgrade`, never a GPU; every
individual job finished below two hours. The corrected Claim 3 work and the
current clean reruns used local CPU and no paid compute.

Repositories and sources:

- GitHub: https://github.com/MachineLearning-Nerd/icml26-repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions
- Hugging Face Space: https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions
- Paper: https://arxiv.org/abs/2605.30153
- Cai and Li comparator: https://arxiv.org/abs/2503.09583
- Zhang et al. cross-check: https://arxiv.org/abs/2402.15602

Every claim page links its contract, raw result, independent checker, negative
control, method, limitations, code, and exact rerun instructions.

---
<!-- trackio-cell
{"type": "figure", "id": "cell_campaign_20260802_poster", "created_at": "2026-08-02T14:30:00+00:00", "title": "Reproduction poster", "pinned": true, "pinned_at": "2026-08-02T14:30:00+00:00", "poster": true}
-->
<iframe title="Reproduction poster" src="https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/resolve/main/logbook/poster_embed.html" width="100%" height="760"></iframe>

[Open the text-only poster directly](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/logbook/poster_embed.html).
