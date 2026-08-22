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

Thirty-five bounded experiments are complete:

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
- `EXP-20260822-011` resolved that narrow reconstruction ambiguity in a separately
  frozen post-failure audit: retaining only sequence-level QC-passing,
  non-excluded rows reproduced 103/103 official WRN scores (maximum discrepancy
  `5.55e-17`) and resolved all three EXP-010 mismatch identities without introducing
  a new one. This establishes only the aggregation rule in the frozen subset; it
  does not retroactively repair EXP-010 or answer guide-omission robustness.
- `EXP-20260822-012` failed its preregistered single-guide robustness criterion:
  only 5/10 previously flagged cross-source WRN gaps stayed flagged under all nine
  global omissions, versus the required 8/10. The complete audit includes 1,030
  screen/configuration rows, 340 paired-model rows, and no inferential or causal
  guide claim.
- `EXP-20260822-013` failed the preregistered same-assay efficacy-process
  association gates: theta was 0.2071, one-sided permutation p was 0.1220, and
  the fixed-rank bootstrap 95% interval was [-0.1697, 0.5334]. The tissue-rho
  floor gate passed, but the positive-association claim did not. Growth rate was
  descriptive only; no growth p-value or confidence interval was computed.
- `EXP-20260822-014` was labeled **FEASIBILITY_ONLY**, not a confirmatory
  replication: matrix-defined damaging STAG2 status versus STAG1 dependency was
  strongly negative in Avana (delta -0.4709) and KY (delta -0.6413), but the
  pre-outcome simulated powers were 0.5070 and 0.2406, and Avana failed the
  frozen lineage-consistency gate. The known interaction is not claimed as newly
  discovered or clinically actionable.
- `EXP-20260822-015` was labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE** for
  the known ARID1A-status/ARID1B-dependency relationship. Avana passed all six
  nominal gates (delta `-0.4583`), while KY failed the bootstrap upper-bound and
  lineage-consistency gates (Bone `+1.0`, Pancreas `+0.2667`). KY's frozen
  design power is below 0.80, so no confirmatory two-source claim is permitted.
- `EXP-20260822-016` was released only as **PROTOCOL_DEVIATION_NONCONFIRMATORY**
  for the distinct ARID1A-status/KEAP1-dependency direction. The executable
  design receipt did not exactly reproduce the frozen candidate-census planning
  draw (Avana `0.8652` vs `0.8622`; KY `0.5875` vs `0.5699`), so the clean
  preregistered and confirmatory claims are prohibited. Avana was negative and
  imprecise (delta `-0.0545`, CI `[-0.1791, 0.0695]`); KY was directionally
  negative (delta `-0.2275`, p `0.0207`) but failed lineage consistency in Bone,
  CNS/Brain, and Lymphoid. No source passed all nominal gates.
- `EXP-20260822-017` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. Matrix-intact TP53
  models had stronger MDM2 dependency in both sources (Avana delta `-0.6241`,
  KY delta `-0.5398`), but Avana failed the frozen lineage-consistency gate
  because Cervix was `+0.3929` and Prostate `+0.3333`. KY passed all nominal
  gates, while its pre-endpoint planning power was only `0.7521`; no
  confirmatory, clinical, treatment, or clean replication claim is permitted.
- `EXP-20260822-018` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix CDKN2A-to-TYMS direction was negative in both sources (Avana
  delta `-0.1345`, KY delta `-0.1803`), but Avana failed the effect-size and
  lineage gates, KY failed effect, permutation, bootstrap, and lineage gates,
  and KY planning power was only `0.5364`. No reliable biomarker, functional-loss,
  TYMP, treatment, clinical, or confirmatory claim is permitted.
- `EXP-20260822-019` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The damaging-matrix
  PTEN-to-PIK3CB direction was negative in Avana (delta `-0.2803`) but failed
  lineage consistency; KY was near zero (delta `-0.0066`, p `0.4831`) and failed
  effect, permutation, bootstrap, and lineage gates. KY planning power was only
  `0.5375`. This does not support a general PTEN-to-PIK3CB dependency claim or
  any PTEN-null, inhibitor, treatment, clinical, or confirmatory claim.
- `EXP-20260822-020` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix TP53-to-WEE1 direction was near zero in Avana (delta
  `-0.0385`, p `0.2119`) with heterogeneous lineages. KY was strongly negative
  in aggregate (delta `-0.3097`, p `0.00018`) but failed the no-positive-lineage
  gate with Peripheral Nervous System `+0.4333` and Prostate `+1.0`. KY planning
  power was `0.7564`, so no confirmatory, functional-TP53, KRAS-restricted,
  inhibitor, treatment, clinical, or pooled claim is permitted.
- `EXP-20260822-021` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix NF1-to-PTPN11 direction was negative in Avana (delta
  `-0.2494`, p `0.00334`) but failed lineage consistency with Bladder/Urinary
  Tract `+1.0` and Esophagus/Stomach `+0.5256`. KY was near zero (delta
  `+0.0462`, p `0.6307`) and failed all substantive gates. KY planning power
  was only `0.4028`; no functional-NF1, RAS-causal, inhibitor, treatment,
  clinical, or confirmatory claim is permitted.
- `EXP-20260822-022` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix EP300-to-CREBBP direction was strongly negative in Avana
  (delta `-0.4172`) and KY (delta `-0.4768`), but both sources failed the
  no-positive-lineage gate (Avana maximum `+0.4`; KY maximum `+1.0`). Both
  source planning powers were below `0.80` (`0.7401` and `0.4984`), so no
  functional-EP300, paralog-causal, inhibitor, treatment, clinical, or
  confirmatory claim is permitted.
- `EXP-20260822-023` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix APC-to-TDO2 direction was weakly negative in Avana (delta
  `-0.1232`, p `0.1548`) but strongly positive in KY (delta `+0.4922`, p
  `0.9965`), failing the source-consistency and lineage gates. Both source
  planning powers were below `0.80` (`0.5184` and `0.2861`), so this does not
  reproduce the published APC/TDO2 dependency in these frozen screen cohorts.
  No functional-APC, WNT-causal, inhibitor, treatment, clinical, or
  confirmatory claim is permitted.
- `EXP-20260822-024` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix KMT2D-to-KMT2C direction was negative in Avana (delta
  `-0.1779`, p `0.00978`) but failed effect size and lineage consistency; KY
  was positive (delta `+0.1004`, p `0.7972`) and failed the substantive gates.
  KY planning power was only `0.5120`, so the emerging KMT2D-null lymphoma
  result is not generalized across these frozen source families. No
  functional-KMT2D, lymphoma-specific, paralog-causal, inhibitor, treatment,
  clinical, or confirmatory claim is permitted.
- `EXP-20260822-025` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix CDKN2A proxy-to-PELO direction was negative in Avana (delta
  `-0.1580`, p `0.01257`) but missed the effect and lineage gates; KY was weakly
  negative (delta `-0.0577`, p `0.3168`) and failed the substantive gates.
  KY planning power was only `0.5265`. This does not test or establish 9p21.3
  deletion, FOCAD loss, MSI-H biology, mechanistic CDKN2A/PELO causality,
  inhibitor response, treatment, clinical utility, or a confirmatory claim.
- `EXP-20260822-026` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix PTEN proxy-to-PAPSS1 direction was near-null in Avana
  (delta `-0.0321`, p `0.3365`) and positive in KY (delta `+0.2074`, p
  `0.9621`), failing the source and lineage gates. KY planning power was only
  `0.5377`. This is compatible with, but does not prove, the reported
  patient-versus-cell-line transport gap; no PTEN deletion, PAPSS2 co-deletion,
  patient, causal, inhibitor, treatment, clinical, or confirmatory claim is
  permitted.
- `EXP-20260822-027` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix ARID1A-proxy-to-EZH2 direction was negative but sub-threshold
  and heterogeneous in Avana (delta `-0.1925`, p `0.00458`) and weakly negative
  and uncertain in KY (delta `-0.0828`, p `0.2323`). KY planning power was only
  `0.5760`. This does not establish functional ARID1A loss, ovarian-specific
  biology, pharmacologic EZH2 inhibition, causal synthetic lethality, treatment,
  clinical utility, or a confirmatory claim.
- `EXP-20260822-028` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The frozen
  damaging-matrix TP53-proxy-to-TIPARP direction was weakly negative but
  uncertain in Avana (delta `-0.0274`, p `0.2850`) and KY (delta `-0.0796`, p
  `0.1835`); both sources failed effect, permutation, bootstrap, and
  no-positive-lineage gates. KY planning power was `0.7509`, so no functional
  TP53, SCHEMATIC interaction, PARP7-inhibitor, treatment, clinical, or
  confirmatory claim is permitted.
- `EXP-20260822-029` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The composite
  BRCA1-or-BRCA2 damaging proxy was source-discordant: KY passed all nominal
  gates (delta `-0.3738`, p `0.00311`), while Avana was weak and heterogeneous
  (delta `-0.0768`, p `0.2219`, maximum lineage delta `+1.0`). Both planning
  powers were below `0.80`, so no biallelic-BRCA, HRD, POLQ-inhibitor,
  treatment, clinical, or confirmatory claim is permitted.
- `EXP-20260822-030` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The composite
  BRCA1-or-BRCA2 damaging proxy was negatively associated with CIP2A dependency
  in both source families (Avana delta `-0.3196`, KY delta `-0.2144`), but
  Avana failed the no-positive-lineage gate and KY failed permutation,
  bootstrap, and no-positive-lineage gates. Corrected pre-endpoint planning
  powers were `0.6686` and `0.4355`; no robust two-source BRCA1/2–CIP2A,
  biallelic-BRCA, HRD, pharmacologic, treatment, clinical, or confirmatory
  claim is permitted.
- `EXP-20260822-031` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The SMAD4
  damaging-matrix proxy did not transport to genetic BRD4 dependency: Avana was
  positive and heterogeneous (delta `+0.0889`, p `0.8132`), while KY was
  near-null and uncertain (delta `-0.0491`, p `0.3582`). Planning powers were
  `0.6414` and `0.4630`; no functional-SMAD4, BET-inhibitor, BRD4-inhibitor,
  treatment, clinical, or confirmatory claim is permitted.
- `EXP-20260822-032` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The SMAD4
  damaging-matrix proxy was positive and heterogeneous for genetic AURKA
  dependency in Avana (delta `+0.0953`, p `0.8276`) and KY (delta `+0.1196`,
  p `0.8238`). Planning powers were `0.6502` and `0.4713`; no functional-SMAD4,
  AURKA-inhibitor, spindle-checkpoint, treatment, clinical, or confirmatory
  claim is permitted.
- `EXP-20260822-033` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The ARID1A
  damaging-matrix proxy was weakly negative but heterogeneous in Avana (delta
  `-0.0893`, p `0.1151`) and near-null in KY (delta `-0.0152`, p `0.4469`).
  Planning powers were `0.8666` and `0.5810`; no functional-ARID1A,
  ATR-inhibitor, DNA-damage, treatment, clinical, or confirmatory claim is
  permitted.
- `EXP-20260822-034` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The TP53
  damaging-matrix proxy was nominally negative in Avana (delta `-0.0953`,
  p `0.0236`) but positive and heterogeneous in KY (delta `+0.1780`,
  p `0.9806`). Planning powers were `0.9951` and `0.7617`; no functional-TP53,
  TDG-inhibitor, DNA-repair, treatment, clinical, or confirmatory claim is
  permitted.
- `EXP-20260822-035` is **T1 descriptive association only; not T2/confirmatory**
  and is labeled **FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**. The TP53
  damaging-matrix proxy was positive and heterogeneous for genetic ENDOD1
  dependency in Avana (delta `+0.0121`, p `0.6002`) and KY (delta `+0.0376`,
  p `0.6680`). Planning powers were `0.9950` and `0.7417`; no functional-TP53,
  TP53-hotspot, ENDOD1-inhibitor, DNA-repair, treatment, clinical, or
  confirmatory claim is permitted.

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
uv run candrel-wrn-sequence-semantics  # expected pass; 103-score semantics audit
uv run candrel-wrn-guide-loo-passing  # expected exit 2; 5/10 robustness criterion failed
uv run candrel-wrn-process-association  # expected exit 2; efficacy association gates failed
uv run candrel-paralog-replication  # expected exit 2; feasibility-only/non-confirmatory result
uv run candrel-arid1a-replication  # expected exit 2; feasibility-only nominal gate failure
uv run candrel-arid1a-keap1-replication  # expected exit 2; protocol-deviation/non-confirmatory result
uv run candrel-tp53-mdm2-replication  # expected exit 2; T1 feasibility-only lineage-gate failure
uv run candrel-cdkn2a-tyms-replication  # expected exit 2; T1 feasibility-only nominal-gate failure
uv run candrel-pten-pik3cb-replication  # expected exit 2; T1 feasibility-only cross-source failure
uv run python -m candrel.tp53_wee1_replication  # expected exit 2; T1 feasibility-only lineage-gate failure
uv run python -m candrel.nf1_ptpn11_replication  # expected exit 2; T1 feasibility-only cross-source failure
uv run python -m candrel.ep300_crebbp_replication  # expected exit 2; T1 feasibility-only lineage-gate failure
uv run python -m candrel.apc_tdo2_replication  # expected exit 2; T1 feasibility-only source-discordance failure
uv run python -m candrel.kmt2d_kmt2c_replication  # expected exit 2; T1 feasibility-only lineage-gate failure
uv run python -m candrel.cdkn2a_pelo_replication  # expected exit 2; T1 feasibility-only proxy/lineage-gate failure
uv run python -m candrel.pten_papss1_replication  # expected exit 2; T1 feasibility-only transport/lineage-gate failure
uv run python -m candrel.arid1a_ezh2_replication  # expected exit 2; T1 feasibility-only proxy/lineage-gate failure
uv run python -m candrel.tp53_tiparp_replication  # expected exit 2; T1 feasibility-only proxy/lineage-gate failure
uv run python -m candrel.brca12_cip2a_replication  # expected exit 2; T1 feasibility-only lineage-gate failure
uv run python -m candrel.brca12_polq_replication  # expected exit 2; T1 feasibility-only composite-proxy/source-discordance failure
uv run python -m candrel.smad4_brd4_replication  # expected exit 2; T1 feasibility-only SMAD4/BRD4 transport failure
uv run python -m candrel.smad4_aurka_replication  # expected exit 2; T1 feasibility-only SMAD4/AURKA transport failure
uv run python -m candrel.arid1a_atr_replication  # expected exit 2; T1 feasibility-only ARID1A/ATR transport failure
uv run python -m candrel.tp53_tdg_replication  # expected exit 2; T1 feasibility-only TP53/TDG transport failure
uv run python -m candrel.tp53_endod1_replication  # expected exit 2; T1 feasibility-only TP53/ENDOD1 transport failure
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
