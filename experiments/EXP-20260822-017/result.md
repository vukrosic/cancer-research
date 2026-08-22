# EXP-20260822-017 result — TP53 matrix-intact status to MDM2 dependency

## Release label

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

**Evidence tier: T1 descriptive association only; not T2/confirmatory.**

This is a source-specific, lineage-stratified reliability result for a
matrix-defined TP53 proxy. It is not a functional-wild-type TP53 claim, a
novelty claim, a treatment claim, or a clinical result. The known biological
motivation and primary CRISPR evidence are documented in the preregistration:
<https://pmc.ncbi.nlm.nih.gov/articles/PMC6080915/>.

## Frozen design and cohort

- Exposure: TP53 matrix value `0`, labeled `matrix_intact`.
- Reference: TP53 matrix values `1` or `2`, labeled `damaging`.
- Endpoint: `MDM2 (4193)` from `ScreenNaiveGeneScore.csv`.
- Eligible screens: `1292`; canonical source/model units: `1290`.
- Avana: `365` exposed, `610` reference, `25` mixed lineages.
- KY: `82` exposed, `233` reference, `16` mixed lineages.
- Planning power: Avana `0.9941`; KY `0.7521`. KY is below the frozen `0.80`
  threshold, so confirmatory labeling was disabled before endpoint access.

## Primary source-specific results

| Source | Delta | Pair count | One-sided p | Bootstrap 95% CI | Nominal gates |
| --- | ---: | ---: | ---: | --- | --- |
| Avana | `-0.6240834452` | `9683` | `0.0000099999` | `[-0.7013373954, -0.5443560880]` | `5/6`; lineage consistency failed |
| KY | `-0.5397973951` | `1382` | `0.0000099999` | `[-0.6917510854, -0.3806078148]` | `6/6` |

The Avana failure was the prespecified lineage-consistency gate. Positive
lineage deltas exceeded `+0.20` in Cervix (`+0.3928571429`) and Prostate
(`+0.3333333333`). The other Avana gates passed. KY passed all six nominal
gates, but that does not override the feasibility-only design label or rescue
the cross-source result.

## Interpretation

The frozen data show a strong negative aggregate association in both screen
families, consistent with stronger MDM2 dependency among matrix-intact TP53
models. The result is not fully reliable under the preregistered lineage gate
because Avana contains two positive lineage contrasts above the allowed limit.
The appropriate output is a reproducible, non-confirmatory reliability signal
with explicit heterogeneity—not a clean replicated biomarker claim.

## Artifact hashes

- `context_ledger.csv`: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`
- `design_sensitivity.csv`: `19cf0a7cad928e8e952a024d1fbc97c33075595a8070f66f67bda33ce8715a5f`
- `endpoint_scores.csv`: `ca3328aac98baa8c16a75bac476a10a2936904e37627f9f398e1e78f876d1ffa`
- `inference.csv`: `134c58a353ab5f5bbec46a3beb3ee6932580aa5ea2b85321ef4d22856dbe31e1`
- `summary.json`: `671d2de04d66c7ad2e39dbe98b331b3b3941c0a822b2897656fec79d74860b66`

The complete machine-readable receipt is in `results/summary.json`.
