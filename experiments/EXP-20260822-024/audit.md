# EXP-20260822-024 audit

## Pre-endpoint gate

**GO.** The sealed candidate census, design receipt, selection seal, and
manifest were verified before endpoint parsing. The metadata-only audit
recomputed `1,290` source/model rows from `1,292` eligible screens, Avana `975`
and KY `315` source/model units, status counts `86/889` and `33/282`, mixed-
lineage counts `17/11`, the canonical roster SHA-256, and planning powers
`0.8433` and `0.5120`. The endpoint file hash and exact `KMT2C (58508)` header
identity were verified before values were parsed.

The candidate was selected because it had the strongest fresh two-source
metadata balance and direct emerging CRISPR evidence. Avana planning power was
adequate, but KY was below the confirmatory threshold, so no T2 label was
possible before endpoint access.

## Post-execution checks

**GO.** The post-execution audit verified:

- exact five-file canonical result set and row counts;
- all non-summary artifact SHA-256 values;
- normalized summary and pre-endpoint receipt digests;
- independent source-specific delta, pair-count, permutation, bootstrap, and
  lineage-delta recomputation;
- runner `validate_staged` result;
- terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The independent recomputation matched Avana delta `-0.1779171894604768` and KY
delta `+0.10040160642570281`, including all pair counts, p-values, bootstrap
intervals, and contributing-lineage deltas. No pooling or lineage rescue was
used.

The full repository suite passed: `126` tests.

## Claim decision

EXP024 is released only as a T1 descriptive feasibility result. It does not
support a general KMT2D/KMT2C dependency claim, a pan-cancer extension of the
emerging lymphoma result, or any functional, inhibitor, treatment, or clinical
claim.
