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


EXPERIMENT_ID = "EXP-20260822-011"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
WRN = "WRN (7486)"
ATOL = 1e-8
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
        "sha256": "f018d7ff6820af6d0bb095f1e2b405ec31d7a744a1e4c019cfd9f3509e63bdee",
    },
    "KY": {
        "size": 1585769082,
        "md5": "c711c9413b63fe7c55b734e43cdeca91",
        "sha256": "5b03df4b4affda1f0ed36f2bd564e1cbd53ec443b20e60295cad577677874767",
    },
}
EXPECTED_HASHES = {
    "avana_guide_map": "5580f89d2bbd26d25cf107c6441dcc30774a333385e104e83e1212ca16ec99a2",
    "ky_guide_map": "23bafc0d2f88b25727af8e2f5d0245495c39243163fb465ceffc9755c012c4b0",
    "sequence_map": "e4b99b4a6cd48c3957c5ada2abeeed1e1de319fe26526e76de6088ec73704c0b",
    "qc_file": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "denominator_file": "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654",
    "parent_preregistration": "6e43ed8144f3ae5aa489be76dd244f0c88e359d9274520af504aa52cd5671382",
    "parent_failure_receipt": "e199e3d8bcbe960721292044de6204bd9317908dfc8fcf859deabd43beb4b3f5",
    "parent_result": "e0d4edba97bf6683070158f00dbe786941e4509f8c010f8ffda4d25bd2268b21",
}
EXPECTED_NAIVE_SHA256 = (
    "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721"
)
PARENT_MISMATCHES = {
    ("ACH-000680", "Avana"),
    ("ACH-000719", "KY"),
    ("ACH-000663", "Avana"),
}


class IntegrityError(RuntimeError):
    """Raised when a frozen provenance, identity, or schema invariant drifts."""


@dataclass(frozen=True)
class FrozenScreen:
    screen_id: str
    model_id: str
    source: str
    tissue: str


@dataclass(frozen=True)
class QCCounters:
    n_passing: int
    n_included: int


@dataclass(frozen=True)
class ReconstructionLedgerRow:
    screen_id: str
    model_id: str
    source: str
    tissue: str
    n_passing_sequences: int
    n_included_sequences: int
    retained_sequence_count: int
    reconstructed_score: float
    official_score: float
    absolute_discrepancy: float
    passes_absolute_1e_8_gate: bool


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


def parse_nonnegative_integer(value: str, identity: object) -> int:
    parsed = parse_finite(value, identity)
    if parsed < 0 or not parsed.is_integer():
        raise IntegrityError(f"invalid nonnegative integer for {identity}")
    return int(parsed)


def parse_canonical_bool(value: str, identity: object) -> bool:
    if value == "True":
        return True
    if value == "False":
        return False
    raise IntegrityError(f"noncanonical boolean for {identity}: {value!r}")


def load_frozen_screens(path: Path) -> list[FrozenScreen]:
    rows = []
    identities = set()
    screens = set()
    counts: Counter[tuple[str, str]] = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tissue = row["tissue"].strip()
            source = row["library"].strip()
            if tissue not in TISSUES or source not in SOURCES:
                continue
            model_id = row["model_id"].strip()
            screen_ids = [part.strip() for part in row["screen_ids"].split(";") if part.strip()]
            if len(screen_ids) != 1:
                raise IntegrityError(f"expected one frozen ScreenID: {model_id} {source}")
            screen_id = screen_ids[0]
            identity = (screen_id, model_id, source)
            if identity in identities or screen_id in screens:
                raise IntegrityError(f"duplicate frozen identity: {identity}")
            identities.add(identity)
            screens.add(screen_id)
            counts[(source, tissue)] += 1
            rows.append(FrozenScreen(screen_id, model_id, source, tissue))
    if len(rows) != 103 or len(screens) != 103 or dict(counts) != EXPECTED_DENOMINATORS:
        raise IntegrityError(
            f"frozen denominator drift: n={len(rows)}, counts={dict(counts)}"
        )
    return sorted(rows, key=lambda row: (row.source, row.tissue, row.model_id))


def load_qc_counts(
    path: Path, frozen_screens: Sequence[FrozenScreen]
) -> dict[tuple[str, str, str], QCCounters]:
    expected = {(row.screen_id, row.model_id, row.source) for row in frozen_screens}
    output = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            identity = (
                row["ScreenID"].strip(),
                row["ModelID"].strip(),
                row["Library"].strip(),
            )
            if identity not in expected:
                continue
            if identity in output:
                raise IntegrityError(f"duplicate exact QC identity: {identity}")
            output[identity] = QCCounters(
                n_passing=parse_nonnegative_integer(
                    row["nPassingSequences"], (identity, "nPassingSequences")
                ),
                n_included=parse_nonnegative_integer(
                    row["nIncludedSequences"], (identity, "nIncludedSequences")
                ),
            )
    if set(output) != expected:
        raise IntegrityError("missing exact QC identities")
    return output


def load_passing_sequences(
    path: Path,
    frozen_screens: Sequence[FrozenScreen],
    qc_counts: dict[tuple[str, str, str], QCCounters],
) -> dict[tuple[str, str, str], tuple[str, ...]]:
    by_screen = {row.screen_id: row for row in frozen_screens}
    retained: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    seen_sequence_ids = set()
    seen_rows = set()
    with path.open(newline="", encoding="utf-8") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            screen_id = row["ScreenID"].strip()
            if screen_id not in by_screen:
                continue
            frozen = by_screen[screen_id]
            identity = (screen_id, row["ModelID"].strip(), row["Library"].strip())
            expected_identity = (screen_id, frozen.model_id, frozen.source)
            if identity != expected_identity:
                raise IntegrityError(
                    f"contradictory sequence identity at row {row_number}: {identity}"
                )
            sequence_id = row["SequenceID"].strip()
            row_identity = (identity, sequence_id)
            if not sequence_id or row_identity in seen_rows:
                raise IntegrityError(f"duplicate/blank sequence row: {row_identity}")
            seen_rows.add(row_identity)
            passes = parse_canonical_bool(
                row["PassesQC"], (row_number, sequence_id, "PassesQC")
            )
            excluded = parse_canonical_bool(
                row["ExcludeFromCRISPRCombined"],
                (row_number, sequence_id, "ExcludeFromCRISPRCombined"),
            )
            if passes and not excluded:
                if sequence_id in seen_sequence_ids:
                    raise IntegrityError(f"retained SequenceID shared across screens: {sequence_id}")
                seen_sequence_ids.add(sequence_id)
                retained[identity].append(sequence_id)
    output = {identity: tuple(sorted(values)) for identity, values in retained.items()}
    if set(output) != set(qc_counts):
        raise IntegrityError("passing-sequence screen coverage drift")
    for identity, counters in qc_counts.items():
        if len(output[identity]) != counters.n_passing:
            raise IntegrityError(
                f"passing count drift for {identity}: expected {counters.n_passing}, got {len(output[identity])}"
            )
    return output


def load_guides(path: Path, source: str) -> tuple[str, ...]:
    selected = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["Gene"].strip() != WRN:
                continue
            if (
                row["UsedByChronos"] == "True"
                and parse_finite(row["nAlignments"], row["sgRNA"]) == 1.0
                and row["DropReason"] == ""
            ):
                selected.append(row["sgRNA"].strip())
    guides = tuple(sorted(selected))
    if guides != EXPECTED_GUIDES[source]:
        raise IntegrityError(f"{source} eligible-guide drift")
    return guides


def _first_csv_field(raw_line: bytes) -> str:
    comma = raw_line.find(b",")
    if comma < 0:
        raise IntegrityError("CSV row lacks comma")
    return raw_line[:comma].decode("utf-8").strip('"')


def extract_lfc(
    path: Path,
    source: str,
    guides: Sequence[str],
    required_sequences: set[str],
) -> tuple[dict[str, dict[str, float]], dict[str, object]]:
    expected = EXPECTED_LFC[source]
    size = path.stat().st_size
    if size != expected["size"]:
        raise IntegrityError(f"{source} LFC size drift")
    md5 = hashlib.md5(usedforsecurity=False)
    sha = hashlib.sha256()
    extracted = {}
    with path.open("rb") as handle:
        header_raw = handle.readline()
        if not header_raw:
            raise IntegrityError(f"empty {source} LFC")
        md5.update(header_raw)
        sha.update(header_raw)
        header = next(csv.reader([header_raw.decode("utf-8-sig")]))
        positions = {}
        for index, name in enumerate(header):
            if name in required_sequences:
                if name in positions:
                    raise IntegrityError(f"duplicate LFC column: {name}")
                positions[name] = index
        if set(positions) != required_sequences:
            raise IntegrityError(f"missing {source} passing-sequence LFC columns")
        guide_set = set(guides)
        for raw_line in handle:
            md5.update(raw_line)
            sha.update(raw_line)
            guide = _first_csv_field(raw_line)
            if guide not in guide_set:
                continue
            if guide in extracted:
                raise IntegrityError(f"duplicate LFC guide: {guide}")
            parsed = next(csv.reader([raw_line.decode("utf-8")]))
            extracted[guide] = {
                sequence: parse_finite(parsed[index], (source, guide, sequence))
                for sequence, index in positions.items()
            }
    actual_md5 = md5.hexdigest()
    actual_sha = sha.hexdigest()
    if actual_md5 != expected["md5"] or actual_sha != expected["sha256"]:
        raise IntegrityError(f"{source} LFC hash drift")
    if set(extracted) != set(guides):
        raise IntegrityError(f"missing {source} WRN guide rows")
    return extracted, {
        "size": size,
        "md5": actual_md5,
        "sha256": actual_sha,
        "guide_rows": len(extracted),
        "retained_sequence_columns": len(required_sequences),
    }


def extract_official_scores(
    path: Path, required_screens: set[str]
) -> tuple[dict[str, float], str]:
    sha = hashlib.sha256()
    scores = {}
    with path.open("rb") as handle:
        header_raw = handle.readline()
        if not header_raw:
            raise IntegrityError("empty official naïve-score matrix")
        sha.update(header_raw)
        header = next(csv.reader([header_raw.decode("utf-8-sig")]))
        indices = [index for index, name in enumerate(header) if name == WRN]
        if len(indices) != 1:
            raise IntegrityError("official matrix must have exactly one WRN column")
        wrn_index = indices[0]
        for raw_line in handle:
            sha.update(raw_line)
            screen_id = _first_csv_field(raw_line)
            if screen_id not in required_screens:
                continue
            if screen_id in scores:
                raise IntegrityError(f"duplicate official ScreenID: {screen_id}")
            parsed = next(csv.reader([raw_line.decode("utf-8")]))
            scores[screen_id] = parse_finite(parsed[wrn_index], screen_id)
    actual_sha = sha.hexdigest()
    if actual_sha != EXPECTED_NAIVE_SHA256:
        raise IntegrityError("official naïve-score SHA-256 drift")
    if set(scores) != required_screens:
        raise IntegrityError("missing official frozen screen scores")
    return scores, actual_sha


def reconstruct_scores(
    frozen_screens: Sequence[FrozenScreen],
    passing_sequences: dict[tuple[str, str, str], tuple[str, ...]],
    lfc_by_source: dict[str, dict[str, dict[str, float]]],
) -> dict[tuple[str, str, str], float]:
    output = {}
    for row in frozen_screens:
        identity = (row.screen_id, row.model_id, row.source)
        guide_means = []
        for guide in EXPECTED_GUIDES[row.source]:
            values = np.asarray(
                [
                    lfc_by_source[row.source][guide][sequence]
                    for sequence in passing_sequences[identity]
                ]
            )
            if len(values) < 1 or not np.all(np.isfinite(values)):
                raise IntegrityError(f"invalid passing guide values: {identity} {guide}")
            guide_means.append(float(np.mean(values)))
        score = float(np.median(np.asarray(guide_means)))
        if not math.isfinite(score):
            raise IntegrityError(f"non-finite reconstructed score: {identity}")
        output[identity] = score
    if len(output) != 103:
        raise IntegrityError("reconstructed score count drift")
    return output


def build_ledger(
    frozen_screens: Sequence[FrozenScreen],
    qc_counts: dict[tuple[str, str, str], QCCounters],
    passing_sequences: dict[tuple[str, str, str], tuple[str, ...]],
    reconstructed: dict[tuple[str, str, str], float],
    official: dict[str, float],
) -> list[ReconstructionLedgerRow]:
    rows = []
    for screen in frozen_screens:
        identity = (screen.screen_id, screen.model_id, screen.source)
        discrepancy = abs(reconstructed[identity] - official[screen.screen_id])
        counters = qc_counts[identity]
        rows.append(
            ReconstructionLedgerRow(
                screen_id=screen.screen_id,
                model_id=screen.model_id,
                source=screen.source,
                tissue=screen.tissue,
                n_passing_sequences=counters.n_passing,
                n_included_sequences=counters.n_included,
                retained_sequence_count=len(passing_sequences[identity]),
                reconstructed_score=reconstructed[identity],
                official_score=official[screen.screen_id],
                absolute_discrepancy=discrepancy,
                passes_absolute_1e_8_gate=discrepancy <= ATOL,
            )
        )
    if len(rows) != 103:
        raise IntegrityError("ledger row count drift")
    return rows


def write_ledger(path: Path, rows: Sequence[ReconstructionLedgerRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ReconstructionLedgerRow.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def summarize_mismatches(rows: Sequence[ReconstructionLedgerRow]) -> dict[str, object]:
    current = {
        (row.model_id, row.source)
        for row in rows
        if not row.passes_absolute_1e_8_gate
    }
    return {
        "parent_mismatch_count": len(PARENT_MISMATCHES),
        "new_mismatch_count": len(current),
        "resolved_parent_mismatch_count": len(PARENT_MISMATCHES - current),
        "persistent_parent_mismatch_count": len(PARENT_MISMATCHES & current),
        "newly_introduced_mismatch_count": len(current - PARENT_MISMATCHES),
        "resolved_parent_model_source": sorted(
            f"{model}|{source}" for model, source in PARENT_MISMATCHES - current
        ),
        "persistent_model_source": sorted(
            f"{model}|{source}" for model, source in PARENT_MISMATCHES & current
        ),
        "newly_introduced_model_source": sorted(
            f"{model}|{source}" for model, source in current - PARENT_MISMATCHES
        ),
    }


def run(args: argparse.Namespace) -> dict[str, object]:
    receipt = verify_small_hashes(args)
    frozen = load_frozen_screens(Path(args.denominator_file))
    qc_counts = load_qc_counts(Path(args.qc_file), frozen)
    passing_sequences = load_passing_sequences(
        Path(args.sequence_map), frozen, qc_counts
    )
    guides = {
        "Avana": load_guides(Path(args.avana_guide_map), "Avana"),
        "KY": load_guides(Path(args.ky_guide_map), "KY"),
    }
    lfc = {}
    lfc_receipts = {}
    for source, argument in (("Avana", "avana_lfc"), ("KY", "ky_lfc")):
        required = {
            sequence
            for (screen_id, model_id, key_source), values in passing_sequences.items()
            if key_source == source
            for sequence in values
        }
        lfc[source], lfc_receipts[source] = extract_lfc(
            Path(getattr(args, argument)), source, guides[source], required
        )
    reconstructed = reconstruct_scores(frozen, passing_sequences, lfc)
    official, naive_sha = extract_official_scores(
        Path(args.naive_file), {row.screen_id for row in frozen}
    )
    ledger = build_ledger(
        frozen, qc_counts, passing_sequences, reconstructed, official
    )
    write_ledger(Path(args.ledger_output), ledger)
    passed = sum(row.passes_absolute_1e_8_gate for row in ledger)
    maximum = max(row.absolute_discrepancy for row in ledger)
    comparison = summarize_mismatches(ledger)
    overall_pass = passed == 103
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": (
            "PASS_PASSING_SEQUENCE_RECONSTRUCTION"
            if overall_pass
            else "FAIL_PASSING_SEQUENCE_RECONSTRUCTION"
        ),
        "analysis_type": "post_failure_single_candidate_pipeline_semantics_audit",
        "input_receipt": {
            **receipt,
            "naive_file_sha256": naive_sha,
            "large_lfc": lfc_receipts,
        },
        "candidate_rule": {
            "sequence_PassesQC": "True",
            "ExcludeFromCRISPRCombined": "False",
            "retained_count_equals": "nPassingSequences",
            "fallback_candidate_available": False,
        },
        "adequacy": {
            "frozen_screens": len(frozen),
            "retained_passing_sequences": sum(
                len(values) for values in passing_sequences.values()
            ),
            "eligible_guides": {source: list(values) for source, values in guides.items()},
            "complete_finite": True,
        },
        "reconstruction_gate": {
            "comparisons": len(ledger),
            "passing_comparisons": passed,
            "failing_comparisons": len(ledger) - passed,
            "absolute_tolerance": ATOL,
            "relative_tolerance": 0,
            "maximum_absolute_discrepancy": maximum,
            "passed": overall_pass,
        },
        "parent_comparison": comparison,
        "forbidden_analysis_receipt": {
            "gap_file_loaded": False,
            "guide_omissions_computed": 0,
            "ranks_or_percentiles_computed": False,
            "robustness_statistics_computed": False,
        },
        "overall_pass": overall_pass,
        "claim_boundary": "frozen 103-screen WRN reconstruction semantics only",
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
        "--parent-preregistration",
        default="experiments/EXP-20260822-010/preregistration.md",
    )
    parser.add_argument(
        "--parent-failure-receipt",
        default="experiments/EXP-20260822-010/baseline_failure_receipt.json",
    )
    parser.add_argument(
        "--parent-result", default="experiments/EXP-20260822-010/result.md"
    )
    parser.add_argument(
        "--output", default="experiments/EXP-20260822-011/results/summary.json"
    )
    parser.add_argument(
        "--ledger-output",
        default="experiments/EXP-20260822-011/results/reconstruction_ledger.csv",
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
