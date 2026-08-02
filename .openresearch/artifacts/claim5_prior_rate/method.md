# Method

Let `D=d+2 beta`. The independent certificate reconstructs the polynomial-rate
part of the Cai-Li proof from its antecedent terms:

1. The theorem selects `tau=n^(-2/D)`.
2. The leading squared score-error exponent is
   `-1+d/D=(-D+d)/D=-2 beta/D`.
3. Taking the square root gives score-error exponent `-beta/D`.
4. The Holder early-stopping term has exponent
   `(-2/D)(beta/2)=-beta/D` for `beta<=2`.
5. The iteration premise makes the discretization term no larger at polynomial
   order. The triangle inequality therefore retains `n^(-beta/D)`.
6. Solving `n^(-beta/D)=epsilon` gives sample exponent `D/beta`.
   Its derivative with respect to ambient dimension is `1/beta>0`.

The checker extracts the assumption, theorem, and proof markers directly from
the three pinned source archives, verifies their SHA-256 hashes, performs the
coefficient identities exactly with rational arithmetic, and checks 20 exact
`(d,beta)` instantiations. A mutation replacing one derived sample exponent by
`999` must make the independent checker exit nonzero.

The Cai-Li proof contains a transparent typographical omission: one simplified
Jacobian-error display drops the leading `n^(-1/2)`. Its immediately preceding
unsimplified expression retains that factor and simplifies to
`n^(-beta/D)`, which is also the exponent used on the next proof line. The
certificate derives from the unsimplified antecedent and records this deviation.
