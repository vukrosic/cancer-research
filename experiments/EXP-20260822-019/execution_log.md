# EXP-20260822-019 execution log

## Run

- Result bundle mtime: `2026-08-22T18:01:40+0200`.
- Command: `UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-pten-pik3cb-replication`.
- Exit code: `2`, expected because the runner permanently labels this
  feasibility-only and sets `overall_pass: false`.
- Endpoint parsing occurred only after the implementation boundary, endpoint
  hash, context ledger, design sensitivity, and pre-endpoint receipt passed.
- The runner wrote the complete five-file result bundle atomically.

## Receipts

- Eligible screens: `1292`; canonical source/model units: `1290` (`975` Avana,
  `315` KY).
- Canonical roster SHA-256:
  `73222b7a148f333399d580107e1ab64672b0920678f3a2a9789b3440f9c2d953`.
- Pre-endpoint receipt SHA-256:
  `db091d171a2b1856beed7da67ad316d5661fc78d4253ebc1c11593328cd85758`.
- Endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.
- Summary normalized self-digest:
  `bef5b62da8d93a9c3ab4aeec3e8ab3dde0ce1b311e28dba6507505ec53e1ec40`.

## Claim safety

The terminal summary contains `analysis_label: FEASIBILITY_ONLY`,
`confirmatory_claim: false`, and `overall_pass: false`. The KY planning power
was `0.5375`, below the frozen `0.80` confirmatory threshold, and the two
source families did not pass the same nominal reliability pattern. No PTEN-null
biology, inhibitor, treatment, clinical, pooled, or confirmatory claim is
permitted.
