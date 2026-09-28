# Reproduction record

Version 1.0.0-rc4 accompanies the 15-page manuscript. Its 18 certificate files
retain the supplied bytes, and the original companion arithmetic is unchanged.

The tested local environment is Python 3.14.6 and MiKTeX pdfTeX 4.23.0
(pdfTeX 1.40.28), with SOURCE_DATE_EPOCH=1790373600. The documented Python
syntax requires 3.10 or later; separate runs on every supported version
have not been performed. No third-party Python dependency is required.

The complete verification command runs 17 companion tests, four package
controls, all certificate identities, and exact checks of the added
corollaries. The latter include both polynomial divisions, six nonzero
remainders, the discriminant identity, and direct enumeration of 7,626
pairs for an actual overlapping family with weights 2 and 3.

Normal and optimized candidate verification produced identical receipts. The clean
PDF build checks exact bytes against the distributed PDF. Byte identity is
specific to the recorded toolchain; other installations may differ.

MANIFEST.json covers every payload plus MANIFEST_SHA256.txt, excluding itself.
MANIFEST_SHA256.txt lists the payloads excluding both manifest files, avoiding
a circular digest definition. The entry point checks that the two inventories
agree. Neither file is an authenticated signature.

The written proofs supply the uniform conclusions. Arithmetic controls,
AI-assisted readings and local computational replays do not establish
human peer review, novelty or a sampling law for actual prime patterns.
