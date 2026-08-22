# EXP-20260822-026 audit

## Pre-endpoint gate

**GO.** The sealed candidate census, design receipt, selection seal, and
manifest were verified before endpoint parsing. The metadata-only audit
recomputed `1,290` source/model rows from `1,292` eligible screens, Avana
`975` and KY `315` source/model units, status counts `94/881` and `38/277`,
mixed-lineage counts `19/11`, the canonical roster SHA-256, and planning powers
`0.8526` and `0.5377`. The endpoint file hash and exact `PAPSS1 (9061)` header
identity were verified before values were parsed.

The candidate was selected because it directly tests the reported patient
translation gap for PAPSS1/PAPSS2 collateral lethality. KY planning power was
below the confirmatory threshold, so no T2 label was possible before endpoint
access.

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

Independent recomputation matched Avana delta `-0.03214552703712933` and KY
delta `+0.2073976221928666`, including all pair counts, p-values, bootstrap
intervals, and contributing-lineage deltas. No pooling or patient-proxy rescue
was used.

The full repository suite passed: `136` tests.

## Claim decision

EXP026 is released only as a T1 descriptive feasibility result. It does not
support a general PTEN/PAPSS1 dependency claim, a PTEN/PAPSS2 collateral-
lethality claim in patients, or any mechanistic, inhibitor, treatment,
clinical, or confirmatory claim.
