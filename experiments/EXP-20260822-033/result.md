# EXP033 result — ARID1A damaging proxy to ATR dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `ATR (545)` / ataxia telangiectasia and Rad3-related from the frozen
  DepMap 23Q4 naive CRISPR screen;
- exposure: ARID1A damaging proxy when the matrix value is `1` or `2`;
- reference: ARID1A matrix value `0`;
- canonical roster SHA-256:
  `62f8bf69649eb375de12daed222a50a4bc3b3df39c40f0e614845fbab12ab9ed`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from a study reporting selective
ATR-inhibitor sensitivity after ARID1A defects
([Nature Communications study](https://www.nature.com/articles/ncomms13837)).
EXP033 tests only an ARID1A damaging-matrix proxy against genetic ATR knockout
dependency; it is not a pharmacology experiment.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | `-0.0893048128` | 3740 | 0.1150588494 | `[-0.2069518717, 0.0294117647]` | 9 | `+1.0` | FAIL |
| KY | `-0.0151691949` | 857 | 0.4469455305 | `[-0.2298716453, 0.1971995333]` | 4 | `+0.5555555556` | FAIL |

Avana was directionally negative but did not reach the preregistered effect,
permutation, bootstrap, or lineage-consistency gates. Its largest positive
lineage delta was Cervix `+1.0`, and Bowel, Liver, Lymphoid, and Soft Tissue
also exceeded the no-positive-lineage threshold.

KY was near-null and uncertain. It had only four negative lineage estimates,
with positive heterogeneity including Lymphoid `+0.5555555556`, and failed the
effect, permutation, bootstrap, negative-lineage, and no-positive-lineage
gates.

The outcome-free planning powers were Avana `0.8666` and KY `0.5810`; the KY
power prevents any confirmatory two-source claim.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
ARID1A damaging-matrix proxy did not show a robust source-consistent association
with genetic ATR dependency. This does not refute ARID1A-defect/ATR-inhibitor
biology; the proxy, endpoint, cell-line composition, and genetic-versus-drug
mechanism are not equivalent.

This does not establish functional ARID1A loss, ATR-inhibitor efficacy,
DNA-damage or replication-stress mechanism, causal synthetic lethality,
treatment benefit, patient selection, clinical utility, or a confirmatory
claim. No source pooling, post hoc lineage exclusion, threshold change, or
proxy rescue was used.

## Artifact receipts

- `context_ledger.csv`: `d808bd50211f644697a2606504e94e8a0cf588c212c8f4e651114821f36b2aad`
- `design_sensitivity.csv`: `e3d31f068ddeecb4a6aafa182800c50b3ac938c9fddb157a7fb1263dcac3d271`
- `endpoint_scores.csv`: `866ff59581feb9c8a8da54482a492c7647a54a65e449c4024b1999b993f28052`
- `inference.csv`: `dd10f50542d67f98f45d368d905b6ce2de195fbc0671c817aa29e417d9b52502`
- normalized `summary.json` digest: `ce2347a2ce01e2135fc93c353d352353a71bbb07c889a9a39d0d9ea6d4ffb8f7`
- pre-endpoint receipt: `3eb99863b1e5d07deef863b336758529bb0cf3e4c9c758373b705ee4284c3170`
