# Historical rejected baseline: Claim 1 Euler attempt

Run `7331cf71-890b-429f-9858-563f591b57c3`, HF job
`DineshAI/6a6e1fc96b79c09949c1e704`, Git `422b728`.

The precommitted verifier exited nonzero. Mean W1 increased from `19.2908` at
`N=256` to `33.5469` at `N=16384` (slope `+0.13748`). At `N=4096`, horizon
factors `0.5,1,1.5` gave mean W1 `0.6772,34.6405,1418.3155`. The
standard-normal-score control was `0.5374`. Step refinement was not stable.

These results are not a numerical falsification because the discretization did
not converge. They motivated the independent continuous-time threshold-escape
certificate, which supersedes this page as the current verifier.
