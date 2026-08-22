# EXP039 audit

## Pre-endpoint gate

**GO after documented remediation.** Attempt 001 stopped before endpoint access
because the implementation and manifest contained a two-character transcription
error in the screen-map SHA-256. Independent rehashing showed that the current
endpoint, QC, screen-map, model, and damaging-matrix files all match the
corrected digests. The corrected contract was sealed and rebound before the
successful endpoint execution. No PARP1 value was opened during attempt 001.

The bound manifest was then checked against the corrected selection seal,
frozen input hashes, exact `PARP1 (142)` endpoint identity, composite status
contract, canonical roster, design receipt, implementation boundary, and
claim contract. The pre-endpoint receipt was written before endpoint values
were loaded and records `sealed_before_endpoint: true`.

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

The audit matched every numerical field in the published summary exactly. A
post-execution metadata hardening corrected only an inherited stale composite
label in `context_receipt` from BRCA1-or-BRCA2 to PBRM1-or-ARID2; it did not
change any score, ledger row, design value, inferential statistic, gate, or
endpoint receipt. The hardened summary digest is recorded in the result card.

## Claim decision

EXP039 is released only as a T1 descriptive feasibility result. Avana was
weakly positive and heterogeneous; KY was more positive and highly
heterogeneous. There is no source-consistent PBRM1-or-ARID2-proxy/PARP1
transport claim.

The source hypothesis concerns PBRM1-deficiency sensitivity to PARP and ATR
inhibitors ([primary PBRM1/DNA-repair study](https://aacrjournals.org/cancerres/article/81/11/2888/673616/PBRM1-Deficiency-Confers-Synthetic-Lethality-to)).
EXP039 tests only a composite damaging-matrix PBRM1-or-ARID2 proxy against
genetic PARP1 dependency in frozen DepMap source cohorts. It does not establish
isolated PBRM1 loss, ARID2 loss, PBAF causality, HRD, PARP-inhibitor efficacy,
treatment benefit, clinical utility, or a confirmatory claim.
