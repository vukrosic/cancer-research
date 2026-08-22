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
from scipy.stats import rankdata

from candrel.wrn_ordering import fixed_percentile_correlation


EXPERIMENT_ID = "EXP-20260822-006"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
METRICS = (
    "ScreenNNMD",
    "ScreenROCAUC",
    "ScreenFPR",
    "ScreenMedianEssentialDepletion",
    "ScreenMedianNonessentialDepletion",
)
EXPECTED_HASHES = {
    "gap_file": "f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a",
    "qc_file": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "essential_file": "496c5ec9eaa2f4c13dc00fd15a8e24df253afcc5a969d3956b7dd3d987640084",
    "nonessential_file": "2aacca44b6a79e7240518e6adbd89c70d7d895da91cd4c8b4d380529bc5b8e5e",
    "model_file": "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654",
}
EXPECTED_DENOMINATORS = {
    ("Avana", "Large Intestine"): 25,
    ("KY", "Large Intestine"): 30,
    ("Avana", "Ovary"): 22,
    ("KY", "Ovary"): 26,
}


class IntegrityError(RuntimeError):
    """Raised when frozen identity, provenance, or adequacy checks fail."""


@dataclass(frozen=True)
class QCRecord:
    model_id: str
    tissue: str
    library: str
    screen_id: str
    values: dict[str, float]


@dataclass(frozen=True)
class AssociationRecord:
    model_id: str
    model_name: str
    tissue: str
    label: str
    avana_screen_id: str
    ky_screen_id: str
    wrn_percentile_gap: float
    exp005_gap_flag: bool
    nnmd_asymmetry: float
    rocauc_asymmetry: float
    fpr_asymmetry: float
    essential_depletion_asymmetry: float
    nonessential_depletion_asymmetry: float
    qc_rank_asymmetry_composite: float


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_hashes(args: argparse.Namespace) -> dict[str, str]:
    receipt = {}
    for argument, expected in EXPECTED_HASHES.items():
        actual = sha256(Path(getattr(args, argument)))
        if actual != expected:
            raise IntegrityError(
                f"{argument} SHA-256 drift: expected {expected}, got {actual}"
            )
        receipt[f"{argument}_sha256"] = actual
    return receipt


def verify_control_list(path: Path) -> int:
    with path.open(newline="", encoding="utf-8") as handle:
        genes = [row["Gene"].strip() for row in csv.DictReader(handle)]
    if "WRN (7486)" in genes:
        raise IntegrityError(f"WRN is present in control list: {path}")
    return len(genes)


def load_model_tissues(
    path: Path,
) -> tuple[dict[tuple[str, str], str], dict[tuple[str, str], str]]:
    mapping: dict[tuple[str, str], str] = {}
    expected_screens: dict[tuple[str, str], str] = {}
    counts: dict[tuple[str, str], int] = defaultdict(int)
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tissue = row["tissue"].strip()
            library = row["library"].strip()
            if tissue not in TISSUES or library not in SOURCES:
                continue
            key = (row["model_id"].strip(), library)
            if key in mapping:
                raise IntegrityError(f"duplicate model-source denominator row: {key}")
            mapping[key] = tissue
            expected_screens[key] = row["screen_ids"].strip()
            if not expected_screens[key]:
                raise IntegrityError(f"missing frozen screen identity: {key}")
            counts[(library, tissue)] += 1
    if dict(counts) != EXPECTED_DENOMINATORS:
        raise IntegrityError(
            f"denominator drift: expected {EXPECTED_DENOMINATORS}, got {dict(counts)}"
        )
    return mapping, expected_screens


def verify_screen_identity(
    key: tuple[str, str], actual: str, expected: str
) -> None:
    if actual != expected:
        raise IntegrityError(
            f"QC screen identity drift for {key}: expected {expected}, got {actual}"
        )


def load_qc(
    path: Path,
    model_tissues: dict[tuple[str, str], str],
    expected_screens: dict[tuple[str, str], str],
) -> list[QCRecord]:
    records: list[QCRecord] = []
    seen_keys: set[tuple[str, str]] = set()
    seen_screens: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["ModelID"].strip(), row["Library"].strip())
            if key not in model_tissues:
                continue
            if (
                row["PassesQC"].strip().lower() != "true"
                or row["CanInclude"].strip().lower() != "true"
            ):
                continue
            if key in seen_keys:
                raise IntegrityError(f"multiple eligible QC screens for model-source: {key}")
            screen_id = row["ScreenID"].strip()
            verify_screen_identity(key, screen_id, expected_screens[key])
            if screen_id in seen_screens:
                raise IntegrityError(f"shared QC ScreenID: {screen_id}")
            values = {}
            for metric in METRICS:
                try:
                    value = float(row[metric])
                except ValueError as exc:
                    raise IntegrityError(f"non-numeric {metric} for {key}") from exc
                if not math.isfinite(value):
                    raise IntegrityError(f"non-finite {metric} for {key}")
                values[metric] = value
            seen_keys.add(key)
            seen_screens.add(screen_id)
            records.append(
                QCRecord(
                    model_id=key[0],
                    tissue=model_tissues[key],
                    library=key[1],
                    screen_id=screen_id,
                    values=values,
                )
            )
    if seen_keys != set(model_tissues):
        missing = sorted(set(model_tissues) - seen_keys)
        raise IntegrityError(f"missing QC records: {missing[:5]}")
    if len(records) != 103 or len(seen_screens) != 103:
        raise IntegrityError("expected 103 unique model-source screens")
    return records


def quality_transform(metric: str, value: float) -> float:
    if metric in {
        "ScreenNNMD",
        "ScreenFPR",
        "ScreenMedianEssentialDepletion",
    }:
        return -value
    if metric == "ScreenROCAUC":
        return value
    if metric == "ScreenMedianNonessentialDepletion":
        return -abs(value)
    raise IntegrityError(f"unknown QC metric: {metric}")


def quality_percentiles(records: Sequence[QCRecord]) -> dict[tuple[str, str, str], float]:
    by_stratum: dict[tuple[str, str], list[QCRecord]] = defaultdict(list)
    for record in records:
        by_stratum[(record.library, record.tissue)].append(record)
    percentiles: dict[tuple[str, str, str], float] = {}
    for (library, tissue), stratum in by_stratum.items():
        ordered = sorted(stratum, key=lambda row: row.model_id)
        for metric in METRICS:
            transformed = np.asarray(
                [quality_transform(metric, row.values[metric]) for row in ordered]
            )
            ranks = rankdata(transformed, method="average")
            q = (ranks - 1) / (len(ranks) - 1)
            if not np.all(np.isfinite(q)) or np.all(q == q[0]):
                raise IntegrityError(f"constant/nonfinite {metric}: {library} {tissue}")
            for row, percentile in zip(ordered, q, strict=True):
                percentiles[(row.model_id, library, metric)] = float(percentile)
    return percentiles


def load_gaps(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 34:
        raise IntegrityError(f"expected 34 frozen WRN gap rows, got {len(rows)}")
    if {row["tissue"] for row in rows} != set(TISSUES):
        raise IntegrityError("WRN gap tissue drift")
    return rows


def build_association_records(
    gaps: Sequence[dict[str, str]],
    qc_records: Sequence[QCRecord],
    percentiles: dict[tuple[str, str, str], float],
) -> list[AssociationRecord]:
    qc_by_key = {(row.model_id, row.library): row for row in qc_records}
    output = []
    metric_fields = {
        "ScreenNNMD": "nnmd_asymmetry",
        "ScreenROCAUC": "rocauc_asymmetry",
        "ScreenFPR": "fpr_asymmetry",
        "ScreenMedianEssentialDepletion": "essential_depletion_asymmetry",
        "ScreenMedianNonessentialDepletion": "nonessential_depletion_asymmetry",
    }
    for row in gaps:
        model_id = row["model_id"].strip()
        tissue = row["tissue"].strip()
        asymmetries = {
            metric_fields[metric]: abs(
                percentiles[(model_id, "Avana", metric)]
                - percentiles[(model_id, "KY", metric)]
            )
            for metric in METRICS
        }
        composite = float(np.mean(list(asymmetries.values())))
        output.append(
            AssociationRecord(
                model_id=model_id,
                model_name=row["model_name"].strip(),
                tissue=tissue,
                label=row["label"].strip(),
                avana_screen_id=qc_by_key[(model_id, "Avana")].screen_id,
                ky_screen_id=qc_by_key[(model_id, "KY")].screen_id,
                wrn_percentile_gap=float(row["absolute_percentile_gap"]),
                exp005_gap_flag=row["discordant_ge_0_25"].strip().lower() == "true",
                qc_rank_asymmetry_composite=composite,
                **asymmetries,
            )
        )
    for tissue in TISSUES:
        values = [
            row.qc_rank_asymmetry_composite for row in output if row.tissue == tissue
        ]
        if len(values) != 17 or len(set(values)) < 2:
            raise IntegrityError(f"inadequate composite vector: {tissue}")
    return output


def frozen_rank_arrays(
    rows: Sequence[AssociationRecord], exposure: str
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    arrays = {}
    for tissue in TISSUES:
        selected = sorted(
            (row for row in rows if row.tissue == tissue),
            key=lambda row: row.model_id,
        )
        x = np.asarray([getattr(row, exposure) for row in selected])
        y = np.asarray([row.wrn_percentile_gap for row in selected])
        x_rank = rankdata(x, method="average")
        y_rank = rankdata(y, method="average")
        if np.all(x_rank == x_rank[0]) or np.all(y_rank == y_rank[0]):
            raise IntegrityError(f"constant primary rank vector: {tissue}")
        arrays[tissue] = (x_rank, y_rank)
    return arrays


def estimate_from_arrays(
    arrays: dict[str, tuple[np.ndarray, np.ndarray]]
) -> tuple[float, dict[str, float]]:
    correlations = {
        tissue: fixed_percentile_correlation(x, y)
        for tissue, (x, y) in arrays.items()
    }
    return float(np.mean(list(correlations.values()))), correlations


def permutation_pvalue(
    arrays: dict[str, tuple[np.ndarray, np.ndarray]],
    observed: float,
    repeats: int,
    rng: np.random.Generator,
) -> float:
    normalized = {}
    for tissue, (x, y) in arrays.items():
        x = (x - x.mean()) / np.sqrt(np.sum((x - x.mean()) ** 2))
        y = (y - y.mean()) / np.sqrt(np.sum((y - y.mean()) ** 2))
        normalized[tissue] = (x, y)
    extreme = generated = 0
    while generated < repeats:
        batch = min(2000, repeats - generated)
        tissue_estimates = []
        for tissue in TISSUES:
            x, y = normalized[tissue]
            indices = np.argsort(rng.random((batch, len(x))), axis=1)
            tissue_estimates.append(x[indices] @ y)
        estimates = np.mean(np.vstack(tissue_estimates), axis=0)
        extreme += int(np.count_nonzero(estimates >= observed))
        generated += batch
    return (1 + extreme) / (repeats + 1)


def bootstrap_interval(
    arrays: dict[str, tuple[np.ndarray, np.ndarray]],
    repeats: int,
    rng: np.random.Generator,
) -> tuple[float, float]:
    estimates = np.empty(repeats)
    for index in range(repeats):
        local = []
        for tissue in TISSUES:
            x, y = arrays[tissue]
            sample = rng.integers(0, len(x), size=len(x))
            local.append(fixed_percentile_correlation(x[sample], y[sample]))
        estimates[index] = float(np.mean(local))
    low, high = np.quantile(estimates, [0.025, 0.975])
    return float(low), float(high)


def descriptive_metric_correlations(
    rows: Sequence[AssociationRecord],
) -> dict[str, dict[str, object]]:
    exposures = (
        "nnmd_asymmetry",
        "rocauc_asymmetry",
        "fpr_asymmetry",
        "essential_depletion_asymmetry",
        "nonessential_depletion_asymmetry",
    )
    output = {}
    for exposure in exposures:
        theta, tissue = estimate_from_arrays(frozen_rank_arrays(rows, exposure))
        output[exposure] = {"equal_tissue_mean": theta, "by_tissue": tissue}
    return output


def group_descriptives(rows: Sequence[AssociationRecord]) -> dict[str, object]:
    output = {}
    for flag in (False, True):
        values = np.asarray(
            [row.qc_rank_asymmetry_composite for row in rows if row.exp005_gap_flag == flag]
        )
        output["gap_flagged" if flag else "not_gap_flagged"] = {
            "n": len(values),
            "median": float(np.median(values)),
            "q1": float(np.quantile(values, 0.25)),
            "q3": float(np.quantile(values, 0.75)),
        }
    return output


def write_records(path: Path, rows: Sequence[AssociationRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(AssociationRecord.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (item.tissue, item.model_id)):
            writer.writerow(asdict(row))


def run(args: argparse.Namespace) -> dict[str, object]:
    receipt = verify_hashes(args)
    essential_n = verify_control_list(Path(args.essential_file))
    nonessential_n = verify_control_list(Path(args.nonessential_file))
    model_tissues, expected_screens = load_model_tissues(Path(args.model_file))
    qc_records = load_qc(Path(args.qc_file), model_tissues, expected_screens)
    percentiles = quality_percentiles(qc_records)
    rows = build_association_records(
        load_gaps(Path(args.gap_file)), qc_records, percentiles
    )
    arrays = frozen_rank_arrays(rows, "qc_rank_asymmetry_composite")
    theta, tissue_correlations = estimate_from_arrays(arrays)
    rng = np.random.default_rng(args.seed)
    p_value = permutation_pvalue(arrays, theta, args.permutations, rng)
    ci_low, ci_high = bootstrap_interval(arrays, args.bootstraps, rng)
    gates = {
        "point_target_theta_at_least_0_40": theta >= 0.40,
        "permutation_p_at_most_0_05": p_value <= 0.05,
        "practical_ci_lower_above_0_10": ci_low > 0.10,
        "no_tissue_below_minus_0_20": min(tissue_correlations.values()) >= -0.20,
    }
    overall_pass = all(gates.values())
    write_records(Path(args.model_output), rows)
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "PASS_QC_GAP_ASSOCIATION" if overall_pass else "FAIL_QC_GAP_ASSOCIATION",
        "analysis_type": "preregistered_derived_observational_analysis_after_endpoint_unsealing",
        "input_receipt": receipt,
        "control_list_counts": {
            "common_essential": essential_n,
            "nonessential": nonessential_n,
            "wrn_present": False,
        },
        "adequacy": {
            "full_model_source_records": len(qc_records),
            "unique_screen_ids": len({row.screen_id for row in qc_records}),
            "paired_models": len(rows),
            "paired_by_tissue": {
                tissue: sum(row.tissue == tissue for row in rows) for tissue in TISSUES
            },
            "complete_finite_metrics": True,
            "adequate": True,
        },
        "seed": args.seed,
        "permutation_repeats": args.permutations,
        "bootstrap_repeats": args.bootstraps,
        "theta_equal_tissue_mean_spearman": theta,
        "tissue_spearman": tissue_correlations,
        "permutation_p_one_sided": p_value,
        "bootstrap_ci_95": [ci_low, ci_high],
        "gates": gates,
        "descriptive_metric_correlations": descriptive_metric_correlations(rows),
        "composite_by_exp005_gap_flag": group_descriptives(rows),
        "overall_pass": overall_pass,
        "claim_boundary": "observational association, not causal explanation",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--gap-file",
        default="experiments/EXP-20260822-005/results/model_percentile_gaps.csv",
    )
    parser.add_argument(
        "--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv"
    )
    parser.add_argument(
        "--essential-file",
        default="data/raw/depmap/23q4/AchillesCommonEssentialControls.csv",
    )
    parser.add_argument(
        "--nonessential-file",
        default="data/raw/depmap/23q4/AchillesNonessentialControls.csv",
    )
    parser.add_argument(
        "--model-file", default="experiments/EXP-20260822-003/results/model_scores.csv"
    )
    parser.add_argument(
        "--output", default="experiments/EXP-20260822-006/results/summary.json"
    )
    parser.add_argument(
        "--model-output",
        default="experiments/EXP-20260822-006/results/model_qc_asymmetry.csv",
    )
    parser.add_argument("--seed", type=int, default=20260827)
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
