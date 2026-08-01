# Claim 2: intrinsic score-error rate


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_bd00f42e3885", "created_at": "2026-08-01T06:47:49+00:00", "title": "Outcome: inconclusive after full-scale numerical protocol and controls"}
-->
## Outcome: inconclusive — full-scale numerical protocol and controls complete

The prior source audit is not treated as a scoreable reproduction. A clean-room streaming implementation of Equations (8)–(14), with independently derived analytic Gaussian-mixture-smoothed score, executed the paper's literal synthetic configuration: `d=48`, `M=128`, `k=3`, `N=50,000`, and 10,000 held-out `p_t` samples. It never materializes a query×training×48 tensor. Full scale has 20 independent training datasets at each new time cell and 21 exact-compatible prior datasets at `t=.25`: mean MSE is **10.38185** at `.1` (95% CI `[10.33624,10.42745]`), **3.69597** at `.25` (`[3.67692,3.71501]`), **1.49812** at `.5` (`[1.49012,1.50613]`), and **.58816** at `1.0` (`[.58489,.59143]`). Raw arrays, rows, commands, timings, and checksums are retained in `outputs/claim2_fullscale/` and `outputs/claim2_fullscale_grid/`; `mse_vs_t.svg` is derived directly from those summaries.

The required controls were executed rather than assumed. At `.25`, deliberately permuting recovered bases yielded MSE **3.08039** (`n=20`, `[3.06933,3.09146]`), and the full-ambient component-KDE diagnostic yielded **3.64899** (`n=10`, `[3.64552,3.65246]`). The reduced-N diagnostics (`n=10` each) gave MSE **3.06009**, **3.36195**, and **3.55108** for `N=6,250`, `12,500`, and `25,000`. These controls do **not** show the documented expected degradation (indeed the permuted/reduced controls have lower MSE), so this evidence cannot honestly verify the claimed intrinsic-rate behavior or be used to falsify the theorem. Verdict remains **inconclusive** pending independent review and a source/protocol audit explaining the discrepancy. All controls are retained in `outputs/claim2_controls/`, including raw NPZs, `results.csv`, `summary.json`, `mse_vs_N.svg`, command log, and `SHA256SUMS`.
