# EXP-20260822-021 preregistration — NF1 damaging status to PTPN11 dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does damaging
matrix-defined NF1 status associate with stronger source-specific PTPN11
dependency in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability test of a proxy-defined association. It is not a test of
functional NF1 loss, RAS-pathway causality, SHP2 inhibitor response, or clinical
benefit.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` and
`design_census_receipt.json` before any PTPN11 score row or endpoint value was
parsed. The primary biological source is the NF1/PTPN11 dependency study:
<https://pmc.ncbi.nlm.nih.gov/articles/PMC6115280/>.

The frozen metadata contrast is:

- exposure: NF1 matrix value `1` or `2`, labeled `damaging`;
- reference: NF1 matrix value `0`, labeled `matrix_intact`;
- endpoint: `PTPN11 (5781)` from `ScreenNaiveGeneScore.csv`;
- eligible source/model units: Avana `975`, KY `315`;
- status counts: Avana `57` damaging / `918` matrix-intact; KY `21`
  damaging / `294` matrix-intact;
- mixed-lineage counts: Avana `15`, KY `9`;
- canonical roster SHA-256:
  `8c3229c5925e533688a9efb8979700d1f2d379a760d0672544a61073a8bfc375`.

No remaining reviewed candidate reached KY planning power `0.80`. EXP021 is
therefore permanently feasibility-only before any PTPN11 endpoint value is
seen.

## Design sensitivity

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(PTPN11_exposed > PTPN11_reference) - P(PTPN11_exposed < PTPN11_reference)`

More negative values indicate stronger dependency among damaging-status models.
Scores are never compared across screen families. The frozen design uses
100,000 null permutations, 10,000 alternative simulations, PCG64, sorted
lineage/status/model order, average ranks, a Normal(0,1) null, and an exposed
Normal(-0.358286909243,1) alternative.

For inference, each eligible source/model unit is assigned the median of all
eligible screen rows for that source/model. Within each source, models are
partitioned by lexicographically ordered lineage; only lineages containing at
least one model in both status groups contribute. For a contributing lineage,
the delta numerator is the number of exposed/reference pairs with exposed
score greater than reference score minus the number with exposed score less
than reference score; the reported delta is the sum of lineage numerators
divided by the sum of `n_exposed * n_reference` across contributing lineages.

The one-sided permutation null independently reshuffles exposed labels within
each lineage while preserving each lineage's exposed count, uses the
source-specific PCG64 inference seed, runs 100,000 draws in batches of 1,000,
and reports `(1 + count(null_delta <= observed_delta)) / (100000 + 1)`. The
bootstrap independently resamples model IDs with replacement within each
lineage/status cell for 10,000 draws using the same source-specific generator
after the permutation draws, recomputes the same fixed-denominator delta, and
uses NumPy's linear quantile method at 0.025 and 0.975. The exact inference
seeds are `20272100` (Avana) and `20272200` (KY).

- Avana seed `20262100`: critical delta `-0.14961776483436476`, planning power
  `0.7173`;
- KY seed `20262200`: critical delta `-0.23846153846153847`, planning power
  `0.4028`.

Because both source powers are below the frozen `0.80` confirmatory threshold,
the analysis label is permanently `FEASIBILITY_ONLY`; no result can receive a
T2/confirmatory label.

## Primary gates

Each source must be reported separately. The nominal gates are:

1. `delta < 0`;
2. `delta <= -0.20`;
3. one-sided lower-tail permutation `p <= 0.05`;
4. bootstrap 95% upper bound `< 0`;
5. at least five contributing lineages have negative deltas;
6. no contributing lineage has delta `> +0.20`.

No source pooling, post hoc lineage exclusion, threshold change, alternate
status definition, or endpoint-derived subgroup rescue is allowed.

## T0 stop rules and sequencing

Before any endpoint value parse, the runner must verify the manifest,
implementation boundary, candidate census, design receipt, all input hashes,
QC eligibility, exact screen identity, lineages, matrix domain `{0,1,2}`, source
and status counts, mixed-lineage counts, canonical roster hash, and both design
rows. It must write and hash a sealed `pre_endpoint_receipt.json` and verify
the endpoint file SHA-256 and exact `PTPN11 (5781)` header identity immediately
before parsing values.

Failures stop with typed T0 receipts. No inference is computed after a T0 stop.
After the pre-endpoint receipt is sealed, the runner may parse PTPN11 values,
median-collapse duplicate eligible screens within source/model, and compute the
frozen source-specific inference. The expected process exit code is `2` because
`overall_pass` is permanently false for a feasibility-only experiment.

## Claim contract

The strongest permitted result is **T1 descriptive association only; not
T2/confirmatory**. Even a nominal pass would mean only that the
damaging-matrix NF1 proxy is associated with source-specific PTPN11 knockout
dependency in these frozen cell-line cohorts. It cannot establish functional
NF1 loss, biallelic status, RAS-pathway causality, SHP2 inhibitor sensitivity,
therapeutic window, patient selection, treatment benefit, or clinical utility.

The design receipt's normalized digest is computed as
`SHA256(json.dumps(payload_with_receipt_sha256_set_to_empty, indent=2,
sort_keys=True) + "\n")` encoded as UTF-8. The canonical roster digest is
computed from one compact sorted-key JSON object per sorted `(source, ModelID)`
row, followed by LF, with fields `source`, `model_id`, `lineage`, `screen_ids`,
`matrix_value`, and `status`.
