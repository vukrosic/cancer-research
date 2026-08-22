# EXP-20260822-026 execution log

## Frozen boundary

- protocol commit: `50e87ec6f85b63b4485c7ffb9251dc18d3b4cb3a`;
- selection seal commit: `1594ac0fa0ddde5dd55b5711191942656b50147d`;
- implementation commit: `b70e8681ed8ea4797d340984ab0b78c636c81806`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `PAPSS1 (9061)`;
- runner: `.venv/bin/python -m candrel.pten_papss1_replication`.

## Execution

The bound runner completed in approximately `21.71` seconds and returned exit
code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before the PAPSS1 column was parsed.

The endpoint receipt reports `1,292` eligible screens seen and `1,290`
median-collapsed source/model values. The source-separated results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `48bf8b95574dc6b79acdb31acbb08cbc9166ffd4c04de600142df9c03baaa11b`;
- design sensitivity: `7cb02134904ee4ecbbb1dce4b72e6c712fcb12ad17ae7d19e0d86ccf239502ed`;
- endpoint scores: `b9b0c7003a9a0e635a7998f56865ec389a33a8726629e7986a96238904995005`;
- inference: `059c58b1ec74981afe6b979365a39ec3849a41d020cda5623d3d5e9f98e88c9a`;
- normalized summary: `722cc5130581630c008a74047a2a2f9f84b478ee5aa17df76146e2f82909dc6d`;
- pre-endpoint receipt: `761192af9227ae38583d3aa0d21cbbb2236775fb2737d340671b4ff6633100d8`.
