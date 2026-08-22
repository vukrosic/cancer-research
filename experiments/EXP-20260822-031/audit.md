# EXP031 audit

## Pre-endpoint gate

**GO.** The independent audit verified the committed selection seal,
implementation manifest, frozen input hashes, exact `BRD4 (23476)` header
identity, SMAD4 status rule, canonical roster, and outcome-free design receipt
before treating endpoint values as an outcome. The frozen cohort contains
`1,292` eligible screens and `1,290` source/model rows: Avana `975`, KY `315`.
SMAD4 damaging/matrix-intact counts are Avana `46/929` and KY `25/290`; mixed
lineage counts are `12/6`. The canonical roster SHA-256 is
`3532122677a66a5fedbd664cb452d7dcd7ea6d179556ca4df1d1dbe4a81cef62`.

The bound planning powers are Avana `0.6414` and KY `0.4630`, both below the
frozen `0.80` confirmatory threshold. The experiment is permanently
`FEASIBILITY_ONLY`. No BRD4 score was opened during selection.

## Post-execution checks

**GO.** An independent direct configuration of the frozen engine recomputed:

- the 1,290-row context and endpoint ledgers;
- both design-sensitivity rows;
- endpoint median-collapse coverage;
- Avana and KY deltas, pair counts, permutation counts and p-values,
  bootstrap intervals, and lineage deltas;
- all non-summary artifact hashes;
- the normalized summary digest and pre-endpoint receipt;
- the terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The first audit pass caught a loader-polarity setup error before endpoint loading;
the corrected rerun returned `GO` and matched the published summary exactly.
No result was changed between the two audit passes.

## Claim decision

EXP031 is released only as a T1 descriptive feasibility result. Both sources
failed the primary gates: Avana was positive and heterogeneous, while KY was
near-null and heterogeneous. The paired result does not support a robust
two-source SMAD4–BRD4 dependency claim.

It does not establish functional SMAD4 loss, BET-inhibitor sensitivity, BRD4
inhibitor efficacy, a MYC mechanism, causal synthetic lethality, treatment
benefit, patient selection, clinical utility, or a confirmatory claim.
