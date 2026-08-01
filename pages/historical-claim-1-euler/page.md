# Historical rejected baseline

## Claim 1 Euler-Maruyama attempt

This numerical route is **REJECTED** and is not the current verifier. It is
preserved to document why a finite discretization was not mistaken for a
theorem counterexample. The current proof is
[Claim 1: threshold-escape counterexample](#/current-claim-1-threshold-escape).

The precommitted route used the exact one-dimensional paper estimator on the
Rademacher target with `N=256..16384`, 16 seeds, 8,192 generated samples per
seed, 768 Euler steps, and exact one-dimensional empirical W1.

| Diagnostic | Result |
| --- | ---: |
| log-log W1 slope | `+0.1374785` |
| W1 at `N=256` | `19.2908` |
| W1 at `N=4096` | `32.3120` |
| W1 at `N=16384` | `33.5469` |
| half/canonical/long horizon W1 at `N=4096` | `0.6772 / 34.6405 / 1418.3155` |
| standard-normal-score control W1 | `0.5374` |
| precommitted checker | exit `1`, as required for rejection |

W1 increased with `N`, horizon amplification was severe, and step refinement
was unstable. Finite Euler failure may be caused by discretization and cannot
falsify a continuous-time theorem. The later exact integrating-factor
certificate explains the amplification without relying on this route.

- [Rejected raw JSON](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_route2_reverse_sde/rejected_raw_results.json)
- [Rejected-attempt record](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_route2_reverse_sde/rejected_attempt.md)
- [Rejected checker output](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/.openresearch/artifacts/claim1_route2_reverse_sde/rejected_checker_output.json)
- [Executable route](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/src/claim1_faithful_reverse_sde.py)
- [Precommitted checker](https://huggingface.co/spaces/DineshAI/repro-L5JTAPUdbQ-diffusion-low-dimensional-distributions/blob/main/verifiers/verify_claim1_faithful_reverse_sde.py)
