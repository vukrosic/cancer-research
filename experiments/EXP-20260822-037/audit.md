# EXP037 audit

## Pre-endpoint gate

**GO.** The bound manifest was checked against the committed selection seal,
frozen input hashes, exact `MAT2A (4144)` endpoint identity, CDKN2A status
contract, canonical roster, and outcome-free design receipt before endpoint
values were loaded. The frozen cohort contains `1,292` eligible screens and
`1,290` source/model values. The canonical roster SHA-256 is
`df50a72ac86b161e16ebc5a2eb2b2f5c8d35151d94da4046c375f5ab0f603bb5`.

The bound planning powers are Avana `0.8906` and KY `0.5361`. KY is below the
frozen `0.80` confirmatory threshold, so EXP037 is permanently
`FEASIBILITY_ONLY`.

## Post-execution checks

**GO.** An independent direct-engine audit recomputed from the committed
context and endpoint ledgers:

- the 1,290-row context and endpoint ledgers;
- both outcome-free design rows;
- endpoint coverage and model collapse;
- Avana and KY deltas, pair counts, permutation counts and p-values,
  bootstrap intervals, lineage deltas, and gate booleans;
- all non-summary artifact hashes;
- the normalized summary digest and pre-endpoint receipt;
- the terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` contract.

The audit matched the published summary exactly. The audit harness initially
attempted to compare raw `summary.json` bytes to its normalized digest; that
assertion was corrected to use the preregistered normalization that blanks the
`summary.json` hash field. No experiment artifact or endpoint value changed.

## Claim decision

EXP037 is released only as a T1 descriptive feasibility result. Avana was
positive and near-null; KY was negative with a robust-looking aggregate
direction but failed the preregistered no-positive-lineage gate. There is no
source-consistent CDKN2A-proxy/MAT2A transport claim.

The source hypothesis concerns MAT2A vulnerability in MTAP-deleted cancers
([primary phase I report](https://www.nature.com/articles/s41467-024-55316-5)). EXP037 tests only a damaging-matrix CDKN2A mutation proxy against genetic MAT2A knockout dependency. It does not establish CDKN2A deletion, MTAP deletion, PRMT5 mechanism, MAT2A-inhibitor efficacy, treatment benefit, patient selection, clinical utility, or a confirmatory claim.
