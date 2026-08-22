# EXP-20260822-039 result — PBAF-loss proxy status to PARP1 dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate screen families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `PARP1 (142)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: PBRM1-or-ARID2 composite damaging proxy when either matrix value
  is `1` or `2`;
- reference: both PBRM1 and ARID2 matrix values `0`;
- status counts: Avana `49/926`, KY `22/293` damaging/matrix-intact;
- mixed-lineage counts: Avana `15`, KY `8`;
- canonical roster SHA-256:
  `6ab143e99b7d58d82a1b1e22b9948aacc5944ebe6daabe448505cd8735188af4`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The outcome-free planning powers were Avana `0.6569` and KY `0.3913`; the
paired-source contract therefore permanently limits this experiment to
`FEASIBILITY_ONLY`.

The biological motivation is primary work reporting PBRM1-deficiency
synthetic lethality with PARP and ATR inhibitors
([primary PBRM1/DNA-repair study](https://aacrjournals.org/cancerres/article/81/11/2888/673616/PBRM1-Deficiency-Confers-Synthetic-Lethality-to)).
The executable proxy broadens isolated PBRM1 status to either PBRM1 or the
related PBAF subunit ARID2 because isolated PBRM1 damage had only 11 eligible
KY models. This experiment is not equivalent to isolated PBRM1 loss, ARID2
loss, homologous-recombination deficiency, or PARP-inhibitor response.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | `+0.0549763033` | 2110 | `0.7132528675` | `[-0.1270379147, +0.2379383886]` | 6 | `+1.0000` | FAIL |
| KY | `+0.2244897959` | 539 | `0.9386206138` | `[-0.0723562152, +0.5064935065]` | 3 | `+1.0000` | FAIL |

Avana is weakly positive in the opposite direction from the preregistered
dependency hypothesis and fails the effect, permutation, bootstrap, and
no-positive-lineage gates. KY is positive and fails every primary gate,
including the requirement for at least five negative lineages. No source
pooling, post hoc lineage exclusion, threshold change, or proxy rescue was
used.

## Interpretation boundary

The strongest allowed statement is: in these frozen DepMap 23Q4 cohorts, the
PBRM1-or-ARID2 composite damaging proxy did not show a robust negative,
source-consistent association with PARP1 genetic dependency. This experiment
does not transport the referenced PBRM1/PARP inhibitor hypothesis under its
explicit composite proxy and endpoint contract.

This does not refute PBRM1/PARP biology. The composite mutation proxy,
isolated PBRM1 loss, ARID2 loss, PBAF function, HRD, PARP1 genetic knockout,
and PARP pharmacology are not equivalent. The result does not establish
mechanism, inhibitor response, treatment benefit, patient selection, clinical
utility, or a confirmatory claim.

## Protocol correction

Attempt 001 stopped at the T0 input-integrity gate before endpoint access
because of a two-character screen-map hash transcription error. All five
current input files matched the corrected digests; the correction was sealed
and rebound before the single endpoint execution. The failed receipt is
preserved in `attempt_001_t0_error_receipt.json`.

## Artifact receipts

- `context_ledger.csv`: `4beaa3d4d6b4ede1b27e8dc3ebffb0dd87a454e235513384b182c3ef50e704be`
- `design_sensitivity.csv`: `cfc878555f978e8fd68e0e7ed9552ff2929121626f6fa656bf6b2be8241b2da3`
- `endpoint_scores.csv`: `b7c5ef73e3399f8dec2c85f9db126f50fd2cf897cbe6bffa6731881bba907227`
- `inference.csv`: `fda19f054f7ed7e6f0feedcf9592e88a779f1ecea4bb8bf7231227342fec49b4`
- normalized `summary.json` digest: `4e3b15cdac892e147725eff444b95e1ae9c97bd54c3a42a1a01d79a07d05e992`
- `pre_endpoint_receipt.json`: `da8966d3c0901d71413cced694df9044e63674ecc7402d0e4557eb40fe08bb72`
