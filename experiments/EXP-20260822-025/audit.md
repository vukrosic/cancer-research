# EXP-20260822-025 audit

## Pre-endpoint gate

The first boundary attempt stopped before endpoint parsing because the loader
threshold orientation was inverted for the metadata-only status orientation;
KY was incorrectly rejected at T0. No PELO value was read and no result
directory was created. The mapping was corrected in implementation commit
`d491092b63cb508c67cccd6f10276b7b914b1cb0`, the manifest was rebound at
`1e40976edff11264f40b047d7fd958b5b8475963`, and the complete pre-endpoint
audit was rerun.

**GO after remediation.** The corrected audit verified the sealed candidate
census, design receipt, selection seal, manifest, input hashes, exact
`1,290`-row canonical roster, `1,292` eligible screens, Avana/KY source-model
counts `975/315`, status counts `110/865` and `37/278`, mixed-lineage counts
`19/11`, planning powers `0.8958/0.5265`, and the exact `PELO (53918)` header
before any endpoint value parse.

## Post-execution checks

**GO.** The post-execution audit verified:

- exact five-file canonical result set and row counts;
- all four non-summary artifact SHA-256 values;
- normalized summary and pre-endpoint receipt digests;
- independent source-specific delta, pair-count, permutation, bootstrap, and
  lineage-delta recomputation;
- runner `validate_staged` result;
- terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

Independent recomputation matched Avana delta `-0.15800121383775034` and KY
delta `-0.057692307692307696`, including all pair counts, p-values, bootstrap
intervals, and contributing-lineage deltas. No pooling or proxy rescue was
used.

The full repository suite passed: `131` tests.

## Claim decision

EXP025 is released only as a T1 descriptive feasibility result. It does not
support a general CDKN2A/PELO dependency claim, a 9p21.3/FOCAD or MSI-H claim,
or any mechanistic, inhibitor, treatment, clinical, or confirmatory claim.
