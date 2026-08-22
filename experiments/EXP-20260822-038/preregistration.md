# EXP-20260822-038 preregistration — PTEN proxy status to ICMT dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does a damaging
matrix-defined PTEN proxy associate with stronger source-specific ICMT
dependency in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability and transportability audit motivated by a primary study
of ICMT dependency in PTEN-deficient triple-negative breast cancer. It is not
a test of triple-negative specificity, PTEN protein loss, PTEN copy-number
loss, pharmacologic ICMT inhibition, or clinical benefit.

## Outcome-free selection and seal

The target identity was selected from metadata and the endpoint header only.
No ICMT score row or endpoint value was parsed before the candidate census,
design receipt, and selection seal were written. The primary source is the
2025 study [Synthetic essentiality of isoprenylcysteine carboxylmethyltransferase in PTEN deficient triple negative breast cancer](https://link.springer.com/article/10.1186/s40164-025-00738-0).

The frozen contrast is:

- exposure: PTEN matrix value `1` or `2`, labeled `damaging`;
- reference: PTEN matrix value `0`, labeled `matrix_intact`;
- endpoint: `ICMT (23463)` from `ScreenNaiveGeneScore.csv`;
- source/model units: Avana `975`, KY `315`;
- status counts: Avana `94` damaging / `881` matrix-intact; KY `38`
  damaging / `277` matrix-intact;
- mixed-lineage counts: Avana `19`, KY `11`;
- canonical roster SHA-256:
  `73222b7a148f333399d580107e1ab64672b0920678f3a2a9789b3440f9c2d953`.

The design powers are Avana `0.8579` and KY `0.5297`. Because the frozen
paired-source contract requires every primary source to meet `0.80`, this
experiment is permanently `FEASIBILITY_ONLY`; no endpoint result can receive
a T2/confirmatory label.

## Design and inference

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(ICMT_exposed > ICMT_reference) - P(ICMT_exposed < ICMT_reference)`

More negative values indicate stronger dependency among damaging-status
models. Scores are never compared across screen families. The frozen design
uses 100,000 null permutations, 10,000 alternative simulations, PCG64,
sorted lineage/status/model order, average ranks, a Normal(0,1) null, and an
exposed Normal(-0.358286909243,1) alternative.

For inference, each eligible source/model is assigned the median of its
eligible screen rows. Within each source, models are partitioned by
lexicographically ordered lineage; only lineages containing both status
groups contribute. The permutation null preserves exposed counts within
lineage and the bootstrap resamples model IDs within lineage/status cells.
The inference seeds are `20273800` (Avana) and `20273900` (KY), with 100,000
permutations and 10,000 bootstraps.

Planning receipts:

- Avana seed `20263800`: critical delta `-0.12334911537503115`, power `0.8579`;
- KY seed `20263900`: critical delta `-0.19418758256274768`, power `0.5297`.

## Primary gates

Each source is reported separately. The frozen gates are `delta < 0`,
`delta <= -0.20`, one-sided permutation `p <= 0.05`, bootstrap upper bound
`< 0`, at least five negative lineages, and no lineage delta `> +0.20`.
There is no source pooling, post hoc lineage exclusion, threshold change,
alternate status definition, or endpoint-derived subgroup rescue.

## T0 stop rules and claim contract

Before any endpoint value parse, verify the manifest, implementation boundary,
candidate census, design receipt, all input hashes, QC eligibility, screen
identity, lineages, matrix domain, status counts, mixed-lineage counts,
canonical roster, both design rows, and the sealed pre-endpoint receipt.
Verify the exact `ICMT (23463)` header before parsing values. T0 failures stop
without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**.

The claim boundary is limited to a damaging-matrix PTEN proxy association with
source-specific ICMT knockout dependency in frozen DepMap 23Q4 cohorts. It
does not establish PTEN protein/copy-number loss, triple-negative specificity,
ICMT inhibitor response, mechanism, treatment benefit, patient selection, or
clinical utility.
