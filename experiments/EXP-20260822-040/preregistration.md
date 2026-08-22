# EXP-20260822-040 preregistration — NF1 proxy status to LAMTOR1 dependency

## Frozen question

Among eligible Avana and KY cancer cell-line models, does damaging-matrix NF1
status associate with stronger source-specific LAMTOR1 dependency in the
frozen DepMap 23Q4 naive CRISPR endpoint?

This is a reliability and transportability audit motivated by a primary
CRISPR-coupled NF1/LAMTOR1 study. It is not a test of NF1 protein loss, RAS
activity, mTOR pathway activation, LAMTOR1 pharmacology, or clinical benefit.

## Outcome-free selection and seal

The target identity was selected from metadata and the endpoint header only.
No LAMTOR1 score row or endpoint value was parsed before the candidate census,
design receipt, and selection seal were written. The primary source is the
study [CRISPR/Cas9-coupled affinity purification/mass spectrometry analysis of
NF1 and mTOR signaling](https://pubmed.ncbi.nlm.nih.gov/28174230/).

The frozen contrast is:

- exposure: NF1 matrix value `1` or `2`, labeled `damaging`;
- reference: NF1 matrix value `0`, labeled `matrix_intact`;
- endpoint: `LAMTOR1 (55004)` from `ScreenNaiveGeneScore.csv`;
- source/model units: Avana `975`, KY `315`;
- status counts: Avana `57` damaging / `918` matrix-intact; KY `21`
  damaging / `294` matrix-intact;
- mixed-lineage counts: Avana `15`, KY `9`;
- canonical roster SHA-256:
  `8c3229c5925e533688a9efb8979700d1f2d379a760d0672544a61073a8bfc375`.

The design powers are Avana `0.7192` and KY `0.4014`. Because the frozen
paired-source contract requires every primary source to meet `0.80`, this
experiment is permanently `FEASIBILITY_ONLY`; no endpoint result can receive
a T2/confirmatory label.

## Design and inference

The primary statistic is a source-specific, lineage-stratified Mann–Whitney
directional delta:

`delta = P(LAMTOR1_exposed > LAMTOR1_reference) - P(LAMTOR1_exposed < LAMTOR1_reference)`

More negative values indicate stronger dependency among NF1-damaging models.
Scores are never compared across screen families. The frozen design uses
100,000 null permutations, 10,000 alternative simulations, PCG64, sorted
lineage/status/model order, average ranks, a Normal(0,1) null, and an exposed
Normal(-0.358286909243,1) alternative.

For inference, each eligible source/model is assigned the median of its
eligible screen rows. Within each source, models are partitioned by
lexicographically ordered lineage; only lineages containing both status
groups contribute. The permutation null preserves exposed counts within
lineage and the bootstrap resamples model IDs within lineage/status cells.
The inference seeds are `20274000` (Avana) and `20274100` (KY), with 100,000
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
identity, lineages, matrix domain, status counts, mixed-lineage counts,
canonical roster, both design rows, and the sealed pre-endpoint receipt.
Verify the exact `LAMTOR1 (55004)` header before parsing values. T0 failures
stop without inference. The strongest permitted result is **T1 descriptive
association only; not T2/confirmatory**.

The claim boundary is limited to an NF1 damaging-matrix proxy association with
source-specific LAMTOR1 knockout dependency in frozen DepMap 23Q4 cohorts. It
does not establish NF1 protein loss, RAS/mTOR mechanism, LAMTOR1 inhibitor
response, treatment benefit, patient selection, or clinical utility.
