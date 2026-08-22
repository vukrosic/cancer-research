# EXP-20260822-017 preregistration — TP53 matrix-intact status to MDM2 dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does matrix-intact
`TP53 (7157)` status predict stronger source-specific `MDM2 (4193)` knockout
dependency within lineage?

The exposure is deliberately narrow: `TP53` matrix value exactly `0` is called
`matrix_intact`; values `1` or `2` are the reference `damaging` group. This is
not a claim of functional wild-type TP53, because the frozen input does not
encode every mechanism that can disable p53 function. The endpoint is the
single MDM2 column in `ScreenNaiveGeneScore.csv`.

This is a replication and reliability audit of a known p53-network dependency,
not a novelty claim. A primary genome-scale CRISPR study reported and validated
MDM2 dependency in TP53-wild-type Ewing sarcoma models:
<https://pmc.ncbi.nlm.nih.gov/articles/PMC6080915/>.

## Outcome-free candidate selection

Selection was sealed in `candidate_census.json` before any MDM2 score row was
opened. The census uses only hashes, screen eligibility metadata, model lineage,
TP53 mutation-matrix values, and the endpoint header identity.

The selected candidate has 365/610 matrix-intact/damaging Avana models and
82/233 KY models, with 25 and 16 mixed lineages. Deterministic planning power
for the frozen permutation gate is 0.9941 Avana and 0.7521 KY. Because KY is
below 0.80, this experiment is permanently `FEASIBILITY_ONLY`; no endpoint
result can upgrade it to a confirmatory claim.

The census also records EP300→CREBBP, BRCA2→POLQ, SMARCA4→SMARCA2, and
MTAP→PRMT5 as outcome-free alternatives and documents why they were not
selected. The exact census hash, canonical roster hash, and a separate
pre-endpoint design receipt containing lineage counts, null critical values, and
algorithm details are bound in the manifest before execution.

## Frozen inputs and cohort

- Dataset release: DepMap 23Q4 public files.
- Screen QC: SHA-256 `fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407`.
- Screen map: SHA-256 `1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad`.
- Model metadata: SHA-256 `6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341`.
- Damaging mutation matrix: SHA-256 `aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3`.
- Naive score file and endpoint header identity: SHA-256
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.
- Eligible libraries: exactly `Avana` and `KY`.
- Eligibility: `PassesQC == True`, `CanInclude == True`, exact screen-to-model
  join, nonblank `OncotreeLineage`, and one canonical row per `(source, ModelID)`.
- Expected canonical models: Avana 975 and KY 315; all eligible duplicate
  screens remain listed in the context ledger and are median-collapsed only for
  the endpoint score.

## Pre-endpoint stops

Before endpoint parsing, the runner must stop with a machine-readable receipt if
any of these fail:

1. `T0_INPUT_HASH`: any frozen input hash, including the endpoint file hash,
   differs. The first endpoint hash check occurs before context loading; a
   second hash check occurs immediately before endpoint header validation.
2. `T0_SCHEMA_HEADER`: required headers or exact TP53/MDM2 column identity drift
   before any MDM2 value is parsed.
3. `T0_IDENTITY_JOIN`: duplicate or unmapped ScreenID/ModelID, missing lineage,
   or an invalid eligible identity.
4. `T0_MATRIX_COVERAGE`: TP53 matrix coverage, row identity, or value domain
   drift; allowed values are exactly `0`, `1`, and `2`.
5. `T0_CONTEXT_ADEQUACY`: the frozen source counts, exposure/reference counts,
   or mixed-lineage counts drift; minimums are 20 exposed, 50 reference, and 5
   mixed lineages per source.
6. `T0_IMPLEMENTATION_BOUNDARY`: the bound commits, module blobs, transitive
   analysis hashes, candidate-census hash, design-receipt hash, or `uv.lock`
   hash drift.

After the context ledger and deterministic design receipt are sealed, the runner
performs the second endpoint hash check and validates the complete endpoint
header before opening MDM2 values. A second hash mismatch is `T0_INPUT_HASH` and
an MDM2/header mismatch is `T0_SCHEMA_HEADER`; both have
`endpoint_opened=false`. Only after the accepted header and value stream are
opened can a missing, duplicate, or nonnumeric value produce
`T0_ENDPOINT_COMPLETENESS` with `endpoint_opened=true`. No inference is allowed
after a completeness stop.

## Design sensitivity

The design is a planning receipt, not an endpoint result:

- One-sided null permutation gate: 100,000 draws per source.
- Alternative simulations: 10,000 per source.
- Normal score shift for the exposed matrix-intact group:
  `-0.358286909243`.
- Planning seeds: Avana `20261730`; KY `20261830`.
- Critical value: the 5th percentile of the null distribution using NumPy's
  linear quantile definition.
- Rejection rule: alternative delta `<=` critical delta.
- Frozen planning power: Avana `0.9941`; KY `0.7521`.
- Confirmatory threshold: `0.80`; confirmatory claims are disabled.

## Primary estimand and inference

Within each lineage and source, define `delta` as the collapsed Mann–Whitney
probability contrast between matrix-intact exposed models and damaging reference
models:

`delta = P(MDM2_exposed > MDM2_reference) - P(MDM2_exposed < MDM2_reference)`.

More negative values indicate stronger MDM2 dependency in matrix-intact models.
The primary result is the denominator-weighted sum of lineage numerators divided
by the sum of within-lineage pair denominators. No cross-source raw-score
comparison is made.

Frozen nominal gates, evaluated separately for Avana and KY:

- `delta < 0`;
- `delta <= -0.20`;
- one-sided permutation `p <= 0.05`, with `p = (1 + extreme_count) / 100001`;
- percentile bootstrap 95% upper bound `< 0`;
- at least five negative lineage deltas; and
- no lineage delta `> +0.20`.

Permutation uses fixed source-specific model memberships and no redraw of
lineage structure. Bootstrap resamples model IDs with replacement independently
within each lineage/status group and recomputes the collapsed estimand. The
endpoint score is median-collapsed within `(source, ModelID)` across eligible
screens.

Inference seeds are Avana `20271730` and KY `20271830`. The exact endpoint
completeness, design, inference, and summary hashes must be tracked.

## Claim boundary

The strongest permitted conclusion is a matrix-defined TP53-intact versus MDM2
dependency association in frozen 23Q4 cancer cell-line cohorts, with source-
specific uncertainty and lineage heterogeneity. The experiment cannot establish
functional TP53 wild type, biological independence, a therapeutic window,
patient benefit, or clinical actionability. Since KY planning power is below
0.80, no two-source confirmatory claim is permitted even if all nominal gates
pass.
