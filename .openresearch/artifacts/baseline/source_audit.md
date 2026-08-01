# Source audit: arXiv 2605.30153

- Source: https://ar5iv.labs.arxiv.org/html/2605.30153
- Retrieved: 2026-08-01T14:48:25Z
- Retrieval: `curl -sL -A "Mozilla/5.0"`
- SHA-256: `d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`
- Scope: Sections 1, 2.2, 3.1, 3.2, 5, and 6; Appendices A--C where cited by the theorems.

## Assumptions

Assumption 1 (`#Thmassumption1`) requires the support of `p*` to be contained
in a union of `M` linear subspaces `V_i` of dimensions `k_i`, assigns zero
probability to every pairwise intersection, and lower-bounds each component
mass by `1/(c_p M)`.

Assumption 2 (`#Thmassumption2`) normalizes each subspace restriction and
requires, for every component and every unit direction in that subspace,
`E exp((X^T theta / sigma_i)^2) <= 2`.

## Exact theorem contracts

Theorem 1 (`#Thmtheorem1`) assumes Assumptions 1 and 2, conditions on exact
subspace recovery, takes `t <= N^{O(1)}`, and uses the score estimator in
Equation (14). Its expectation is over the training sample and `X ~ p_t`. It
bounds the integrated squared score error by

`C_score d M^3 / N [1/t + sigma^(k v 2) / t^((k v 2)/2 + 1)] polylog(N)`.

Theorem 2 (`#Thmtheorem2`) assumes Assumptions 1 and 2. For sufficiently large
`n`, it sets `n0 = C_sc M^2 k log(n)`, `N = n - n0`, `T = log(n)`, and
`tau = n^(-2/k)`, and applies Algorithm 1 with the Equation (14) score. Its
expectation is over the training sample. It bounds

`W1(p*, p_hat) <= C d M^(3/2) n^(-1/(k v 2)) polylog(n)`.

The sample-complexity interpretation is therefore sufficient, not necessary:
up to logarithms, `epsilon^(-(k v 2))` samples suffice. The theorem retains a
linear ambient-dimension prefactor.

Equation (1) in Section 1 attributes `epsilon^(-(d+2 beta)/beta)` sample
complexity, up to logarithms, to prior analyses of broad `d`-dimensional
`beta`-Holder smooth densities, in total variation distance.

## Experimental scope and known source limitations

Section 5 studies score MSE rather than end-to-end Wasserstein sampling. It
reports `d=48`, `M=128`, `k=3`, `N=50,000`, 10,000 evaluation samples per
diffusion time, and 20 independent training datasets. The randomized Gaussian
mixture parameters are not fully specified in the paper, so an exact numerical
replication requires author parameters or code. Section 6 leaves reverse-time
SDE/ODE discretization for future work.

Finite experiments can corroborate but cannot prove the universally quantified
Theorems 1 and 2. A final `VERIFIED` result for those theorems therefore
requires a machine-checkable proof certificate or independently reconstructed
derivation; `FALSIFIED` requires an assumption-satisfying counterexample to the
exact quantified statement.
