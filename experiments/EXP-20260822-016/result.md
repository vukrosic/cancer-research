# EXP-20260822-016 result — ARID1A status to KEAP1 dependency

## Release classification

`PROTOCOL_DEVIATION_NONCONFIRMATORY`. The endpoint analysis is internally
reproducible, but the executable outcome-free design power (`0.8652` Avana,
`0.5875` KY) did not exactly match the frozen shortlist planning receipt
(`0.8622`, `0.5699`). The deviation is preserved rather than retroactively
amending the preregistration. `analysis_label` remains `FEASIBILITY_ONLY` and
`confirmatory_claim` remains `false`.

## Frozen context and endpoint result

- DepMap Public 23Q4, Avana and KY source-specific cohorts.
- 1,292 eligible screens collapsed to 1,290 source/model units: Avana 975,
  KY 315; 1,098 unique ModelIDs across both sources.
- Matrix-defined damaging ARID1A status: Avana 101 and KY 43 damaging models.
- KEAP1 scores were median-collapsed within `(source, ModelID)` and never
  compared as raw values across sources.

| Source | Delta | Permutation p | Bootstrap 95% CI | Nominal result |
|---|---:|---:|---:|---|
| Avana | -0.0545454545 | 0.2320476795 | [-0.1791443850, 0.0695187166] | Fails |
| KY | -0.2275379230 | 0.0207097929 | [-0.4095682614, -0.0431738623] | Fails lineage gate |

Avana failed the effect-size, permutation, bootstrap, and lineage-consistency
gates. KY passed direction, effect-size, permutation, bootstrap, and negative-
lineage gates, but failed lineage consistency: Bone `+1.0`, CNS/Brain `+0.75`,
and Lymphoid `+0.7777777778` exceeded the frozen `+0.20` limit.

## Claim boundary

This result is only an internally reproducible feasibility/protocol-deviation
receipt for the ARID1A-status versus KEAP1-dependency direction in public
cell-line screens. It is not a clean preregistered replication, confirmatory
claim, causal result, universal dependency claim, druggability claim, or
clinical conclusion. No source pooling, subgroup rescue, or threshold rescue
was used.

## Receipts

- Context ledger: `23369e7d1d43f738bb1bcf511512edc6cde0e770bde690c350d5d8d6025ad815`
- Design sensitivity: `abda119a93c6cd0c2620f69d75bae53420121368f7f7eec703c44c866375eba2`
- Endpoint ledger: `0b112d68824ede9f2d4d4336a93ce8dac59b90a69768ffba5a5c709b0f7d84a8`
- Inference ledger: `fd3d89e94d69d58af483a863c42e9186ef582698af5b12c61b1e9a58cac36e6c`
- Summary normalized self-digest: `e2a833fb237ab89f0d8dc3ef833f1642e594919c584f84e748b9b7d4152e5b1b`
- Pre-endpoint receipt: `d68704a69551b036081bcb23450630e3ae04bf7cd4f40f42870ea8a551bb4d18`

## Reproduction

```bash
UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run pytest
UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-arid1a-keap1-replication
```

The command is expected to exit `2` after publishing the five result artifacts.
