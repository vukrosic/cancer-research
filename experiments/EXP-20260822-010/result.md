# EXP-20260822-010 result

## Status

**FAIL T0 — the frozen raw reconstruction did not reproduce all 103 official WRN
screen scores, so no guide omission or robustness result was computed.**

Evidence label: preregistered baseline reconstruction/adequacy failure after endpoint
unsealing. This is not a leave-one-guide-out outcome.

## Exact execution order

The protocol was pushed as `996a866` and the tested implementation as `d37e714`
before execution.

```bash
uv sync --extra dev --locked
uv run pytest
uv run candrel-wrn-guide-loo
```

Fifty-one tests passed. Both pre-Chronos LFC matrices matched official byte sizes and
MD5 receipts; locally computed SHA-256 receipts are preserved below. The command
exited 1 with `ERROR_INTEGRITY` at the baseline gate.

The implementation orders operations as acquisition/hash verification, frozen
identity and sequence joins, guide-mean reconstruction, official-score extraction,
and baseline comparison. The gap file is not parsed and the omission loop is not
entered unless that comparison passes.

## Baseline gate result

The frozen rule was:

1. retain exact frozen-screen sequence rows with
   `ExcludeFromCRISPRCombined=False`;
2. require that count to equal `nIncludedSequences`;
3. mean LFC across those sequences for each eligible guide;
4. median across four Avana or five KY WRN guides; and
5. require absolute discrepancy from the official naïve score at most `1e-8`.

One hundred of 103 source screens matched to numerical precision. Exactly three
failed:

| Model | Source | Tissue | Passing / included | Reconstructed | Official | Absolute discrepancy |
|---|---|---|---:|---:|---:|---:|
| ACH-000680 | Avana | Large Intestine | 1 / 2 | -0.622188 | -1.197649 | **0.575461** |
| ACH-000719 | KY | Ovary | 2 / 3 | -0.095395 | -0.135522 | **0.040127** |
| ACH-000663 | Avana | Ovary | 2 / 3 | 0.065621 | 0.071632 | **0.006011** |

The maximum discrepancy was 0.575461, far beyond the frozen tolerance.

## Diagnostic boundary

These are exactly the three frozen records where `nIncludedSequences` exceeds
`nPassingSequences`. Each corresponding screen has one sequence row with
`PassesQC=False` but `ExcludeFromCRISPRCombined=False`. Every other frozen screen
reconstructed within `1e-8`.

This alignment suggests that the official naïve-score aggregation may apply a
passing-sequence rule or another exception not captured by the preregistered
included-sequence rule. That is an inference from the mismatch pattern, not a
verified alternative reconstruction: no alternative filter, mapping, aggregation,
or tolerance was run after failure.

## What was not computed

- zero Avana guide omissions;
- zero KY guide omissions;
- zero perturbed scores, percentiles, or gaps;
- no fully robust model count;
- no transition count;
- no ordering-sensitivity range; and
- no pass/fail decision for the proposed 8/10 robustness criterion.

The substantive question—whether the 10 large WRN gaps survive every single-guide
omission—remains unresolved.

## Interpretation and maximum claim

EXP-010 establishes a narrow but important data-engineering result: the literal
`ExcludeFromCRISPRCombined=False` / `nIncludedSequences` reconstruction reproduces
100 of 103 frozen official WRN scores but fails on all three screens where included
and passing sequence counts differ.

It does not identify the official pipeline's undocumented exception, show that
passing-only aggregation is correct, say anything about guide robustness, establish
a WRN mechanism, or support therapeutic or clinical claims.

## Artifacts and receipts

- `results/summary.json`: SHA-256
  `ec8b04c8963fb53f54ce40911736190d780a63fa59c4a0b6a678c02a53ea88cf`.
- `baseline_failure_receipt.json`: exact mismatch ledger and stop receipt.
- `AvanaLogfoldChange.csv`: 3,173,505,617 bytes, MD5
  `58b1f479091a9f8b3e858d69d55413c4`, SHA-256
  `f018d7ff6820af6d0bb095f1e2b405ec31d7a744a1e4c019cfd9f3509e63bdee`.
- `KYLogfoldChange.csv`: 1,585,769,082 bytes, MD5
  `c711c9413b63fe7c55b734e43cdeca91`, SHA-256
  `5b03df4b4affda1f0ed36f2bd564e1cbd53ec443b20e60295cad577677874767`.

Independent audit reproduced every receipt, identity, guide, join, discrepancy, and
the 51-test suite. It confirmed the stop occurs before gap loading or any omission,
returned GO to preserve the T0 failure, and returned NO-GO for guide omissions.
