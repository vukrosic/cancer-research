# EXP-20260822-022 audit

## Pre-endpoint gate

**GO.** The sealed candidate census, design receipt, selection seal, and
manifest were verified before endpoint parsing. The metadata-only audit
recomputed `1,290` source/model rows from `1,292` eligible screens, Avana `975`
and KY `315` source/model units, status counts `61/914` and `34/281`, mixed-
lineage counts `18/11`, the canonical roster SHA-256, and planning powers
`0.7401` and `0.4984`. The endpoint file hash and exact `CREBBP (1387)` header
identity were verified before values were parsed.

The candidate scout reviewed distinct remaining directions without opening
endpoint values and selected EP300→CREBBP on two-source metadata balance,
lineage coverage, and primary CRISPR literature support. The design was sealed
as permanently feasibility-only because both source powers were below `0.80`.

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

The independent recomputation matched Avana delta `-0.4171511627906977` and KY
delta `-0.4767932489451477`, including all pair counts, p-values, bootstrap
intervals, and contributing-lineage deltas. Both sources failed only the
no-positive-lineage gate among the substantive gates; the aggregate signal was
not upgraded or rescued.

The full repository suite passed: `116` tests.

## Claim decision

EXP022 is released only as a T1 descriptive feasibility result. It supports no
general EP300/CREBBP dependency claim, functional EP300-loss claim, paralog-
causal claim, inhibitor response, treatment, or clinical claim.
