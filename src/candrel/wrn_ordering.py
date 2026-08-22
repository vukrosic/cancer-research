from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.stats import rankdata, spearmanr


EXPERIMENT_ID = "EXP-20260822-005"
INPUT_SHA256 = "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
EXPECTED_SOURCE_TISSUE_COUNTS = {
    ("Avana", "Large Intestine"): 25,
    ("Avana", "Ovary"): 22,
    ("KY", "Large Intestine"): 30,
    ("KY", "Ovary"): 26,
}
EXPECTED_OVERLAP_COUNTS = {"Large Intestine": 17, "Ovary": 17}


class IntegrityError(RuntimeError):
    """Raised when frozen input, identity, or adequacy invariants fail."""


@dataclass(frozen=True)
class SourceScore:
    model_id: str
    model_name: str
    tissue: str
    label: str
    library: str
    score: float


@dataclass(frozen=True)
class PairRecord:
    model_id: str
    model_name: str
    tissue: str
    label: str
    avana_score: float
    ky_score: float
    avana_percentile: float
    ky_percentile: float
    absolute_percentile_gap: float
    discordant_ge_0_25: bool


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_scores(path: Path) -> list[SourceScore]:
    actual = sha256(path)
    if actual != INPUT_SHA256:
        raise IntegrityError(f"input SHA-256 drift: expected {INPUT_SHA256}, got {actual}")
    rows: list[SourceScore] = []
    seen: set[tuple[str, str, str]] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tissue = row["tissue"].strip()
            library = row["library"].strip()
            if tissue not in TISSUES or library not in SOURCES:
                continue
            identity = (row["model_id"].strip(), library, tissue)
            if identity in seen:
                raise IntegrityError(f"duplicate model×source×tissue row: {identity}")
            seen.add(identity)
            try:
                score = float(row["score"])
            except ValueError as exc:
                raise IntegrityError(f"non-numeric score for {identity}") from exc
            if not math.isfinite(score):
                raise IntegrityError(f"non-finite score for {identity}")
            rows.append(
                SourceScore(
                    model_id=identity[0],
                    model_name=row["model_name"].strip(),
                    tissue=tissue,
                    label=row["label"].strip(),
                    library=library,
                    score=score,
                )
            )
    return rows


def dependency_percentiles(values: Sequence[float]) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if len(array) < 2 or not np.all(np.isfinite(array)):
        raise IntegrityError("percentile denominator must have at least two finite scores")
    ranks = rankdata(array, method="average")
    return (len(array) - ranks) / (len(array) - 1)


def build_pairs(rows: Sequence[SourceScore]) -> tuple[list[PairRecord], dict[str, object]]:
    by_stratum: dict[tuple[str, str], list[SourceScore]] = defaultdict(list)
    for row in rows:
        by_stratum[(row.library, row.tissue)].append(row)
    observed_counts = {key: len(value) for key, value in by_stratum.items()}
    if observed_counts != EXPECTED_SOURCE_TISSUE_COUNTS:
        raise IntegrityError(
            f"source×tissue denominator drift: expected {EXPECTED_SOURCE_TISSUE_COUNTS}, "
            f"got {observed_counts}"
        )

    percentile_by_key: dict[tuple[str, str, str], float] = {}
    row_by_key: dict[tuple[str, str, str], SourceScore] = {}
    for (library, tissue), stratum_rows in by_stratum.items():
        ordered = sorted(stratum_rows, key=lambda row: row.model_id)
        percentiles = dependency_percentiles([row.score for row in ordered])
        if np.all(percentiles == percentiles[0]):
            raise IntegrityError(f"constant percentile vector: {library} {tissue}")
        for row, percentile in zip(ordered, percentiles, strict=True):
            key = (row.model_id, library, tissue)
            percentile_by_key[key] = float(percentile)
            row_by_key[key] = row

    pairs: list[PairRecord] = []
    overlap_counts: dict[str, int] = {}
    for tissue in TISSUES:
        avana_ids = {
            row.model_id for row in by_stratum[("Avana", tissue)]
        }
        ky_ids = {row.model_id for row in by_stratum[("KY", tissue)]}
        overlap = sorted(avana_ids & ky_ids)
        overlap_counts[tissue] = len(overlap)
        for model_id in overlap:
            avana = row_by_key[(model_id, "Avana", tissue)]
            ky = row_by_key[(model_id, "KY", tissue)]
            if (avana.model_name, avana.label) != (ky.model_name, ky.label):
                raise IntegrityError(f"cross-source metadata mismatch: {model_id}")
            avana_percentile = percentile_by_key[(model_id, "Avana", tissue)]
            ky_percentile = percentile_by_key[(model_id, "KY", tissue)]
            gap = abs(avana_percentile - ky_percentile)
            pairs.append(
                PairRecord(
                    model_id=model_id,
                    model_name=avana.model_name,
                    tissue=tissue,
                    label=avana.label,
                    avana_score=avana.score,
                    ky_score=ky.score,
                    avana_percentile=avana_percentile,
                    ky_percentile=ky_percentile,
                    absolute_percentile_gap=gap,
                    discordant_ge_0_25=gap >= 0.25,
                )
            )
    adequacy = {
        "source_tissue_counts": {
            f"{source}|{tissue}": count
            for (source, tissue), count in sorted(observed_counts.items())
        },
        "overlap_counts": overlap_counts,
        "total_overlap": len(pairs),
        "complete_finite_endpoints": True,
        "adequate": (
            len(pairs) >= 30
            and all(count >= 15 for count in overlap_counts.values())
            and overlap_counts == EXPECTED_OVERLAP_COUNTS
        ),
    }
    return pairs, adequacy


def tissue_arrays(pairs: Sequence[PairRecord]) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    arrays = {}
    for tissue in TISSUES:
        selected = sorted(
            (pair for pair in pairs if pair.tissue == tissue),
            key=lambda pair: pair.model_id,
        )
        arrays[tissue] = (
            np.asarray([pair.avana_percentile for pair in selected]),
            np.asarray([pair.ky_percentile for pair in selected]),
        )
    return arrays


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    result = float(spearmanr(x, y).statistic)
    if not math.isfinite(result):
        raise IntegrityError("non-finite Spearman correlation")
    return result


def fixed_percentile_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Pearson correlation of already-frozen percentile values without reranking."""
    x_centered = np.asarray(x, dtype=float) - float(np.mean(x))
    y_centered = np.asarray(y, dtype=float) - float(np.mean(y))
    denominator = float(
        np.sqrt(np.sum(x_centered**2) * np.sum(y_centered**2))
    )
    if denominator == 0:
        raise IntegrityError("constant fixed-percentile bootstrap vector")
    result = float(np.sum(x_centered * y_centered) / denominator)
    if not math.isfinite(result):
        raise IntegrityError("non-finite fixed-percentile correlation")
    return result


def primary_estimate(
    pairs: Sequence[PairRecord],
) -> tuple[float, dict[str, float]]:
    correlations = {
        tissue: spearman(avana, ky)
        for tissue, (avana, ky) in tissue_arrays(pairs).items()
    }
    return float(np.mean(list(correlations.values()))), correlations


def permutation_pvalue(
    pairs: Sequence[PairRecord], observed: float, repeats: int, rng: np.random.Generator
) -> float:
    arrays = tissue_arrays(pairs)
    rank_vectors = {}
    for tissue, (avana, ky) in arrays.items():
        a = rankdata(avana, method="average")
        b = rankdata(ky, method="average")
        a = (a - a.mean()) / np.sqrt(np.sum((a - a.mean()) ** 2))
        b = (b - b.mean()) / np.sqrt(np.sum((b - b.mean()) ** 2))
        rank_vectors[tissue] = (a, b)
    extreme = 0
    batch_size = 2000
    generated = 0
    while generated < repeats:
        batch = min(batch_size, repeats - generated)
        tissue_correlations = []
        for tissue in TISSUES:
            a, b = rank_vectors[tissue]
            permutation_indices = np.argsort(
                rng.random((batch, len(b))), axis=1
            )
            tissue_correlations.append(b[permutation_indices] @ a)
        estimates = np.mean(np.vstack(tissue_correlations), axis=0)
        extreme += int(np.count_nonzero(estimates >= observed))
        generated += batch
    return (1 + extreme) / (repeats + 1)


def bootstrap_interval(
    pairs: Sequence[PairRecord], repeats: int, rng: np.random.Generator
) -> tuple[float, float]:
    arrays = tissue_arrays(pairs)
    estimates = np.empty(repeats, dtype=float)
    for index in range(repeats):
        tissue_correlations = []
        for tissue in TISSUES:
            avana, ky = arrays[tissue]
            sample = rng.integers(0, len(avana), size=len(avana))
            tissue_correlations.append(
                fixed_percentile_correlation(avana[sample], ky[sample])
            )
        estimates[index] = float(np.mean(tissue_correlations))
    low, high = np.quantile(estimates, [0.025, 0.975])
    return float(low), float(high)


def kendall_pair_concordance(pairs: Sequence[PairRecord]) -> dict[str, object]:
    concordant = discordant = ties = 0
    by_tissue: dict[str, float | None] = {}
    for tissue in TISSUES:
        selected = [pair for pair in pairs if pair.tissue == tissue]
        local_c = local_d = local_t = 0
        for left_index, left in enumerate(selected):
            for right in selected[left_index + 1 :]:
                product = np.sign(left.avana_percentile - right.avana_percentile) * np.sign(
                    left.ky_percentile - right.ky_percentile
                )
                if product > 0:
                    local_c += 1
                elif product < 0:
                    local_d += 1
                else:
                    local_t += 1
        denominator = local_c + local_d
        by_tissue[tissue] = (
            (local_c - local_d) / denominator if denominator else None
        )
        concordant += local_c
        discordant += local_d
        ties += local_t
    denominator = concordant + discordant
    return {
        "pooled_concordance_minus_discordance": (
            (concordant - discordant) / denominator if denominator else None
        ),
        "concordant_pairs": concordant,
        "discordant_pairs": discordant,
        "tied_pairs": ties,
        "by_tissue": by_tissue,
    }


def gap_summary(pairs: Sequence[PairRecord]) -> dict[str, object]:
    gaps = np.asarray([pair.absolute_percentile_gap for pair in pairs])
    ordered = sorted(pairs, key=lambda pair: (-pair.absolute_percentile_gap, pair.model_id))
    cutoff = ordered[min(4, len(ordered) - 1)].absolute_percentile_gap
    top = [asdict(pair) for pair in ordered if pair.absolute_percentile_gap >= cutoff]
    by_label = {}
    for label in ("MSI", "MSS"):
        values = np.asarray(
            [pair.absolute_percentile_gap for pair in pairs if pair.label == label]
        )
        by_label[label] = {
            "n": len(values),
            "median": float(np.median(values)),
            "q1": float(np.quantile(values, 0.25)),
            "q3": float(np.quantile(values, 0.75)),
        }
    return {
        "median": float(np.median(gaps)),
        "q1": float(np.quantile(gaps, 0.25)),
        "q3": float(np.quantile(gaps, 0.75)),
        "flagged_ge_0_25": int(np.count_nonzero(gaps >= 0.25)),
        "flagged_fraction": float(np.mean(gaps >= 0.25)),
        "top_five_expanding_ties": top,
        "by_label": by_label,
    }


def write_pairs(path: Path, pairs: Sequence[PairRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(PairRecord.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for pair in sorted(pairs, key=lambda row: (row.tissue, row.model_id)):
            writer.writerow(asdict(pair))


def run(args: argparse.Namespace) -> dict[str, object]:
    input_path = Path(args.input)
    rows = load_scores(input_path)
    pairs, adequacy = build_pairs(rows)
    if not adequacy["adequate"]:
        return {
            "experiment_id": EXPERIMENT_ID,
            "status": "FAIL_T0_ADEQUACY",
            "input_sha256": sha256(input_path),
            "adequacy": adequacy,
            "overall_pass": False,
        }
    theta, correlations = primary_estimate(pairs)
    rng = np.random.default_rng(args.seed)
    p_value = permutation_pvalue(pairs, theta, args.permutations, rng)
    ci_low, ci_high = bootstrap_interval(pairs, args.bootstraps, rng)
    gates = {
        "theta_at_least_0_50": theta >= 0.50,
        "permutation_p_at_most_0_05": p_value <= 0.05,
        "bootstrap_lower_above_0_20": ci_low > 0.20,
        "no_tissue_below_minus_0_20": min(correlations.values()) >= -0.20,
    }
    overall_pass = all(gates.values())
    write_pairs(Path(args.model_output), pairs)
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "PASS_ORDERING_RELIABILITY" if overall_pass else "FAIL_ORDERING_RELIABILITY",
        "analysis_type": "preregistered_derived_analysis_after_endpoint_unsealing",
        "input_sha256": sha256(input_path),
        "seed": args.seed,
        "permutation_repeats": args.permutations,
        "bootstrap_repeats": args.bootstraps,
        "adequacy": adequacy,
        "theta_equal_tissue_mean_spearman": theta,
        "tissue_spearman": correlations,
        "permutation_p_one_sided": p_value,
        "bootstrap_ci_95": [ci_low, ci_high],
        "gates": gates,
        "gap_summary": gap_summary(pairs),
        "kendall_pair_concordance": kendall_pair_concordance(pairs),
        "overall_pass": overall_pass,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default="experiments/EXP-20260822-003/results/model_scores.csv",
    )
    parser.add_argument(
        "--output", default="experiments/EXP-20260822-005/results/summary.json"
    )
    parser.add_argument(
        "--model-output",
        default="experiments/EXP-20260822-005/results/model_percentile_gaps.csv",
    )
    parser.add_argument("--seed", type=int, default=20260826)
    parser.add_argument("--permutations", type=int, default=100000)
    parser.add_argument("--bootstraps", type=int, default=10000)
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.smoke:
        args.permutations = 200
        args.bootstraps = 200
    output = Path(args.output)
    try:
        result = run(args)
    except IntegrityError as exc:
        result = {
            "experiment_id": EXPERIMENT_ID,
            "status": "ERROR_INTEGRITY",
            "error": str(exc),
            "overall_pass": False,
        }
        exit_code = 1
    else:
        exit_code = 0 if result["overall_pass"] else 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
