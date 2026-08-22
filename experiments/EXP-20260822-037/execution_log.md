# EXP037 execution log

## Frozen boundary

- selection checkpoint: `d0832f7`;
- implementation commit: `8bf9e4c`;
- manifest binding commit: `23e75e1`;
- endpoint target column: `MAT2A (4144)`;
- status column: `CDKN2A (1029)`;
- runner: `.venv/bin/python -m candrel.cdkn2a_mat2a_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `20.18` seconds and returned exit
code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before MAT2A scores were parsed. It reports
`1,292` eligible screens, `1,290` source/model values, and
`sealed_before_endpoint: true`.

This runner was executed exactly once. The results directory did not exist
before execution; no prior result files or endpoint values were present.

## Result receipts

- context ledger: `1c6b1df176468f25de48585b97d456b7e83c3d2fa63352a31a527b4f3263e725`;
- design sensitivity: `d79398107dea3d888ca9c10be3855eef242cb16aa88d9ed477398fdf59730260`;
- endpoint scores: `41ed3ccd4d7679247fc9bdfac663e34f524412c73bd078d947a6fbe6ce2ae5d6`;
- inference: `3fc988c9ce1d20c008a5866853536f5fd788b10ff52303a30e7a5fc27a0b49ad`;
- normalized `summary.json`: `99f3330dc3f17949aaf8ed5c691206d01c61f639edb5cf243922ef45a6d6562c`;
- pre-endpoint receipt: `6a977c2df3823d22b92fa4f0027f15dd00f22850fade46a3f6b75ea22e22105e`.

## Verification

The independent direct-engine audit returned `GO` and recomputed the same
summary digest and source-specific statistics from the committed result
ledgers and frozen engine. The heartbeat remains deleted by user request.
