# EXP-20260822-009 result

## Status

**FAIL — relative source asymmetry in sequence inclusion did not positively track
absolute WRN percentile discordance under the frozen gates.**

Evidence label: preregistered derived observational analysis after EXP-005 endpoint
unsealing. This is not blinded confirmation and not a causal test.

## Exact execution

The preregistration and outcome-blind methods audit were committed and pushed as
`8fa611e` before implementation or outcome association.

```bash
uv sync --extra dev --locked
uv run pytest
uv run candrel-sequence-inclusion-asymmetry --smoke \
  --output experiments/EXP-20260822-009/results/smoke_summary.json \
  --model-output experiments/EXP-20260822-009/results/smoke_model_sequence_asymmetry.csv
uv run candrel-sequence-inclusion-asymmetry \
  --output experiments/EXP-20260822-009/results/summary.json \
  --model-output experiments/EXP-20260822-009/results/model_sequence_asymmetry.csv
```

Forty-six tests passed. The expected scientific-failure exit code was 2 for smoke
and full runs. The full run used 100,000 tissue-preserving permutations and 10,000
within-tissue bootstraps of frozen ranks for each prespecified field. Smoke and full
model tables are byte-identical.

## Integrity and adequacy

- All four input SHA-256 receipts matched the frozen manifest.
- Exposure adequacy was completed before the WRN-gap file was hashed or opened.
- The full denominator contained 103 model-source records and 103 unique exact
  ScreenIDs: Avana 25 / KY 30 Large Intestine and Avana 22 / KY 26 Ovary.
- All counts were finite nonnegative integers. Exactly three records had different
  included and passing counts; in all three, included exceeded passing, and none was
  repaired or excluded.
- The paired population was exactly 34 models, 17 per tissue.
- Primary inclusion-asymmetry exposure had six distinct values in Large Intestine
  and five in Ovary; each tissue's largest tie contained seven models. The
  sensitivity exposure met the same gate.
- No sequence was treated as an inferential unit.

## Primary result

| Estimand | Result | Frozen gate | Pass? |
|---|---:|---:|:---:|
| Equal-tissue mean Spearman `theta` | **0.0667** | >= 0.40 | No |
| One-sided tissue-preserving permutation p | **0.3542** | <= 0.05 | No |
| Fixed-rank paired-bootstrap 95% CI | **[-0.2377, 0.3391]** | lower > 0.10 | No |
| Lowest tissue rho | **-0.3679** | >= -0.20 | No |

All four frozen primary gates failed. Tissue estimates disagreed:

| Tissue | Paired models | Spearman rho |
|---|---:|---:|
| Large Intestine | 17 | **-0.3679** |
| Ovary | 17 | **0.5014** |

The smoke run already showed the same near-zero aggregate and opposite tissue
directions. The full run was still completed because smoke was a correctness and
adequacy gate, not an outcome-selection rule.

## Prespecified sensitivity result

`nPassingSequences` was explicitly frozen as near-duplicate sensitivity evidence,
not independent corroboration and not a rescue path. Its result was nearly the same:

- equal-tissue theta: **0.0710**;
- Large Intestine rho: **-0.3679**;
- Ovary rho: **0.5100**;
- one-sided permutation p: **0.3465**;
- bootstrap 95% CI: **[-0.2322, 0.3448]**.

It cannot alter the failed primary decision.

## Interpretation

This experiment falsifies the specific proposed explanation that relative
Avana-versus-KY sequence-inclusion asymmetry consistently tracks the observed WRN
ranking gaps across the two frozen tissues. The aggregate association was close to
zero and its uncertainty crossed zero broadly.

The positive ovarian estimate and negative colorectal estimate are preserved as
heterogeneity, not used to launch a subgroup rescue. With 17 models per tissue and
highly tied count exposures, neither tissue-specific estimate is treated as a
standalone discovery.

This failure does not show that assay process is irrelevant. Screen duration is
perfectly source-confounded here; direct doubling-time and Cas9-activity fields are
missing for KY; and guide-level LFC sensitivity remains a separately testable but
mechanically coupled direction.

## Claim boundary

Maximum supported claim: in this frozen, post-endpoint-unsealing two-tissue
cell-model set, relative source asymmetry in sequence inclusion did not positively
track absolute WRN percentile discordance under the preregistered estimator and
gates.

This does not establish absence of all technical effects, causality, source
superiority, a WRN mechanism, treatment actionability, patient benefit, or clinical
relevance.

## Artifacts

- `results/summary.json`: SHA-256
  `81a3cec9baa9116eeb9de7220e3199673d85f6260a4baba5ef4621b4dd20db5c`.
- `results/model_sequence_asymmetry.csv`: SHA-256
  `4e15632f37adf77e185465b484fdf52a0967ac59d63c736a8b79850c592491c3`.
- `results/smoke_summary.json`: SHA-256
  `f8eeeaf8305ebd35aed69fc6819caade768374e94683448af29c5c94dfb589cb`.
- Smoke and full model tables share SHA-256
  `4e15632f37adf77e185465b484fdf52a0967ac59d63c736a8b79850c592491c3`.

Independent audit reproduced all identities, adequacy facts, estimates, inference,
failed gates, artifact hashes, exit behavior, and claim boundaries. It found no
post-preregistration method drift and returned GO.
