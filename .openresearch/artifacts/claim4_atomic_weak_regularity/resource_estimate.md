# Claim 4 resource estimate

- Useful cores estimated before run: `8`
- Selected HF flavor: `cpu-upgrade`
- Expected allocation: `8 vCPU`, `32 GB RAM`, no accelerator
- Expected scientific runtime: `5-20 minutes`
- Work: 20 seeds, 4 sample sizes, 10,000 queries, 768 exact atoms
- Timeout: `30 minutes`
- Rate: `$0.0005/minute`

Duplicate training atoms are aggregated exactly, reducing memory and runtime
without changing the paper's empirical KDE.
