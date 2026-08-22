# EXP-20260822-005 result

## Status

**PASS — positive within-tissue WRN model-ordering agreement in the frozen
two-tissue overlap set.**

Evidence label: preregistered derived analysis after EXP-003 endpoint unsealing. This
is not a pristine data-blind confirmation.

## Exact execution

The preregistration and outcome-blind methods audit were committed and pushed as
`583b80d` before any cross-source model-ordering statistic or percentile gap was
computed.

```bash
uv run pytest
uv run candrel-wrn-ordering --smoke \
  --output experiments/EXP-20260822-005/results/smoke_summary.json \
  --model-output experiments/EXP-20260822-005/results/smoke_model_percentile_gaps.csv
uv run candrel-wrn-ordering
```

Twenty-six tests passed. The final full run used 100,000 tissue-preserving
permutations and 10,000 paired-model bootstraps and completed in 0.88 seconds on the
project Mac.

## Integrity and adequacy

- Input SHA-256 matched
  `072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654`.
- Full percentile denominators were Avana 25 / KY 30 Large Intestine models and
  Avana 22 / KY 26 Ovary models.
- Overlap was exactly 17 distinct ModelIDs per tissue, 34 total.
- All endpoints were finite; no duplicate model×source×tissue row or constant rank
  vector was present.
- Source-only models contributed to percentile denominators, but only overlapping
  model pairs entered correlations.

## Primary result

| Estimand | Result | Frozen gate |
|---|---:|---:|
| Equal-tissue mean Spearman `theta` | **0.5956** | >= 0.50 |
| One-sided stratified permutation p | **13 / 100,001 = 0.000130** | <= 0.05 |
| Fixed-percentile paired-bootstrap 95% CI | **[0.3186, 0.7870]** | lower > 0.20 |
| Lowest tissue rho | **0.3701** | >= -0.20 |

All four gates passed.

The first implementation incorrectly re-ranked duplicated bootstrap observations.
Independent audit blocked it. The final interval above correlates the already-frozen
full-denominator percentile pairs directly in each resample, as preregistered. The
point estimate, permutation result, model gaps, and pass decision did not change.

Tissue-specific agreement was heterogeneous:

| Tissue | Overlap models | Spearman rho |
|---|---:|---:|
| Large Intestine | 17 | **0.8211** |
| Ovary | 17 | **0.3701** |

The equal weighting is intentional: the primary result is not allowed to hide the
weaker ovarian stratum behind the stronger colorectal one.

## Secondary reliability diagnostics

- Median absolute source-percentile gap: 0.1750.
- IQR: [0.0977, 0.2771].
- 10/34 models (29.4%) crossed the fixed discordance flag `gap >= 0.25`.
- Pooled within-tissue Kendall concordance-minus-discordance: 0.4559, based on 198
  concordant and 74 discordant model pairs with no ties.
- Descriptive median gap by MSI label: MSI 0.1117 (n=10), MSS 0.2074 (n=24). No
  inferential comparison was preregistered.

The five largest gaps were:

| Model | Tissue | Label | Avana percentile | KY percentile | Gap |
|---|---|---|---:|---:|---:|
| A2780 (`ACH-000657`) | Ovary | MSI | 0.095 | 0.840 | **0.745** |
| TOV-112D (`ACH-000048`) | Ovary | MSS | 0.524 | 0.000 | **0.524** |
| OVISE (`ACH-000527`) | Ovary | MSS | 0.190 | 0.680 | **0.490** |
| T84 (`ACH-000381`) | Large Intestine | MSS | 0.625 | 0.172 | **0.453** |
| OVCAR-8 (`ACH-000696`) | Ovary | MSS | 0.238 | 0.640 | **0.402** |

These are audit leads, not biological exceptions established by this experiment.
Their gaps could reflect library design, assay duration, guide behavior, model drift,
or biology and require separate preregistered investigation.

## Interpretation

The known group-level MSI–WRN signal from EXP-003 is accompanied by positive
model-level ordering agreement in the two adequately sized tissues. However,
agreement is not uniform: ovarian ordering is much weaker, almost one-third of models
cross the fixed 0.25 gap flag, and A2780 changes from near the weak-dependency end in
Avana to near the strong-dependency end in KY.

This distinction matters. A biomarker-defined dependency can replicate strongly at
the group level while individual model rankings remain materially source-sensitive.
The next high-value question is whether the largest gaps are explained by known
technical confounders or reproducible model biology.

EXP-004 remains a T0 four-tissue failure. EXP-005 supports only its narrower
Large-Intestine-and-Ovary population.

## Claim boundary

Maximum supported claim: in the preregistered Large Intestine and Ovary overlap set,
source-specific WRN dependency rankings showed positive within-tissue agreement
across Avana and KY, with stronger agreement in colorectal than ovarian models.

This is conditional measurement/ranking agreement in shared cell models. It does not
establish a novel dependency, mechanism, universal reproducibility, therapeutic
effect, patient benefit, or clinical relevance.

## Artifacts

- `results/summary.json`: SHA-256
  `d513c88a383361953012ece94067c88f9370c36ff66208518f5721c241366774`.
- `results/model_percentile_gaps.csv`: SHA-256
  `f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a`.
- `results/smoke_summary.json`: SHA-256
  `a56d3a8a7d5df2fff80029e57a6fc8a236e2974b44e6ca42147ea4f8d6dc3e78`.
- `results/full_timing.txt`: SHA-256
  `911769da9048d0d5d379ee295445576f00bc196d988b30a56534f7fe79ec4f06`.

Independent audit reproduced all point estimates and found the initial bootstrap
bug. Re-audit exactly reproduced the corrected fixed-percentile interval, verified
all hashes and 26 tests, and returned GO for commit/push under the narrow claim.
