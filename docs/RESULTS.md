# Results and proof dependencies

The random set is always a uniformly sampled fixed-size subset.

| Result | Domain and conclusion | Proof and certificate dependence |
| --- | --- | --- |
| Theorem 1 | Decimal carrier, d >= 2, q positive and coprime to 30; every sample size | Deterministic ranges, matching window, bands and small-modulus reduction |
| Theorem 2 | Three rows (a+2,a+2,a), a >= 40; exact oriented column restrictions | Majorization, urn increment and six anchors |
| Corollary 10 | Prime q >= 7 in the finite uniform-subset model | Affine covariance identity for two local sieve factors |
| Corollary 11 | Gap 7 for d >= 2 and gap 19 for d >= 3 | Two polynomial divisions, monotone size bounds and six nonzero remainders |
| Corollary 12 | Finite family of admissible sets, fixed nonnegative weights with positive total | Single-set inequality from Theorem 2 and linearity; overlaps allowed |

The extra condition for the oriented increment (0,0,2) is b >= 6. The third
coordinate is the shorter row. This restriction is retained in Corollary 12.

Corollaries 11 and 12 add no certificate files. Their proofs are deductive;
scripts/check_corollaries.py supplies exact arithmetic and subset-enumeration
controls. The [certificate map](../companion/CERTIFICATE_MAP.md) specifies the
18 certificate dependencies of the central theorems.

## Limits and open questions

The remaining possible nontrivial integer zeros occur only in gaps 1 and 3.
Their complete exclusion is not proved; the equivalent square equation is
displayed in Section 9.1. Optimal thresholds and proofs without coefficient
certificates are further questions, not missing hypotheses of the results.

No arbitrary signed weights, negative-association theorem, actual-prime
sampling law or full singular-series average is claimed.
