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
- Candidate later files: model metadata, screen map, gene effect, copy number,
  mutation, and expression subsets.
- Observed full gene-effect file size: about 440.6 MB.
- Use: current Broad discovery and release-stability analyses.

## Storage policy

The full project may use at most 12 GB. Raw guide counts, BAM, FASTQ, and whole-slide
images are excluded from this program. Every external file requires URL, retrieval
time, version, size, SHA-256, and terms note.
