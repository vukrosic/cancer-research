# EXP-20260822-015 result — ARID1A status to ARID1B dependency

## Decision

`FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE`. This is not a confirmatory result:
the preregistered KY design power is below 0.80, so `primary_confirmatory` and
`overall_pass` are permanently false. The command intentionally exits `2` for
this non-confirmatory outcome after publishing all artifacts.

## Frozen context and execution

- DepMap Public 23Q4, Avana and KY source-specific cohorts.
- 1,292 eligible screens collapsed to 1,290 source/model units: Avana 975,
  KY 315; 1,098 unique ModelIDs across both sources.
- Matrix-defined ARID1A damaging status: 101 Avana and 43 KY damaging models.
- Endpoint: median ARID1B score per source/ModelID; no cross-source raw-score
  comparison.
- Realized seeded design-sensitivity power: Avana `0.8642`, KY `0.5787`.
  Frozen outcome-free planning estimates were Avana `0.8651`, KY `0.5636`;
  they are separate approximate Monte Carlo planning receipts, not a required
  byte-identical execution value. Both support the permanent feasibility-only
  label because KY is below `0.80`.

## Primary nominal results

| Source | Delta | Permutation p | Bootstrap 95% CI | Nominal gates | Claim eligible |
|---|---:|---:|---:|---|---|
| Avana | -0.4582887701 | 0.0000100000 | [-0.5967914439, -0.3122994652] | 6/6 pass | No |
| KY | -0.2158693116 | 0.0263397366 | [-0.4329054842, 0.0058343057] | 4/6 pass | No |

Avana passed all six nominal gates. KY failed the bootstrap upper-bound gate
because its upper bound was not below zero, and failed lineage consistency:
Bone had delta `+1.0` and Pancreas `+0.2666666667`, both above the frozen
`+0.20` limit. KY’s direction, effect-size, permutation, and negative-lineage
gates passed.

## Claim boundary

The result supports only a feasibility/robustness receipt for the frozen
ARID1A-status versus ARID1B-dependency direction in these public cell-line
screens. It does not establish a confirmatory replication, biological
independence of Avana and KY, causality, functional or biallelic ARID1A loss,
drug action, patient benefit, or clinical utility.

## Receipts

- Context ledger: `23369e7d1d43f738bb1bcf511512edc6cde0e770bde690c350d5d8d6025ad815`
- Design sensitivity: `5645c87a351c7daf28233c434b373575c35a578ed68096eae2622b505ccb589d`
- Endpoint ledger: `da56e757e1c5682cd600c530367d43409b4c77dcdbcc947ec4bdbf36c50d25ce`
- Inference ledger: `0182528c108d85416928dd897924e7d30211f5b44508352847a79c6783293912`
- Summary normalized self-digest: `7080ee945ffad26787f6576f43be1333b2a75bb003beac98b975b7ab2a29624a`
- Pre-endpoint receipt: `a9706b29bc3e80aee287db25ed61e20d2a3693a9b1fe885b3d6296b667705a97`

## Reproduction

```bash
UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run pytest
UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-arid1a-replication
```

The second command is expected to exit `2` while writing
`results/summary.json`. Raw input files are hash-locked and excluded from Git.
