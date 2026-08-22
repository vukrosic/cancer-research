# EXP-20260822-037 preregistration — CDKN2A proxy status to MAT2A dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does a damaging
matrix-defined CDKN2A proxy associate with stronger source-specific MAT2A
dependency in the frozen DepMap 23Q4 naive CRISPR screen endpoint?

This is a reliability test of a proxy-defined association motivated by the
MTAP-deletion/MAT2A synthetic-lethal program. It is not a test of MTAP
homozygous deletion, CDKN2A copy-number deletion, PRMT5 mechanism, MAT2A
inhibitor response, treatment benefit, or patient selection.

## Outcome-free selection and seal

The target identity was selected from metadata and the endpoint header only.
No MAT2A score row or endpoint value was parsed before the candidate census,
design receipt, and selection seal were written. The primary source is the
phase I MAT2A inhibitor report:
<https://www.nature.com/articles/s41467-024-55316-5>.

The frozen contrast is:

- exposure: CDKN2A matrix value `1` or `2`, labeled `damaging`;
- reference: CDKN2A matrix value `0`, labeled `matrix_intact`;
- endpoint: `MAT2A (4144)` from `ScreenNaiveGeneScore.csv`;
- source/model units: Avana `975`, KY `315`;
- status counts: Avana `110` damaging / `865` matrix-intact; KY `37`
  damaging / `278` matrix-intact;
- mixed-lineage counts: Avana `19`, KY `11`;
- canonical roster SHA-256:
  `df50a72ac86b161e16ebc5a2eb2b2f5c8d35151d94da4046c375f5ab0f603bb5`.

The design powers are Avana `0.8906` and KY `0.5361`. Because the frozen
paired-source contract requires every primary source to meet `0.80`, this
experiment is permanently `FEASIBILITY_ONLY`; no endpoint result can receive
a T2/confirmatory label.

The clinical source describes MAT2A inhibition as a strategy for homozygous
MTAP-deleted cancers and notes that CDKN2A deletion is an imperfect surrogate
for MTAP loss. The repository exposure is a damaging-mutation matrix proxy,
not even the clinical CDKN2A-deletion surrogate. This distinction is part of
the preregistered claim boundary.

## Design and inference

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(MAT2A_exposed > MAT2A_reference) - P(MAT2A_exposed < MAT2A_reference)`

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
The inference seeds are `20273700` (Avana) and `20273800` (KY), with 100,000
permutations and 10,000 bootstraps.

Planning receipts:

- Avana seed `20263700`: critical delta `-0.11592150515881045`, power `0.8906`;
- KY seed `20263800`: critical delta `-0.19230769230769232`, power `0.5361`.

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
Verify the exact `MAT2A (4144)` header before parsing values. T0 failures stop
without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**.

The claim boundary is limited to a damaging-matrix CDKN2A proxy association
with source-specific MAT2A knockout dependency in frozen DepMap 23Q4 cohorts.
It does not establish MTAP deletion, CDKN2A deletion, PRMT5 mechanism, MAT2A
inhibitor response, treatment benefit, patient selection, or clinical utility.
