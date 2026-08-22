# EXP-20260822-012 result

## Status

**FAIL — only 5 of the 10 locked baseline-flagged models remained flagged under
every one of the nine eligible global single-guide omissions.** The preregistered
criterion required at least 8 of 10.

Evidence label: preregistered deterministic same-assay robustness audit after
endpoint unsealing. EXP-005's endpoints and selected models were already known, and
EXP-011's passing-sequence rule was selected after EXP-010's failure. This is not
independent biological confirmation.

## Exact execution

The protocol was pushed as `cc0329c` and the tested implementation as `8098f4e`
before the real-data run.

```bash
uv sync --extra dev --locked
uv run pytest
uv run candrel-wrn-guide-loo-passing
```

The full suite had 69 passing tests. The runner exited 2 with status
`FAIL_SINGLE_GUIDE_ROBUSTNESS` after completing all preregistered configurations.
Results were staged and atomically published only after the six-artifact validator
passed.

## Baseline gates

- 103/103 official WRN screen scores reproduced within absolute tolerance `1e-8`
  and relative tolerance zero.
- Maximum official-score discrepancy: `5.551115123125783e-17`.
- All 103 EXP-011 ledger rows matched exactly; maximum reconstructed-score drift and
  official-score drift were both zero.
- The 34 paired EXP-005 scores, percentiles, gaps, and ten stored flags reproduced
  exactly; maximum score discrepancy was `5.551115123125783e-17`, and percentile and
  gap discrepancies were zero.
- Full denominators remained Avana/KY 25/30 in Large Intestine and 22/26 in Ovary.

No omission was entered until these baseline gates passed.

## Frozen robustness result

Exactly nine global perturbations ran: four Avana-only guide omissions and five
KY-only guide omissions. The ten baseline-flagged models were:

- `ACH-000350` COLO-678
- `ACH-000381` T84
- `ACH-000048` TOV-112D
- `ACH-000132` JHOS-2
- `ACH-000527` OVISE
- `ACH-000657` A2780
- `ACH-000696` OVCAR-8
- `ACH-000936` EFO-27
- `ACH-001151` OVCAR-5
- `ACH-001418` UWB1.289

Five remained flagged under all nine omissions: `ACH-000350`, `ACH-000048`,
`ACH-000527`, `ACH-000657`, and `ACH-000696`. Six of ten retained the flag under
all four Avana omissions, and six of ten under all five KY omissions. Therefore the
primary gate failed at 5/10 versus the required 8/10.

The equal-tissue ordering theta was `0.5790913398452961` at baseline and ranged
from `0.45316986228026923` to `0.6356495181766879` across the nine omissions.
Among the 24 baseline-unflagged models, there were 26 unflagged-to-flagged
model-configuration transitions involving 10 unique models.

## Interpretation and non-computation boundaries

Under this frozen same-assay reconstruction, the ten largest preselected
cross-source WRN percentile gaps were not uniformly robust to single-guide
omission. This fails the preregistered descriptive robustness criterion; it does
not identify a bad guide or prove that guide behavior causes the source gaps.

The nine perturbations are dependent deterministic stress tests. No p-value,
confidence interval, multiplicity correction, guide ranking, subgroup rescue,
multi-guide perturbation, causal guide-quality analysis, biological mechanism,
therapeutic claim, or clinical claim was computed or supported.

EXP-010 remains an immutable `FAIL_T0_RECONSTRUCTION` with 100/103 baseline matches
and three mismatches. EXP-012 is a separate child using the passing-sequence rule
validated in EXP-011; it does not retroactively repair EXP-010.

## Maximum claim

**Within the frozen 103-screen, same-assay, passing-sequence reconstruction, only 5
of the 10 pre-flagged cross-source WRN percentile gaps stayed flagged under every
eligible single-guide omission.**

This does not establish independent replication, a causal guide defect, robustness
to multi-guide or library changes, a WRN mechanism, therapeutic relevance, patient
benefit, or clinical utility.

## Artifacts and receipts

- `results/summary.json`: literal file SHA-256
  `9f482bdd89d0671e1902fb914942e4a80cc981edddbcbff6639b880a232bce95`;
  normalized self-digest recorded in its artifact receipt:
  `41ebd91b96542f90a3d39b55bd86e9095df38efcdb197c91f188465abb867710`.
- `results/configurations.csv`: SHA-256
  `6d0bd64fe602c9203775c0b17225278190ef43bcb28676df0ec3b07c604f2940`.
- `results/model_configuration_gaps.csv`: SHA-256
  `6e6c804fa69dc0458bc1e8dbf10eb6de85fb8645d546055c55631334109704be`.
- `results/model_robustness.csv`: SHA-256
  `5b9a41c7794b88694a4e95de44509085555cc90fa179a1b72051ade8427ba387`.
- `results/reconstructed_guide_means.csv`: SHA-256
  `6011fab5a99a56cda3c972e12da7f6faa6e52796aa90ad74ca8e7cc8e4cd0a73`.
- `results/screen_configuration_ledger.csv`: SHA-256
  `2c6463fc9758dc1b900321f3fd36bcab1bad52b61a409cfe4cb50db64ba60533`.

The screen ledger has 1,030 rows (103 screens × baseline plus nine omissions), the
paired-gap ledger has 340 rows (34 models × 10 configurations), and the robustness
table has 34 rows. Independent audit reproduced the receipts, all gates, ledger
identities, invariance checks, summary statistics, and the narrow claim, returning
GO.
