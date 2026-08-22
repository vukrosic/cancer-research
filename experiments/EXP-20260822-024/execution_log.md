# EXP-20260822-024 execution log

## Frozen boundary

- selection seal commit: `311d6b212f9c3c7564e4279ee41fbd59eab61f3e`;
- protocol commit: `5af7d8cf583abf46ad0a4ca3e598519020d70163`;
- implementation commit: `f6ea8341bcbabd0ca15c009c52d868222ec9dc3e`;
- manifest commit: `bf86eca`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `KMT2C (58508)`;
- runner: `.venv/bin/python -m candrel.kmt2d_kmt2c_replication`.

## Execution

The bound runner completed in approximately `19.196` seconds and returned
exit code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before the KMT2C column was parsed.

The endpoint receipt reports `1,292` eligible screens seen and `1,290`
median-collapsed source/model values. The source-separated results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `95af290eb5384cf360156709c42087e3c5013ca9087b617f48dde3ec15ee0c49`;
- design sensitivity: `e33a2556ac46ca617749095e8d78f8bc6210a2c62ed9349f9fb4c0125fdeb4e8`;
- endpoint scores: `f91af4e96a2b0598249cbce23fb4d84dc6dd5c71210472c37232681d6a96baf7`;
- inference: `46b6e6778098baf5486112f5817df1133f718386f6dfb5876d95176c1674c235`;
- normalized summary: `4efb6a9fec2a73e25e133c29d8abd7540af0c6868e535270d63e3e5f2703c4ab`;
- pre-endpoint receipt: `9d6543bc1457eea3741b4eda3c947b3de20de743908126a63e0fb1d00c6948d1`.
