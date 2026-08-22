# Cancer Dependency Reliability Lab

An open, falsification-first computational cancer-research program.

## North star

Identify genetic-vulnerability hypotheses that remain stable across independently
generated cancer CRISPR screens, survive artifact checks, and are documented well
enough for another researcher or AI agent to reproduce or refute.

The project nominates hypotheses for experimental validation. It does **not**
establish treatments, therapeutic windows, patient benefit, or clinical utility.

## Why this question

Broad and Sanger have independently screened many of the same cancer cell models.
Overall agreement is established, but rare lineage- or biomarker-defined effects can
still be unstable. The unresolved target is claim-level reliability: which specific
context-dependent vulnerabilities survive a held-out screen family with honest
uncertainty and artifact controls?

## Current phase

Ten bounded experiments are complete:

- `EXP-20260822-001` passed the API engineering gate: all eight frozen genes had 177
  paired Broad/Sanger models and positive source correlations.
- `EXP-20260822-002` **falsified** the preregistered claim that `fc_clean_qn`
  materially inflates agreement relative to source-labelled `bf_scaled`: median
  correlation difference was -0.0031 and only 4/8 genes favored `fc_clean_qn`.
- `EXP-20260822-003` recovered the known MSI–WRN positive control with a
  source-separated naïve endpoint: tissue-stratified delta was -0.743 in Broad
  Avana discovery and -0.931 in the sequentially gated Sanger KY confirmation
  contrast, with all four tissues negative in both sources and preregistered gates
  passed. A recorded implementation deviation forbids calling KY values fully unseen.
- `EXP-20260822-004` stopped at T0: the four-tissue model-ordering design required
  at least 8 overlapping models per tissue, but Endometrium has 5. No rank outcome
  was computed and the gate was not weakened.
- `EXP-20260822-005` passed its narrower preregistered derived analysis: equal-tissue
  WRN ordering agreement was 0.596 across 17 colorectal and 17 ovarian paired models,
  but ovarian agreement was weaker and 10/34 models had percentile gaps at least
  0.25. Independent audit corrected the bootstrap implementation and returned GO;
  the corrected CI is [0.319, 0.787].
- `EXP-20260822-006` **falsified** the preregistered QC-asymmetry hypothesis: the
  equal-tissue association between a five-metric source-QC-rank-asymmetry composite
  and WRN percentile gap was -0.066 (permutation p=0.645, bootstrap 95% CI
  [-0.392, 0.278]). All four gates failed and tissue directions disagreed. This
  rules out the proposed simple QC composite as a useful explanation in this set;
  it does not rule out guide design, assay duration, cell state, or other technical
  factors.
- `EXP-20260822-007` stopped at T0 without reading WRN gaps: all 34 paired models had
  zero annotated mutations across four eligible Avana and five eligible KY WRN guide
  locations. The source-asymmetry exposure was constant in both tissues, so no
  association was computed. This excludes only the specific annotated guide-site
  mutation explanation, not other guide-design mechanisms.
- `EXP-20260822-008` **falsified** the model-general discordance hypothesis: median
  cross-source rank disagreement across 1,227 common-essential controls had
  equal-tissue association 0.115 with WRN gap (p=0.261, CI [-0.242, 0.440]); a
  separate 618-gene nonessential panel was slightly negative at -0.108. Independent
  audit returned GO. Broad control-gene instability does not explain the WRN gaps
  under these frozen summaries.
- `EXP-20260822-009` **falsified** the sequence-inclusion-asymmetry hypothesis:
  primary equal-tissue association was 0.067 (p=0.354, CI [-0.238, 0.339]), with
  negative Large Intestine and positive Ovary estimates. The near-duplicate passing-
  sequence sensitivity field gave the same conclusion and could not rescue the
  primary failure.
- `EXP-20260822-010` stopped at its preregistered baseline reconstruction gate:
  100/103 official WRN screen scores were reproduced, but the three screens where
  included sequence count exceeded passing count failed (maximum discrepancy
  0.5755). No guide omission was computed, leaving single-guide robustness
  unresolved while exposing a sequence-inclusion pipeline ambiguity.

A label-only provenance audit found that the CRC-only cohort has only 7 MSI Broad
models, below the independently proposed minimum of 8. That CRC-only gate remains a
deliberate failure. EXP-003 is a separately preregistered four-tissue positive-control
test and does not retroactively rescue it.

```bash
uv sync
uv run pytest
uv run candrel-smoke  # writes rerun_latest.json and stops if the API inputs drift
uv run candrel-processing-sensitivity  # expected exit 2: frozen hypothesis failed
uv run candrel-msi-wrn-replication  # source-separated discovery -> gated confirmation
uv run candrel-wrn-ordering  # expected pass; two-tissue model-ordering reliability
uv run candrel-wrn-qc-asymmetry  # expected exit 2; frozen QC-gap hypothesis failed
uv run candrel-wrn-guide-mutation-adequacy  # expected exit 2; constant exposure
uv run candrel-control-discordance  # expected exit 2; primary control panel failed
uv run candrel-sequence-inclusion-asymmetry  # expected exit 2; inclusion audit failed
uv run candrel-wrn-guide-loo  # expected exit 1; frozen baseline reconstruction failed
```

Raw API responses are cached under `data/raw/` and excluded from Git. Every run
writes hashes and a machine-readable result under its experiment directory.

## Repository map

- `AGENTS.md` — mandatory operating rules for human and AI contributors.
- `docs/` — research charter, question selection, prior art, datasets, claim policy.
- `protocols/` — preregistration and experiment lifecycle.
- `experiments/` — immutable experiment records and tracked results.
- `state/` — compact continuation state for fresh agents.
- `logs/` — append-only decision and orchestration logs.
- `src/` and `tests/` — reproducible acquisition and analysis code.

## Scientific contract

1. Freeze hypotheses and thresholds before inspecting test results.
2. Keep discovery and independent screen-family evaluation separate.
3. Preserve negative and failed runs.
4. Record exact source versions, URLs, hashes, code commit, and environment.
5. Label claims by evidence tier and never imply clinical actionability from cell lines.
6. Treat “not found in our search” as uncertainty, not proof of novelty.

See [docs/RESEARCH_CHARTER.md](docs/RESEARCH_CHARTER.md) for the full contract.
