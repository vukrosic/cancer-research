# EXP-20260822-023 audit

## Pre-endpoint gate

**GO.** The sealed candidate census, design receipt, selection seal, and
manifest were verified before endpoint parsing. The metadata-only audit
recomputed `1,290` source/model rows from `1,292` eligible screens, Avana `975`
and KY `315` source/model units, status counts `54/921` and `30/285`, mixed-
lineage counts `11/5`, the canonical roster SHA-256, and planning powers
`0.5184` and `0.2861`. The endpoint file hash and exact `TDO2 (6999)` header
identity were verified before values were parsed.

The candidate scouts reviewed distinct directions without opening endpoint
values and selected APC→TDO2 because it met the frozen minimum in both source
families and had direct genetic/isogenic literature support. The KY mixed-
lineage count is exactly at the floor, and both source powers forced a
permanent feasibility-only label.

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

The independent recomputation matched Avana delta `-0.12317880794701987` and
KY delta `+0.49216300940438873`, including all pair counts, p-values,
bootstrap intervals, and contributing-lineage deltas. The source families
disagreed in direction; no pooling or rescue was used.

The full repository suite passed: `121` tests.

## Claim decision

EXP023 is released only as a T1 descriptive feasibility result. It does not
support a cross-source APC/TDO2 dependency claim, and it does not invalidate
the published mechanistic APC/TDO2 results in their own experimental systems.
No functional-APC, WNT-causal, inhibitor-response, treatment, or clinical claim
is permitted.
