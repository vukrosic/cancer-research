from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


EXPERIMENT_ID = "EXP-20260822-007"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
WRN_GENE = "WRN (7486)"
EXPECTED_HASHES = {
    "cohort_file": "2bc84868962b35c55e456aeb953429206e97c9b25f648b5deabe5a1488e60b67",
    "avana_guide_map": "5580f89d2bbd26d25cf107c6441dcc30774a333385e104e83e1212ca16ec99a2",
    "ky_guide_map": "23bafc0d2f88b25727af8e2f5d0245495c39243163fb465ceffc9755c012c4b0",
    "avana_mutations": "6b5a4060936603642a4a2b7229e2b148728b8c8a0097f1ae0dd768588bfd6a02",
    "ky_mutations": "71af643cd06b637afcae08112b02496197b2a59a4f689b07ed23f50a69accdad",
}
EXPECTED_MD5 = {
    "avana_guide_map": "b694af3982d70117fd6214fdd8ce2e2e",
    "ky_guide_map": "2ef1cb175dd2c3314edd86705a598fd5",
    "avana_mutations": "fa242f255113a00809019ed2e7be1ad1",
    "ky_mutations": "7f070bb17014728216877650c8c2f088",
}


class IntegrityError(RuntimeError):
    """Raised when frozen provenance or adequacy identities drift."""


@dataclass(frozen=True)
class ModelExposure:
    model_id: str
    tissue: str
    avana_mutated_guides: int
    avana_total_guides: int
    avana_fraction: float
    ky_mutated_guides: int
    ky_total_guides: int
    ky_fraction: float
    absolute_fraction_difference: float


def digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_receipts(args: argparse.Namespace) -> dict[str, str]:
    receipt: dict[str, str] = {}
    for argument, expected in EXPECTED_HASHES.items():
        path = Path(getattr(args, argument))
        actual = digest(path, "sha256")
        if actual != expected:
            raise IntegrityError(
                f"{argument} SHA-256 drift: expected {expected}, got {actual}"
            )
        receipt[f"{argument}_sha256"] = actual
        if argument in EXPECTED_MD5:
            actual_md5 = digest(path, "md5")
            if actual_md5 != EXPECTED_MD5[argument]:
                raise IntegrityError(
                    f"{argument} MD5 drift: expected {EXPECTED_MD5[argument]}, "
                    f"got {actual_md5}"
                )
            receipt[f"{argument}_md5"] = actual_md5
    return receipt


def load_outcome_blind_cohort(path: Path) -> dict[str, str]:
    cohort: dict[str, str] = {}
    counts: Counter[str] = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            model_id = row["model_id"].strip()
            tissue = row["tissue"].strip()
            if model_id in cohort:
                raise IntegrityError(f"duplicate cohort ModelID: {model_id}")
            if tissue not in TISSUES:
                raise IntegrityError(f"unexpected cohort tissue: {tissue}")
            cohort[model_id] = tissue
            counts[tissue] += 1
    expected = {tissue: 17 for tissue in TISSUES}
    if dict(counts) != expected or len(cohort) != 34:
        raise IntegrityError(f"cohort drift: expected {expected}, got {dict(counts)}")
    return cohort


def load_wrn_guides(path: Path) -> dict[str, dict[str, str]]:
    guides: dict[str, dict[str, str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["Gene"].strip() != WRN_GENE:
                continue
            if (
                row["UsedByChronos"].strip().lower() != "true"
                or float(row["nAlignments"]) != 1.0
                or row["DropReason"].strip()
            ):
                continue
            sgrna = row["sgRNA"].strip()
            if sgrna in guides:
                raise IntegrityError(f"duplicate eligible WRN guide: {sgrna}")
            guides[sgrna] = row
    if len(guides) < 3:
        raise IntegrityError(f"fewer than three eligible WRN guides in {path}")
    return guides


def load_mutation_burdens(
    path: Path,
    guides: dict[str, dict[str, str]],
    cohort: dict[str, str],
) -> tuple[dict[str, int], dict[str, object]]:
    found: dict[str, dict[str, str]] = {}
    model_columns: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fixed = {"chrom", "start", "end", "sgRNA"}
        model_columns = set(reader.fieldnames or []) - fixed
        missing_models = sorted(set(cohort) - model_columns)
        if missing_models:
            raise IntegrityError(f"cohort models absent from mutation matrix: {missing_models}")
        for row in reader:
            sgrna = row["sgRNA"].strip()
            if sgrna not in guides:
                continue
            if sgrna in found:
                raise IntegrityError(f"duplicate mutation row for WRN guide: {sgrna}")
            found[sgrna] = row
    if set(found) != set(guides):
        raise IntegrityError(
            f"WRN guide/mutation row mismatch: missing {sorted(set(guides)-set(found))}"
        )
    burdens = {model_id: 0 for model_id in cohort}
    guide_receipt = []
    for sgrna in sorted(guides):
        row = found[sgrna]
        values = {}
        for model_id in model_columns:
            try:
                value = int(row[model_id])
            except ValueError as exc:
                raise IntegrityError(
                    f"non-binary mutation value: {sgrna} {model_id}"
                ) from exc
            if value not in (0, 1):
                raise IntegrityError(f"non-binary mutation value: {sgrna} {model_id}")
            values[model_id] = value
        for model_id in cohort:
            burdens[model_id] += values[model_id]
        guide_receipt.append(
            {
                "sgRNA": sgrna,
                "chrom": row["chrom"],
                "start": int(row["start"]),
                "end": int(row["end"]),
                "mutated_all_1750_models": sum(values.values()),
                "mutated_frozen_34_models": sum(values[m] for m in cohort),
            }
        )
    return burdens, {
        "matrix_model_columns": len(model_columns),
        "cohort_coverage": len(set(cohort) & model_columns),
        "eligible_wrn_guides": len(guides),
        "guide_rows": guide_receipt,
    }


def build_exposures(
    cohort: dict[str, str],
    avana: dict[str, int],
    ky: dict[str, int],
    avana_n: int,
    ky_n: int,
) -> list[ModelExposure]:
    rows = []
    for model_id, tissue in cohort.items():
        avana_fraction = avana[model_id] / avana_n
        ky_fraction = ky[model_id] / ky_n
        rows.append(
            ModelExposure(
                model_id=model_id,
                tissue=tissue,
                avana_mutated_guides=avana[model_id],
                avana_total_guides=avana_n,
                avana_fraction=avana_fraction,
                ky_mutated_guides=ky[model_id],
                ky_total_guides=ky_n,
                ky_fraction=ky_fraction,
                absolute_fraction_difference=abs(avana_fraction - ky_fraction),
            )
        )
    return rows


def exposure_adequacy(rows: Sequence[ModelExposure]) -> dict[str, object]:
    by_tissue = {}
    for tissue in TISSUES:
        selected = [row for row in rows if row.tissue == tissue]
        values = [row.absolute_fraction_difference for row in selected]
        by_tissue[tissue] = {
            "n": len(selected),
            "unique_exposure_values": len(set(values)),
            "mutated_any_avana": sum(row.avana_mutated_guides > 0 for row in selected),
            "mutated_any_ky": sum(row.ky_mutated_guides > 0 for row in selected),
            "mutated_any_either": sum(
                row.avana_mutated_guides > 0 or row.ky_mutated_guides > 0
                for row in selected
            ),
            "nonconstant": len(set(values)) >= 2,
        }
    adequate = all(
        result["n"] >= 15 and result["nonconstant"]
        for result in by_tissue.values()
    )
    return {"by_tissue": by_tissue, "adequate_for_association": adequate}


def write_exposures(path: Path, rows: Sequence[ModelExposure]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ModelExposure.__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in sorted(rows, key=lambda item: (item.tissue, item.model_id)):
            writer.writerow(asdict(row))


def run(args: argparse.Namespace) -> dict[str, object]:
    receipt = verify_receipts(args)
    cohort = load_outcome_blind_cohort(Path(args.cohort_file))
    source_receipts = {}
    burdens = {}
    guide_counts = {}
    for source in SOURCES:
        key = source.lower()
        guides = load_wrn_guides(Path(getattr(args, f"{key}_guide_map")))
        guide_counts[source] = len(guides)
        burdens[source], source_receipts[source] = load_mutation_burdens(
            Path(getattr(args, f"{key}_mutations")), guides, cohort
        )
    rows = build_exposures(
        cohort,
        burdens["Avana"],
        burdens["KY"],
        guide_counts["Avana"],
        guide_counts["KY"],
    )
    adequacy = exposure_adequacy(rows)
    write_exposures(Path(args.model_output), rows)
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": (
            "PASS_T0_EXPOSURE_ADEQUACY"
            if adequacy["adequate_for_association"]
            else "FAIL_T0_EXPOSURE_CONSTANCY"
        ),
        "analysis_type": "outcome_blind_data_availability_and_exposure_adequacy_audit",
        "input_receipt": receipt,
        "source_receipts": source_receipts,
        "cohort_models": len(cohort),
        "adequacy": adequacy,
        "association_computed": False,
        "wrn_gap_values_parsed": False,
        "overall_adequate": adequacy["adequate_for_association"],
        "claim_boundary": (
            "guide-site mutation exposure adequacy only; no WRN-gap association"
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cohort-file",
        default="experiments/EXP-20260822-007/cohort.csv",
    )
    parser.add_argument(
        "--avana-guide-map", default="data/raw/depmap/23q4/AvanaGuideMap.csv"
    )
    parser.add_argument(
        "--ky-guide-map", default="data/raw/depmap/23q4/KYGuideMap.csv"
    )
    parser.add_argument(
        "--avana-mutations",
        default="data/raw/depmap/23q4/OmicsGuideMutationsBinaryAvana.csv",
    )
    parser.add_argument(
        "--ky-mutations",
        default="data/raw/depmap/23q4/OmicsGuideMutationsBinaryKY.csv",
    )
    parser.add_argument(
        "--output", default="experiments/EXP-20260822-007/results/summary.json"
    )
    parser.add_argument(
        "--model-output",
        default="experiments/EXP-20260822-007/results/model_exposure.csv",
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
            "association_computed": False,
            "overall_adequate": False,
        }
        exit_code = 1
    else:
        exit_code = 0 if result["overall_adequate"] else 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
