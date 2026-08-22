# EXP-20260822-027 result — ARID1A proxy status to EZH2 dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `EZH2 (2146)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: ARID1A matrix value `1` or `2`, labeled `damaging`;
- reference: ARID1A matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `62f8bf69649eb375de12daed222a50a4bc3b3df39c40f0e614845fbab12ab9ed`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from metadata and the primary
ARID1A/EZH2 literature:
[Nature Medicine study](https://www.nature.com/articles/nm.3799). That work
reports an ARID1A-mutant/EZH2-inhibition interaction in ovarian cancer models.
This experiment uses an ARID1A damaging-matrix proxy and a genetic EZH2 screen
endpoint; it does not recreate pharmacologic EZH2 inhibition or prove that the
two contexts are biologically equivalent.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.1925133689839572 | 3740 | 0.0045799542004579955 | [-0.3165909090909091, -0.0679144385026738] | 11 | +0.35 | FAIL |
| KY | -0.08284714119019837 | 857 | 0.23229767702322976 | [-0.2485414235705951, 0.08284714119019837] | 5 | +0.2698412698412698 | FAIL |

Avana was negative and statistically separated under the preregistered
permutation test, but it missed the required delta threshold of `-0.20` and
failed the no-positive-lineage gate. Its positive lineage deltas included
Biliary Tract `+0.35`, Lymphoid `+0.24571428571428572`, and Kidney
`+0.15151515151515152`.

KY was weakly negative but uncertain: the bootstrap interval crossed zero,
the permutation p-value exceeded 0.05, and positive lineage deltas included
Bowel `+0.2698412698412698`, Uterus `+0.25`, and CNS/Brain `+0.125`.

Avana planning power was `0.8621`, but KY planning power was `0.5760`; the
paired experiment is permanently feasibility-only.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
ARID1A damaging-matrix proxy showed a negative but sub-threshold and
lineage-heterogeneous association with Avana EZH2 dependency, while KY was
weakly negative and uncertain. Neither source passed the complete
preregistered gate contract.

This does not establish functional ARID1A loss, ovarian-specific biology,
pharmacologic EZH2 inhibition, causal synthetic lethality, inhibitor response,
treatment benefit, patient selection, or clinical utility. No source pooling,
post hoc lineage exclusion, threshold change, or proxy rescue was used.

## Artifact receipts

- `context_ledger.csv`: `d808bd50211f644697a2606504e94e8a0cf588c212c8f4e651114821f36b2aad`
- `design_sensitivity.csv`: `c47db1bf4e19ee9af4978bad1ddc4c4f3c1de49bf0f84dafb32c8ce2dd9c6993`
- `endpoint_scores.csv`: `7925b76cd2606684633532c74107cb6305643d51dcb6012946312063778ae59c`
- `inference.csv`: `1534c8682958c01ac77f248350e9d36c77aaf824e18895b233ad02be5a50ab97`
- normalized `summary.json` digest: `dcf59dc6fc31ade64fa631258f0a30ba43e0eb1cb3e4fa293cb5f220a3765053`
- pre-endpoint receipt: `c5d8fd516a70641842e65fa1b98ab20a1f9eb72234a9a20e8769d6e8105e6b8e`
