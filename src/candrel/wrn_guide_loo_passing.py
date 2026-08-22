from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import tempfile
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from candrel.wrn_ordering import dependency_percentiles, fixed_percentile_correlation
from candrel import wrn_sequence_semantics as base


EXPERIMENT_ID = "EXP-20260822-012"
FLAG_THRESHOLD = 0.25
MINIMUM_FULLY_ROBUST = 8
BASELINE_ATOL = 1e-8
EXPECTED_GAP_HASH = "f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a"
EXPECTED_PREBASELINE_HASHES = {
    "avana_guide_map": "5580f89d2bbd26d25cf107c6441dcc30774a333385e104e83e1212ca16ec99a2",
    "ky_guide_map": "23bafc0d2f88b25727af8e2f5d0245495c39243163fb465ceffc9755c012c4b0",
    "sequence_map": "e4b99b4a6cd48c3957c5ada2abeeed1e1de319fe26526e76de6088ec73704c0b",
    "qc_file": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "naive_file": "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721",
    "denominator_file": "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654",
    "parent_preregistration": "d95cdfda5cdad1e4f7a223dc9cd4e31da3cad90c38f7953d4f27609a6d381272",
    "parent_manifest": "54f5c13ed17de783275c46b7442d6bd41a199acc269134528d568210ebfe1042",
    "parent_implementation": "22538414d2cafa94215354e6af9087d47afbd38d6f897f34f13b68ea7f93b3e4",
    "parent_summary": "f1df2711856ea08ba166c18436ea96c799c6494c5cf069f5cb71c1f6a0ed5b9a",
    "parent_ledger": "29eb728f0b05e1ff4838f1a4012a5bf76f577bee92986380c0f9c9d9f7b73354",
    "parent_result": "ccd1e33dc2c764b0f8cd229f63ed7cb63c4534b6831349b0ba9467834e599dd1",
    "parent_audit": "d4be1b9d2d314db6de59bfb1805af98af9d9a033e8419b46bde6e49e622b7ee6",
}

IntegrityError = base.IntegrityError
FrozenScreen = base.FrozenScreen


@dataclass(frozen=True)
class GapRecord:
    model_id: str
    model_name: str
    tissue: str
    label: str
    avana_score: float
    ky_score: float
    avana_percentile: float
    ky_percentile: float
    baseline_gap: float
    baseline_flagged: bool


@dataclass(frozen=True)
class ModelRobustness:
    model_id: str
    model_name: str
    tissue: str
    label: str
    baseline_gap: float
    baseline_flagged: bool
    avana_all_omissions_retain_flag: bool
    ky_all_omissions_retain_flag: bool
    fully_robust_all_nine: bool
    flagged_omissions_of_nine: int
    min_gap_all_ten_configurations: float
    median_gap_all_ten_configurations: float
    max_gap_all_ten_configurations: float


def verify_prebaseline_hashes(args: argparse.Namespace) -> dict[str, str]:
    receipt = {}
    for argument, expected in EXPECTED_PREBASELINE_HASHES.items():
        actual = base.sha256(Path(getattr(args, argument)))
        if actual != expected:
            raise IntegrityError(
                f"{argument} SHA-256 drift: expected {expected}, got {actual}"
            )
        receipt[f"{argument}_sha256"] = actual
    return receipt


def strict_median(values: Sequence[float]) -> float:
    ordered = sorted(float(value) for value in values)
    if not ordered or not all(math.isfinite(value) for value in ordered):
        raise IntegrityError("median requires nonempty finite values")
    middle = len(ordered) // 2
    if len(ordered) % 2:
        result = ordered[middle]
    else:
        result = (ordered[middle - 1] + ordered[middle]) / 2.0
    if not math.isfinite(result):
        raise IntegrityError("non-finite median")
    return result


def reconstruct_guide_means(
    frozen: Sequence[FrozenScreen],
    passing_sequences: dict[tuple[str, str, str], tuple[str, ...]],
    lfc_by_source: dict[str, dict[str, dict[str, float]]],
) -> dict[tuple[str, str, str], dict[str, float]]:
    output = {}
    for screen in frozen:
        identity = (screen.screen_id, screen.model_id, screen.source)
        sequence_ids = passing_sequences[identity]
        guide_means = {}
        for guide in base.EXPECTED_GUIDES[screen.source]:
            values = [lfc_by_source[screen.source][guide][seq] for seq in sequence_ids]
            if not values or not all(math.isfinite(value) for value in values):
                raise IntegrityError(f"invalid guide values: {identity} {guide}")
            guide_means[guide] = float(np.mean(np.asarray(values, dtype=float)))
        if tuple(sorted(guide_means)) != base.EXPECTED_GUIDES[screen.source]:
            raise IntegrityError(f"guide-mean identity drift: {identity}")
        output[identity] = guide_means
    if len(output) != 103:
        raise IntegrityError("guide-mean screen count drift")
    return output


def scores_from_guide_means(
    guide_means: dict[tuple[str, str, str], dict[str, float]],
    omitted_source: str | None = None,
    omitted_guide: str | None = None,
    expected_records: int = 103,
) -> dict[tuple[str, str, str], float]:
    if (omitted_source is None) != (omitted_guide is None):
        raise IntegrityError("omitted source and guide must be specified together")
    if omitted_source is not None:
        if omitted_source not in base.SOURCES:
            raise IntegrityError(f"invalid omitted source: {omitted_source}")
        if omitted_guide not in base.EXPECTED_GUIDES[omitted_source]:
            raise IntegrityError(f"invalid omitted guide: {omitted_source} {omitted_guide}")
    output = {}
    for identity, means in guide_means.items():
        source = identity[2]
        retained = [
            means[guide]
            for guide in base.EXPECTED_GUIDES[source]
            if not (source == omitted_source and guide == omitted_guide)
        ]
        expected_count = len(base.EXPECTED_GUIDES[source]) - int(source == omitted_source)
        if len(retained) != expected_count:
            raise IntegrityError(f"retained-guide count drift: {identity}")
        output[identity] = strict_median(retained)
    if len(output) != expected_records:
        raise IntegrityError("score identity count drift")
    return output


def verify_official_baseline(
    ledger: Sequence[base.ReconstructionLedgerRow],
) -> dict[str, object]:
    if len(ledger) != 103:
        raise IntegrityError("baseline ledger count drift")
    maximum = max(row.absolute_discrepancy for row in ledger)
    passing = sum(row.passes_absolute_1e_8_gate for row in ledger)
    if passing != 103 or maximum > BASELINE_ATOL:
        raise IntegrityError(
            f"baseline reconstruction drift: passing={passing}/103 max={maximum}"
        )
    return {
        "comparisons": 103,
        "passing_comparisons": passing,
        "absolute_tolerance": BASELINE_ATOL,
        "relative_tolerance": 0,
        "maximum_absolute_discrepancy": maximum,
        "passed": True,
    }


def verify_parent_ledger(
    path: Path, current: Sequence[base.ReconstructionLedgerRow]
) -> dict[str, object]:
    expected_fields = tuple(base.ReconstructionLedgerRow.__dataclass_fields__)
    parent = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected_fields:
            raise IntegrityError("parent ledger schema drift")
        for row in reader:
            identity = (row["screen_id"], row["model_id"], row["source"])
            if identity in parent:
                raise IntegrityError(f"duplicate parent ledger identity: {identity}")
            parent[identity] = row
    if len(parent) != 103:
        raise IntegrityError("parent ledger row count drift")
    maximum_score_drift = 0.0
    maximum_official_drift = 0.0
    for row in current:
        identity = (row.screen_id, row.model_id, row.source)
        stored = parent.get(identity)
        if stored is None:
            raise IntegrityError(f"missing parent ledger identity: {identity}")
        if stored["tissue"] != row.tissue:
            raise IntegrityError(f"parent ledger tissue drift: {identity}")
        for field, value in (
            ("n_passing_sequences", row.n_passing_sequences),
            ("n_included_sequences", row.n_included_sequences),
            ("retained_sequence_count", row.retained_sequence_count),
        ):
            if base.parse_nonnegative_integer(stored[field], (identity, field)) != value:
                raise IntegrityError(f"parent ledger count drift: {identity} {field}")
        stored_pass = base.parse_canonical_bool(
            stored["passes_absolute_1e_8_gate"], (identity, "gate")
        )
        if not stored_pass or stored_pass != row.passes_absolute_1e_8_gate:
            raise IntegrityError(f"parent ledger gate drift: {identity}")
        reconstructed = base.parse_finite(stored["reconstructed_score"], identity)
        official = base.parse_finite(stored["official_score"], identity)
        discrepancy = base.parse_finite(stored["absolute_discrepancy"], identity)
        maximum_score_drift = max(maximum_score_drift, abs(reconstructed - row.reconstructed_score))
        maximum_official_drift = max(maximum_official_drift, abs(official - row.official_score))
        if (
            abs(reconstructed - row.reconstructed_score) > BASELINE_ATOL
            or abs(official - row.official_score) > BASELINE_ATOL
            or abs(discrepancy - row.absolute_discrepancy) > BASELINE_ATOL
        ):
            raise IntegrityError(f"parent ledger numeric drift: {identity}")
    return {
        "rows": len(parent),
        "maximum_reconstructed_score_drift": maximum_score_drift,
        "maximum_official_score_drift": maximum_official_drift,
        "passed": True,
    }


def load_gap_records(
    path: Path, frozen: Sequence[FrozenScreen]
) -> tuple[list[GapRecord], str]:
    actual_hash = base.sha256(path)
    if actual_hash != EXPECTED_GAP_HASH:
        raise IntegrityError(
            f"gap file SHA-256 drift: expected {EXPECTED_GAP_HASH}, got {actual_hash}"
        )
    expected_tissues = {}
    source_counts = Counter()
    for screen in frozen:
        key = (screen.model_id, screen.source)
        if key in source_counts:
            raise IntegrityError(f"duplicate model-source denominator: {key}")
        source_counts[key] += 1
        if screen.model_id in expected_tissues and expected_tissues[screen.model_id] != screen.tissue:
            raise IntegrityError(f"cross-tissue model drift: {screen.model_id}")
        expected_tissues[screen.model_id] = screen.tissue
    rows = []
    seen = set()
    counts = Counter()
    flagged = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            model_id = row["model_id"].strip()
            tissue = row["tissue"].strip()
            if (
                not model_id
                or model_id in seen
                or tissue not in base.TISSUES
                or expected_tissues.get(model_id) != tissue
                or source_counts[(model_id, "Avana")] != 1
                or source_counts[(model_id, "KY")] != 1
            ):
                raise IntegrityError(f"invalid gap identity: {model_id} {tissue}")
            is_flagged = base.parse_canonical_bool(
                row["discordant_ge_0_25"], (model_id, "discordant_ge_0_25")
            )
            gap = base.parse_finite(row["absolute_percentile_gap"], (model_id, "gap"))
            if is_flagged != (gap >= FLAG_THRESHOLD):
                raise IntegrityError(f"stored gap flag drift: {model_id}")
            rows.append(
                GapRecord(
                    model_id=model_id,
                    model_name=row["model_name"].strip(),
                    tissue=tissue,
                    label=row["label"].strip(),
                    avana_score=base.parse_finite(row["avana_score"], (model_id, "avana_score")),
                    ky_score=base.parse_finite(row["ky_score"], (model_id, "ky_score")),
                    avana_percentile=base.parse_finite(
                        row["avana_percentile"], (model_id, "avana_percentile")
                    ),
                    ky_percentile=base.parse_finite(
                        row["ky_percentile"], (model_id, "ky_percentile")
                    ),
                    baseline_gap=gap,
                    baseline_flagged=is_flagged,
                )
            )
            seen.add(model_id)
            counts[tissue] += 1
            flagged += int(is_flagged)
    if (
        len(rows) != 34
        or dict(counts) != {tissue: 17 for tissue in base.TISSUES}
        or flagged != 10
    ):
        raise IntegrityError(
            f"gap population drift: n={len(rows)} counts={dict(counts)} flagged={flagged}"
        )
    return sorted(rows, key=lambda row: (row.tissue, row.model_id)), actual_hash


def percentiles_for_scores(
    frozen: Sequence[FrozenScreen],
    scores: dict[tuple[str, str, str], float],
) -> dict[tuple[str, str], float]:
    grouped: dict[tuple[str, str], list[FrozenScreen]] = defaultdict(list)
    for screen in frozen:
        grouped[(screen.source, screen.tissue)].append(screen)
    if {key: len(value) for key, value in grouped.items()} != base.EXPECTED_DENOMINATORS:
        raise IntegrityError("percentile denominator drift")
    output = {}
    for (source, _tissue), screens in grouped.items():
        ordered = sorted(screens, key=lambda row: row.model_id)
        values = [scores[(row.screen_id, row.model_id, source)] for row in ordered]
        percentiles = dependency_percentiles(values)
        for screen, percentile in zip(ordered, percentiles, strict=True):
            key = (screen.model_id, source)
            if key in output:
                raise IntegrityError(f"duplicate percentile identity: {key}")
            output[key] = float(percentile)
    if len(output) != 103 or not all(math.isfinite(value) for value in output.values()):
        raise IntegrityError("percentile identity/value drift")
    return output


def gaps_for_configuration(
    records: Sequence[GapRecord], percentiles: dict[tuple[str, str], float]
) -> dict[str, float]:
    output = {}
    for row in records:
        gap = abs(
            percentiles[(row.model_id, "Avana")]
            - percentiles[(row.model_id, "KY")]
        )
        if not math.isfinite(gap):
            raise IntegrityError(f"non-finite gap: {row.model_id}")
        output[row.model_id] = gap
    if len(output) != 34:
        raise IntegrityError("gap count drift")
    return output


def verify_exp005_baseline(
    records: Sequence[GapRecord],
    frozen: Sequence[FrozenScreen],
    scores: dict[tuple[str, str, str], float],
    percentiles: dict[tuple[str, str], float],
    gaps: dict[str, float],
) -> dict[str, object]:
    identity_by_model_source = {
        (row.model_id, row.source): (row.screen_id, row.model_id, row.source)
        for row in frozen
    }
    maximum_score = 0.0
    maximum_percentile = 0.0
    maximum_gap = 0.0
    for row in records:
        for source, stored_score, stored_percentile in (
            ("Avana", row.avana_score, row.avana_percentile),
            ("KY", row.ky_score, row.ky_percentile),
        ):
            identity = identity_by_model_source[(row.model_id, source)]
            score_drift = abs(scores[identity] - stored_score)
            percentile_drift = abs(percentiles[(row.model_id, source)] - stored_percentile)
            maximum_score = max(maximum_score, score_drift)
            maximum_percentile = max(maximum_percentile, percentile_drift)
            if score_drift > BASELINE_ATOL or percentile_drift > BASELINE_ATOL:
                raise IntegrityError(f"EXP-005 baseline drift: {row.model_id} {source}")
        gap_drift = abs(gaps[row.model_id] - row.baseline_gap)
        maximum_gap = max(maximum_gap, gap_drift)
        if gap_drift > BASELINE_ATOL:
            raise IntegrityError(f"EXP-005 gap drift: {row.model_id}")
    return {
        "paired_models": len(records),
        "locked_flagged_models": sum(row.baseline_flagged for row in records),
        "maximum_score_discrepancy": maximum_score,
        "maximum_percentile_discrepancy": maximum_percentile,
        "maximum_gap_discrepancy": maximum_gap,
        "absolute_tolerance": BASELINE_ATOL,
        "passed": True,
    }


def equal_tissue_theta(
    records: Sequence[GapRecord], percentiles: dict[tuple[str, str], float]
) -> float:
    estimates = []
    for tissue in base.TISSUES:
        selected = [row for row in records if row.tissue == tissue]
        if len(selected) != 17:
            raise IntegrityError(f"paired tissue count drift: {tissue}")
        avana = np.asarray([percentiles[(row.model_id, "Avana")] for row in selected])
        ky = np.asarray([percentiles[(row.model_id, "KY")] for row in selected])
        estimates.append(fixed_percentile_correlation(avana, ky))
    result = float(np.mean(estimates))
    if not math.isfinite(result):
        raise IntegrityError("non-finite equal-tissue theta")
    return result


def summarize_robustness(
    records: Sequence[GapRecord],
    omission_gaps: dict[str, dict[str, float]],
) -> tuple[list[ModelRobustness], dict[str, object]]:
    avana_configs = sorted(name for name in omission_gaps if name.startswith("omit_Avana_"))
    ky_configs = sorted(name for name in omission_gaps if name.startswith("omit_KY_"))
    if len(avana_configs) != 4 or len(ky_configs) != 5 or len(omission_gaps) != 9:
        raise IntegrityError("omission configuration count drift")
    rows = []
    for record in records:
        avana_all = all(
            omission_gaps[name][record.model_id] >= FLAG_THRESHOLD
            for name in avana_configs
        )
        ky_all = all(
            omission_gaps[name][record.model_id] >= FLAG_THRESHOLD
            for name in ky_configs
        )
        omitted_values = [
            omission_gaps[name][record.model_id]
            for name in [*avana_configs, *ky_configs]
        ]
        all_values = [record.baseline_gap, *omitted_values]
        rows.append(
            ModelRobustness(
                model_id=record.model_id,
                model_name=record.model_name,
                tissue=record.tissue,
                label=record.label,
                baseline_gap=record.baseline_gap,
                baseline_flagged=record.baseline_flagged,
                avana_all_omissions_retain_flag=avana_all,
                ky_all_omissions_retain_flag=ky_all,
                fully_robust_all_nine=avana_all and ky_all,
                flagged_omissions_of_nine=sum(
                    value >= FLAG_THRESHOLD for value in omitted_values
                ),
                min_gap_all_ten_configurations=min(all_values),
                median_gap_all_ten_configurations=strict_median(all_values),
                max_gap_all_ten_configurations=max(all_values),
            )
        )
    locked = [row for row in rows if row.baseline_flagged]
    unflagged_ids = {row.model_id for row in rows if not row.baseline_flagged}
    fully_robust = sum(row.fully_robust_all_nine for row in locked)
    unique_new = {
        model_id
        for model_id in unflagged_ids
        if any(values[model_id] >= FLAG_THRESHOLD for values in omission_gaps.values())
    }
    transitions = sum(
        values[model_id] >= FLAG_THRESHOLD
        for model_id in unflagged_ids
        for values in omission_gaps.values()
    )
    return rows, {
        "locked_baseline_flagged_models": len(locked),
        "fully_robust_flagged_models": fully_robust,
        "minimum_fully_robust_required": MINIMUM_FULLY_ROBUST,
        "avana_all_omissions_robust_models": sum(
            row.avana_all_omissions_retain_flag for row in locked
        ),
        "ky_all_omissions_robust_models": sum(
            row.ky_all_omissions_retain_flag for row in locked
        ),
        "unique_baseline_unflagged_becoming_flagged": len(unique_new),
        "unique_transition_model_ids": sorted(unique_new),
        "total_unflagged_to_flagged_transitions": int(transitions),
        "possible_unflagged_configuration_transitions": 24 * 9,
        "primary_pass": fully_robust >= MINIMUM_FULLY_ROBUST,
    }


def write_rows(path: Path, fields: Sequence[str], rows: Sequence[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_guide_means(
    path: Path,
    frozen: Sequence[FrozenScreen],
    guide_means: dict[tuple[str, str, str], dict[str, float]],
) -> None:
    fields = ["screen_id", "model_id", "source", "tissue"]
    for index in range(1, 6):
        fields.extend([f"guide_{index}_sequence", f"guide_{index}_mean"])
    rows = []
    for screen in frozen:
        identity = (screen.screen_id, screen.model_id, screen.source)
        payload: dict[str, object] = {
            "screen_id": screen.screen_id,
            "model_id": screen.model_id,
            "source": screen.source,
            "tissue": screen.tissue,
        }
        for index, guide in enumerate(base.EXPECTED_GUIDES[screen.source], start=1):
            payload[f"guide_{index}_sequence"] = guide
            payload[f"guide_{index}_mean"] = guide_means[identity][guide]
        rows.append(payload)
    write_rows(path, fields, rows)


def build_screen_configuration_rows(
    frozen: Sequence[FrozenScreen],
    configurations: Sequence[
        tuple[
            str,
            str,
            str,
            dict[tuple[str, str, str], float],
            dict[tuple[str, str], float],
        ]
    ],
) -> list[dict[str, object]]:
    rows = []
    for name, omitted_source, omitted_guide, scores, percentiles in configurations:
        for screen in frozen:
            identity = (screen.screen_id, screen.model_id, screen.source)
            retained_guide_count = len(base.EXPECTED_GUIDES[screen.source]) - int(
                screen.source == omitted_source
            )
            rows.append(
                {
                    "configuration": name,
                    "omitted_source": omitted_source,
                    "omitted_guide": omitted_guide,
                    "screen_id": screen.screen_id,
                    "model_id": screen.model_id,
                    "source": screen.source,
                    "tissue": screen.tissue,
                    "reconstructed_score": scores[identity],
                    "dependency_percentile": percentiles[(screen.model_id, screen.source)],
                    "retained_guide_count": retained_guide_count,
                }
            )
    expected = len(frozen) * len(configurations)
    if len(rows) != expected:
        raise IntegrityError(
            f"screen-configuration ledger count drift: {len(rows)} != {expected}"
        )
    return rows


def run(args: argparse.Namespace, output_dir: Path) -> dict[str, object]:
    prebaseline_receipt = verify_prebaseline_hashes(args)
    frozen = base.load_frozen_screens(Path(args.denominator_file))
    qc_counts = base.load_qc_counts(Path(args.qc_file), frozen)
    passing_sequences = base.load_passing_sequences(Path(args.sequence_map), frozen, qc_counts)
    guides = {
        "Avana": base.load_guides(Path(args.avana_guide_map), "Avana"),
        "KY": base.load_guides(Path(args.ky_guide_map), "KY"),
    }
    lfc = {}
    lfc_receipts = {}
    for source, argument in (("Avana", "avana_lfc"), ("KY", "ky_lfc")):
        required_sequences = {
            sequence
            for identity, values in passing_sequences.items()
            if identity[2] == source
            for sequence in values
        }
        lfc[source], lfc_receipts[source] = base.extract_lfc(
            Path(getattr(args, argument)), source, guides[source], required_sequences
        )
    guide_means = reconstruct_guide_means(frozen, passing_sequences, lfc)
    baseline_scores = scores_from_guide_means(guide_means)
    official, naive_hash = base.extract_official_scores(
        Path(args.naive_file), {row.screen_id for row in frozen}
    )
    current_ledger = base.build_ledger(
        frozen, qc_counts, passing_sequences, baseline_scores, official
    )
    official_gate = verify_official_baseline(current_ledger)
    parent_ledger_gate = verify_parent_ledger(Path(args.parent_ledger), current_ledger)

    # The outcome-bearing EXP-005 gap file is not loaded before both baseline gates pass.
    gap_records, gap_hash = load_gap_records(Path(args.gap_file), frozen)
    baseline_percentiles = percentiles_for_scores(frozen, baseline_scores)
    baseline_gaps = gaps_for_configuration(gap_records, baseline_percentiles)
    exp005_gate = verify_exp005_baseline(
        gap_records, frozen, baseline_scores, baseline_percentiles, baseline_gaps
    )

    omission_gaps = {}
    configuration_rows = [
        {
            "configuration": "baseline",
            "source": "",
            "omitted_guide": "",
            "equal_tissue_theta": equal_tissue_theta(gap_records, baseline_percentiles),
            "flagged_models": sum(value >= FLAG_THRESHOLD for value in baseline_gaps.values()),
        }
    ]
    screen_configurations = [
        ("baseline", "", "", baseline_scores, baseline_percentiles)
    ]
    perturbed_thetas = []
    for source in base.SOURCES:
        for guide in sorted(guides[source]):
            name = f"omit_{source}_{guide}"
            scores = scores_from_guide_means(guide_means, source, guide)
            percentiles = percentiles_for_scores(frozen, scores)
            gaps = gaps_for_configuration(gap_records, percentiles)
            theta = equal_tissue_theta(gap_records, percentiles)
            omission_gaps[name] = gaps
            perturbed_thetas.append(theta)
            screen_configurations.append((name, source, guide, scores, percentiles))
            configuration_rows.append(
                {
                    "configuration": name,
                    "source": source,
                    "omitted_guide": guide,
                    "equal_tissue_theta": theta,
                    "flagged_models": sum(value >= FLAG_THRESHOLD for value in gaps.values()),
                }
            )
    if len(omission_gaps) != 9 or len(configuration_rows) != 10:
        raise IntegrityError("configuration count drift")
    model_rows, primary = summarize_robustness(gap_records, omission_gaps)
    overall_pass = bool(primary["primary_pass"])

    model_configuration_rows = []
    for record in gap_records:
        for configuration, gaps in [("baseline", baseline_gaps), *omission_gaps.items()]:
            gap = gaps[record.model_id]
            model_configuration_rows.append(
                {
                    "model_id": record.model_id,
                    "model_name": record.model_name,
                    "tissue": record.tissue,
                    "label": record.label,
                    "baseline_flagged": record.baseline_flagged,
                    "configuration": configuration,
                    "gap": gap,
                    "flagged_ge_0_25": gap >= FLAG_THRESHOLD,
                }
            )
    screen_configuration_rows = build_screen_configuration_rows(
        frozen, screen_configurations
    )
    if len(screen_configuration_rows) != 1030:
        raise IntegrityError("full screen-configuration ledger must have 1,030 rows")
    write_rows(
        output_dir / "model_configuration_gaps.csv",
        [
            "model_id",
            "model_name",
            "tissue",
            "label",
            "baseline_flagged",
            "configuration",
            "gap",
            "flagged_ge_0_25",
        ],
        model_configuration_rows,
    )
    write_rows(
        output_dir / "model_robustness.csv",
        list(ModelRobustness.__dataclass_fields__),
        [asdict(row) for row in model_rows],
    )
    write_rows(
        output_dir / "configurations.csv",
        ["configuration", "source", "omitted_guide", "equal_tissue_theta", "flagged_models"],
        configuration_rows,
    )
    write_guide_means(output_dir / "reconstructed_guide_means.csv", frozen, guide_means)
    write_rows(
        output_dir / "screen_configuration_ledger.csv",
        [
            "configuration",
            "omitted_source",
            "omitted_guide",
            "screen_id",
            "model_id",
            "source",
            "tissue",
            "reconstructed_score",
            "dependency_percentile",
            "retained_guide_count",
        ],
        screen_configuration_rows,
    )

    artifact_receipt = {
        name: base.sha256(output_dir / name)
        for name in (
            "model_configuration_gaps.csv",
            "model_robustness.csv",
            "configurations.csv",
            "reconstructed_guide_means.csv",
            "screen_configuration_ledger.csv",
        )
    }
    artifact_receipt["summary.json"] = ""

    return {
        "experiment_id": EXPERIMENT_ID,
        "status": (
            "PASS_SINGLE_GUIDE_ROBUSTNESS"
            if overall_pass
            else "FAIL_SINGLE_GUIDE_ROBUSTNESS"
        ),
        "analysis_type": "preregistered_deterministic_same_assay_single_guide_robustness_after_endpoint_unsealing",
        "input_receipt": {
            **prebaseline_receipt,
            "gap_file_sha256_after_baseline_gates": gap_hash,
            "naive_file_sha256_recomputed_during_extraction": naive_hash,
            "large_lfc": lfc_receipts,
        },
        "adequacy": {
            "denominator_records": len(frozen),
            "paired_models": len(gap_records),
            "retained_passing_sequence_columns": {
                source: len(
                    {
                        sequence
                        for identity, values in passing_sequences.items()
                        if identity[2] == source
                        for sequence in values
                    }
                )
                for source in base.SOURCES
            },
            "eligible_guides": {source: list(values) for source, values in guides.items()},
            "official_baseline_gate": official_gate,
            "parent_ledger_gate": parent_ledger_gate,
            "exp005_baseline_gate": exp005_gate,
            "adequate": True,
        },
        "configurations": {
            "baseline_plus_omissions": 10,
            "single_guide_omissions": 9,
            "avana_omissions": 4,
            "ky_omissions": 5,
        },
        "primary": primary,
        "ordering_sensitivity": {
            "baseline_equal_tissue_theta": configuration_rows[0]["equal_tissue_theta"],
            "minimum_perturbed_theta": min(perturbed_thetas),
            "maximum_perturbed_theta": max(perturbed_thetas),
        },
        "interpretation_receipt": {
            "dependent_deterministic_perturbations": True,
            "p_values_computed": 0,
            "confidence_intervals_computed": 0,
            "guide_quality_or_causal_claim_supported": False,
            "multi_guide_robustness_tested": False,
        },
        "artifact_receipt_sha256": artifact_receipt,
        "overall_pass": overall_pass,
        "claim_boundary": "frozen same-assay passing-sequence single-guide robustness only",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--avana-lfc", default="data/raw/depmap/23q4/AvanaLogfoldChange.csv")
    parser.add_argument("--ky-lfc", default="data/raw/depmap/23q4/KYLogfoldChange.csv")
    parser.add_argument("--avana-guide-map", default="data/raw/depmap/23q4/AvanaGuideMap.csv")
    parser.add_argument("--ky-guide-map", default="data/raw/depmap/23q4/KYGuideMap.csv")
    parser.add_argument("--sequence-map", default="data/raw/depmap/23q4/ScreenSequenceMap.csv")
    parser.add_argument("--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv")
    parser.add_argument("--naive-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv")
    parser.add_argument("--denominator-file", default="experiments/EXP-20260822-003/results/model_scores.csv")
    parser.add_argument("--gap-file", default="experiments/EXP-20260822-005/results/model_percentile_gaps.csv")
    parser.add_argument("--parent-preregistration", default="experiments/EXP-20260822-011/preregistration.md")
    parser.add_argument("--parent-manifest", default="experiments/EXP-20260822-011/manifest.json")
    parser.add_argument("--parent-implementation", default="src/candrel/wrn_sequence_semantics.py")
    parser.add_argument("--parent-summary", default="experiments/EXP-20260822-011/results/summary.json")
    parser.add_argument("--parent-ledger", default="experiments/EXP-20260822-011/results/reconstruction_ledger.csv")
    parser.add_argument("--parent-result", default="experiments/EXP-20260822-011/result.md")
    parser.add_argument("--parent-audit", default="experiments/EXP-20260822-011/audit.md")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-012/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-012/error_receipt.json")
    return parser


EXPECTED_RESULT_FILES = {
    "summary.json",
    "model_configuration_gaps.csv",
    "model_robustness.csv",
    "configurations.csv",
    "reconstructed_guide_means.csv",
    "screen_configuration_ledger.csv",
}


def write_error_receipt(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
        delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def read_staged_csv(path: Path, fields: Sequence[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != tuple(fields):
            raise IntegrityError(f"staged CSV schema drift: {path.name}")
        rows = list(reader)
    return rows


def summary_digest(result: dict[str, object]) -> str:
    payload = json.loads(json.dumps(result))
    receipt = payload.get("artifact_receipt_sha256")
    if not isinstance(receipt, dict):
        raise IntegrityError("summary artifact receipt missing")
    receipt["summary.json"] = ""
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_summary_against_ledgers(
    result: dict[str, object],
    config_rows: Sequence[dict[str, str]],
    model_gap_rows: Sequence[dict[str, str]],
    robustness_rows: Sequence[dict[str, str]],
) -> None:
    configs = [row["configuration"] for row in config_rows]
    baseline_rows = [row for row in model_gap_rows if row["configuration"] == "baseline"]
    baseline_flags = {
        row["model_id"]: base.parse_canonical_bool(row["baseline_flagged"], row["model_id"])
        for row in baseline_rows
    }
    locked_ids = {model_id for model_id, flagged in baseline_flags.items() if flagged}
    unflagged_ids = set(baseline_flags) - locked_ids
    avana_names = [name for name in configs if name.startswith("omit_Avana_")]
    ky_names = [name for name in configs if name.startswith("omit_KY_")]
    gap_rows = {
        (row["configuration"], row["model_id"]): row for row in model_gap_rows
    }
    unique_new = {
        model_id
        for model_id in unflagged_ids
        if any(
            base.parse_canonical_bool(gap_rows[(configuration, model_id)]["flagged_ge_0_25"], model_id)
            for configuration in [*avana_names, *ky_names]
        )
    }
    transitions = sum(
        base.parse_canonical_bool(gap_rows[(configuration, model_id)]["flagged_ge_0_25"], model_id)
        for model_id in unflagged_ids
        for configuration in [*avana_names, *ky_names]
    )
    derived_fully_robust = sum(
        base.parse_canonical_bool(row["fully_robust_all_nine"], row["model_id"])
        for row in robustness_rows
        if row["model_id"] in locked_ids
    )
    derived_primary = {
        "locked_baseline_flagged_models": len(locked_ids),
        "fully_robust_flagged_models": derived_fully_robust,
        "minimum_fully_robust_required": MINIMUM_FULLY_ROBUST,
        "avana_all_omissions_robust_models": sum(
            base.parse_canonical_bool(row["avana_all_omissions_retain_flag"], row["model_id"])
            for row in robustness_rows
            if row["model_id"] in locked_ids
        ),
        "ky_all_omissions_robust_models": sum(
            base.parse_canonical_bool(row["ky_all_omissions_retain_flag"], row["model_id"])
            for row in robustness_rows
            if row["model_id"] in locked_ids
        ),
        "unique_baseline_unflagged_becoming_flagged": len(unique_new),
        "unique_transition_model_ids": sorted(unique_new),
        "total_unflagged_to_flagged_transitions": int(transitions),
        "possible_unflagged_configuration_transitions": 24 * 9,
        "primary_pass": derived_fully_robust >= MINIMUM_FULLY_ROBUST,
    }
    if result.get("primary") != derived_primary:
        raise IntegrityError("staged summary primary cross-check drift")
    if result.get("configurations") != {
        "baseline_plus_omissions": 10,
        "single_guide_omissions": 9,
        "avana_omissions": 4,
        "ky_omissions": 5,
    }:
        raise IntegrityError("staged summary configuration-count drift")
    theta_by_config = {
        row["configuration"]: base.parse_finite(row["equal_tissue_theta"], row["configuration"])
        for row in config_rows
    }
    ordering = result.get("ordering_sensitivity")
    if not isinstance(ordering, dict):
        raise IntegrityError("staged summary ordering schema drift")
    expected_ordering = {
        "baseline_equal_tissue_theta": theta_by_config["baseline"],
        "minimum_perturbed_theta": min(theta_by_config[name] for name in [*avana_names, *ky_names]),
        "maximum_perturbed_theta": max(theta_by_config[name] for name in [*avana_names, *ky_names]),
    }
    for key, expected in expected_ordering.items():
        actual = base.parse_finite(str(ordering.get(key)), key)
        if abs(actual - expected) > 1e-12:
            raise IntegrityError("staged summary ordering cross-check drift")
    if result["overall_pass"] != derived_primary["primary_pass"]:
        raise IntegrityError("staged summary overall-pass cross-check drift")


def validate_staged_result_files(
    stage: Path,
    result: dict[str, object],
    frozen: Sequence[FrozenScreen] | None = None,
) -> None:
    actual_files = {path.name for path in stage.iterdir() if path.is_file()}
    if actual_files != EXPECTED_RESULT_FILES:
        raise IntegrityError(f"staged result-file drift: {sorted(actual_files)}")

    config_fields = (
        "configuration", "source", "omitted_guide", "equal_tissue_theta", "flagged_models"
    )
    config_rows = read_staged_csv(stage / "configurations.csv", config_fields)
    configs = [row["configuration"] for row in config_rows]
    if len(config_rows) != 10 or len(set(configs)) != 10 or configs[0] != "baseline":
        raise IntegrityError("staged configuration row drift")
    if any(
        not math.isfinite(base.parse_finite(row["equal_tissue_theta"], row["configuration"]))
        or not 0 <= base.parse_nonnegative_integer(row["flagged_models"], row["configuration"]) <= 34
        for row in config_rows
    ):
        raise IntegrityError("staged configuration value drift")
    for row in config_rows:
        name = row["configuration"]
        if name == "baseline":
            if row["source"] or row["omitted_guide"]:
                raise IntegrityError("staged configuration baseline metadata drift")
        else:
            if not name.startswith("omit_"):
                raise IntegrityError("staged configuration name drift")
            _, expected_source, expected_guide = name.split("_", 2)
            if (
                row["source"] != expected_source
                or row["omitted_guide"] != expected_guide
                or expected_guide not in base.EXPECTED_GUIDES[expected_source]
            ):
                raise IntegrityError("staged configuration omission metadata drift")

    model_gap_fields = (
        "model_id", "model_name", "tissue", "label", "baseline_flagged",
        "configuration", "gap", "flagged_ge_0_25"
    )
    model_gap_rows = read_staged_csv(stage / "model_configuration_gaps.csv", model_gap_fields)
    model_gap_keys = {(row["model_id"], row["configuration"]) for row in model_gap_rows}
    if len(model_gap_rows) != 340 or len(model_gap_keys) != 340:
        raise IntegrityError("staged paired-gap ledger row/identity drift")
    if {row["configuration"] for row in model_gap_rows} != set(configs):
        raise IntegrityError("staged paired-gap configuration drift")
    for configuration in configs:
        configuration_models = {
            row["model_id"]
            for row in model_gap_rows
            if row["configuration"] == configuration
        }
        if len(configuration_models) != 34:
            raise IntegrityError("staged paired-gap per-configuration row drift")
    for row in model_gap_rows:
        gap = base.parse_finite(row["gap"], row["model_id"])
        baseline_flagged = base.parse_canonical_bool(
            row["baseline_flagged"], (row["model_id"], "baseline_flagged")
        )
        flagged = base.parse_canonical_bool(
            row["flagged_ge_0_25"], (row["model_id"], "flagged_ge_0_25")
        )
        if flagged != (gap >= FLAG_THRESHOLD):
            raise IntegrityError("staged paired-gap threshold drift")
        if row["configuration"] == "baseline" and baseline_flagged != flagged:
            raise IntegrityError("staged baseline flag drift")
    for config in config_rows:
        observed_flagged = sum(
            base.parse_canonical_bool(row["flagged_ge_0_25"], row["model_id"])
            for row in model_gap_rows
            if row["configuration"] == config["configuration"]
        )
        if observed_flagged != int(config["flagged_models"]):
            raise IntegrityError("staged configuration flagged-count drift")

    robustness_fields = tuple(ModelRobustness.__dataclass_fields__)
    robustness_rows = read_staged_csv(stage / "model_robustness.csv", robustness_fields)
    robustness_models = {row["model_id"] for row in robustness_rows}
    if len(robustness_rows) != 34 or len(robustness_models) != 34:
        raise IntegrityError("staged robustness row/identity drift")
    for row in robustness_rows:
        for field in (
            "baseline_flagged",
            "avana_all_omissions_retain_flag",
            "ky_all_omissions_retain_flag",
            "fully_robust_all_nine",
        ):
            base.parse_canonical_bool(row[field], (row["model_id"], field))
        base.parse_nonnegative_integer(row["flagged_omissions_of_nine"], row["model_id"])
        for field in (
            "baseline_gap",
            "min_gap_all_ten_configurations",
            "median_gap_all_ten_configurations",
            "max_gap_all_ten_configurations",
        ):
            base.parse_finite(row[field], (row["model_id"], field))
    if robustness_models != {row["model_id"] for row in model_gap_rows}:
        raise IntegrityError("staged robustness/gap model identity drift")
    gap_by_configuration_model = {
        (row["configuration"], row["model_id"]): row for row in model_gap_rows
    }
    avana_config_names = sorted(name for name in configs if name.startswith("omit_Avana_"))
    ky_config_names = sorted(name for name in configs if name.startswith("omit_KY_"))
    for row in robustness_rows:
        model_id = row["model_id"]
        values = [
            base.parse_finite(
                gap_by_configuration_model[(configuration, model_id)]["gap"],
                (model_id, configuration),
            )
            for configuration in configs
        ]
        avana_all = all(
            base.parse_canonical_bool(
                gap_by_configuration_model[(configuration, model_id)]["flagged_ge_0_25"],
                (model_id, configuration),
            )
            for configuration in avana_config_names
        )
        ky_all = all(
            base.parse_canonical_bool(
                gap_by_configuration_model[(configuration, model_id)]["flagged_ge_0_25"],
                (model_id, configuration),
            )
            for configuration in ky_config_names
        )
        all_nine = avana_all and ky_all
        flagged_count = sum(
            base.parse_canonical_bool(
                gap_by_configuration_model[(configuration, model_id)]["flagged_ge_0_25"],
                (model_id, configuration),
            )
            for configuration in [*avana_config_names, *ky_config_names]
        )
        if (
            base.parse_canonical_bool(row["avana_all_omissions_retain_flag"], model_id) != avana_all
            or base.parse_canonical_bool(row["ky_all_omissions_retain_flag"], model_id) != ky_all
            or base.parse_canonical_bool(row["fully_robust_all_nine"], model_id) != all_nine
            or base.parse_nonnegative_integer(row["flagged_omissions_of_nine"], model_id) != flagged_count
            or abs(base.parse_finite(row["min_gap_all_ten_configurations"], model_id) - min(values)) > 1e-12
            or abs(base.parse_finite(row["median_gap_all_ten_configurations"], model_id) - strict_median(values)) > 1e-12
            or abs(base.parse_finite(row["max_gap_all_ten_configurations"], model_id) - max(values)) > 1e-12
        ):
            raise IntegrityError("staged robustness summary cross-check drift")

    guide_fields = ["screen_id", "model_id", "source", "tissue"]
    for index in range(1, 6):
        guide_fields.extend([f"guide_{index}_sequence", f"guide_{index}_mean"])
    guide_rows = read_staged_csv(stage / "reconstructed_guide_means.csv", guide_fields)
    guide_keys = {(row["screen_id"], row["model_id"], row["source"]) for row in guide_rows}
    if len(guide_rows) != 103 or len(guide_keys) != 103:
        raise IntegrityError("staged guide-mean row/identity drift")
    for row in guide_rows:
        source = row["source"]
        if source not in base.SOURCES or row["tissue"] not in base.TISSUES:
            raise IntegrityError("staged guide-mean source/tissue drift")
        expected_count = len(base.EXPECTED_GUIDES[source])
        for index in range(1, 6):
            sequence = row[f"guide_{index}_sequence"]
            mean = row[f"guide_{index}_mean"]
            if index <= expected_count:
                if sequence != base.EXPECTED_GUIDES[source][index - 1]:
                    raise IntegrityError("staged guide sequence drift")
                base.parse_finite(mean, (row["screen_id"], sequence))
            elif sequence or mean:
                raise IntegrityError("staged unused guide column drift")

    screen_fields = (
        "configuration", "omitted_source", "omitted_guide", "screen_id", "model_id",
        "source", "tissue", "reconstructed_score", "dependency_percentile",
        "retained_guide_count"
    )
    screen_rows = read_staged_csv(stage / "screen_configuration_ledger.csv", screen_fields)
    screen_keys = {
        (row["configuration"], row["screen_id"], row["model_id"], row["source"])
        for row in screen_rows
    }
    if len(screen_rows) != 1030 or len(screen_keys) != 1030:
        raise IntegrityError("staged full screen ledger row/identity drift")
    if {row["configuration"] for row in screen_rows} != set(configs):
        raise IntegrityError("staged full screen ledger configuration drift")
    counts_by_config = Counter(row["configuration"] for row in screen_rows)
    if counts_by_config != Counter({name: 103 for name in configs}):
        raise IntegrityError("staged full screen ledger configuration counts drift")
    if frozen is None:
        raise IntegrityError("frozen identity set required for staged validation")
    frozen_identities = {
        (row.screen_id, row.model_id, row.source, row.tissue) for row in frozen
    }
    screen_by_config_identity = {}
    for row in screen_rows:
        source = row["source"]
        omitted_source = row["omitted_source"]
        if source not in base.SOURCES or row["tissue"] not in base.TISSUES:
            raise IntegrityError("staged full screen ledger identity drift")
        if omitted_source not in ("", *base.SOURCES):
            raise IntegrityError("staged omitted source drift")
        configuration = row["configuration"]
        if configuration == "baseline":
            if omitted_source or row["omitted_guide"]:
                raise IntegrityError("staged baseline omission metadata drift")
        else:
            if not configuration.startswith("omit_"):
                raise IntegrityError("staged omission configuration name drift")
            _, expected_source, expected_guide = configuration.split("_", 2)
            if (
                omitted_source != expected_source
                or row["omitted_guide"] != expected_guide
                or expected_guide not in base.EXPECTED_GUIDES[expected_source]
            ):
                raise IntegrityError("staged omission metadata drift")
        identity = (row["screen_id"], row["model_id"], source, row["tissue"])
        screen_by_config_identity[(configuration, row["model_id"], source)] = row
        if identity not in frozen_identities:
            raise IntegrityError("staged screen ledger frozen identity drift")
        expected_guides = len(base.EXPECTED_GUIDES[source]) - int(source == omitted_source)
        if base.parse_nonnegative_integer(row["retained_guide_count"], row["screen_id"]) != expected_guides:
            raise IntegrityError("staged retained guide count drift")
        base.parse_finite(row["reconstructed_score"], row["screen_id"])
        base.parse_finite(row["dependency_percentile"], row["screen_id"])
    for configuration in configs:
        observed = {
            (row["screen_id"], row["model_id"], row["source"], row["tissue"])
            for row in screen_rows
            if row["configuration"] == configuration
        }
        if observed != frozen_identities:
            raise IntegrityError("staged screen ledger configuration identity drift")
    for row in model_gap_rows:
        configuration = row["configuration"]
        avana = screen_by_config_identity.get((configuration, row["model_id"], "Avana"))
        ky = screen_by_config_identity.get((configuration, row["model_id"], "KY"))
        if avana is None or ky is None or avana["tissue"] != ky["tissue"]:
            raise IntegrityError("staged paired/source ledger identity drift")
        derived_gap = abs(
            base.parse_finite(avana["dependency_percentile"], row["model_id"])
            - base.parse_finite(ky["dependency_percentile"], row["model_id"])
        )
        if abs(derived_gap - base.parse_finite(row["gap"], row["model_id"])) > 1e-12:
            raise IntegrityError("staged paired/source gap cross-check drift")
        if row["baseline_flagged"] != next(
            candidate["baseline_flagged"]
            for candidate in model_gap_rows
            if candidate["model_id"] == row["model_id"] and candidate["configuration"] == "baseline"
        ):
            raise IntegrityError("staged baseline flag consistency drift")
    for configuration in configs:
        for screen in frozen:
            baseline = screen_by_config_identity[("baseline", screen.model_id, screen.source)]
            current = screen_by_config_identity[(configuration, screen.model_id, screen.source)]
            if configuration != "baseline" and current["omitted_source"] != screen.source:
                for field in ("reconstructed_score", "dependency_percentile"):
                    if abs(
                        base.parse_finite(current[field], screen.screen_id)
                        - base.parse_finite(baseline[field], screen.screen_id)
                    ) > 1e-12:
                        raise IntegrityError("staged unaffected-source consistency drift")

    required_summary_keys = {
        "experiment_id", "status", "analysis_type", "input_receipt", "adequacy",
        "configurations", "primary", "ordering_sensitivity", "interpretation_receipt",
        "artifact_receipt_sha256", "overall_pass", "claim_boundary",
    }
    if set(result) != required_summary_keys or result["experiment_id"] != EXPERIMENT_ID:
        raise IntegrityError("staged summary schema drift")
    if result["status"] not in {"PASS_SINGLE_GUIDE_ROBUSTNESS", "FAIL_SINGLE_GUIDE_ROBUSTNESS"}:
        raise IntegrityError("staged summary status drift")
    if result["overall_pass"] != (result["status"] == "PASS_SINGLE_GUIDE_ROBUSTNESS"):
        raise IntegrityError("staged summary pass/status drift")
    validate_summary_against_ledgers(result, config_rows, model_gap_rows, robustness_rows)
    artifact_receipt = result.get("artifact_receipt_sha256")
    if not isinstance(artifact_receipt, dict):
        raise IntegrityError("missing staged artifact receipt")
    if set(artifact_receipt) != EXPECTED_RESULT_FILES:
        raise IntegrityError("staged artifact receipt schema drift")
    for name in EXPECTED_RESULT_FILES - {"summary.json"}:
        actual = base.sha256(stage / name)
        if artifact_receipt.get(name) != actual:
            raise IntegrityError(f"staged artifact hash drift: {name}")
    if artifact_receipt["summary.json"] != summary_digest(result):
        raise IntegrityError("staged summary hash drift")


def publish(args: argparse.Namespace) -> int:
    target = Path(args.results_dir)
    error_receipt = Path(args.error_receipt)
    if target.exists():
        write_error_receipt(
            error_receipt,
            {
                "experiment_id": EXPERIMENT_ID,
                "status": "ERROR_RESULTS_DIRECTORY_EXISTS",
                "error": f"refusing to overwrite existing result set: {target}",
                "published_results_unchanged": True,
                "results_written": False,
                "overall_pass": False,
            },
        )
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(
            dir=target.parent, prefix=f".{target.name}.stage."
        ) as temporary_name:
            stage = Path(temporary_name)
            result = run(args, stage)
            receipt = result.get("artifact_receipt_sha256")
            if not isinstance(receipt, dict):
                raise IntegrityError("run did not return artifact receipt")
            receipt["summary.json"] = summary_digest(result)
            (stage / "summary.json").write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            parsed_summary = json.loads((stage / "summary.json").read_text())
            if parsed_summary != result:
                raise IntegrityError("staged summary round-trip drift")
            frozen = base.load_frozen_screens(Path(args.denominator_file))
            validate_staged_result_files(stage, result, frozen)
            os.replace(stage, target)
    except Exception as exc:
        write_error_receipt(
            error_receipt,
            {
                "experiment_id": EXPERIMENT_ID,
                "status": "ERROR_INTEGRITY",
                "error": str(exc),
                "error_type": type(exc).__name__,
                "published_results_exist": target.exists(),
                "results_written": False,
                "overall_pass": False,
            },
        )
        return 1
    if error_receipt.exists():
        error_receipt.unlink()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 2


def main() -> None:
    args = build_parser().parse_args()
    raise SystemExit(publish(args))


if __name__ == "__main__":
    main()
