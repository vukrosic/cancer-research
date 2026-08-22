# EXP-20260822-022 preregistration — EP300 damaging status to CREBBP dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does damaging
matrix-defined EP300 status associate with stronger source-specific CREBBP
dependency in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability test of a proxy-defined association. It is not a test of
functional EP300 loss, paralog causality, CREBBP inhibitor response, or
clinical benefit.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` and
`design_census_receipt.json` before any CREBBP score row or endpoint value was
parsed. The primary biological source is the CRISPR paralog study:
<https://pmc.ncbi.nlm.nih.gov/articles/PMC8080727/>.

The frozen metadata contrast is:

- exposure: EP300 matrix value `1` or `2`, labeled `damaging`;
- reference: EP300 matrix value `0`, labeled `matrix_intact`;
- endpoint: `CREBBP (1387)` from `ScreenNaiveGeneScore.csv`;
- eligible source/model units: Avana `975`, KY `315`;
- status counts: Avana `61` damaging / `914` matrix-intact; KY `34`
  damaging / `281` matrix-intact;
- mixed-lineage counts: Avana `18`, KY `11`;
- canonical roster SHA-256:
  `9a49f37dbde7785df261c92abaf9cb9ec4ccef3c1a1f8fc524865426763407d1`.

Both source powers are below `0.80`; EXP022 is permanently feasibility-only.

## Design sensitivity

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(CREBBP_exposed > CREBBP_reference) - P(CREBBP_exposed < CREBBP_reference)`

More negative values indicate stronger dependency among damaging-status models.
Scores are never compared across screen families. The frozen design uses
100,000 null permutations, 10,000 alternative simulations, PCG64, sorted
lineage/status/model order, average ranks, a Normal(0,1) null, and an exposed
Normal(-0.358286909243,1) alternative.

For inference, each eligible source/model unit is assigned the median of all
eligible screen rows for that source/model. Within each source, models are
partitioned by lexicographically ordered lineage; only lineages containing at
least one model in both status groups contribute. The one-sided permutation
null preserves exposed counts within lineage; the bootstrap resamples model
IDs within lineage/status cells. The exact inference seeds are `20272200`
(Avana) and `20272300` (KY), with 100,000 permutations and 10,000 bootstraps.

- Avana seed `20262200`: critical delta `-0.14680232558139536`, planning power
  `0.7401`;
- KY seed `20262300`: critical delta `-0.2039381153305204`, planning power
  `0.4984`.

Because both source powers are below the frozen `0.80` confirmatory threshold,
the analysis label is permanently `FEASIBILITY_ONLY`; no result can receive a
T2/confirmatory label.

## Primary gates

Each source must be reported separately: `delta < 0`, `delta <= -0.20`, one-sided
permutation `p <= 0.05`, bootstrap upper bound `< 0`, at least five negative
lineages, and no lineage delta `> +0.20`. No source pooling, post hoc lineage
exclusion, threshold change, alternate status definition, or endpoint-derived
subgroup rescue is allowed.

## T0 stop rules and claim contract

Before any endpoint value parse, verify the manifest, implementation boundary,
candidate census, design receipt, all input hashes, QC eligibility, screen
identity, lineages, matrix domain, status counts, mixed-lineage counts,
canonical roster, both design rows, and a sealed `pre_endpoint_receipt.json`.
Verify the exact `CREBBP (1387)` header before parsing values. T0 failures stop
without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**. The matrix proxy does not establish
functional EP300 loss, protein state, paralog causality, drug response,
treatment benefit, patient selection, or clinical utility.

