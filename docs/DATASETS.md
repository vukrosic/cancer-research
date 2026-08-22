# Dataset ledger

## Cell Model Passports CRISPR KO

- Owner: Wellcome Sanger Institute.
- API: <https://api.cellmodelpassports.sanger.ac.uk/swagger/>
- API version observed: 1.23.0.
- Data version observed on portal: 2.19.0.
- CRISPR measurements observed: 22,218,273.
- Fields used initially: model ID, gene ID, source, QC flag, `fc_clean_qn`, `bf`, and
  `bf_scaled`.
- Sources represented: Broad and Sanger.
- Acquisition: narrow gene-level JSON API calls, locally cached and SHA-256 hashed.
- Redistribution: raw API responses are not committed pending a dataset-specific
  terms audit; only derived summary statistics and hashes are tracked.
- Usage policy checked 2026-08-22: public API use by individuals is permitted for
  non-commercial use without login; commercial and third-party website use requires
  consent. <https://cellmodelpassports.sanger.ac.uk/documentation/guides/API>
- Current model annotation frozen for the cohort audit:
  `model_list_20260814.csv`, SHA-256
  `eb43e92042ab430adabbbcf65e577459ac52d57df802eb388aea5865ff9b49aa`.
- MSI method: MSIsensor-pro score at least 7 is labelled MSI; lower scores are MSS.
  <https://depmap.sanger.ac.uk/documentation/cell-models/msi-ploidy-mutational-burden/>
- CRISPR processing documentation records overlap-informed ComBat correction for
  combined Broad/Sanger analysis and BAGEL2-derived source and combined fitness
  metrics. <https://depmap.sanger.ac.uk/documentation/datasets/wg-crispr-knockout/>

## DepMap Public 26Q1

- Portal: <https://depmap.org/portal/data_page/?tab=currentRelease>
- Breadbox screen metadata audited: 1,518 screens; among `PassesQC && CanInclude`,
  Avana 1,049, Brunello 13, Humagne-CD 70, KY 322, and TKOv3 4.
- `ScreenGeneEffect` is not used as a source-independent endpoint. The official
  26Q1 notes state that Chronos library correction affects both screen- and
  model-level gene-effect matrices.

## DepMap Public 23Q4

- Official record: <https://doi.org/10.25452/figshare.plus.24667905.v2>.
- `ScreenNaiveGeneScore.csv`: 469,333,423 bytes; official and observed MD5
  `265f8372e9cd0fad56c1a6b66b8a783d`; observed SHA-256
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.
- Download URL: <https://ndownloader.figshare.com/files/43347798>; retrieved
  2026-08-22 at approximately 11:01 Europe/Sarajevo.
- Semantics: LFC collapsed by mean of sequences and median of guides, computed per
  library-screen type and then concatenated.
- `AchillesScreenQCReport.csv`: SHA-256
  `fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407`.
- `ScreenSequenceMap.csv`: SHA-256
  `e4b99b4a6cd48c3957c5ada2abeeed1e1de319fe26526e76de6088ec73704c0b`.
- `Model.csv`: SHA-256
  `6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341`.
- `AchillesCommonEssentialControls.csv`: official MD5
  `1cbfa612d5d4d16e287bb9f23964839c`; observed SHA-256
  `496c5ec9eaa2f4c13dc00fd15a8e24df253afcc5a969d3956b7dd3d987640084`.
- `AchillesNonessentialControls.csv`: official MD5
  `9b210b75fdc9c9af6408941f730279ab`; observed SHA-256
  `2aacca44b6a79e7240518e6adbd89c70d7d895da91cd4c8b4d380529bc5b8e5e`.
- WRN (7486) is absent from both official control lists; EXP-006 uses this to rule out
  direct inclusion of WRN in the selected screen-control QC metrics.
- Avana denotes Broad screens and KY denotes Sanger screens. EXP-003 uses ranks
  within source and tissue; raw score magnitudes are not compared across libraries.
- Raw matrices remain gitignored. Hashes, derived model tables, code, and results
  are tracked.
- Terms checked at acquisition: DepMap portal terms apply;
  <https://depmap.org/portal/terms/>. This repository redistributes derived results,
  not the raw matrix.

## Storage policy

The full project may use at most 12 GB. Raw guide counts, BAM, FASTQ, and whole-slide
images are excluded from this program. Every external file requires URL, retrieval
time, version, size, SHA-256, and terms note.
