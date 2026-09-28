# Reproduce the paper and computations

## Python checks

Python 3.10 or later and its standard library suffice. No installation command,
network access, solver, symbolic algebra library or prime dataset is needed.

From the repository root:

~~~console
python -B scripts/verify.py
python -B -O scripts/verify.py
~~~

Each invocation checks this package's byte inventory, executes the mathematical
companion, runs 17 companion tests and four package controls, and checks the
two corollaries with exact arithmetic and direct enumeration of 7,626 pairs.
Those additional controls support the written deductions and use no new
certificate file. A nonzero
exit status is a failure. The two companion receipts must be byte-identical.
The verifier reports 51,752 exact polynomial-grid equalities, 38,784 stored
integer coefficients and 460 finite boundary fractions. These are different
counts of evidence, not 91,000 independent tests.

For direct access:

~~~console
cd companion
python -B verify.py
python -B -O verify.py
python -B -m unittest -v test_companion
python -B -O -m unittest -v test_companion
~~~

Do not redirect outputs into the companion or repository tree. The exact
inventory permits only version-control metadata, Python bytecode caches, and
the root build/ output directory as exclusions. Copy the repository to a new
location and repeat the same commands to check independence from its location.

## PDF

paper/Covariance_Signs_for_Residue_Class_Occupancy.tex is a standalone source with an inline bibliography.
Use an existing LaTeX installation with the packages listed in its preamble.

~~~console
python -B scripts/build_pdf.py --check
~~~

The helper copies the source into an empty temporary directory, sets
SOURCE_DATE_EPOCH=1790373600, and runs pdflatex twice with shell escape disabled.
For MiKTeX it also disables automatic package installation. The --check option
compares the result byte for byte with the distributed PDF; any difference
returns a nonzero exit status. Without --check, the result is saved under
build/Covariance_Signs_for_Residue_Class_Occupancy.pdf for inspection.

The recorded toolchain is MiKTeX pdfTeX 4.23.0 (pdfTeX 1.40.28). Fixed-epoch
rebuilds were checked with that installed environment. Fonts, packages and
engine versions can change bytes or page layout; no cross-toolchain byte
identity is promised. The epoch fixes metadata, not the scientific content.
The helper does not install software.

## Evidence limits

The proof derives degree bounds and positivity conditions. Exact finite
interpolation certifies the corresponding polynomial identities. The written
arguments that connect those identities to the theorem remain reviewable
mathematics, not consequences of a checksum or a successful test alone.
