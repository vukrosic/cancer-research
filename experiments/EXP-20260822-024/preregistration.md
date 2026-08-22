# EXP-20260822-024 preregistration — KMT2D damaging status to KMT2C dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does damaging matrix-
defined KMT2D status associate with stronger source-specific KMT2C dependency
in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability test of a proxy-defined association. It is not a test of
functional KMT2D loss, lymphoma-specific causality, paralog causality, KMT2C
inhibitor response, or clinical benefit.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` and
`design_census_receipt.json` before any KMT2C score row or endpoint value was
parsed. The primary biological source is the 2026 AACR CRISPR report:
<https://doi.org/10.1158/1538-7445.AM2026-7060>.

The frozen metadata contrast is:

- exposure: KMT2D matrix value `1` or `2`, labeled `damaging`;
- reference: KMT2D matrix value `0`, labeled `matrix_intact`;
- endpoint: `KMT2C (58508)` from `ScreenNaiveGeneScore.csv`;
- eligible source/model units: Avana `975`, KY `315`;
- status counts: Avana `86` damaging / `889` matrix-intact; KY `33`
  damaging / `282` matrix-intact;
- mixed-lineage counts: Avana `17`, KY `11`;
- canonical roster SHA-256:
  `e8f440a118065e4fc23535dca196c03b8c9a08b9a4f4348516f214d19b2e9164`.

Avana planning power is `0.8433`, but KY planning power is `0.5120`; EXP024
is permanently feasibility-only because the paired source contract requires
all primary sources to meet the `0.80` threshold.

## Design sensitivity

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(KMT2C_exposed > KMT2C_reference) - P(KMT2C_exposed < KMT2C_reference)`

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
IDs within lineage/status cells. The exact inference seeds are `20272400`
(Avana) and `20272500` (KY), with 100,000 permutations and 10,000 bootstraps.

- Avana seed `20262400`: critical delta `-0.12622333751568382`, planning power
  `0.8433`;
- KY seed `20262500`: critical delta `-0.1994645247657296`, planning power
  `0.5120`.

Because KY is below the frozen `0.80` confirmatory threshold, the analysis
label is permanently `FEASIBILITY_ONLY`; no result can receive a
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
Verify the exact `KMT2C (58508)` header before parsing values. T0 failures stop
without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**. The matrix proxy does not establish
functional KMT2D loss, lymphoma-specific causality, paralog causality, KMT2C
inhibitor response, treatment benefit, patient selection, or clinical utility.

The design receipt's normalized digest is computed as
`SHA256(json.dumps(payload_with_receipt_sha256_set_to_empty, indent=2,
sort_keys=True) + "\n")` encoded as UTF-8. The canonical roster digest is computed
from one compact sorted-key JSON object per sorted `(source, ModelID)` row,
followed by LF, with fields `source`, `model_id`, `lineage`, `screen_ids`,
`matrix_value`, and `status`.
