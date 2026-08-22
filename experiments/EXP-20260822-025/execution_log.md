# EXP-20260822-025 execution log

## Frozen boundary

- protocol commit: `1fd72544be7a09d6c9d21bee9a4cf6a04c864b5a`;
- selection seal commit: `b903b994a040965a88067a9fd27c2eb8c3da8e95`;
- implementation commit after pre-endpoint remediation:
  `d491092b63cb508c67cccd6f10276b7b914b1cb0`;
- manifest rebind commit: `1e40976edff11264f40b047d7fd958b5b8475963`;
- endpoint values were not parsed before the sealed pre-endpoint receipt;
- endpoint target column: `PELO (53918)`;
- runner: `.venv/bin/python -m candrel.cdkn2a_pelo_replication`.

## Execution

The corrected bound runner completed in approximately `19.92` seconds and
returned exit code `2`, as required by the permanent feasibility-only contract.
The pre-endpoint receipt was written before the PELO column was parsed.

The endpoint receipt reports `1,292` eligible screens seen and `1,290`
median-collapsed source/model values. The source-separated results are in
`results/summary.json`, with the concise interpretation in `result.md`.

## Result receipts

- context ledger: `1c6b1df176468f25de48585b97d456b7e83c3d2fa63352a31a527b4f3263e725`;
- design sensitivity: `4d1a2acf900d7033702c5fcc3018c40d55c69accad71e546de4642e9926325bc`;
- endpoint scores: `ae85894b710b0eea0f0d2a6bf3f9cd7ca00a2193071815895be76a89df538ff1`;
- inference: `2da3a19fcb761c63a321f0db3bc3c14822a3a09110512eecd3d922028891cac3`;
- normalized summary: `8c25695dc89556510b20286b0082c94066f7b7eca552641a84c826ad1016fc73`;
- pre-endpoint receipt: `d472cdb83390cdd4c35f8f4895360442c4f81901ce31e20ff5ad4845fa29b538`.
