# EXP-20260822-017 execution log

## Run

- Timestamp from result artifact: `2026-08-22T17:10:46+0200`.
- Command: `UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-tp53-mdm2-replication`.
- Exit code: `2`, expected because the runner permanently labels this
  feasibility-only and sets `overall_pass: false`.
- Endpoint file was opened only after the pre-endpoint context ledger and design
  receipt were sealed.
- No results directory existed before the run; the runner wrote the complete
  five-file result bundle atomically.

## Receipts

- Eligible screens: `1292`; canonical source/model units: `1290` (`975` Avana,
  `315` KY).
- Canonical roster SHA-256:
  `61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`.
- Pre-endpoint receipt SHA-256:
  `f33c2959b0183c9c1f5a584be2c0a529b1d5cc99f7891b6dcc2b4175ffe2a724`.
- Endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.
- Summary normalized self-digest:
  `671d2de04d66c7ad2e39dbe98b331b3b3941c0a822b2897656fec79d74860b66`.

## Claim safety

The terminal summary contains `analysis_label: FEASIBILITY_ONLY`,
`confirmatory_claim: false`, and `overall_pass: false`. The KY planning power
was `0.7521`, below the frozen `0.80` confirmatory threshold, so no two-source
confirmatory claim is permitted regardless of nominal endpoint gates.
