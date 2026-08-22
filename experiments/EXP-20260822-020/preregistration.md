# EXP-20260822-020 preregistration — TP53 damaging status to WEE1 dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does damaging
matrix-defined TP53 status associate with stronger source-specific WEE1
dependency in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability test of a proxy-defined association. It is not a test of
functional TP53 loss, TP53 protein state, KRAS co-mutation, WEE1 inhibitor
response, or clinical benefit.

## Outcome-free candidate selection

The selected direction was sealed in `candidate_census.json` and
`design_census_receipt.json` before any WEE1 score row or endpoint value was
parsed. The primary biological sources are the CRISPR/functional-genomic and
TP53-context studies by Fukuda et al. and Joshi et al.:

- <https://pubmed.ncbi.nlm.nih.gov/38776912/>
- <https://pubmed.ncbi.nlm.nih.gov/28978051/>

Those studies support a restricted TP53-associated WEE1 vulnerability, but
they do not validate this exact DepMap proxy-defined replication question.

The frozen metadata contrast is:

- exposure: TP53 matrix value `1` or `2`, labeled `damaging`;
- reference: TP53 matrix value `0`, labeled `matrix_intact`;
- endpoint: `WEE1 (7465)` from `ScreenNaiveGeneScore.csv`;
- eligible source/model units: Avana `975`, KY `315`;
- status counts: Avana `610` damaging / `365` matrix-intact; KY `233`
  damaging / `82` matrix-intact;
- mixed-lineage counts: Avana `25`, KY `16`;
- canonical roster SHA-256:
  `61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`.

EXP020 is distinct from EXP017 because both the endpoint gene and status
orientation change: EXP017 tested matrix-intact TP53 against MDM2, whereas
EXP020 tests damaging-matrix TP53 against WEE1.

## Design sensitivity

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(WEE1_exposed > WEE1_reference) - P(WEE1_exposed < WEE1_reference)`

More negative values indicate stronger dependency among damaging-status
models. Scores are never compared across screen families. The frozen design
uses 100,000 null permutations, 10,000 alternative simulations, PCG64,
sorted lineage/status/model order, average ranks, a Normal(0,1) null, and an
exposed Normal(-0.358286909243,1) alternative. The exact receipt is bound by
the manifest and sealed before endpoint access.

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
seeds are `20272000` (Avana) and `20272100` (KY).

- Avana seed `20262000`: critical delta `-0.07859134565733761`, planning power
  `0.9948`;
- KY seed `20262100`: critical delta `-0.14327062228654125`, planning power
  `0.7564`.

Because KY planning power is below the frozen `0.80` confirmatory threshold,
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

Before any endpoint value parse, the runner must:

- verify the manifest, implementation boundary, candidate census, design
  receipt, and all input hashes;
- verify QC eligibility, exact ScreenID-to-ModelID identity, lineages, matrix
  domain `{0,1,2}`, source/model counts, status counts, mixed-lineage counts,
  and canonical roster hash;
- recompute both design-sensitivity rows and match the frozen receipt;
- write and hash the context ledger and design-sensitivity receipt into a
  sealed `pre_endpoint_receipt.json`;
- verify the endpoint file SHA-256 and exact `WEE1 (7465)` header identity
  immediately before parsing values.

Failures stop with a typed T0 receipt. A missing/non-numeric/non-finite TP53
matrix value is `T0_MATRIX_COVERAGE`; input hash drift is `T0_INPUT_HASH`;
schema drift is `T0_SCHEMA_HEADER`; endpoint identity or coverage drift is a
typed T0 endpoint stop. No inference is computed after a T0 stop.

After the pre-endpoint receipt is sealed, the runner may parse the WEE1
column, median-collapse duplicate eligible screens within source/model, and
compute the frozen source-specific inference. The expected process exit code
is `2` because `overall_pass` is permanently false for a feasibility-only
experiment.

## Claim contract

The strongest permitted result is **T1 descriptive association only; not
T2/confirmatory**. Even a nominal pass would mean only that the
damaging-matrix TP53 proxy is associated with source-specific WEE1 knockout
dependency in these frozen cell-line cohorts. It cannot establish functional
TP53 loss, TP53 protein state, KRAS restriction, WEE1 inhibitor sensitivity,
therapeutic window, patient selection, treatment benefit, or clinical utility.

The design receipt's normalized digest is computed as
`SHA256(json.dumps(payload_with_receipt_sha256_set_to_empty, indent=2,
sort_keys=True) + "\n")` encoded as UTF-8. The canonical roster digest is
computed from one compact sorted-key JSON object per sorted `(source, ModelID)`
row, followed by LF, with fields `source`, `model_id`, `lineage`, `screen_ids`,
`matrix_value`, and `status`.
