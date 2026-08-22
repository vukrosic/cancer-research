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

from candrel.wrn_ordering import dependency_percentiles, fixed_percentile_correlation


EXPERIMENT_ID = "EXP-20260822-010"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
WRN = "WRN (7486)"
FLAG_THRESHOLD = 0.25
BASELINE_ATOL = 1e-8
MINIMUM_FULLY_ROBUST = 8
EXPECTED_DENOMINATORS = {
    ("Avana", "Large Intestine"): 25,
    ("KY", "Large Intestine"): 30,
    ("Avana", "Ovary"): 22,
    ("KY", "Ovary"): 26,
}
EXPECTED_GUIDES = {
    "Avana": (
        "AGAAAACCTCAATAGTGGCA",
        "CTAACATTGAGACTGAACTG",
        "GTAGCAGTAAGTGCAACGAT",
        "TCTTCCATCAGAGAAATAAG",
    ),
    "KY": (
        "GCACGTACATAAGCATCAG",
        "GTCTATCCGCTGTAGCAAT",
        "TAGCAGTAAGTGCAACGAT",
        "TAGCATGAGTCTATCAGAT",
        "TGGAGTTACGTATACAATC",
    ),
}
EXPECTED_LFC = {
    "Avana": {
        "size": 3173505617,
        "md5": "58b1f479091a9f8b3e858d69d55413c4",
    },
    "KY": {
        "size": 1585769082,
        "md5": "c711c9413b63fe7c55b734e43cdeca91",
    },
}
EXPECTED_HASHES = {
    "avana_guide_map": "5580f89d2bbd26d25cf107c6441dcc30774a333385e104e83e1212ca16ec99a2",
    "ky_guide_map": "23bafc0d2f88b25727af8e2f5d0245495c39243163fb465ceffc9755c012c4b0",
    "sequence_map": "e4b99b4a6cd48c3957c5ada2abeeed1e1de319fe26526e76de6088ec73704c0b",
    "qc_file": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "denominator_file": "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654",
    "gap_file": "f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a",
}
EXPECTED_NAIVE_SHA256 = (
    "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721"
)


class IntegrityError(RuntimeError):
    """Raised when a frozen provenance, identity, or robustness invariant drifts."""


@dataclass(frozen=True)
class DenominatorRecord:
    model_id: str
    model_name: str
    tissue: str
    label: str
    source: str
    screen_id: str
    extracted_score: float


@dataclass(frozen=True)
class GapRecord:
    model_id: str
    model_name: str
    tissue: str
    label: str
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


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_small_hashes(args: argparse.Namespace) -> dict[str, str]:
    receipt = {}
    for argument, expected in EXPECTED_HASHES.items():
        actual = sha256(Path(getattr(args, argument)))
        if actual != expected:
            raise IntegrityError(
                f"{argument} SHA-256 drift: expected {expected}, got {actual}"
            )
        receipt[f"{argument}_sha256"] = actual
    return receipt


def parse_finite(value: str, identity: object) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise IntegrityError(f"non-numeric value for {identity}") from exc
    if not math.isfinite(parsed):
        raise IntegrityError(f"non-finite value for {identity}")
    return parsed


def load_denominators(path: Path) -> list[DenominatorRecord]:
    rows: list[DenominatorRecord] = []
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
            screen_ids = [part.strip() for part in row["screen_ids"].split(";") if part.strip()]
            if len(screen_ids) != 1:
                raise IntegrityError(f"expected exactly one frozen ScreenID for {key}")
            screen_id = screen_ids[0]
            if screen_id in screens:
                raise IntegrityError(f"shared denominator ScreenID: {screen_id}")
            rows.append(
                DenominatorRecord(
                    model_id=model_id,
                    model_name=row["model_name"].strip(),
                    tissue=tissue,
                    label=row["label"].strip(),
                    source=source,
                    screen_id=screen_id,
                    extracted_score=parse_finite(row["score"], key),
                )
            )
            seen.add(key)
            screens.add(screen_id)
            counts[(source, tissue)] += 1
    if dict(counts) != EXPECTED_DENOMINATORS or len(rows) != 103 or len(screens) != 103:
        raise IntegrityError(
            f"denominator drift: expected {EXPECTED_DENOMINATORS}, got {dict(counts)}"
        )
    return sorted(rows, key=lambda row: (row.source, row.tissue, row.model_id))


def load_guides(path: Path, source: str) -> tuple[str, ...]:
    selected = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["Gene"].strip() != WRN:
                continue
            if (
                row["UsedByChronos"].strip().lower() == "true"
                and parse_finite(row["nAlignments"], row["sgRNA"]) == 1.0
                and not row["DropReason"].strip()
            ):
                selected.append(row["sgRNA"].strip())
    guides = tuple(sorted(selected))
    if guides != EXPECTED_GUIDES[source]:
        raise IntegrityError(
            f"{source} eligible-guide drift: expected {EXPECTED_GUIDES[source]}, got {guides}"
        )
    return guides


def load_included_counts(
    path: Path, denominators: Sequence[DenominatorRecord]
) -> dict[tuple[str, str], int]:
    expected = {(row.model_id, row.source): row for row in denominators}
    counts = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["ModelID"].strip(), row["Library"].strip())
            if key not in expected:
                continue
            if row["ScreenID"].strip() != expected[key].screen_id:
                continue
            if key in counts:
                raise IntegrityError(f"duplicate exact QC row: {key}")
            value = parse_finite(row["nIncludedSequences"], key)
            if value < 1 or not value.is_integer():
                raise IntegrityError(f"invalid included-sequence count: {key}")
            counts[key] = int(value)
    if set(counts) != set(expected):
        raise IntegrityError("missing exact QC included-sequence counts")
    return counts


def load_screen_sequences(
    path: Path,
    denominators: Sequence[DenominatorRecord],
    included_counts: dict[tuple[str, str], int],
) -> dict[tuple[str, str], tuple[str, ...]]:
    by_screen = {row.screen_id: row for row in denominators}
    sequences: dict[tuple[str, str], list[str]] = defaultdict(list)
    sequence_owner: dict[str, tuple[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            screen_id = row["ScreenID"].strip()
            if screen_id not in by_screen:
                continue
            frozen = by_screen[screen_id]
            if (
                row["ModelID"].strip() != frozen.model_id
                or row["Library"].strip() != frozen.source
            ):
                raise IntegrityError(f"sequence-map identity drift: {screen_id}")
            if row["ExcludeFromCRISPRCombined"].strip().lower() != "false":
                continue
            sequence_id = row["SequenceID"].strip()
            key = (frozen.model_id, frozen.source)
            if not sequence_id or sequence_id in sequence_owner:
                raise IntegrityError(f"duplicate/blank included SequenceID: {sequence_id}")
            sequence_owner[sequence_id] = key
            sequences[key].append(sequence_id)
    output = {key: tuple(sorted(values)) for key, values in sequences.items()}
    if set(output) != set(included_counts):
        raise IntegrityError("screen-sequence identity coverage drift")
    for key, expected_count in included_counts.items():
        if len(output[key]) != expected_count:
            raise IntegrityError(
                f"included-sequence count drift for {key}: expected {expected_count}, got {len(output[key])}"
            )
    return output


def _first_csv_field(raw_line: bytes) -> str:
    comma = raw_line.find(b",")
    if comma < 0:
        raise IntegrityError("large CSV row lacks a comma")
    return raw_line[:comma].decode("utf-8").strip('"')


def extract_lfc_values(
    path: Path,
    source: str,
    guides: Sequence[str],
    required_sequences: set[str],
) -> tuple[dict[str, dict[str, float]], dict[str, object]]:
    expected = EXPECTED_LFC[source]
    observed_size = path.stat().st_size
    if observed_size != expected["size"]:
        raise IntegrityError(
            f"{source} LFC byte-size drift: expected {expected['size']}, got {observed_size}"
        )
    md5 = hashlib.md5(usedforsecurity=False)
    sha = hashlib.sha256()
    extracted: dict[str, dict[str, float]] = {}
    with path.open("rb") as handle:
        header_raw = handle.readline()
        if not header_raw:
            raise IntegrityError(f"empty {source} LFC matrix")
        md5.update(header_raw)
        sha.update(header_raw)
        header = next(csv.reader([header_raw.decode("utf-8-sig")]))
        positions: dict[str, int] = {}
        for index, name in enumerate(header):
            if name in required_sequences:
                if name in positions:
                    raise IntegrityError(f"duplicate LFC SequenceID column: {name}")
                positions[name] = index
        if set(positions) != required_sequences:
            missing = sorted(required_sequences - set(positions))
            raise IntegrityError(f"missing {source} LFC sequence columns: {missing[:5]}")
        guide_set = set(guides)
        for raw_line in handle:
            md5.update(raw_line)
            sha.update(raw_line)
            guide = _first_csv_field(raw_line)
            if guide not in guide_set:
                continue
            if guide in extracted:
                raise IntegrityError(f"duplicate {source} LFC guide row: {guide}")
            parsed = next(csv.reader([raw_line.decode("utf-8")]))
            values = {
                sequence: parse_finite(parsed[index], (source, guide, sequence))
                for sequence, index in positions.items()
            }
            extracted[guide] = values
    actual_md5 = md5.hexdigest()
    if actual_md5 != expected["md5"]:
        raise IntegrityError(
            f"{source} LFC MD5 drift: expected {expected['md5']}, got {actual_md5}"
        )
    if set(extracted) != set(guides):
        raise IntegrityError(f"missing {source} LFC guide rows")
    return extracted, {
        "size": observed_size,
        "md5": actual_md5,
        "sha256": sha.hexdigest(),
        "guide_rows": len(extracted),
        "selected_sequence_columns": len(required_sequences),
    }


def extract_official_wrn_scores(
    path: Path, required_screen_ids: set[str]
) -> tuple[dict[str, float], str]:
    sha = hashlib.sha256()
    scores: dict[str, float] = {}
    with path.open("rb") as handle:
        header_raw = handle.readline()
        if not header_raw:
            raise IntegrityError("empty naïve gene-score matrix")
        sha.update(header_raw)
        header = next(csv.reader([header_raw.decode("utf-8-sig")]))
        wrn_indices = [index for index, name in enumerate(header) if name == WRN]
        if len(wrn_indices) != 1:
            raise IntegrityError(f"expected one WRN naïve-score column, got {wrn_indices}")
        wrn_index = wrn_indices[0]
        for raw_line in handle:
            sha.update(raw_line)
            screen_id = _first_csv_field(raw_line)
            if screen_id not in required_screen_ids:
                continue
            if screen_id in scores:
                raise IntegrityError(f"duplicate naïve-score ScreenID: {screen_id}")
            parsed = next(csv.reader([raw_line.decode("utf-8")]))
            scores[screen_id] = parse_finite(parsed[wrn_index], screen_id)
    actual_sha = sha.hexdigest()
    if actual_sha != EXPECTED_NAIVE_SHA256:
        raise IntegrityError(
            f"naive score SHA-256 drift: expected {EXPECTED_NAIVE_SHA256}, got {actual_sha}"
        )
    if set(scores) != required_screen_ids:
        raise IntegrityError("missing official WRN screen scores")
    return scores, actual_sha


def reconstruct_guide_means(
    denominators: Sequence[DenominatorRecord],
    screen_sequences: dict[tuple[str, str], tuple[str, ...]],
    lfc_by_source: dict[str, dict[str, dict[str, float]]],
) -> dict[tuple[str, str], dict[str, float]]:
    output = {}
    for row in denominators:
        key = (row.model_id, row.source)
        sequence_ids = screen_sequences[key]
        guide_means = {}
        for guide, values in lfc_by_source[row.source].items():
            selected = np.asarray([values[sequence] for sequence in sequence_ids])
            if not np.all(np.isfinite(selected)):
                raise IntegrityError(f"non-finite retained guide values: {key} {guide}")
            guide_means[guide] = float(np.mean(selected))
        output[key] = guide_means
    if len(output) != 103:
        raise IntegrityError("guide-mean reconstruction count drift")
    return output


def scores_from_guide_means(
    guide_means: dict[tuple[str, str], dict[str, float]],
    omitted_source: str | None = None,
    omitted_guide: str | None = None,
    expected_records: int = 103,
) -> dict[tuple[str, str], float]:
    if (omitted_source is None) != (omitted_guide is None):
        raise IntegrityError("omitted source and guide must be specified together")
    scores = {}
    for key, values in guide_means.items():
        source = key[1]
        retained = [
            value
            for guide, value in values.items()
            if not (source == omitted_source and guide == omitted_guide)
        ]
        expected_count = len(EXPECTED_GUIDES[source]) - (source == omitted_source)
        if len(retained) != expected_count or expected_count < (3 if source == "Avana" else 4):
            raise IntegrityError(f"retained-guide count drift: {key}")
        score = float(np.median(np.asarray(retained)))
        if not math.isfinite(score):
            raise IntegrityError(f"non-finite reconstructed score: {key}")
        scores[key] = score
    if len(scores) != expected_records:
        raise IntegrityError("reconstructed score identity drift")
    return scores


def verify_baseline(
    denominators: Sequence[DenominatorRecord],
    reconstructed: dict[tuple[str, str], float],
    official_by_screen: dict[str, float],
    expected_records: int = 103,
) -> dict[str, object]:
    discrepancies = []
    extract_discrepancies = []
    for row in denominators:
        score = reconstructed[(row.model_id, row.source)]
        official = official_by_screen[row.screen_id]
        discrepancies.append(abs(score - official))
        extract_discrepancies.append(abs(row.extracted_score - official))
    maximum = max(discrepancies)
    maximum_extract = max(extract_discrepancies)
    if len(discrepancies) != expected_records or maximum > BASELINE_ATOL:
        raise IntegrityError(
            f"baseline reconstruction drift: n={len(discrepancies)}, max_abs={maximum}"
        )
    if maximum_extract > BASELINE_ATOL:
        raise IntegrityError(
            f"tracked EXP-003 score extract drift: max_abs={maximum_extract}"
        )
    return {
        "scores_checked": len(discrepancies),
        "absolute_tolerance": BASELINE_ATOL,
        "relative_tolerance": 0,
        "maximum_reconstruction_discrepancy": maximum,
        "maximum_tracked_extract_discrepancy": maximum_extract,
        "passed": True,
    }


def load_gaps(path: Path) -> list[GapRecord]:
    rows = []
    seen = set()
    counts: Counter[str] = Counter()
    flagged = 0
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            model_id = row["model_id"].strip()
            tissue = row["tissue"].strip()
            if model_id in seen or tissue not in TISSUES:
                raise IntegrityError(f"invalid gap identity: {model_id} {tissue}")
            flag_text = row["discordant_ge_0_25"].strip().lower()
            if flag_text not in {"true", "false"}:
                raise IntegrityError(f"invalid gap flag: {model_id}")
            gap = parse_finite(row["absolute_percentile_gap"], model_id)
            is_flagged = flag_text == "true"
            if is_flagged != (gap >= FLAG_THRESHOLD):
                raise IntegrityError(f"gap flag/threshold mismatch: {model_id}")
            rows.append(
                GapRecord(
                    model_id=model_id,
                    model_name=row["model_name"].strip(),
                    tissue=tissue,
                    label=row["label"].strip(),
                    baseline_gap=gap,
                    baseline_flagged=is_flagged,
                )
            )
            seen.add(model_id)
            counts[tissue] += 1
            flagged += is_flagged
    if len(rows) != 34 or dict(counts) != {tissue: 17 for tissue in TISSUES} or flagged != 10:
        raise IntegrityError(
            f"gap population drift: n={len(rows)}, counts={dict(counts)}, flagged={flagged}"
        )
    return sorted(rows, key=lambda row: (row.tissue, row.model_id))


def percentiles_for_scores(
    denominators: Sequence[DenominatorRecord], scores: dict[tuple[str, str], float]
) -> dict[tuple[str, str], float]:
    grouped: dict[tuple[str, str], list[DenominatorRecord]] = defaultdict(list)
    for row in denominators:
        grouped[(row.source, row.tissue)].append(row)
    if {key: len(value) for key, value in grouped.items()} != EXPECTED_DENOMINATORS:
        raise IntegrityError("percentile denominator drift")
    output = {}
    for (source, tissue), rows in grouped.items():
        ordered = sorted(rows, key=lambda row: row.model_id)
        values = [scores[(row.model_id, source)] for row in ordered]
        percentiles = dependency_percentiles(values)
        for row, percentile in zip(ordered, percentiles, strict=True):
            output[(row.model_id, source)] = float(percentile)
    return output


def gaps_for_configuration(
    gap_records: Sequence[GapRecord], percentiles: dict[tuple[str, str], float]
) -> dict[str, float]:
    gaps = {}
    for row in gap_records:
        gap = abs(
            percentiles[(row.model_id, "Avana")]
            - percentiles[(row.model_id, "KY")]
        )
        if not math.isfinite(gap):
            raise IntegrityError(f"non-finite perturbed gap: {row.model_id}")
        gaps[row.model_id] = gap
    return gaps


def equal_tissue_theta(
    gap_records: Sequence[GapRecord], percentiles: dict[tuple[str, str], float]
) -> float:
    tissue_rhos = []
    for tissue in TISSUES:
        selected = [row for row in gap_records if row.tissue == tissue]
        avana = np.asarray([percentiles[(row.model_id, "Avana")] for row in selected])
        ky = np.asarray([percentiles[(row.model_id, "KY")] for row in selected])
        tissue_rhos.append(fixed_percentile_correlation(avana, ky))
    return float(np.mean(tissue_rhos))


def summarize_robustness(
    gap_records: Sequence[GapRecord],
    gaps_by_configuration: dict[str, dict[str, float]],
) -> tuple[list[ModelRobustness], dict[str, object]]:
    avana_configs = [name for name in gaps_by_configuration if name.startswith("omit_Avana_")]
    ky_configs = [name for name in gaps_by_configuration if name.startswith("omit_KY_")]
    if len(avana_configs) != 4 or len(ky_configs) != 5:
        raise IntegrityError("omission configuration count drift")
    model_rows = []
    for row in gap_records:
        omission_gaps = {
            name: values[row.model_id] for name, values in gaps_by_configuration.items()
        }
        avana_all = all(omission_gaps[name] >= FLAG_THRESHOLD for name in avana_configs)
        ky_all = all(omission_gaps[name] >= FLAG_THRESHOLD for name in ky_configs)
        all_values = [row.baseline_gap, *omission_gaps.values()]
        model_rows.append(
            ModelRobustness(
                model_id=row.model_id,
                model_name=row.model_name,
                tissue=row.tissue,
                label=row.label,
                baseline_gap=row.baseline_gap,
                baseline_flagged=row.baseline_flagged,
                avana_all_omissions_retain_flag=avana_all,
                ky_all_omissions_retain_flag=ky_all,
                fully_robust_all_nine=avana_all and ky_all,
                flagged_omissions_of_nine=sum(
                    value >= FLAG_THRESHOLD for value in omission_gaps.values()
                ),
                min_gap_all_ten_configurations=float(min(all_values)),
                median_gap_all_ten_configurations=float(np.median(all_values)),
                max_gap_all_ten_configurations=float(max(all_values)),
            )
        )
    flagged_rows = [row for row in model_rows if row.baseline_flagged]
    unflagged_ids = {row.model_id for row in model_rows if not row.baseline_flagged}
    fully_robust = sum(row.fully_robust_all_nine for row in flagged_rows)
    unique_new = {
        model_id
        for model_id in unflagged_ids
        if any(
            gaps[model_id] >= FLAG_THRESHOLD
            for gaps in gaps_by_configuration.values()
        )
    }
    total_transitions = sum(
        gaps[model_id] >= FLAG_THRESHOLD
        for model_id in unflagged_ids
        for gaps in gaps_by_configuration.values()
    )
    summary = {
        "baseline_flagged_models": len(flagged_rows),
        "fully_robust_flagged_models": fully_robust,
        "avana_all_omissions_robust_models": sum(
            row.avana_all_omissions_retain_flag for row in flagged_rows
        ),
        "ky_all_omissions_robust_models": sum(
            row.ky_all_omissions_retain_flag for row in flagged_rows
        ),
        "unique_baseline_unflagged_becoming_flagged": len(unique_new),
        "unique_transition_model_ids": sorted(unique_new),
        "total_unflagged_to_flagged_transitions": int(total_transitions),
        "possible_unflagged_configuration_transitions": 24 * 9,
        "primary_pass": fully_robust >= MINIMUM_FULLY_ROBUST,
    }
    return model_rows, summary


def write_dataclass_rows(path: Path, rows: Sequence[object], fields: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def write_guide_means(
    path: Path,
    denominators: Sequence[DenominatorRecord],
    guide_means: dict[tuple[str, str], dict[str, float]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    guide_columns = [f"guide_mean_{index + 1}" for index in range(5)]
    fields = ["model_id", "tissue", "source", "screen_id", *guide_columns]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in denominators:
            ordered = [guide_means[(row.model_id, row.source)][g] for g in EXPECTED_GUIDES[row.source]]
            payload = {
                "model_id": row.model_id,
                "tissue": row.tissue,
                "source": row.source,
                "screen_id": row.screen_id,
                **{
                    column: ordered[index] if index < len(ordered) else ""
                    for index, column in enumerate(guide_columns)
                },
            }
            writer.writerow(payload)


def run(args: argparse.Namespace) -> dict[str, object]:
    receipt = verify_small_hashes(args)
    denominators = load_denominators(Path(args.denominator_file))
    guides = {
        "Avana": load_guides(Path(args.avana_guide_map), "Avana"),
        "KY": load_guides(Path(args.ky_guide_map), "KY"),
    }
    included_counts = load_included_counts(Path(args.qc_file), denominators)
    screen_sequences = load_screen_sequences(
        Path(args.sequence_map), denominators, included_counts
    )
    lfc_values = {}
    lfc_receipts = {}
    for source, argument in (("Avana", "avana_lfc"), ("KY", "ky_lfc")):
        required_sequences = {
            sequence
            for (model_id, key_source), values in screen_sequences.items()
            if key_source == source
            for sequence in values
        }
        lfc_values[source], lfc_receipts[source] = extract_lfc_values(
            Path(getattr(args, argument)), source, guides[source], required_sequences
        )
    guide_means = reconstruct_guide_means(denominators, screen_sequences, lfc_values)
    baseline_scores = scores_from_guide_means(guide_means)
    official_scores, naive_sha = extract_official_wrn_scores(
        Path(args.naive_file), {row.screen_id for row in denominators}
    )
    baseline_gate = verify_baseline(denominators, baseline_scores, official_scores)

    # No guide omission is computed before the baseline no-drift gate passes.
    gap_records = load_gaps(Path(args.gap_file))
    baseline_percentiles = percentiles_for_scores(denominators, baseline_scores)
    baseline_gaps = gaps_for_configuration(gap_records, baseline_percentiles)
    maximum_gap_drift = max(
        abs(baseline_gaps[row.model_id] - row.baseline_gap) for row in gap_records
    )
    if maximum_gap_drift > BASELINE_ATOL:
        raise IntegrityError(f"baseline percentile-gap drift: {maximum_gap_drift}")

    gaps_by_configuration = {}
    configuration_rows = []
    perturbed_thetas = []
    for source in SOURCES:
        for guide in guides[source]:
            name = f"omit_{source}_{guide}"
            scores = scores_from_guide_means(guide_means, source, guide)
            percentiles = percentiles_for_scores(denominators, scores)
            gaps = gaps_for_configuration(gap_records, percentiles)
            theta = equal_tissue_theta(gap_records, percentiles)
            gaps_by_configuration[name] = gaps
            perturbed_thetas.append(theta)
            configuration_rows.append(
                {
                    "configuration": name,
                    "source": source,
                    "omitted_guide": guide,
                    "equal_tissue_theta": theta,
                    "flagged_models": sum(value >= FLAG_THRESHOLD for value in gaps.values()),
                }
            )
    model_rows, robustness = summarize_robustness(gap_records, gaps_by_configuration)
    overall_pass = bool(robustness["primary_pass"])
    write_dataclass_rows(
        Path(args.model_output), model_rows, ModelRobustness.__dataclass_fields__
    )
    write_guide_means(Path(args.guide_mean_output), denominators, guide_means)
    config_path = Path(args.configuration_output)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "configuration",
                "source",
                "omitted_guide",
                "equal_tissue_theta",
                "flagged_models",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(configuration_rows)
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": "PASS_SINGLE_GUIDE_ROBUSTNESS" if overall_pass else "FAIL_SINGLE_GUIDE_ROBUSTNESS",
        "analysis_type": "preregistered_exhaustive_derived_robustness_audit_after_endpoint_unsealing",
        "input_receipt": {
            **receipt,
            "naive_file_sha256": naive_sha,
            "large_lfc": lfc_receipts,
        },
        "adequacy": {
            "denominator_records": len(denominators),
            "paired_models": len(gap_records),
            "included_sequence_columns": {
                source: len(
                    {
                        sequence
                        for (model_id, key_source), values in screen_sequences.items()
                        if key_source == source
                        for sequence in values
                    }
                )
                for source in SOURCES
            },
            "eligible_guides": {source: list(values) for source, values in guides.items()},
            "baseline_gate": baseline_gate,
            "maximum_baseline_gap_discrepancy": maximum_gap_drift,
            "adequate": True,
        },
        "configurations": {
            "baseline_plus_omissions": 10,
            "single_guide_omissions": 9,
            "avana_omissions": 4,
            "ky_omissions": 5,
        },
        "primary": robustness,
        "ordering_sensitivity": {
            "baseline_equal_tissue_theta": equal_tissue_theta(
                gap_records, baseline_percentiles
            ),
            "minimum_perturbed_theta": min(perturbed_thetas),
            "maximum_perturbed_theta": max(perturbed_thetas),
        },
        "overall_pass": overall_pass,
        "claim_boundary": "deterministic same-assay single-guide robustness audit",
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
    parser.add_argument(
        "--denominator-file", default="experiments/EXP-20260822-003/results/model_scores.csv"
    )
    parser.add_argument(
        "--gap-file", default="experiments/EXP-20260822-005/results/model_percentile_gaps.csv"
    )
    parser.add_argument("--output", default="experiments/EXP-20260822-010/results/summary.json")
    parser.add_argument(
        "--model-output",
        default="experiments/EXP-20260822-010/results/model_robustness.csv",
    )
    parser.add_argument(
        "--guide-mean-output",
        default="experiments/EXP-20260822-010/results/reconstructed_guide_means.csv",
    )
    parser.add_argument(
        "--configuration-output",
        default="experiments/EXP-20260822-010/results/configurations.csv",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
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
