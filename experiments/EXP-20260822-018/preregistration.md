# EXP-20260822-018 preregistration — CDKN2A damaging status to TYMS dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does damaging matrix-defined
`CDKN2A (1029)` status predict stronger source-specific `TYMS (7298)` knockout
dependency within lineage?

The exposure is exactly CDKN2A matrix value `1` or `2`, called `damaging`; the
reference is value `0`, called `matrix_intact`. This does not establish CDKN2A
deletion, biallelic loss, p16/p14 functional status, or high TYMP expression.
Those distinctions are biologically important and are an explicit limitation of
this feasibility audit.

A primary DepMap-linked study reported and experimentally tested a CDKN2A-
deficiency/TYMS vulnerability, including genetic and isogenic validation:
<https://pmc.ncbi.nlm.nih.gov/articles/PMC8401190/>. This experiment tests
whether a matrix-defined proxy is reliable across two independent CRISPR screen
families; it is not a novelty or treatment claim.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` before any TYMS
score row was opened. The metadata-only census records 110/865 damaging/intact
Avana models and 37/278 KY models, with 19 and 11 mixed lineages. The exact
deterministic planning receipt is 0.8954 Avana and 0.5364 KY. KY is below the
0.80 confirmatory threshold, so this experiment is permanently
`FEASIBILITY_ONLY` and cannot produce a T2/confirmatory claim.

PTEN→PIK3CB was the closest feasible alternative; BRCA2→POLQ, RB1→E2F3, and
PBRM1→EZH2 were excluded by the frozen KY exposure/context gate. The exact
candidate census, canonical roster, and design receipt hashes are bound in the
manifest before execution.

## Frozen inputs and cohort

- Dataset release: DepMap 23Q4 public files.
- Screen QC SHA-256: `fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407`.
- Screen map SHA-256: `1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad`.
- Model metadata SHA-256: `6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341`.
- Damaging mutation matrix SHA-256: `aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3`.
- Naive score file and endpoint-header identity SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.
- Eligible libraries: exactly `Avana` and `KY`.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact screen-to-model
  join, nonblank `OncotreeLineage`, and one canonical row per `(source, ModelID)`.
- Expected canonical units: Avana 975 and KY 315; duplicate eligible screens
  remain in the ledger and are median-collapsed only for endpoint scores.

## Pre-endpoint stops

The runner must stop before endpoint values are parsed for any frozen input hash,
schema/header, screen/model identity, matrix coverage/domain, context adequacy,
or implementation-boundary failure. The endpoint hash is checked once before
context loading and again immediately before endpoint-header validation.

- `T0_INPUT_HASH`: frozen file hash drift, including either endpoint hash check.
- `T0_SCHEMA_HEADER`: required headers or exact CDKN2A/TYMS column identity drift,
  before any TYMS value is parsed.
- `T0_IDENTITY_JOIN`: duplicate/unmapped screen or model identity, missing
  eligible lineage, or invalid eligible row.
- `T0_MATRIX_COVERAGE`: duplicate/short/missing CDKN2A matrix row or value outside
  `{0,1,2}`.
- `T0_CONTEXT_ADEQUACY`: expected source counts, 110/37 and 865/278 status
  counts, or 19/11 mixed-lineage counts drift; minimums are 20 exposed, 50
  reference, and 5 mixed lineages per source.
- `T0_IMPLEMENTATION_BOUNDARY`: manifest, candidate census, design receipt,
  canonical roster, transitive code, or `uv.lock` drift.
- `T0_ENDPOINT_COMPLETENESS`: only after the accepted endpoint header and value
  stream are opened, for missing, duplicate, or nonnumeric TYMS values.

No inference is allowed after any stop.

## Design sensitivity

- Null permutations: 100,000 per source.
- Alternative simulations: 10,000 per source.
- Exposed-group score distribution: `Normal(-0.358286909243, 1)`.
- Reference-group score distribution: `Normal(0, 1)`.
- Planning seeds: Avana `20261800`; KY `20261900`.
- RNG: NumPy `Generator(PCG64(seed))`; lexicographic lineage/status/model
  ordering; rank method `average`; null batches of 1,000.
- Critical quantile: NumPy linear 5th percentile.
- Rejection rule: alternative delta `<=` critical delta.
- Frozen critical values: Avana `-0.11511227999190775`; KY
  `-0.19230769230769232`.
- Frozen planning power: Avana `0.8954`; KY `0.5364`.
- Confirmatory threshold: `0.80`; confirmatory claims disabled.

## Primary estimand and inference

Within each lineage and source, define:

`delta = P(TYMS_exposed > TYMS_reference) - P(TYMS_exposed < TYMS_reference)`.

Because more negative dependency scores indicate stronger dependency, more
negative delta means stronger TYMS dependency in damaging CDKN2A models. The
estimand is the denominator-weighted sum of lineage Mann–Whitney numerators
divided by the sum of within-lineage pair denominators. Endpoint scores are
median-collapsed within `(source, ModelID)`.

Nominal gates, evaluated separately for Avana and KY, are:

- delta `< 0`;
- delta `<= -0.20`;
- one-sided permutation `p <= 0.05`, with `p = (1 + extreme_count) / 100001`;
- percentile bootstrap 95% upper bound `< 0`;
- at least five negative lineage deltas; and
- no lineage delta `> +0.20`.

Inference seeds are Avana `20271800` and KY `20271900`. No source pooling,
post-hoc lineage exclusion, threshold change, TYMP expression rescue, or
cross-source raw-score comparison is allowed.

## Claim boundary

The strongest permitted conclusion is a T1 descriptive association for a
damaging-matrix CDKN2A proxy and source-specific TYMS dependency in frozen
23Q4 cell-line cohorts. It cannot establish CDKN2A deletion or functional loss,
TYMP-high biology, treatment sensitivity, patient benefit, or clinical
actionability. KY's pre-endpoint planning power is below 0.80, so no T2 or
confirmatory claim is allowed even if all nominal gates pass.
