# EXP-20260822-022 execution log

## Frozen boundary

- selection seal commit: `fd8d9b52d3dc9251c841612cd7e08447fd4ab5cd`;
- protocol commit: `400469ac742a4c25ebc2669ac22ae613d45316c7`;
- implementation commit: `68b1771ce50b732f02130bff7b51cf9ce0693e73`;
- manifest commit: `e713534`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `CREBBP (1387)`;
- runner: `.venv/bin/python -m candrel.ep300_crebbp_replication`.

## Execution

The bound runner completed in approximately `21.006` seconds and returned
exit code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before the CREBBP column was parsed.

The endpoint receipt reports `1,292` eligible screens seen and `1,290`
median-collapsed source/model values. The source-separated results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `02e3845021772123b80c77b5317bbbffb484f88c74d2ba5c8bcbb74935563ea2`;
- design sensitivity: `7ed684a32ae9b9c9d5290a14e236660f71187c8dc3acbba1d177eac5e32469b9`;
- endpoint scores: `5c04bafb467a9dcbb91c2a30f29739a9ba9b0f5795a56dc74173cca320d86378`;
- inference: `8d75b782d0820d0fe7a85434356e401ad03ed7756825ab98006b007af42d0071`;
- normalized summary: `6847f52a8daab687a433c70c94e638ceee32212b1e439b65632d19b18db8dfda`;
- pre-endpoint receipt: `daff66c8aa4509c5e8f8904db47445b1431c256dd1d3534363a39ba10ee293c8`.
