# Claim 2 alternate proof-dependency route

## Scope

This route is a local-CPU, analytic `d=6, M=3, k=2` Gaussian-mixture diagnostic. It is deliberately not the completed `d=48, M=128` grid and does not assert a theorem outcome. The positive arm conditions the estimator on the known correct labels and bases, exactly matching the theorem's *conditional exact-subspace-recovery* premise. The cyclically wrong-basis arm uses identical data/seeds and intentionally violates that premise.

## Primary-source mapping

The pinned archive is `evidence/source/arxiv_source.tar` (validated by `evidence/source/SHA256SUMS`).

* `Results.tex:135-150` states Theorem 1: conditional on exact recovery, its target is the training-and-query expectation, and the bound has `d M^3/N` times `1/t + sigma^(k vee 2)/t^((k vee 2)/2+1)`, up to `C_score polylog N`.
* `pf-of-theorems.tex:6-19` defines the per-component count event `A`, with `N_i >= N/(2 c_p M)` and its `M exp(-N/(2 c_p^2 M^2))` complement bound.
* `pf-of-theorems.tex:21-31` applies Cauchy--Schwarz to create the outer component-count factor and separates mixture-weight (`L_i,1`) from conditional component-score (`L_i,2`) error.
* `pf-of-theorems.tex:34-123` supplies the bounded-tail/KDE (`B_t`, `kappa_1..3`) terms, and `:126-140` supplies the mixture-weight term and combines them to `d M^3/(N t) (1 + sigma^(k vee 2)/t^((k vee 2)/2))`, hiding constants/polylogs.
* `pf-of-theorems.tex:143-160` adds the `A^c` tail and gives the summary equivalent to Theorem 1.

## Checked algebra and interval/count obligations

For `N=1800, M=3, k=2, t=.6, sigma=1`, `proof_checks.json` verifies:

`(1/t)(1 + sigma^q/t^(q/2)) = 1/t + sigma^q/t^(q/2+1)`, with `q=k vee 2=2`, to absolute error `8.88e-16`. It also records the exact-recovery component threshold `N/(2M)=300` for equal weights (`c_p=1`) and the source Chernoff upper bound `3 exp(-1800/(2*3^2)) = 1.116e-43`. These checks only validate displayed algebra and a numerical premise bound; they do not determine hidden constants or polylog factors.

## M>1 analytic fixture and controls

Three equal-weight Gaussians lie on disjoint coordinate 2-planes in `R^6`; after VE smoothing by `t=.6`, the mixture score is evaluated analytically using the Woodbury inverse of `A A^T + t I`. The estimator uses the source-style hard-threshold KDE component score, normal score, and ambient Gaussian-kernel mixture weights. Three fixed seeds (`171,172,173`) each share training/query samples between exact-recovered and cyclic-wrong-base arms. `results.csv` stores all raw rows and standard errors; `summary.json` reports only descriptive finite MSEs.

The fixture demonstrates that this implementation separates its known-basis premise from an intentionally wrong-basis control. It cannot estimate the theorem's full expectation or establish its unspecified constant/polylog bound; its required verdict is **inconclusive**.
