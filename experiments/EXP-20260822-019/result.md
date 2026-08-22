# EXP-20260822-019 result — PTEN damaging status to PIK3CB dependency

## Release label

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

**Evidence tier: T1 descriptive association only; not T2/confirmatory.**

This is a source-specific, lineage-stratified reliability result for a
damaging-matrix PTEN proxy. It is not a PTEN-null or biallelic-functional-loss
claim, a PTEN protein or copy-number claim, a PI3K-beta inhibitor claim, a
treatment claim, a clinical result, or a confirmatory biomarker claim. The
biological motivation is the genetic PIK3CB study by Wee et al.:
<https://pubmed.ncbi.nlm.nih.gov/18755892/>.

## Frozen design and cohort

- Exposure: PTEN matrix values `1` or `2`, labeled `damaging`.
- Reference: PTEN matrix value `0`, labeled `matrix_intact`.
- Endpoint: `PIK3CB (5291)` from `ScreenNaiveGeneScore.csv`.
- Eligible screens: `1292`; canonical source/model units: `1290`.
- Avana: `94` exposed, `881` reference, `19` mixed lineages.
- KY: `38` exposed, `277` reference, `11` mixed lineages.
- Planning power: Avana `0.8562`; KY `0.5375`. KY is below the frozen `0.80`
  threshold, so confirmatory labeling was disabled before endpoint access.

## Primary source-specific results

| Source | Delta | Pair count | One-sided p | Bootstrap 95% CI | Nominal gates |
| --- | ---: | ---: | ---: | --- | --- |
| Avana | `-0.2803388986` | `4013` | `0.0001199988` | `[-0.3954647396, -0.1572389733]` | `5/6`; lineage consistency failed |
| KY | `-0.0066050198` | `757` | `0.4830751692` | `[-0.2153236460, 0.2021136063]` | `2/6`; effect, uncertainty, and lineage gates failed |

Avana passed the direction, effect-size, permutation, bootstrap, and
five-negative-lineage gates. It failed only the no-positive-lineage gate:
Bowel was `+0.4728682171`, Cervix `+1.0`, and Uterus `+0.2946428571`.

KY was near zero and failed the effect-size, permutation, bootstrap, and
no-positive-lineage gates. Its positive lineage deltas included CNS/Brain
`+0.3412698413` and Esophagus/Stomach `+0.3243243243`.

## Interpretation

The two source families disagree materially: Avana shows a negative aggregate
association, while KY is essentially null with a confidence interval crossing
zero. The prespecified reliability gates fail in both sources, and KY has
inadequate planning power for a confirmatory label. The appropriate output is
a reproducible, non-confirmatory T1 result showing source/lineage instability
of the matrix-defined PTEN-to-PIK3CB proxy—not evidence that PTEN loss reliably
creates PIK3CB dependency.

## Artifact hashes

- `context_ledger.csv`: `48bf8b95574dc6b79acdb31acbb08cbc9166ffd4c04de600142df9c03baaa11b`
- `design_sensitivity.csv`: `f849c280dc056c2192ca1c3ac4bfd0256944bac48a661006ddb76f277648a963`
- `endpoint_scores.csv`: `85d0a72e00b8f43a39970efd8e94069dee84dabceb9bd9589079ed7061b54982`
- `inference.csv`: `bc8fbd40ea92e8ce84bfaa8c85d5d8e5dd7415d9e4f95505dc021c95cb124ee1`
- `summary.json`: `bef5b62da8d93a9c3ab4aeec3e8ab3dde0ce1b311e28dba6507505ec53e1ec40`

The complete machine-readable receipt is in `results/summary.json`.
