# EXP032 audit

## Pre-endpoint gate

**GO.** The independent audit checked the committed selection seal, frozen
input hashes, exact `AURKA (6790)` endpoint identity, SMAD4 status contract,
canonical roster, and outcome-free design receipt before endpoint values were
loaded. The frozen cohort contains `1,292` eligible screens and `1,290`
source/model values: Avana `975`, KY `315`. SMAD4 damaging/matrix-intact
counts are Avana `46/929` and KY `25/290`; mixed-lineage counts are `12/6`.
The canonical roster SHA-256 is
`3532122677a66a5fedbd664cb452d7dcd7ea6d179556ca4df1d1dbe4a81cef62`.

The bound planning powers are Avana `0.6502` and KY `0.4713`, both below the
frozen `0.80` confirmatory threshold. EXP032 is permanently
`FEASIBILITY_ONLY`. No AURKA score was used during selection.

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

EXP032 is released only as a T1 descriptive feasibility result. Avana was
positive and heterogeneous; KY was also positive and heterogeneous. Neither
source passed the preregistered gates, so the frozen data do not support a
robust SMAD4-proxy–AURKA dependency transport claim.

The source hypothesis concerned SMAD4-loss/AURKA-inhibitor biology reported in
the literature ([Oncogene study](https://www.nature.com/articles/s41388-022-02293-y)).
EXP032 tests only a damaging-matrix SMAD4 proxy against genetic AURKA knockout
dependency. It does not establish functional SMAD4 loss, AURKA-inhibitor
sensitivity, spindle-checkpoint mechanism, causal synthetic lethality,
pharmacologic response, treatment benefit, patient selection, clinical utility,
or a confirmatory claim.
