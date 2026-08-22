# EXP-20260822-023 execution log

## Frozen boundary

- selection seal commit: `7e77bd2c5c8936cc72d3af1fdd39c433a1ae408c`;
- protocol commit: `2b5ae5ae33c5cb999f82458e53397841cc6879ff`;
- implementation commit: `d48f8358de3d7bbee30bb483af4829d788123fac`;
- manifest commit: `211522e`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `TDO2 (6999)`;
- runner: `.venv/bin/python -m candrel.apc_tdo2_replication`.

## Execution

The bound runner completed in approximately `18.031` seconds and returned
exit code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before the TDO2 column was parsed.

The endpoint receipt reports `1,292` eligible screens seen and `1,290`
median-collapsed source/model values. The source-separated results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `9123ac9b0ec93d7c772cd37a2e3e7ab83666ffdbaed9fc4edfb5abe95dc36e18`;
- design sensitivity: `be87ae6b7e265948d789a0fdf02950ff6d9ea21a342f742f9579f975c3314ced`;
- endpoint scores: `05104dfe6becd13c908524748dac7061958fb87096cc35050caf09a653785425`;
- inference: `61d29592337f2a9f1d01c5fe4e3101f688428d6470f2e6ceab42e5c339c326aa`;
- normalized summary: `4ee2d29210ab51c4223ff81e57c0390d8b70dbf37f78c2960af139331f78e027`;
- pre-endpoint receipt: `3d97124d177407b9940a0833ca14aa560790057de2ac9e2eb6a527f56caa21c2`.
