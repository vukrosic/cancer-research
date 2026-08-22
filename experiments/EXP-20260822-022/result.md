# EXP-20260822-022 result — EP300 damaging status to CREBBP dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `CREBBP (1387)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: EP300 matrix value `1` or `2`, labeled `damaging`;
- reference: EP300 matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `9a49f37dbde7785df261c92abaf9cb9ec4ccef3c1a1f8fc524865426763407d1`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from metadata and a primary CRISPR
paralog study supporting EP300/CREBBP interaction:
[PMC8080727](https://pmc.ncbi.nlm.nih.gov/articles/PMC8080727/). That literature
does not convert the damaging matrix into functional EP300 loss.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.4171511627906977 | 2752 | 0.00000999990000099999 | [-0.5566860465116279, -0.2609011627906977] | 14 | +0.4 | FAIL |
| KY | -0.4767932489451477 | 711 | 0.00004999950000499995 | [-0.6708860759493671, -0.26863572433192684] | 6 | +1.0 | FAIL |

Both sources passed the aggregate direction, effect-size, permutation,
bootstrap, and negative-lineage-count gates. Both failed the frozen
no-positive-lineage gate: Avana had CNS/Brain `+0.3333333333333333` and
Pancreas `+0.4`; KY had Lymphoid `+0.7777777777777778`, Ovary/Fallopian Tube
`+0.44`, Prostate `+1.0`, and Skin `+0.3333333333333333`.

The result is therefore a strong but heterogeneous source-specific aggregate
association, not a lineage-consistent dependency claim. Both source planning
powers were below `0.80` before endpoint access (Avana `0.7401`, KY `0.4984`),
so the experiment is permanently feasibility-only.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
damaging-matrix EP300 proxy was associated with stronger CREBBP knockout
dependency in both source families, but the association failed the frozen
lineage-consistency gate in both sources.

This does not establish functional EP300 loss, EP300-null biology, paralog
causality, CREBBP inhibitor sensitivity, treatment benefit, patient selection,
or clinical utility. No source pooling, post hoc lineage exclusion, threshold
change, or endpoint-derived rescue was used.

## Artifact receipts

- `context_ledger.csv`: `02e3845021772123b80c77b5317bbbffb484f88c74d2ba5c8bcbb74935563ea2`
- `design_sensitivity.csv`: `7ed684a32ae9b9c9d5290a14e236660f71187c8dc3acbba1d177eac5e32469b9`
- `endpoint_scores.csv`: `5c04bafb467a9dcbb91c2a30f29739a9ba9b0f5795a56dc74173cca320d86378`
- `inference.csv`: `8d75b782d0820d0fe7a85434356e401ad03ed7756825ab98006b007af42d0071`
- normalized `summary.json` digest: `6847f52a8daab687a433c70c94e638ceee32212b1e439b65632d19b18db8dfda`
- pre-endpoint receipt: `daff66c8aa4509c5e8f8904db47445b1431c256dd1d3534363a39ba10ee293c8`
