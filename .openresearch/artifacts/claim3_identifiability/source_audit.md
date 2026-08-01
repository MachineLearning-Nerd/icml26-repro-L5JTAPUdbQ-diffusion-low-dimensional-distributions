# Claim 3 source audit

- Primary HTML: https://ar5iv.labs.arxiv.org/html/2605.30153
- Retrieved: 2026-08-01T14:48:25Z with explicit `Mozilla/5.0` user agent
- HTML SHA-256: `d2577722849d961902b3a8942036623342b96cbeb3c8607d74eae649680324f4`
- Assumption 1 anchor: `#Thmassumption1`
- Assumption 2 anchor: `#Thmassumption2`
- Exact-recovery lemma anchor: `#Thmlemma3`; source file Appendix B.1

Assumption 1 requires only support containment in declared subspaces, zero mass
on pairwise intersections, and component mass at least `1/(c_p M)`. It does not
require the conditional support on `V_i` to span `V_i`, have a density on
`V_i`, or be non-degenerate in every tangent direction.

Appendix B.1 nevertheless claims exact recovery under Assumption 1 alone. Its
key step sets the probability of a sample falling in the intersection of a
declared subspace and an arbitrary span of prior samples to zero. The stated
assumption supplies zero mass only for intersections between two declared
subspaces, so that inference is not valid for arbitrary sample spans.
