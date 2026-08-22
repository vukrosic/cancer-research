# EXP-20260822-015 execution log

## Attempt 001 — 2026-08-22 15:59:54 +0200

- Command: `UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-arid1a-replication`
- Outcome: `ERROR_INTEGRITY`; no result directory was published.
- Durable error: `error_receipt.json` reported `invalid Model.csv identity:
  ACH-003132`.
- Endpoint boundary: `endpoint_opened=false` in substance. The stop occurred
  while loading hash-locked `Model.csv`, before context completion, before the
  pre-endpoint receipt, and before `load_endpoint` could open
  `ScreenNaiveGeneScore.csv`; no ARID1B score was parsed.
- Cause: the first implementation treated any blank lineage anywhere in
  `Model.csv` as invalid. The offending model is a non-eligible non-cancer
  model; the preregistered contract requires nonblank lineage for joined
  eligible models, not for unrelated rows in the full metadata table.
- Correction: allow blank lineage in unrelated metadata rows, then reject it
  when an eligible QC/model join selects that model. This preserves the exact
  eligible-model identity gate without excluding unrelated metadata.
