# EXP-20260822-021 execution log

## Frozen boundary

- selection seal commit: `bd8eeae757dbc0221727202ed67b7b0936f1cdd9`;
- protocol commit: `ad16b66838d3e8413ce10b8f73f3a50cc093fd40`;
- implementation commit: `a94698339585e39ff045fb26901ae4092543bdd1`;
- manifest commit: `0667689`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `PTPN11 (5781)`;
- runner: `.venv/bin/python -m candrel.nf1_ptpn11_replication`.

## Execution

The bound runner completed in approximately `20.237` seconds and returned exit
code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before the PTPN11 column was parsed.

The endpoint receipt reports `1,292` eligible screens seen and `1,290` median-
collapsed source/model values. The source-separated results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `5523b2105d6313d82aa15db66f5ed784b0356bb67f8b3d64beb175614a2ae5f5`;
- design sensitivity: `194e137c72c2b8190c37e552dcc05f5b190d1bac78e47d7b74ff518878ba1759`;
- endpoint scores: `991c062f799e4c37d37dd4d9557583ff95dfafdae2965173605279fce1012c93`;
- inference: `eb19e60df392dcbff37992a176014a9f50a61649c35e06694c87f22ace26c408`;
- normalized summary: `b71b85bff9fec326e005f0f0885a0c648a780bce0f4a6e0409bd48df6c290f96`;
- pre-endpoint receipt: `7e15546d92bf6e20f52890e1c393053220a0a91821b8469cbef11687234bdaac`.
