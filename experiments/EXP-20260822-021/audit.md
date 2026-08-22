# EXP-20260822-021 audit

## Pre-endpoint gate

**GO.** The sealed candidate census, design receipt, selection seal, and
manifest were verified before endpoint parsing. The exact metadata audit
recomputed `1,292` eligible screens, Avana `975` and KY `315` source/model
units, status counts `57/918` and `21/294`, mixed-lineage counts `15/9`, the
canonical roster SHA-256, and design powers `0.7173` and `0.4028`. The endpoint
file hash and exact `PTPN11 (5781)` header identity were verified before values
were parsed.

The independent metadata scout returned NF1→PTPN11 as the recommended
remaining candidate and explicitly noted the KY feasibility-only ceiling. A
second read-only code reviewer timed out before returning; it was closed
without editing files or accessing endpoint values. The local boundary audit
was the decisive pre-endpoint implementation check.

## Post-execution checks

**GO.** The post-execution audit verified:

- exact five-file canonical result set and row counts;
- all non-summary artifact SHA-256 values;
- normalized summary and pre-endpoint receipt digests;
- independent source-specific delta, pair-count, and lineage-delta
  recomputation;
- runner `validate_staged` result;
- terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The independent recomputation matched Avana delta `-0.24936294139060794` and
KY delta `+0.046153846153846156`, including both pair counts and all
contributing-lineage deltas. The full repository suite passed at `111` tests.

No source pooling, lineage exclusion, threshold change, or rescue is allowed.

## Claim decision

EXP021 is released only as a T1 descriptive feasibility result. It does not
establish a general NF1/PTPN11 dependency, functional NF1 biology, inhibitor
response, or clinical utility.
