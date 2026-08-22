# EXP-20260822-018 result — CDKN2A damaging status to TYMS dependency

## Release label

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

**Evidence tier: T1 descriptive association only; not T2/confirmatory.**

This is a source-specific, lineage-stratified reliability result for a
damaging-matrix CDKN2A proxy. It is not a deletion claim, a biallelic
functional-loss claim, a TYMP-high claim, a treatment claim, a clinical result,
or a confirmatory biomarker claim. The biological motivation and its limits are
documented in the preregistration: <https://pmc.ncbi.nlm.nih.gov/articles/PMC8401190/>.

## Frozen design and cohort

- Exposure: CDKN2A matrix values `1` or `2`, labeled `damaging`.
- Reference: CDKN2A matrix value `0`, labeled `matrix_intact`.
- Endpoint: `TYMS (7298)` from `ScreenNaiveGeneScore.csv`.
- Eligible screens: `1292`; canonical source/model units: `1290`.
- Avana: `110` exposed, `865` reference, `19` mixed lineages.
- KY: `37` exposed, `278` reference, `11` mixed lineages.
- Planning power: Avana `0.8954`; KY `0.5364`. KY is below the frozen `0.80`
  threshold, so confirmatory labeling was disabled before endpoint access.

## Primary source-specific results

| Source | Delta | Pair count | One-sided p | Bootstrap 95% CI | Nominal gates |
| --- | ---: | ---: | ---: | --- | --- |
| Avana | `-0.1345336840` | `4943` | `0.0277497225` | `[-0.2603783128, -0.0062714950]` | `4/6`; effect and lineage gates failed |
| KY | `-0.1802884615` | `832` | `0.0624193758` | `[-0.3701923077, 0.0120793269]` | `2/6`; effect, uncertainty, and lineage gates failed |

Avana passed the negative-direction, bootstrap-upper-below-zero, and
permutation gates, but failed the prespecified delta threshold and lineage
consistency. Positive lineage deltas exceeded `+0.20` in Bowel (`+0.6136363636`),
Eye (`+0.5555555556`), and Ampulla of Vater (`+1.0`). KY did not pass the
permutation gate (`p=0.0624193758`) or the bootstrap-upper-below-zero gate; its
positive lineage deltas included Lymphoid and Prostate at `+1.0`.

## Interpretation

Both source-specific aggregate deltas are negative, which is directionally
consistent with stronger TYMS dependency among CDKN2A-damaging models. The
prespecified reliability gates fail in both sources, and KY has inadequate
planning power for a confirmatory label. The appropriate output is a
reproducible, non-confirmatory T1 signal with substantial lineage and
source-specific uncertainty—not a replicated biomarker claim.

## Artifact hashes

- `context_ledger.csv`: `1c6b1df176468f25de48585b97d456b7e83c3d2fa63352a31a527b4f3263e725`
- `design_sensitivity.csv`: `11924a082212fdecd0f8c39dba6ff0606a68e29f938ee905c4009b9cd5ed21ee`
- `endpoint_scores.csv`: `86d8ac605067390f77deabb25018be1da84db2724d66551d9055d7418e0f5d7a`
- `inference.csv`: `1450d96233f33bdb88d06768e8cb5f2b5444ae797fe43fce9c439c698f294548`
- `summary.json`: `520a1c9bc1115fab92f080c1b98ab07242c80939e67e753a1414709622027c81`

The complete machine-readable receipt is in `results/summary.json`.
