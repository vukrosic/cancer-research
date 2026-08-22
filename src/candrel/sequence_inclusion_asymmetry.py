from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.stats import rankdata

from candrel.wrn_qc_asymmetry import (
    bootstrap_interval,
    estimate_from_arrays,
    permutation_pvalue,
)


EXPERIMENT_ID = "EXP-20260822-009"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
FIELDS = ("nIncludedSequences", "nPassingSequences")
PRIMARY_FIELD = "nIncludedSequences"
SENSITIVITY_FIELD = "nPassingSequences"
EXPECTED_PRE_OUTCOME_HASHES = {
    "cohort_file": "2bc84868962b35c55e456aeb953429206e97c9b25f648b5deabe5a1488e60b67",
    "qc_file": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "model_file": "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654",
}
EXPECTED_OUTCOME_HASH = (
    "f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a"
)
EXPECTED_DENOMINATORS = {
    ("Avana", "Large Intestine"): 25,
    ("KY", "Large Intestine"): 30,
    ("Avana", "Ovary"): 22,
    ("KY", "Ovary"): 26,
}
MINIMUM_DISTINCT_EXPOSURES = 5
MAXIMUM_LARGEST_TIE = 8


class IntegrityError(RuntimeError):
    """Raised when frozen identity, provenance, or adequacy invariants drift."""


@dataclass(frozen=True)
class DenominatorRecord:
    model_id: str
    tissue: str
    source: str
    screen_id: str


@dataclass(frozen=True)
class ScreenCountRecord:
    model_id: str
    tissue: str
    source: str
    screen_id: str
    n_included: int
    n_passing: int


@dataclass(frozen=True)
class ExposureRecord:
    model_id: str
    tissue: str
    avana_n_included: int
    ky_n_included: int
    avana_included_percentile: float
    ky_included_percentile: float
    included_asymmetry: float
    avana_n_passing: int
    ky_n_passing: int
    avana_passing_percentile: float
    ky_passing_percentile: float
    passing_asymmetry: float


@dataclass(frozen=True)
class AnalysisRecord:
    model_id: str
    model_name: str
    tissue: str
    label: str
    avana_n_included: int
    ky_n_included: int
    avana_included_percentile: float
    ky_included_percentile: float
    included_asymmetry: float
    avana_n_passing: int
    ky_n_passing: int
    avana_passing_percentile: float
    ky_passing_percentile: float
    passing_asymmetry: float
    wrn_percentile_gap: float
    exp005_gap_flag: bool


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_pre_outcome_hashes(args: argparse.Namespace) -> dict[str, str]:
    receipt = {}
    for argument, expected in EXPECTED_PRE_OUTCOME_HASHES.items():
        actual = sha256(Path(getattr(args, argument)))
        if actual != expected:
            raise IntegrityError(
                f"{argument} SHA-256 drift: expected {expected}, got {actual}"
            )
        receipt[f"{argument}_sha256"] = actual
    return receipt


def parse_count(value: str, field: str, identity: object) -> int:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise IntegrityError(f"non-numeric {field} for {identity}") from exc
    if not math.isfinite(parsed) or parsed < 0 or not parsed.is_integer():
        raise IntegrityError(f"invalid nonnegative integer {field} for {identity}")
    return int(parsed)


def load_cohort(path: Path) -> dict[str, str]:
    cohort: dict[str, str] = {}
    counts: Counter[str] = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["model_id", "tissue"]:
            raise IntegrityError("cohort must contain only model_id,tissue")
        for row in reader:
            model_id = row["model_id"].strip()
            tissue = row["tissue"].strip()
            if not model_id or model_id in cohort or tissue not in TISSUES:
                raise IntegrityError(f"invalid cohort row: {model_id} {tissue}")
            cohort[model_id] = tissue
            counts[tissue] += 1
    expected = {tissue: 17 for tissue in TISSUES}
    if len(cohort) != 34 or dict(counts) != expected:
        raise IntegrityError(f"cohort drift: expected {expected}, got {dict(counts)}")
    return cohort


def load_denominators(path: Path) -> list[DenominatorRecord]:
    records: list[DenominatorRecord] = []
    seen: set[tuple[str, str]] = set()
    screens: set[str] = set()
    counts: Counter[tuple[str, str]] = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tissue = row["tissue"].strip()
            source = row["library"].strip()
            if tissue not in TISSUES or source not in SOURCES:
                continue
            model_id = row["model_id"].strip()
            key = (model_id, source)
            if key in seen:
                raise IntegrityError(f"duplicate denominator model-source: {key}")
            screen_parts = [part.strip() for part in row["screen_ids"].split(";") if part.strip()]
            if len(screen_parts) != 1:
                raise IntegrityError(f"expected one frozen screen for {key}")
            screen_id = screen_parts[0]
            if screen_id in screens:
                raise IntegrityError(f"shared denominator ScreenID: {screen_id}")
            seen.add(key)
            screens.add(screen_id)
            counts[(source, tissue)] += 1
            records.append(DenominatorRecord(model_id, tissue, source, screen_id))
    if dict(counts) != EXPECTED_DENOMINATORS or len(records) != 103 or len(screens) != 103:
        raise IntegrityError(
            f"denominator drift: expected {EXPECTED_DENOMINATORS}, got {dict(counts)}"
        )
    return sorted(records, key=lambda row: (row.source, row.tissue, row.model_id))


def load_screen_counts(
    path: Path, denominators: Sequence[DenominatorRecord]
) -> tuple[list[ScreenCountRecord], dict[str, int]]:
    expected = {(row.model_id, row.source): row for row in denominators}
    records: list[ScreenCountRecord] = []
    seen: set[tuple[str, str]] = set()
    screens: set[str] = set()
    differing = 0
    included_gt_passing = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["ModelID"].strip(), row["Library"].strip())
            if key not in expected:
                continue
            if row["PassesQC"].strip().lower() != "true" or row[
                "CanInclude"
            ].strip().lower() != "true":
                continue
            if key in seen:
                raise IntegrityError(f"multiple eligible QC rows for {key}")
            frozen = expected[key]
            screen_id = row["ScreenID"].strip()
            if screen_id != frozen.screen_id:
                raise IntegrityError(
                    f"QC screen identity drift for {key}: expected {frozen.screen_id}, got {screen_id}"
                )
            if screen_id in screens:
                raise IntegrityError(f"shared QC ScreenID: {screen_id}")
            n_included = parse_count(row[PRIMARY_FIELD], PRIMARY_FIELD, key)
            n_passing = parse_count(row[SENSITIVITY_FIELD], SENSITIVITY_FIELD, key)
            differing += n_included != n_passing
            included_gt_passing += n_included > n_passing
            seen.add(key)
            screens.add(screen_id)
            records.append(
                ScreenCountRecord(
                    model_id=frozen.model_id,
                    tissue=frozen.tissue,
                    source=frozen.source,
                    screen_id=screen_id,
                    n_included=n_included,
                    n_passing=n_passing,
                )
            )
    if seen != set(expected) or len(records) != 103 or len(screens) != 103:
        missing = sorted(set(expected) - seen)
        raise IntegrityError(f"missing frozen QC count records: {missing[:5]}")
    if differing != 3 or included_gt_passing != 3:
        raise IntegrityError(
            "frozen count-field relationship drift: expected three differing records "
            "and three included-greater-than-passing records"
        )
    return records, {
        "differing_records": differing,
        "included_greater_than_passing_records": included_gt_passing,
    }


def count_percentiles(
    records: Sequence[ScreenCountRecord], field: str
) -> dict[tuple[str, str], float]:
    attribute = {
        PRIMARY_FIELD: "n_included",
        SENSITIVITY_FIELD: "n_passing",
    }.get(field)
    if attribute is None:
        raise IntegrityError(f"unknown count field: {field}")
    grouped: dict[tuple[str, str], list[ScreenCountRecord]] = defaultdict(list)
    for row in records:
        grouped[(row.source, row.tissue)].append(row)
    if {key: len(rows) for key, rows in grouped.items()} != EXPECTED_DENOMINATORS:
        raise IntegrityError("count percentile denominator drift")
    percentiles: dict[tuple[str, str], float] = {}
    for (source, tissue), stratum in grouped.items():
        ordered = sorted(stratum, key=lambda row: row.model_id)
        values = np.asarray([getattr(row, attribute) for row in ordered], dtype=float)
        ranks = rankdata(values, method="average")
        q = (ranks - 1) / (len(values) - 1)
        for row, percentile in zip(ordered, q, strict=True):
            percentiles[(row.model_id, source)] = float(percentile)
    return percentiles


def validate_exposure_adequacy(
    values: Sequence[float], tissue: str, field: str
) -> dict[str, object]:
    if len(values) != 17 or not all(math.isfinite(value) for value in values):
        raise IntegrityError(f"incomplete/nonfinite {field} exposure: {tissue}")
    ties = Counter(values)
    distinct = len(ties)
    largest_tie = max(ties.values())
    if distinct < MINIMUM_DISTINCT_EXPOSURES:
        raise IntegrityError(
            f"inadequate {field} exposure levels for {tissue}: {distinct}"
        )
    if largest_tie > MAXIMUM_LARGEST_TIE:
        raise IntegrityError(
            f"inadequate {field} largest tie for {tissue}: {largest_tie}"
        )
    return {
        "n": len(values),
        "distinct_exposure_values": distinct,
        "largest_tie": largest_tie,
        "nonzero_exposures": sum(value != 0 for value in values),
    }


def build_exposures(
    records: Sequence[ScreenCountRecord], cohort: dict[str, str]
) -> tuple[list[ExposureRecord], dict[str, dict[str, object]]]:
    by_key = {(row.model_id, row.source): row for row in records}
    included_q = count_percentiles(records, PRIMARY_FIELD)
    passing_q = count_percentiles(records, SENSITIVITY_FIELD)
    exposures: list[ExposureRecord] = []
    for model_id, tissue in sorted(cohort.items(), key=lambda item: (item[1], item[0])):
        avana = by_key.get((model_id, "Avana"))
        ky = by_key.get((model_id, "KY"))
        if avana is None or ky is None or avana.tissue != tissue or ky.tissue != tissue:
            raise IntegrityError(f"paired cohort identity absent from denominator: {model_id}")
        avana_included_q = included_q[(model_id, "Avana")]
        ky_included_q = included_q[(model_id, "KY")]
        avana_passing_q = passing_q[(model_id, "Avana")]
        ky_passing_q = passing_q[(model_id, "KY")]
        exposures.append(
            ExposureRecord(
                model_id=model_id,
                tissue=tissue,
                avana_n_included=avana.n_included,
                ky_n_included=ky.n_included,
                avana_included_percentile=avana_included_q,
                ky_included_percentile=ky_included_q,
                included_asymmetry=abs(avana_included_q - ky_included_q),
                avana_n_passing=avana.n_passing,
                ky_n_passing=ky.n_passing,
                avana_passing_percentile=avana_passing_q,
                ky_passing_percentile=ky_passing_q,
                passing_asymmetry=abs(avana_passing_q - ky_passing_q),
            )
        )
    adequacy: dict[str, dict[str, object]] = {}
    for field, attribute in (
        (PRIMARY_FIELD, "included_asymmetry"),
        (SENSITIVITY_FIELD, "passing_asymmetry"),
    ):
        adequacy[field] = {}
        for tissue in TISSUES:
            values = [
                getattr(row, attribute) for row in exposures if row.tissue == tissue
            ]
            adequacy[field][tissue] = validate_exposure_adequacy(values, tissue, field)
    return exposures, adequacy


def load_outcomes(path: Path, cohort: dict[str, str]) -> tuple[list[dict[str, str]], str]:
    actual = sha256(path)
    if actual != EXPECTED_OUTCOME_HASH:
        raise IntegrityError(
            f"gap_file SHA-256 drift: expected {EXPECTED_OUTCOME_HASH}, got {actual}"
        )
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    seen: set[str] = set()
    for row in rows:
        model_id = row["model_id"].strip()
        tissue = row["tissue"].strip()
        if model_id in seen or cohort.get(model_id) != tissue:
            raise IntegrityError(f"outcome identity drift: {model_id} {tissue}")
        try:
            gap = float(row["absolute_percentile_gap"])
        except ValueError as exc:
            raise IntegrityError(f"non-numeric outcome: {model_id}") from exc
        if not math.isfinite(gap) or not 0 <= gap <= 1:
            raise IntegrityError(f"invalid outcome: {model_id}")
        if row["discordant_ge_0_25"].strip().lower() not in {"true", "false"}:
            raise IntegrityError(f"invalid outcome flag: {model_id}")
        seen.add(model_id)
    if len(rows) != 34 or seen != set(cohort):
        raise IntegrityError("outcome cohort drift")
    return rows, actual


def build_analysis_records(
    exposures: Sequence[ExposureRecord], outcomes: Sequence[dict[str, str]]
) -> list[AnalysisRecord]:
    exposure_by_id = {row.model_id: row for row in exposures}
    output: list[AnalysisRecord] = []
    for outcome in outcomes:
        exposure = exposure_by_id[outcome["model_id"].strip()]
        output.append(
            AnalysisRecord(
                model_id=exposure.model_id,
                model_name=outcome["model_name"].strip(),
                tissue=exposure.tissue,
                label=outcome["label"].strip(),
                avana_n_included=exposure.avana_n_included,
                ky_n_included=exposure.ky_n_included,
                avana_included_percentile=exposure.avana_included_percentile,
                ky_included_percentile=exposure.ky_included_percentile,
                included_asymmetry=exposure.included_asymmetry,
                avana_n_passing=exposure.avana_n_passing,
                ky_n_passing=exposure.ky_n_passing,
                avana_passing_percentile=exposure.avana_passing_percentile,
                ky_passing_percentile=exposure.ky_passing_percentile,
                passing_asymmetry=exposure.passing_asymmetry,
                wrn_percentile_gap=float(outcome["absolute_percentile_gap"]),
                exp005_gap_flag=outcome["discordant_ge_0_25"].strip().lower() == "true",
            )
        )
    return sorted(output, key=lambda row: (row.tissue, row.model_id))


def frozen_rank_arrays(
    rows: Sequence[AnalysisRecord], exposure_attribute: str
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    arrays = {}
    for tissue in TISSUES:
        selected = [row for row in rows if row.tissue == tissue]
        if len(selected) != 17:
            raise IntegrityError(f"analysis tissue count drift: {tissue}")
        exposure = np.asarray([getattr(row, exposure_attribute) for row in selected])
        outcome = np.asarray([row.wrn_percentile_gap for row in selected])
        x_rank = rankdata(exposure, method="average")
        y_rank = rankdata(outcome, method="average")
        if np.all(x_rank == x_rank[0]) or np.all(y_rank == y_rank[0]):
            raise IntegrityError(f"constant analysis rank vector: {tissue}")
        arrays[tissue] = (x_rank, y_rank)
    return arrays


def analyze_field(
    rows: Sequence[AnalysisRecord], field: str, seed: int, permutations: int, bootstraps: int
) -> dict[str, object]:
    attribute = {
        PRIMARY_FIELD: "included_asymmetry",
        SENSITIVITY_FIELD: "passing_asymmetry",
    }[field]
    arrays = frozen_rank_arrays(rows, attribute)
    theta, tissue = estimate_from_arrays(arrays)
    rng = np.random.default_rng(seed)
    p_value = permutation_pvalue(arrays, theta, permutations, rng)
    ci_low, ci_high = bootstrap_interval(arrays, bootstraps, rng)
    return {
        "field": field,
        "theta_equal_tissue_mean_spearman": theta,
        "tissue_spearman": tissue,
        "permutation_p_one_sided": p_value,
        "bootstrap_ci_95": [ci_low, ci_high],
    }


def write_records(path: Path, rows: Sequence[AnalysisRecord]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(AnalysisRecord.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def run(args: argparse.Namespace) -> dict[str, object]:
    pre_outcome_receipt = verify_pre_outcome_hashes(args)
    cohort = load_cohort(Path(args.cohort_file))
    denominators = load_denominators(Path(args.model_file))
    count_records, count_relationship = load_screen_counts(
        Path(args.qc_file), denominators
    )
    exposures, exposure_adequacy = build_exposures(count_records, cohort)

    # The outcome file is neither hashed nor opened until every exposure-only gate passes.
    outcomes, outcome_hash = load_outcomes(Path(args.gap_file), cohort)
    rows = build_analysis_records(exposures, outcomes)
    primary = analyze_field(
        rows, PRIMARY_FIELD, args.seed, args.permutations, args.bootstraps
    )
    sensitivity = analyze_field(
        rows, SENSITIVITY_FIELD, args.seed, args.permutations, args.bootstraps
    )
    gates = {
        "point_target_theta_at_least_0_40": primary[
            "theta_equal_tissue_mean_spearman"
        ]
        >= 0.40,
        "permutation_p_at_most_0_05": primary["permutation_p_one_sided"] <= 0.05,
        "practical_ci_lower_above_0_10": primary["bootstrap_ci_95"][0] > 0.10,
        "no_tissue_below_minus_0_20": min(primary["tissue_spearman"].values())
        >= -0.20,
    }
    overall_pass = all(gates.values())
    write_records(Path(args.model_output), rows)
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": (
            "PASS_SEQUENCE_INCLUSION_ASSOCIATION"
            if overall_pass
            else "FAIL_SEQUENCE_INCLUSION_ASSOCIATION"
        ),
        "analysis_type": "preregistered_derived_observational_analysis_after_endpoint_unsealing",
        "input_receipt": {
            **pre_outcome_receipt,
            "gap_file_sha256_after_adequacy": outcome_hash,
        },
        "adequacy": {
            "full_model_source_records": len(count_records),
            "unique_screen_ids": len({row.screen_id for row in count_records}),
            "paired_models": len(exposures),
            "paired_by_tissue": {tissue: 17 for tissue in TISSUES},
            "count_field_relationship": count_relationship,
            "exposure_structure": exposure_adequacy,
            "adequate": True,
        },
        "seed_per_field": args.seed,
        "permutation_repeats_per_field": args.permutations,
        "bootstrap_repeats_per_field": args.bootstraps,
        "primary": primary,
        "sensitivity": {
            **sensitivity,
            "independent_corroboration": False,
            "can_rescue_primary_failure": False,
        },
        "primary_gates": gates,
        "overall_pass": overall_pass,
        "claim_boundary": "descriptive observational association, not causal explanation",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cohort-file", default="experiments/EXP-20260822-007/cohort.csv"
    )
    parser.add_argument(
        "--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv"
    )
    parser.add_argument(
        "--model-file", default="experiments/EXP-20260822-003/results/model_scores.csv"
    )
    parser.add_argument(
        "--gap-file",
        default="experiments/EXP-20260822-005/results/model_percentile_gaps.csv",
    )
    parser.add_argument(
        "--output", default="experiments/EXP-20260822-009/results/summary.json"
    )
    parser.add_argument(
        "--model-output",
        default="experiments/EXP-20260822-009/results/model_sequence_asymmetry.csv",
    )
    parser.add_argument("--seed", type=int, default=20260829)
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
