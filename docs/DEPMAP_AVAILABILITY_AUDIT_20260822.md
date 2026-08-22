# DepMap screen availability audit — 2026-08-22

## Scope and outcome blinding

This is a label-and-provenance audit. No MSI-conditioned WRN score was read or
computed while producing it. The audit used screen metadata, model identifiers,
lineage labels, MSI/MSS labels, release documentation, and file catalogs only.

## Current 26Q1 finding

The public Breadbox API exposes `ScreenGeneEffect` for 1,518 screens. Among
screens with both `PassesQC` and `CanInclude`, library counts were Avana 1,049,
Brunello 13, Humagne-CD 70, KY 322, and TKOv3 4.

For the frozen colorectal definition in the Cell Model Passports model list:

- Avana: 7 MSI and 17 MSS unique models;
- any non-KY screen: 8 MSI and 17 MSS unique models, with HCT-116 supplied only
  by a Brunello screen;
- KY: 10 MSI and 20 MSS unique models.

This does not authorize a current-release biological test. DepMap's 26Q1 release
notes state that library correction is applied to both `CRISPRGeneEffect.csv` and
`ScreenGeneEffect.csv` for genes present in more than one screen batch. Selecting
non-KY rows after that joint correction does not create a source-independent Broad
endpoint.

## Stable 23Q4 source-separated option

The official DepMap 23Q4 Figshare release provides:

- `ScreenNaiveGeneScore.csv`: LFC collapsed per library-screen type and then
  concatenated; MD5 `265f8372e9cd0fad56c1a6b66b8a783d`;
- `ScreenGeneEffectUncorrected.csv`: Chronos processed by library and then
  concatenated; MD5 `a143942e36d172a4afc31dd75470886a`;
- `AchillesScreenQCReport.csv`: screen/QC/library mapping;
- `ScreenSequenceMap.csv`: sequence-to-screen mapping.

The 23Q4 CRC-only eligible cohort still fails the frozen Broad minimum:

| Library/source | MSI | MSS |
|---|---:|---:|
| Avana/Broad | 7 | 18 |
| KY/Sanger | 10 | 20 |

The CRC failure is preserved. It is not repaired by lowering the minimum, adding
an outcome-selected model, or treating combined scores as independent.

## Preregistered successor

Before downloading `ScreenNaiveGeneScore.csv`, a separate four-tissue experiment
was frozen as EXP-20260822-003. It covers Large Intestine, Ovary, Endometrium, and
Stomach and uses within-tissue comparisons, so between-tissue score differences do
not contribute to the primary effect. This is a new population and cannot rescue
the failed CRC-only adequacy gate.

## Sources

- DepMap Public 26Q1 release notes:
  <https://forum.depmap.org/t/announcing-the-26q1-release/4606>
- DepMap Public 23Q4 Figshare record:
  <https://doi.org/10.25452/figshare.plus.24667905.v2>
- DepMap data page file descriptions:
  <https://depmap.org/portal/data_page/?tab=allData>
- Official statement that Avana is Broad and KY is Sanger:
  <https://forum.depmap.org/t/march-family-genes-are-missing-from-crispr-chronos-data/2384/3>

