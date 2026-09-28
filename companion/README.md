# Exact companion: residue-class occupancy covariance

This folder accompanies *Covariance Signs for Residue-Class Occupancy on Decimal Unit Carriers* by Oleksiy Babanskyy. It contains 18 exact certificate files, three mathematical checkers, an entry point and 17 unit tests (16 negative controls and one positive inventory check). No prime dataset, source archive, symbolic algebra package or internal dossier is needed.

## Run

Use Python 3.10 or later with only its standard library. From this directory:

```console
python -B verify.py > /path/outside/repository/receipt.json
python -B -O verify.py > /path/outside/repository/receipt_optimized.json
python -B -m unittest -v test_companion
python -B -O -m unittest -v test_companion
```

Save receipts **outside this directory** (replace the example destinations accordingly), because the integrity check rejects unlisted files. The verifier itself writes nothing. The two verification receipts must be byte-identical. A successful run prints a JSON object with `status: PASS`, 51,752 exact polynomial-grid equalities, 38,784 stored integer coefficients and 460 finite boundary fractions. Exceptions or a nonzero exit status mean failure. Sixteen negative controls deliberately omit or corrupt cases and must reject them even under optimized Python; the mathematical checkers do not rely on `assert`.

The simplest clean-copy replay is to copy this entire folder elsewhere and run these commands with receipt destinations outside the copy. The manuscript is a separate standalone LaTeX source at `../paper/Covariance_Signs_for_Residue_Class_Occupancy.tex`; it is not read by the mathematical verifier.

## What is proved by the computation

The written proof derives explicit polynomial degree bounds. The checkers independently reconstruct the finite column geometry and the raw polynomials, then compare their exact rational values with the certificate polynomials on complete interpolation grids. The elementary root bound promotes those finite comparisons to polynomial identities. Signs follow from nonnegative power coefficients with strictly positive constants in Bernstein coefficients. This is a computer-assisted proof with auditable integer and rational arithmetic, not a proof-assistant formalization.

`CERTIFICATE_MAP.md` gives the exact roles, dimensions and conventions. `MANIFEST.json` records every distributed file except itself. Its hashes detect accidental drift; they do not authenticate a trusted issuer. `PROVENANCE.json` identifies the original author-supplied ZIP members. Certificates are byte-preserved. The adapted checkers retain their mathematical kernels and derive degree bounds independently of the certificate declarations. They do not import the symbolic generators. The new direct checker is an additional implementation of the finite probability formula.

## Limits

The results concern uniform fixed-size subsets, not observed prime sets. For prime moduli the occupancy counts determine exact local sieve factors; passing to actual prime frequencies or a full singular-series average requires additional work. The sufficient three-row criterion is not claimed to be sharp, and its special oriented column restriction cannot simply be discarded.

Preparation details and distribution terms are recorded in the repository's AI_USE.md and LICENSE_SCOPE.md.
