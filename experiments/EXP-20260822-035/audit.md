# EXP035 audit

## Pre-endpoint gate

**GO.** The independent audit checked the committed selection seal, frozen
input hashes, exact `ENDOD1 (23052)` endpoint identity, TP53 status contract,
canonical roster, and outcome-free design receipt before endpoint values were
loaded. The frozen cohort contains `1,292` eligible screens and `1,290`
source/model values: Avana `975`, KY `315`. TP53 damaging/matrix-intact counts
are Avana `610/365` and KY `233/82`; mixed-lineage counts are `25/16`. The
canonical roster SHA-256 is
`61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`.

The bound planning powers are Avana `0.9950` and KY `0.7417`. KY is below the
frozen `0.80` confirmatory threshold, so EXP035 is permanently
`FEASIBILITY_ONLY`. No ENDOD1 score was used during selection.

The metadata-only SHA correction is preserved in
`selection_correction.md`. It changed no outcome, no cohort rule, and no
endpoint value; the original selection draft remains available at commit
`3cffc90`.

## Post-execution checks

**GO.** A direct independent configuration of the frozen engine recomputed:

- the 1,290-row context and endpoint ledgers;
- both outcome-free design-sensitivity rows;
- endpoint median-collapse coverage;
- Avana and KY deltas, pair counts, permutation counts and p-values,
  bootstrap intervals, and lineage deltas;
- all non-summary artifact hashes;
- the normalized summary digest and pre-endpoint receipt;
- the terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The audit matched the published summary exactly. No result was changed between
execution and audit.

## Claim decision

EXP035 is released only as a T1 descriptive feasibility result. Both sources
were positive and heterogeneous in the preregistered direction, with no
support for a robust TP53-proxy–ENDOD1 dependency transport claim.

The source hypothesis concerned an ENDOD1/TP53 synthetic-lethal interaction
reported in the literature ([Nature Communications study](https://www.nature.com/articles/s41467-022-30311-w)).
EXP035 tests only a damaging-matrix TP53 proxy against genetic ENDOD1 knockout
dependency. It does not establish functional TP53 loss, TP53 hotspot mutation,
ENDOD1-inhibitor sensitivity, DNA-repair mechanism, causal synthetic lethality,
pharmacologic response, treatment benefit, patient selection, clinical utility,
or a confirmatory claim.
