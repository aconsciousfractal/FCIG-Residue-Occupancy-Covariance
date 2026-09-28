# Reviewer guide

Start with the abstract, Theorems 1 and 2, and the limitations section of the
[paper](paper/Covariance_Signs_for_Residue_Class_Occupancy.pdf). Then follow
[REPRODUCE.md](REPRODUCE.md) and the
[certificate map](companion/CERTIFICATE_MAP.md).

## Mathematical review

- Check the deterministic zero regions and all four exceptional gap families,
  including the depth restriction on gap 19.
- Check the exhaustive coverage of the decimal modulus ranges and the
  transition between band certificates and the small-modulus argument.
- Preserve the orientation of the three-row column vectors and the special
  restriction for the (0,0,2) increment in Theorem 2.
- Check that interpolation grids match the independently derived degrees,
  and that positivity arguments cover their entire stated domains.
- Distinguish the uniform-subset local-sieve identity from any sampling law
  for actual primes.

The bibliography describes the frameworks and comparisons used. No exhaustive
novelty certification or formal proof-assistant verification is claimed.

## Reproducibility review

The package has no dependency on private dossiers, source ZIPs or prime
datasets. All 18 certificate files and all mathematical checker kernels are
preserved from the reviewed precursor; documentation and preparation statements
were adapted for readers. Read AI_USE.md for the review boundary.

Run both Python modes, inspect rejection tests, rebuild the PDF with the
documented fixed epoch, and check source/PDF consistency. MANIFEST.json detects
drift against this package; it is not an authenticated signature.

## Two derived corollaries

Check both exact polynomial divisions and the finite remainder cases in
Corollary 11; the large-depth exclusion uses monotonicity, not enumeration.
For Corollary 12 check the one-set identity, positive avoidance probability,
retained orientation restriction and the nonnegative weight condition.
Neither result introduces another certificate family. Review the remaining
gap-1/3 question as an open problem, not a claimed theorem.
