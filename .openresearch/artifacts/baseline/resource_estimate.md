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
