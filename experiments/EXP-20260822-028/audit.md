# EXP028 audit

## Pre-endpoint gate

**GO.** The independent audit verified the committed selection seal,
implementation manifest, frozen input hashes, target header identity, canonical
roster, and executable-engine design receipt before treating endpoint values as
an outcome. The frozen cohort contains `1,292` eligible screens and `1,290`
source/model rows: Avana `975`, KY `315`. TP53 damaging/matrix-intact counts
are Avana `610/365` and KY `233/82`; mixed-lineage counts are `25/16`. The
canonical roster SHA-256 is
`61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`.

The bound planning results were Avana critical delta
`-0.07879789321491273`, power `0.9952`, and KY critical delta
`-0.14327062228654125`, power `0.7509`. Because KY power is below `0.80`,
the experiment is permanently `FEASIBILITY_ONLY`. The exact `TIPARP (25976)`
header was checked during selection without parsing score values. The sealed
pre-endpoint receipt was written before endpoint values were parsed.

## Post-execution checks

**GO.** An independent configuration of the frozen engine recomputed:

- the exact five-file result set;
- the 1,290-row context and endpoint ledgers;
- both design-sensitivity rows;
- the endpoint median-collapse receipt;
- Avana and KY deltas, pair counts, permutation counts and p-values,
  bootstrap intervals, and lineage deltas;
- all non-summary artifact hashes;
- the normalized summary digest and pre-endpoint receipt;
- the terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The recomputation matched the published summary exactly. No source pooling,
lineage exclusion, threshold change, endpoint-derived rescue, or raw-score
comparison across sources was used.

## Audit correction

The first manifest draft used a descriptive pair label that differed from the
sealed pair identifier. The value was corrected to
`TP53_damaging_to_TIPARP` before release; the runner, selection seal, and all
published result artifacts already used that identifier. No endpoint values or
statistics changed.

## Claim decision

EXP028 is released only as a T1 descriptive feasibility result. It does not
support a general TP53/TIPARP dependency claim, a causal interaction claim, a
pharmacologic PARP7 inhibitor claim, a treatment claim, a clinical claim, or a
confirmatory claim.
