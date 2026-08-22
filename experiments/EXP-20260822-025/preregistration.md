# EXP-20260822-025 preregistration — CDKN2A proxy status to PELO dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does a damaging
matrix-defined CDKN2A proxy associate with stronger source-specific PELO
dependency in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability test of a proxy-defined association prompted by the
reported PELO vulnerability in 9p21.3-deleted or MSI-H cancers. It is not a
test of 9p21.3 copy-number loss, FOCAD loss, MSI-H status, mechanistic
causality, PELO inhibitor response, or clinical benefit.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` and
`design_census_receipt.json` before any PELO score row or endpoint value was
parsed. The primary biological source is the 2025 Nature study:
<https://www.nature.com/articles/s41586-024-08509-3>.

The frozen metadata contrast is:

- exposure: CDKN2A matrix value `1` or `2`, labeled `damaging`;
- reference: CDKN2A matrix value `0`, labeled `matrix_intact`;
- endpoint: `PELO (53918)` from `ScreenNaiveGeneScore.csv`;
- eligible source/model units: Avana `975`, KY `315`;
- status counts: Avana `110` damaging / `865` matrix-intact; KY `37`
  damaging / `278` matrix-intact;
- mixed-lineage counts: Avana `19`, KY `11`;
- canonical roster SHA-256:
  `df50a72ac86b161e16ebc5a2eb2b2f5c8d35151d94da4046c375f5ab0f603bb5`.

Avana planning power is `0.8958`, but KY planning power is `0.5265`; EXP025
is permanently feasibility-only because the paired source contract requires
all primary sources to meet the `0.80` threshold.

The source paper identifies biallelic 9p21.3 deletion and FOCAD loss as the
causal context for PELO dependency. CDKN2A loss is a common driver of the
deletion but is not equivalent to the cytoband or FOCAD state. The result can
therefore only test whether this available mutation proxy transports across
screen families.

## Design sensitivity

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(PELO_exposed > PELO_reference) - P(PELO_exposed < PELO_reference)`

More negative values indicate stronger dependency among damaging-status
models. Scores are never compared across screen families. The frozen design
uses 100,000 null permutations, 10,000 alternative simulations, PCG64, sorted
lineage/status/model order, average ranks, a Normal(0,1) null, and an exposed
Normal(-0.358286909243,1) alternative.

For inference, each eligible source/model unit is assigned the median of all
eligible screen rows for that source/model. Within each source, models are
partitioned by lexicographically ordered lineage; only lineages containing at
least one model in both status groups contribute. The one-sided permutation
null preserves exposed counts within lineage; the bootstrap resamples model
IDs within lineage/status cells. The exact inference seeds are `20272500`
(Avana) and `20272600` (KY), with 100,000 permutations and 10,000 bootstraps.

- Avana seed `20262500`: critical delta `-0.1147076674084564`, planning power
  `0.8958`;
- KY seed `20262600`: critical delta `-0.19471153846153846`, planning power
  `0.5265`.

Because KY is below the frozen `0.80` confirmatory threshold, the analysis
label is permanently `FEASIBILITY_ONLY`; no result can receive a
T2/confirmatory label.

## Primary gates

Each source must be reported separately: `delta < 0`, `delta <= -0.20`,
one-sided permutation `p <= 0.05`, bootstrap upper bound `< 0`, at least five
negative lineages, and no lineage delta `> +0.20`. No source pooling, post hoc
lineage exclusion, threshold change, alternate status definition, or
endpoint-derived subgroup rescue is allowed.

## T0 stop rules and claim contract

Before any endpoint value parse, verify the manifest, implementation boundary,
candidate census, design receipt, all input hashes, QC eligibility, screen
identity, lineages, matrix domain, status counts, mixed-lineage counts,
canonical roster, both design rows, and a sealed `pre_endpoint_receipt.json`.
Verify the exact `PELO (53918)` header before parsing values. T0 failures stop
without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**. The matrix proxy does not establish
9p21.3 deletion, FOCAD loss, MSI-H biology, mechanistic causality, PELO
inhibitor response, treatment benefit, patient selection, or clinical utility.

The design receipt's normalized digest is computed as
`SHA256(json.dumps(payload_with_receipt_sha256_set_to_empty, indent=2,
sort_keys=True) + "\n")` encoded as UTF-8. The canonical roster digest is computed
from one compact sorted-key JSON object per sorted `(source, ModelID)` row,
followed by LF, with fields `source`, `model_id`, `lineage`, `screen_ids`,
`matrix_value`, and `status`.
