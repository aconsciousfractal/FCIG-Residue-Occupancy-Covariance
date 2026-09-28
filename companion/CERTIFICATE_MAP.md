# Certificate-to-proof map

The mathematical definitions and degree arguments are in the manuscript, not inferred from checker output. The two central statements are the decimal sign classification (Theorem 1) and the abstract three-row criterion (Theorem 2). The additional small-modulus proposition permits cutoffs congruent to 10 modulo 30.

| Proof component | Certificate | Checker | Identity or finite domain |
|---|---|---|---|
| Intermediate bands, ell = 3,...,16 | `certificates/band_03.json` through `band_16.json` | `band_check.py:check_one` | All eight unit residues modulo 30, both formal band endpoints, every Bernstein index |
| Three-row urn increment | `certificates/urn_monotonicity.json` | `urn_check.py:check_all` | All 15 triples (0,p,r), 0 <= p <= r <= 4 |
| Six oriented column anchors | `certificates/column_anchors.json` | `urn_check.py:check_all` | (4,4,4), (4,4,5), (4,5,5), (4,5,6), (4,6,6), (6,6,8) |
| Small decimal depth | `certificates/depth2.json` | `band_check.py:small_depth` | N=100; q=7,11,13,17,19,23; all 41 cardinalities |
| Extended small cutoffs | `certificates/small_cutoffs.json` | `urn_check.py:check_all` | (N,q)=(250,7),(280,7); all 101+113 cardinalities |
| Matching window and examples | No stored certificate needed | `math_checks.py` | Independent finite checks; the uniform proof and period count are written out |

## Exact encoding

All coefficients are arbitrary-precision JSON integers in ascending powers of the shifted parameter. For a band, `negative_scaled_B_at_shift_plus_y` is the coefficient list of **minus** `scale` times the corresponding Bernstein coefficient at `a=132+y`. Its Bernstein degree is J and its parameter degree is J+D-1. For the urn and anchor files, `coefficients[i][h]` multiplies `y^h` in `sign*scale*B_i(shift+y)`. Thus the reconstructed Bernstein coefficient is `sign/scale` times that polynomial. The urn sign/shift are +1/16; the anchor sign/shift are -1/40. Every scale is a positive integer. Arrays have their full declared length, including zero padding.

The common factor removed from raw polynomials is k(k-1). It is certified by equality of the full raw polynomial with k(k-1) times the encoded polynomial; it is not assumed from integer probability samples. The grids are rational and include endpoints.

| Family | Raw parameter degree | Raw x degree | Parameter samples | x samples | Total exact identities |
|---|---:|---:|---:|---:|---:|
| Band | J+D+1 | J+2 | J+D+2 | J+3 | 47,696 |
| Urn profile (0,p,r) | r+5 | r+3 | r+6 | r+4 | 890 |
| Anchor | J+D | J+2 | J+D+1 | J+3 | 3,166 |

Parameter nodes start at the corresponding shift and increase by one. For raw x degree e, nodes are j/e, j=0,...,e. Band counts include eight residues and two endpoints. There are 35,664 band integers, 490 urn integers and 2,630 anchor integers. The 19 normalized column types and the oriented exceptional shape are checked by finite enumeration in addition to the written arguments. Direct hypergeometric comparisons check the algebra-to-probability conversion on finite inputs, without replacing the global identity proof.

The matching table, deterministic zeros, denominator positivity, Schur-convexity argument, valid intermediate urn domains and periodic column reduction remain mathematical obligations in the text. A PASS receipt alone does not certify arbitrary modifications to those arguments.

