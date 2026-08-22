# EXP038 audit

## Pre-endpoint gate

**GO.** The bound manifest was checked against the committed outcome-blind
selection seal, frozen input hashes, exact `ICMT (23463)` endpoint identity,
PTEN status contract, canonical roster, and design receipt before endpoint
values were loaded. The selection seal records
`endpoint_values_opened: false`, and the pre-endpoint receipt was sealed before
the endpoint ledger was written. The frozen cohort contains `1,292` eligible
screens and `1,290` source/model values.

The bound planning powers are Avana `0.8579` and KY `0.5297`. KY is below the
frozen `0.80` confirmatory threshold, so EXP038 is permanently
`FEASIBILITY_ONLY`.

## Post-execution checks

**GO.** An independent direct-engine audit recomputed from the result ledgers:

- the 1,290-row context and endpoint ledgers;
- both outcome-free design powers;
- endpoint coverage and model collapse;
- Avana and KY deltas, pair counts, permutation counts and p-values,
  bootstrap intervals, lineage deltas, and gate booleans;
- all non-summary artifact hashes;
- the normalized summary digest and pre-endpoint receipt; and
- the terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The audit matched the published summary exactly. It returned
`INDEPENDENT_AUDIT=GO`; no experiment artifact or endpoint value changed.

## Claim decision

EXP038 is released only as a T1 descriptive feasibility result. Avana was
positive and heterogeneous; KY was weakly negative but also heterogeneous and
failed every meaningful robustness gate other than direction. There is no
source-consistent PTEN-proxy/ICMT transport claim.

The source hypothesis concerns ICMT dependency in PTEN-deficient triple-negative
breast cancer ([primary PTEN/ICMT study](https://link.springer.com/article/10.1186/s40164-025-00738-0)).
EXP038 tests only a damaging-matrix PTEN mutation proxy against genetic ICMT
dependency in frozen DepMap source cohorts. It does not establish PTEN protein
loss, PTEN copy loss, subtype-specific biology, mechanism, ICMT-inhibitor
efficacy, treatment benefit, clinical utility, or a confirmatory claim.
