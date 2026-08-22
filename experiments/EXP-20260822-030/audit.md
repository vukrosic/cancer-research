# EXP030 audit

## Pre-endpoint gate

**GO after correction.** The first execution stopped at `T0_CONTEXT_ADEQUACY`
before endpoint access because the planning receipt reused EXP029's power
values under new EXP030 seeds. The preserved `t0_error_receipt.json` records
`endpoint_opened: false`. The outcome-free receipt was corrected to the exact
EXP030 seeded powers: Avana `0.6686` and KY `0.4355`; both remain below the
frozen `0.80` confirmatory threshold. The correction changed no cohort, target
header, or endpoint value.

The independent pre-endpoint checks verified the selection hashes, input hashes,
composite BRCA1/BRCA2 rule, canonical roster, exact `CIP2A (57650)` header
identity, and the implementation boundary. The frozen cohort contains `1,292`
eligible screens and `1,290` source/model rows: Avana `975`, KY `315`. Composite
damaging/matrix-intact counts are Avana `46/929` and KY `25/290`; mixed-lineage
counts are `16/8`. The canonical roster SHA-256 is
`058842fec2d6750661de8d3109950f7e6376456baa564b5bd3cb49697fa3d083`.

## Post-execution checks

**GO.** An independent process configured the previously audited composite
loader and the frozen rank-delta engine directly, then recomputed:

- the 1,290-row context and endpoint ledgers;
- both corrected design-sensitivity rows;
- endpoint median-collapse coverage;
- Avana and KY deltas, pair counts, permutation counts and p-values,
  bootstrap intervals, and lineage deltas;
- all non-summary artifact hashes;
- the normalized summary digest and pre-endpoint receipt;
- the terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The recomputation matched the published summary exactly. No source pooling,
lineage exclusion, endpoint-derived rescue, target-specific threshold, or raw
cross-source score comparison was used.

## Claim decision

EXP030 is released only as a T1 descriptive feasibility result. The Avana
association is negative but fails the no-positive-lineage gate; KY is weaker and
uncertain under the frozen gates. The paired result does not support a robust
two-source composite BRCA1/2–CIP2A dependency claim.

It does not establish biallelic BRCA1/2 loss, HRD, functional BRCA status,
causal synthetic lethality, pharmacologic CIP2A inhibition, treatment benefit,
patient selection, clinical utility, or a confirmatory claim.
