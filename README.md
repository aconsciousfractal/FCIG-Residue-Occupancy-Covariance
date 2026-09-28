# Covariance Signs for Residue-Class Occupancy on Decimal Unit Carriers

**Oleksiy Babanskyy** · [ORCID](https://orcid.org/0009-0001-6176-6208)

For a uniformly chosen fixed-size subset of the integers below a power of ten
that are coprime to ten, how do the numbers of occupied residue classes modulo
3 and modulo q vary together? This article determines the sign of their
covariance throughout its stated domain.

- [Paper](paper/Covariance_Signs_for_Residue_Class_Occupancy.pdf) and [LaTeX source](paper/Covariance_Signs_for_Residue_Class_Occupancy.tex).
- [Reviewer guide](README_REVIEWER.md).
- [Reproduction instructions](REPRODUCE.md) and [certificate map](companion/CERTIFICATE_MAP.md).
- [Preparation and AI assistance](AI_USE.md), [distribution terms](LICENSE_SCOPE.md)
  and [citation metadata](CITATION.cff).

## Main results

1. A complete sign classification for decimal carriers, every modulus q coprime
   to 30, and every allowed sample size. Apart from deterministic zero cases,
   the covariance is negative except in four families near half the carrier
   endpoint. Those exceptional families have explicit quadratic sign formulas.
2. A sufficient negative-covariance criterion for a general three-row partition.
   Its hypotheses include the column orientation and a special lower bound
   for one oriented column type; the statement is not claimed to be sharp.

The proofs combine exact probability identities, monotonicity arguments and
18 exact certificate files: 16 polynomial certificates and two files of
finite boundary checks. The companion reconstructs the identities with integer
and rational arithmetic using only Python's standard library.
See Theorems 1 and 2 for the complete hypotheses; this overview does not
replace them.

Two short consequences make the scope more explicit: the exceptional gaps
7 and 19 never have a nontrivial integer zero; the three-row argument also
controls nonnegative weighted sums of occupancies of admissible overlapping
sets. These are Corollaries 11 and 12, derived from the two main theorems.

See the [results map](docs/RESULTS.md) and [source notes](docs/SOURCES.md).

## Relation to primes

The prime motivation yields a precise corollary about two local sieve-survival
proportions. The random object here is a **uniform subset of a finite carrier**.
The paper does not establish a distribution law for actual prime patterns,
prime prediction, or control of the full product of local factors.

## Verify

With Python 3.10 or later, from the repository root:

~~~console
python -B scripts/verify.py
python -B -O scripts/verify.py
~~~

Each command checks the package inventory, replays the exact companion,
runs its 17 tests (16 negative controls and one positive inventory control),
and runs four package-integrity controls plus the exact corollary checks.
Normal and optimized companion
receipts must agree. Run these commands from a clean copy without saving
additional files inside it.

The checks support the written computer-assisted proof. They do not establish
novelty or replace scrutiny of the proof's domains and reductions. This version
identifier identifies the files; it does not imply a published release,
journal acceptance or human peer review.

## Repository layout

| Path | Contents |
| --- | --- |
| paper/ | Complete English manuscript source and title-named PDF |
| companion/ | 18 exact certificates and unchanged mathematical verification |
| scripts/ | Complete verification, corollary checks and clean PDF build |
| tests/ | Package-integrity rejection controls |
| docs/ | Results, hypotheses, dependencies and source comparison |
| MANIFEST.json / MANIFEST_SHA256.txt | Exact distributed file identities |

Companion version **1.0.0-rc4**. The [reproduction record](REPRODUCTION_RECORD.md)
states the environment and checks performed. The version denotes these files;
no DOI, journal acceptance or public release is implied.
