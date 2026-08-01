# Campaign command ledger

No research computation ran on the local machine. Local commands were limited
to repository/ledger inspection, Git editing and commits, hashing text
artifacts, and OpenResearch/Hugging Face orchestration.

## Startup and source audit

```sh
orx skill
orx skill orx-experiment-tree
orx skill orx-evidence
orx skill orx-git
orx skill orx-compute
orx projects --json
git branch --show-current
git rev-parse HEAD
git status --short
df -h .
curl -sL -A "Mozilla/5.0" "https://ar5iv.labs.arxiv.org/html/2605.30153" -o paper.html
```

Authenticated HF read operations used the Python API with `get_token()` passed
explicitly. The token was never printed or placed on a command line. Those
operations listed protected/running jobs, fetched the exact-space verdict,
downloaded revision `fe1fd273934cf8568fbcc1187d857e7662313648`, and verified
its 21-file SHA-256 manifest.

## Fixed command executed by every experiment node

```sh
./scripts/bootstrap_reproduction.sh && ./.venv/bin/python scripts/validate_release.py && ./scripts/run_full_poster_gates.sh
```

The inherited HF submission shape was:

```sh
orx exp run <experiment-id> --backend hf --flavor cpu-upgrade \
  --image ghcr.io/astral-sh/uv:python3.14-bookworm --timeout 30m
orx exp wait <experiment-id> --timeout 60 --interval 10
orx logs <run-id> --bytes <bounded-byte-count>
```

Each child was created with `orx create-experiment <project-id> --parent
<parent-id>`, then its scoped commit was pushed before submission. The project
ID was `17feb5ef-61a1-4317-b0df-a2dac43e08cd`.

## HF run IDs through evaluator Round 2

```text
a1fe10ca-f773-4a4d-8bd3-e41e46877348
ba9cdf2f-754a-4a91-abe8-73ec77d405db
831b732e-b387-4f85-b00b-9096fc826d53
71e51c0f-2023-4b18-bffb-10ed53c8d160
160bf23b-9746-4f3e-b141-7c08f6eaa2c0
1bbdfbc1-3ab4-4b24-a50b-55c18405d322
b1e14ced-5a54-45aa-b81d-508648c87239
8d48a1ba-41d0-42cb-9250-1aa9a50c641a
f6bad546-b9ef-46ae-8a36-a9d6fc64dc41
c8c463cd-93c4-4c0a-b4bb-6ef86f02fddb
166ea628-979c-4c96-a5c1-f5f2e1277df9
e1002fce-0e85-44fd-9dd5-0dfc5ca3ca3e
7c13df18-239c-4a2a-8718-22b711684f30
1aebd211-6e18-4b7d-aba8-facb741ddee0
7331cf71-890b-429f-9858-563f591b57c3
f5848f05-c51d-4b31-8caf-e09f140ad9f5
70f5d228-5ef0-45d6-8938-f6c442eba1d4
19244290-dad3-4ece-bc53-805174dfcd6d
c5a8d7c4-4d7b-4368-bd77-840417fcb435
928f3571-fcb6-4e42-94be-04d8a5f6901e
5e5abf5a-9eec-441a-9ac7-28e0fc94ec04
62ddd189-4616-4bd5-b573-959ba2fbd632
d7372b6a-1b68-46ec-9962-d9fc6c6bd51d
4b29d0fe-6893-436c-95bb-e9f93fad89cb
b21f515c-dddf-4277-b867-ce0987c68f39
0bf1fc1d-4741-4654-a8ee-9b68e66d69c2
9ec85de3-636f-4ecb-ab7b-d2ffc70b6316
```

Several runs have backend status `failed` because the cumulative command
correctly stopped on a later expected poster/release gate. Their scientific
checker status and mutation exits are recorded separately and are never
inferred from the backend label.

## Release preparation

```sh
sha256sum <each allowlisted text path>
orx logs 0bf1fc1d-4741-4654-a8ee-9b68e66d69c2 --bytes 400000
orx logs 9ec85de3-636f-4ecb-ab7b-d2ffc70b6316 --bytes 400000
```

Publication uses the authenticated Hugging Face `create_commit` text path with
`parent_commit=fe1fd273934cf8568fbcc1187d857e7662313648`, followed by an exact
revision download/hash check. GitHub mirroring occurs only afterward via a
fast-forward push to `main` and `git ls-remote` confirmation.
