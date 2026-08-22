# EXP-20260822-026 preregistration — PTEN proxy status to PAPSS1 dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does a damaging
matrix-defined PTEN proxy associate with stronger source-specific PAPSS1
dependency in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a transportability audit of a patient-derived collateral-lethality
hypothesis. It is not a test of PTEN copy-number deletion, PAPSS2 co-deletion,
patient tumor biology, causal collateral lethality, inhibitor response, or
clinical benefit.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` and
`design_census_receipt.json` before any PAPSS1 score row or endpoint value was
parsed. The primary source is the Nature Cancer translational dependency map:
<https://doi.org/10.1038/s43018-024-00789-y>.

The frozen metadata contrast is:

- exposure: PTEN matrix value `1` or `2`, labeled `damaging`;
- reference: PTEN matrix value `0`, labeled `matrix_intact`;
- endpoint: `PAPSS1 (9061)` from `ScreenNaiveGeneScore.csv`;
- eligible source/model units: Avana `975`, KY `315`;
- status counts: Avana `94` damaging / `881` matrix-intact; KY `38`
  damaging / `277` matrix-intact;
- mixed-lineage counts: Avana `19`, KY `11`;
- canonical roster SHA-256:
  `73222b7a148f333399d580107e1ab64672b0920678f3a2a9789b3440f9c2d953`.

Avana planning power is `0.8526`, but KY planning power is `0.5377`; EXP026
is permanently feasibility-only because the paired source contract requires
all primary sources to meet the `0.80` threshold.

The source study reports that PAPSS1/PAPSS2 synthetic lethality is visible in
patient-translational settings and is driven by collateral PAPSS2 loss near
PTEN, while the interaction is not detectable in ordinary DepMap cell lines.
This experiment tests that model-system boundary with an imperfect PTEN
mutation proxy and must not be interpreted as a patient-level replication.

## Design sensitivity

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(PAPSS1_exposed > PAPSS1_reference) - P(PAPSS1_exposed < PAPSS1_reference)`

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
IDs within lineage/status cells. The exact inference seeds are `20272600`
(Avana) and `20272700` (KY), with 100,000 permutations and 10,000 bootstraps.

- Avana seed `20262600`: critical delta `-0.12384749563917269`, planning power
  `0.8526`;
- KY seed `20262700`: critical delta `-0.19418758256274768`, planning power
  `0.5377`.

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
Verify the exact `PAPSS1 (9061)` header before parsing values. T0 failures stop
without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**. The matrix proxy does not establish
PTEN deletion, PAPSS2 co-deletion, patient tumor biology, causal collateral
lethality, inhibitor response, treatment benefit, or clinical utility.

The design receipt's normalized digest is computed as
`SHA256(json.dumps(payload_with_receipt_sha256_set_to_empty, indent=2,
sort_keys=True) + "\n")` encoded as UTF-8. The canonical roster digest is computed
from one compact sorted-key JSON object per sorted `(source, ModelID)` row,
followed by LF, with fields `source`, `model_id`, `lineage`, `screen_ids`,
`matrix_value`, and `status`.
