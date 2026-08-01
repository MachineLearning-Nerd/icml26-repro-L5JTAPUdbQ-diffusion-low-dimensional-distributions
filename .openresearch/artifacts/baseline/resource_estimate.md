# Baseline resource estimate

- Run purpose: install the locked environment, execute the repository's current
  tests and release validator, and run the pinned poster gates once before any
  scientific child variants.
- Estimated useful cores: 8. Test collection contains mostly single-process
  Python work, while dependency installation, browser setup, and poster tooling
  can use parallel CPU and I/O; the fixed HF flavor is the smallest authorized
  `cpu-upgrade` allocation.
- Selected flavor: Hugging Face `cpu-upgrade`
- Expected allocation: 8 vCPU, 32 GB RAM, 50 GB storage, no accelerator
- Timeout: 2 hours
- Estimated runtime: 10--30 minutes
- Estimated cost: $0.005--$0.015 at $0.0005/minute

Actual allocation, elapsed runtime, terminal status, and computed cost will be
recorded from the HF job after completion.

## Infrastructure attempt 1

- HF job: `DineshAI/6a6e0aa1a00abefd4b28b8b8`
- Run: `a1fe10ca-f773-4a4d-8bd3-e41e46877348`
- Result: setup failure after 21 seconds, before tests or research computation
- Cause: exact Python 3.14.6 was unavailable in the selected container
- Cost at listed rate: approximately $0.000175
- Repair: select the installed Python 3.14 patch while retaining the same
  Python minor line and unchanged hash-locked dependency graph; print the
  actual patch and allocated core count in every bootstrap log.

## Infrastructure attempt 2

- HF job: `DineshAI/6a6e0bc0a00abefd4b28b8c6`
- Run: `ba9cdf2f-754a-4a91-abe8-73ec77d405db`
- Result: collection failure after 37 seconds; no tests executed
- Resolved runtime: Python 3.14.2 with all 36 locked third-party packages
- Cause: the historical `pytest` console entrypoint did not add the repository
  root to its import path in this container
- Cost at listed rate: approximately $0.000308
- Repair: invoke the same suite as `python -m pytest`; record cgroup and CPU
  affinity limits instead of the misleading host-wide processor count.
