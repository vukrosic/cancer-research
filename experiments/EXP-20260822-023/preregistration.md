# EXP-20260822-023 preregistration — APC damaging status to TDO2 dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does damaging matrix-
defined APC status associate with stronger source-specific TDO2 dependency in
the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability test of a proxy-defined association. It is not a test of
functional APC loss, WNT causality, TDO2 inhibitor response, immune remodeling,
or clinical benefit.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` and
`design_census_receipt.json` before any TDO2 score row or endpoint value was
parsed. The primary biological source is the APC/TDO2 synthetic-essentiality
study: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9262860/>.

The frozen metadata contrast is:

- exposure: APC matrix value `1` or `2`, labeled `damaging`;
- reference: APC matrix value `0`, labeled `matrix_intact`;
- endpoint: `TDO2 (6999)` from `ScreenNaiveGeneScore.csv`;
- eligible source/model units: Avana `975`, KY `315`;
- status counts: Avana `54` damaging / `921` matrix-intact; KY `30`
  damaging / `285` matrix-intact;
- mixed-lineage counts: Avana `11`, KY `5`;
- canonical roster SHA-256:
  `64d3f95cf8bac59c1b7293b464c8cbe9133441a94c9e44897529540c9c58fb8d`.

Both source powers are below `0.80`; EXP023 is permanently feasibility-only.

## Design sensitivity

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(TDO2_exposed > TDO2_reference) - P(TDO2_exposed < TDO2_reference)`

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
IDs within lineage/status cells. The exact inference seeds are `20272300`
(Avana) and `20272400` (KY), with 100,000 permutations and 10,000 bootstraps.

- Avana seed `20262300`: critical delta `-0.19735099337748344`, planning power
  `0.5184`;
- KY seed `20262400`: critical delta `-0.3103448275862069`, planning power
  `0.2861`.

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
Verify the exact `TDO2 (6999)` header before parsing values. T0 failures stop
without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**. The matrix proxy does not establish
functional APC loss, WNT causality, protein state, TDO2 inhibitor response,
treatment benefit, patient selection, or clinical utility.

The design receipt's normalized digest is computed as
`SHA256(json.dumps(payload_with_receipt_sha256_set_to_empty, indent=2,
sort_keys=True) + "\n")` encoded as UTF-8. The canonical roster digest is computed
from one compact sorted-key JSON object per sorted `(source, ModelID)` row,
followed by LF, with fields `source`, `model_id`, `lineage`, `screen_ids`,
`matrix_value`, and `status`.
