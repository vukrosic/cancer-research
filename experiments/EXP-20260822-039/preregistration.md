# EXP-20260822-039 preregistration — PBAF-loss proxy status to PARP1 dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does a composite damaging
proxy defined by PBRM1 or ARID2 matrix damage associate with stronger
source-specific PARP1 dependency in the frozen DepMap 23Q4 naive CRISPR
endpoint?

This is a reliability and transportability audit motivated by primary work on
PBRM1-deficiency synthetic lethality with PARP inhibitors. It is not a test of
isolated PBRM1 loss, ARID2 loss, homologous-recombination deficiency,
pharmacologic PARP inhibition, or clinical benefit.

## Outcome-free selection and seal

The target identity was selected from metadata and the endpoint header only.
No PARP1 score row or endpoint value was parsed before the candidate census,
design receipt, and selection seal were written. The primary source is the
Cancer Research study [PBRM1 Deficiency Confers Synthetic Lethality to DNA
Repair Inhibitors in Cancer](https://aacrjournals.org/cancerres/article/81/11/2888/673616/PBRM1-Deficiency-Confers-Synthetic-Lethality-to).

The frozen contrast is:

- exposure: PBRM1 or ARID2 matrix value `1` or `2`, labeled `damaging`;
- reference: both PBRM1 and ARID2 matrix values `0`, labeled `matrix_intact`;
- endpoint: `PARP1 (142)` from `ScreenNaiveGeneScore.csv`;
- source/model units: Avana `975`, KY `315`;
- status counts: Avana `49` damaging / `926` matrix-intact; KY `22`
  damaging / `293` matrix-intact;
- mixed-lineage counts: Avana `15`, KY `8`;
- canonical roster SHA-256:
  `6ab143e99b7d58d82a1b1e22b9948aacc5944ebe6daabe448505cd8735188af4`.

The design powers are Avana `0.6569` and KY `0.3913`. Because the frozen
paired-source contract requires every primary source to meet `0.80`, this
experiment is permanently `FEASIBILITY_ONLY`; no endpoint result can receive
a T2/confirmatory label.

## Design and inference

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(PARP1_exposed > PARP1_reference) - P(PARP1_exposed < PARP1_reference)`

More negative values indicate stronger dependency among composite damaging
models. Scores are never compared across screen families. The frozen design
uses 100,000 null permutations, 10,000 alternative simulations, PCG64,
sorted lineage/status/model order, average ranks, a Normal(0,1) null, and an
exposed Normal(-0.358286909243,1) alternative.

For inference, each eligible source/model is assigned the median of its
eligible screen rows. Within each source, models are partitioned by
lexicographically ordered lineage; only lineages containing both status
groups contribute. The permutation null preserves exposed counts within
lineage and the bootstrap resamples model IDs within lineage/status cells.
The inference seeds are `20273900` (Avana) and `20274000` (KY), with 100,000
permutations and 10,000 bootstraps.

## Primary gates

Each source is reported separately. The frozen gates are `delta < 0`,
`delta <= -0.20`, one-sided permutation `p <= 0.05`, bootstrap upper bound
`< 0`, at least five negative lineages, and no lineage delta `> +0.20`.
There is no source pooling, post hoc lineage exclusion, threshold change,
alternate status definition, or endpoint-derived subgroup rescue.

## T0 stop rules and claim contract

Before any endpoint value parse, verify the manifest, implementation boundary,
candidate census, design receipt, all input hashes, QC eligibility, screen
identity, lineages, composite matrix domain, status counts, mixed-lineage
counts, canonical roster, both design rows, and the sealed pre-endpoint
receipt. Verify the exact `PARP1 (142)` header before parsing values. T0
failures stop without inference. The strongest permitted result is **T1
descriptive association only; not T2/confirmatory**.

The claim boundary is limited to a composite PBRM1-or-ARID2 damaging-matrix
proxy association with source-specific PARP1 knockout dependency in frozen
DepMap 23Q4 cohorts. It does not establish isolated PBRM1 loss, ARID2 loss,
PBAF causality, HRD, PARP inhibitor response, mechanism, treatment benefit,
patient selection, or clinical utility.
