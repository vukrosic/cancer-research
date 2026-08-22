# EXP033 audit

## Pre-endpoint gate

**GO.** The independent audit checked the committed selection seal, frozen
input hashes, exact `ATR (545)` endpoint identity, ARID1A status contract,
canonical roster, and outcome-free design receipt before endpoint values were
loaded. The frozen cohort contains `1,292` eligible screens and `1,290`
source/model values: Avana `975`, KY `315`. ARID1A damaging/matrix-intact
counts are Avana `101/874` and KY `43/272`; mixed-lineage counts are `19/11`.
The canonical roster SHA-256 is
`62f8bf69649eb375de12daed222a50a4bc3b3df39c40f0e614845fbab12ab9ed`.

The bound planning powers are Avana `0.8666` and KY `0.5810`. KY is below the
frozen `0.80` confirmatory threshold, so EXP033 is permanently
`FEASIBILITY_ONLY`. No ATR score was used during selection.

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

EXP033 is released only as a T1 descriptive feasibility result. Avana was
directionally negative but missed the effect, permutation, bootstrap, and
lineage-consistency requirements. KY was near-null and heterogeneous and
failed the substantive gates. The frozen data do not support a robust
ARID1A-proxy–ATR dependency transport claim.

The source hypothesis concerned ARID1A-defect/ATR-inhibitor biology reported in
the literature ([Nature Communications study](https://www.nature.com/articles/ncomms13837)).
EXP033 tests only a damaging-matrix ARID1A proxy against genetic ATR knockout
dependency. It does not establish functional ARID1A loss, ATR-inhibitor
sensitivity, DNA-damage or replication-stress mechanism, causal synthetic
lethality, pharmacologic response, treatment benefit, patient selection,
clinical utility, or a confirmatory claim.
