from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median
from typing import Iterable, Sequence

import numpy as np


TISSUES = ("Large Intestine", "Ovary", "Endometrium", "Stomach")
LIBRARIES = ("Avana", "KY")
WRN_COLUMN = "WRN (7486)"
EXPECTED_SCORE_MD5 = "265f8372e9cd0fad56c1a6b66b8a783d"
EXPECTED_METADATA_SHA256 = {
    "qc_file": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "sequence_map_file": "e4b99b4a6cd48c3957c5ada2abeeed1e1de319fe26526e76de6088ec73704c0b",
    "model_file": "6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341",
    "msi_file": "eb43e92042ab430adabbbcf65e577459ac52d57df802eb388aea5865ff9b49aa",
}


class IntegrityError(RuntimeError):
    """Raised when frozen input or cohort invariants do not hold."""


@dataclass(frozen=True)
class EligibleScreen:
    screen_id: str
    model_id: str
    model_name: str
    tissue: str
    label: str
    library: str
    qc_status: str


@dataclass(frozen=True)
class ModelScore:
    model_id: str
    model_name: str
    tissue: str
    label: str
    library: str
    screen_ids: str
    score: float


def file_digest(path: Path, algorithm: str) -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_cmp_models(path: Path) -> dict[str, tuple[str, str, str]]:
    by_broad_id: dict[str, tuple[str, str, str]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            broad_id = row["BROAD_ID"].strip()
            tissue = row["tissue"].strip()
            label = row["msi_status"].strip()
            if not broad_id or tissue not in TISSUES or label not in {"MSI", "MSS"}:
                continue
            value = (row["model_name"].strip(), tissue, label)
            if broad_id in by_broad_id and by_broad_id[broad_id] != value:
                raise IntegrityError(f"non-unique BROAD_ID mapping: {broad_id}")
            by_broad_id[broad_id] = value
    return by_broad_id


def load_depmap_model_ids(path: Path) -> set[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        return {row["ModelID"].strip() for row in csv.DictReader(handle)}


def load_eligible_screens(
    qc_path: Path, cmp_path: Path, depmap_model_path: Path
) -> list[EligibleScreen]:
    cmp_models = load_cmp_models(cmp_path)
    depmap_ids = load_depmap_model_ids(depmap_model_path)
    screens: list[EligibleScreen] = []
    seen_screen_ids: set[str] = set()
    with qc_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            model_id = row["ModelID"].strip()
            library = row["Library"].strip()
            if (
                model_id not in cmp_models
                or model_id not in depmap_ids
                or library not in LIBRARIES
                or row["PassesQC"].strip().lower() != "true"
                or row["CanInclude"].strip().lower() != "true"
            ):
                continue
            screen_id = row["ScreenID"].strip()
            if screen_id in seen_screen_ids:
                raise IntegrityError(f"duplicate eligible ScreenID: {screen_id}")
            seen_screen_ids.add(screen_id)
            model_name, tissue, label = cmp_models[model_id]
            screens.append(
                EligibleScreen(
                    screen_id=screen_id,
                    model_id=model_id,
                    model_name=model_name,
                    tissue=tissue,
                    label=label,
                    library=library,
                    qc_status=row["QCStatus"].strip(),
                )
            )
    return screens


def extract_endpoint(
    path: Path,
    column: str = WRN_COLUMN,
    include_screen_ids: set[str] | None = None,
) -> dict[str, float]:
    values: dict[str, float] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise IntegrityError("empty endpoint matrix") from exc
        if header.count(column) != 1:
            raise IntegrityError(f"expected exactly one {column!r} column")
        index = header.index(column)
        for row in reader:
            if not row:
                continue
            screen_id = row[0].strip()
            if include_screen_ids is not None and screen_id not in include_screen_ids:
                continue
            if screen_id in values:
                raise IntegrityError(f"duplicate endpoint ScreenID: {screen_id}")
            if index >= len(row) or row[index].strip() == "":
                continue
            try:
                value = float(row[index])
            except ValueError as exc:
                raise IntegrityError(f"non-numeric {column} for {screen_id}") from exc
            if math.isfinite(value):
                values[screen_id] = value
    return values


def collapse_model_scores(
    eligible: Sequence[EligibleScreen], endpoint: dict[str, float]
) -> list[ModelScore]:
    grouped: dict[tuple[str, str], list[tuple[EligibleScreen, float]]] = defaultdict(list)
    for screen in eligible:
        if screen.screen_id in endpoint:
            grouped[(screen.library, screen.model_id)].append(
                (screen, endpoint[screen.screen_id])
            )
    rows: list[ModelScore] = []
    for (library, model_id), records in sorted(grouped.items()):
        first = records[0][0]
        if any(
            (r.model_name, r.tissue, r.label) !=
            (first.model_name, first.tissue, first.label)
            for r, _ in records
        ):
            raise IntegrityError(f"inconsistent metadata within model: {model_id}")
        rows.append(
            ModelScore(
                model_id=model_id,
                model_name=first.model_name,
                tissue=first.tissue,
                label=first.label,
                library=library,
                screen_ids=";".join(sorted(r.screen_id for r, _ in records)),
                score=float(median(v for _, v in records)),
            )
        )
    return rows


def _group_values(rows: Sequence[ModelScore]) -> dict[str, dict[str, np.ndarray]]:
    grouped: dict[str, dict[str, list[float]]] = {
        tissue: {"MSI": [], "MSS": []} for tissue in TISSUES
    }
    for row in rows:
        grouped[row.tissue][row.label].append(row.score)
    return {
        tissue: {
            label: np.asarray(values, dtype=float)
            for label, values in by_label.items()
        }
        for tissue, by_label in grouped.items()
    }


def pair_delta(msi: np.ndarray, mss: np.ndarray) -> tuple[float, np.ndarray]:
    differences = (msi[:, None] - mss[None, :]).reshape(-1)
    return float(np.sign(differences).mean()), differences


def stratified_delta(rows: Sequence[ModelScore]) -> tuple[float, dict[str, float], float]:
    grouped = _group_values(rows)
    pair_sign_sum = 0.0
    pair_count = 0
    all_differences: list[np.ndarray] = []
    tissue_deltas: dict[str, float] = {}
    for tissue in TISSUES:
        msi = grouped[tissue]["MSI"]
        mss = grouped[tissue]["MSS"]
        if not len(msi) or not len(mss):
            raise IntegrityError(f"empty label group in {tissue}")
        delta, differences = pair_delta(msi, mss)
        tissue_deltas[tissue] = delta
        pair_sign_sum += float(np.sign(differences).sum())
        pair_count += differences.size
        all_differences.append(differences)
    return (
        pair_sign_sum / pair_count,
        tissue_deltas,
        float(np.median(np.concatenate(all_differences))),
    )


def check_adequacy(
    eligible: Sequence[EligibleScreen], rows: Sequence[ModelScore], library: str
) -> dict[str, object]:
    eligible_models = {
        s.model_id for s in eligible if s.library == library
    }
    scored = [row for row in rows if row.library == library]
    scored_models = {row.model_id for row in scored}
    completeness = len(scored_models) / len(eligible_models) if eligible_models else 0.0
    counts: dict[str, dict[str, int]] = {}
    adequate = completeness >= 0.8
    for tissue in TISSUES:
        counts[tissue] = {
            label: sum(r.tissue == tissue and r.label == label for r in scored)
            for label in ("MSI", "MSS")
        }
        adequate = adequate and all(value >= 2 for value in counts[tissue].values())
    return {
        "eligible_models": len(eligible_models),
        "scored_models": len(scored_models),
        "completeness": completeness,
        "counts": counts,
        "adequate": bool(adequate),
    }


def permutation_pvalue(
    rows: Sequence[ModelScore], observed: float, repeats: int, rng: np.random.Generator
) -> float:
    grouped = _group_values(rows)
    extreme = 0
    for _ in range(repeats):
        sign_sum = 0.0
        pair_count = 0
        for tissue in TISSUES:
            msi = grouped[tissue]["MSI"]
            mss = grouped[tissue]["MSS"]
            shuffled = rng.permutation(np.concatenate((msi, mss)))
            perm_msi = shuffled[: len(msi)]
            perm_mss = shuffled[len(msi) :]
            differences = perm_msi[:, None] - perm_mss[None, :]
            sign_sum += float(np.sign(differences).sum())
            pair_count += differences.size
        if sign_sum / pair_count <= observed:
            extreme += 1
    return (1 + extreme) / (repeats + 1)


def bootstrap_interval(
    rows: Sequence[ModelScore], repeats: int, rng: np.random.Generator
) -> tuple[float, float]:
    grouped = _group_values(rows)
    estimates = np.empty(repeats, dtype=float)
    for index in range(repeats):
        sign_sum = 0.0
        pair_count = 0
        for tissue in TISSUES:
            msi = grouped[tissue]["MSI"]
            mss = grouped[tissue]["MSS"]
            boot_msi = rng.choice(msi, size=len(msi), replace=True)
            boot_mss = rng.choice(mss, size=len(mss), replace=True)
            differences = boot_msi[:, None] - boot_mss[None, :]
            sign_sum += float(np.sign(differences).sum())
            pair_count += differences.size
        estimates[index] = sign_sum / pair_count
    low, high = np.quantile(estimates, [0.025, 0.975])
    return float(low), float(high)


def evaluate_source(
    rows: Sequence[ModelScore], library: str, permutations: int, bootstraps: int, seed: int
) -> dict[str, object]:
    source_rows = [row for row in rows if row.library == library]
    observed, tissue_deltas, median_shift = stratified_delta(source_rows)
    rng = np.random.default_rng(seed)
    p_value = permutation_pvalue(source_rows, observed, permutations, rng)
    ci_low, ci_high = bootstrap_interval(source_rows, bootstraps, rng)
    negative_tissues = sum(value < 0 for value in tissue_deltas.values())
    gates = {
        "negative_direction": observed < 0,
        "practical_effect": observed <= -0.33,
        "permutation_p": p_value <= 0.05,
        "ci_not_materially_opposite": ci_high < 0.10,
        "negative_tissues": negative_tissues >= 3,
        "no_materially_opposite_tissue": max(tissue_deltas.values()) <= 0.33,
    }
    return {
        "library": library,
        "n_models": len(source_rows),
        "stratified_delta": observed,
        "tissue_deltas": tissue_deltas,
        "median_within_tissue_msi_minus_mss": median_shift,
        "permutation_p_one_sided": p_value,
        "bootstrap_ci_95": [ci_low, ci_high],
        "negative_tissue_count": negative_tissues,
        "gates": gates,
        "pass": all(gates.values()),
    }


def write_model_table(path: Path, rows: Iterable[ModelScore]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [field.name for field in ModelScore.__dataclass_fields__.values()]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in sorted(rows, key=lambda r: (r.library, r.tissue, r.label, r.model_id)):
            writer.writerow(asdict(row))


def verify_input_hashes(args: argparse.Namespace) -> dict[str, str]:
    score_path = Path(args.score_file)
    actual_md5 = file_digest(score_path, "md5")
    if actual_md5 != EXPECTED_SCORE_MD5:
        raise IntegrityError(
            f"score MD5 drift: expected {EXPECTED_SCORE_MD5}, got {actual_md5}"
        )
    input_hashes: dict[str, str] = {"score_file_md5": actual_md5}
    for argument, expected in EXPECTED_METADATA_SHA256.items():
        actual = file_digest(Path(getattr(args, argument)), "sha256")
        if actual != expected:
            raise IntegrityError(
                f"{argument} SHA-256 drift: expected {expected}, got {actual}"
            )
        input_hashes[f"{argument}_sha256"] = actual
    return input_hashes


def sequential_effect_evaluation(
    avana_rows: Sequence[ModelScore],
    ky_rows_loader,
    permutations: int,
    bootstraps: int,
    seed: int,
) -> tuple[dict[str, object], dict[str, object] | None, list[ModelScore]]:
    discovery = evaluate_source(
        avana_rows, "Avana", permutations, bootstraps, seed
    )
    if not discovery["pass"]:
        return discovery, None, list(avana_rows)
    ky_rows = list(ky_rows_loader())
    confirmation = evaluate_source(
        ky_rows, "KY", permutations, bootstraps, seed + 1
    )
    return discovery, confirmation, list(avana_rows) + ky_rows


def run(args: argparse.Namespace) -> dict[str, object]:
    score_path = Path(args.score_file)
    input_hashes = verify_input_hashes(args)
    eligible = load_eligible_screens(
        Path(args.qc_file), Path(args.msi_file), Path(args.model_file)
    )
    avana_eligible = [screen for screen in eligible if screen.library == "Avana"]
    avana_endpoint = extract_endpoint(
        score_path,
        include_screen_ids={screen.screen_id for screen in avana_eligible},
    )
    avana_scores = collapse_model_scores(avana_eligible, avana_endpoint)
    adequacy: dict[str, object] = {
        "Avana": check_adequacy(avana_eligible, avana_scores, "Avana")
    }
    if not adequacy["Avana"]["adequate"]:
        return {
            "experiment_id": "EXP-20260822-003",
            "status": "FAIL_T0_AVAILABILITY",
            "input_hashes": input_hashes,
            "adequacy": adequacy,
            "discovery": None,
            "confirmation": None,
            "overall_pass": False,
        }

    def load_ky_rows() -> list[ModelScore]:
        ky_eligible = [screen for screen in eligible if screen.library == "KY"]
        ky_endpoint = extract_endpoint(
            score_path,
            include_screen_ids={screen.screen_id for screen in ky_eligible},
        )
        ky_scores = collapse_model_scores(ky_eligible, ky_endpoint)
        ky_adequacy = check_adequacy(ky_eligible, ky_scores, "KY")
        adequacy["KY"] = ky_adequacy
        if not ky_adequacy["adequate"]:
            raise IntegrityError("KY endpoint failed the frozen confirmation adequacy gate")
        return ky_scores

    discovery, confirmation, emitted_rows = sequential_effect_evaluation(
        avana_scores,
        load_ky_rows,
        args.permutations,
        args.bootstraps,
        args.seed,
    )
    write_model_table(Path(args.model_output), emitted_rows)
    overall_pass = bool(discovery["pass"] and confirmation and confirmation["pass"])
    if not discovery["pass"]:
        status = "FAIL_DISCOVERY"
    elif not confirmation["pass"]:
        status = "FAIL_CONFIRMATION"
    else:
        status = "PASS_POSITIVE_CONTROL_RECOVERY"
    return {
        "experiment_id": "EXP-20260822-003",
        "status": status,
        "input_hashes": input_hashes,
        "seed": args.seed,
        "permutation_repeats": args.permutations,
        "bootstrap_repeats": args.bootstraps,
        "adequacy": adequacy,
        "discovery": discovery,
        "confirmation": confirmation,
        "overall_pass": overall_pass,
        "confirmation_policy": "KY contrast evaluated only after Avana passes",
        "protocol_deviation": {
            "occurred": True,
            "summary": (
                "The first implementation parsed KY endpoint values before the "
                "Avana gate. No KY contrast was calculated until Avana passed, but "
                "KY values cannot be described as unseen. Final code is source-sequential."
            ),
            "claim_label": "sequentially_gated_confirmation_not_unseen_held_out",
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--score-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv"
    )
    parser.add_argument(
        "--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv"
    )
    parser.add_argument(
        "--model-file", default="data/raw/depmap/23q4/Model.csv"
    )
    parser.add_argument(
        "--sequence-map-file", default="data/raw/depmap/23q4/ScreenSequenceMap.csv"
    )
    parser.add_argument(
        "--msi-file",
        default="data/raw/cell_model_passports/provenance_gate/model_list_20260814.csv",
    )
    parser.add_argument(
        "--output",
        default="experiments/EXP-20260822-003/results/summary.json",
    )
    parser.add_argument(
        "--model-output",
        default="experiments/EXP-20260822-003/results/model_scores.csv",
    )
    parser.add_argument("--seed", type=int, default=20260824)
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
            "experiment_id": "EXP-20260822-003",
            "status": "ERROR_INTEGRITY",
            "error": str(exc),
            "overall_pass": False,
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result, indent=2, sort_keys=True))
        raise SystemExit(1) from exc
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["overall_pass"] else 2)


if __name__ == "__main__":
    main()
