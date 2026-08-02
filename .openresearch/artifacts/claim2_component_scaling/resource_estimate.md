# Claim 2 component-study resource estimate

- Useful cores estimated before run: `8`
- Selected HF flavor: `cpu-upgrade`
- Expected allocation: `8 vCPU`, `32 GB RAM`, no accelerator
- Expected scientific runtime: `2-10 minutes`
- Maximum dense working block: about `256 x 2048` float64 values
- Timeout: `30 minutes`
- Rate: `$0.0005/minute`

The matrix multiplications and kernel evaluations can use all eight allocated
CPU cores. No GPU code path is present.
