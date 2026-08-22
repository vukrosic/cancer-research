from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.stats import rankdata

from candrel.wrn_ordering import fixed_percentile_correlation


EXPERIMENT_ID = "EXP-20260822-013"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
EXPECTED_DENOMINATORS = {
    ("Avana", "Large Intestine"): 25,
    ("KY", "Large Intestine"): 30,
    ("Avana", "Ovary"): 22,
    ("KY", "Ovary"): 26,
}
EXPECTED_PAIRS = {"Large Intestine": 17, "Ovary": 17}
EFFICIENCY_SHA256 = "a64065456d8d1e83d2fac94fc7e3ae28e65272cd2a45c3fa969848555f0b7aa0"
GROWTH_SHA256 = "4f2f4a9f80af1e9862319156f9a8de38d677797074823bebec7853060550f29c"
DENOMINATOR_SHA256 = "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654"
OUTCOME_SHA256 = "f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a"
SOURCE_COLUMNS = {
    "Avana": "Achilles-Avana-2D",
    "KY": "Achilles-KY-2D",
}
PERMUTATIONS = 100_000
BOOTSTRAPS = 10_000
SEED = 20260830
ATOL = 1e-8
MIN_DISTINCT = 10
MAX_TIE = 8
THETA_TARGET = 0.40
P_MAX = 0.05
CI_LOW_MIN = 0.10
MIN_TISSUE_RHO = -0.20


class IntegrityError(RuntimeError):
    """Raised when a frozen input or analysis invariant drifts."""


@dataclass(frozen=True)
class Denominator:
    model_id: str
    model_name: str
    tissue: str
    label: str
    source: str
    screen_id: str


@dataclass(frozen=True)
class ParameterRow:
    model_id: str
    source: str
    tissue: str
    raw_efficacy: float
    raw_growth_rate: float
    efficacy_percentile: float
    growth_percentile: float


@dataclass(frozen=True)
class OutcomeRow:
    model_id: str
    model_name: str
    tissue: str
    label: str
    gap: float
    flagged: bool


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_float(value: str, identity: object) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise IntegrityError(f"non-numeric value for {identity}") from exc
    if not math.isfinite(parsed):
        raise IntegrityError(f"non-finite value for {identity}")
    return parsed


def parse_bool(value: str, identity: object) -> bool:
    if value == "True":
        return True
    if value == "False":
        return False
    raise IntegrityError(f"noncanonical boolean for {identity}")


def load_denominators(path: Path) -> tuple[list[Denominator], dict[str, str]]:
    actual = sha256(path)
    if actual != DENOMINATOR_SHA256:
        raise IntegrityError(f"denominator SHA-256 drift: {actual}")
    rows = []
    identities = set()
    screens = set()
    counts = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            source = raw["library"].strip()
            tissue = raw["tissue"].strip()
            if source not in SOURCES or tissue not in TISSUES:
                continue
            model_id = raw["model_id"].strip()
            screen_ids = [part.strip() for part in raw["screen_ids"].split(";") if part.strip()]
            if len(screen_ids) != 1:
                raise IntegrityError(f"expected one ScreenID: {model_id} {source}")
            screen_id = screen_ids[0]
            identity = (model_id, source, tissue)
            if identity in identities or screen_id in screens:
                raise IntegrityError(f"duplicate denominator identity: {identity}")
            identities.add(identity)
            screens.add(screen_id)
            counts[(source, tissue)] += 1
            rows.append(
                Denominator(
                    model_id=model_id,
                    model_name=raw["model_name"].strip(),
                    tissue=tissue,
                    label=raw["label"].strip(),
                    source=source,
                    screen_id=screen_id,
                )
            )
    if len(rows) != 103 or dict(counts) != EXPECTED_DENOMINATORS:
        raise IntegrityError(f"denominator drift: rows={len(rows)} counts={dict(counts)}")
    return sorted(rows, key=lambda row: (row.source, row.tissue, row.model_id)), {
        "sha256": actual,
        "rows": str(len(rows)),
    }


def load_parameter_file(
    path: Path,
    expected_hash: str,
    denominators: Sequence[Denominator],
    domain: str,
) -> tuple[dict[tuple[str, str], float], dict[str, object]]:
    actual = sha256(path)
    if actual != expected_hash:
        raise IntegrityError(f"parameter SHA-256 drift: {path.name}")
    target_ids = {row.model_id for row in denominators}
    required_sources_by_model: dict[str, set[str]] = defaultdict(set)
    for row in denominators:
        required_sources_by_model[row.model_id].add(row.source)
    values = {}
    seen_all = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "ModelID" not in reader.fieldnames:
            raise IntegrityError(f"parameter header drift: {path.name}")
        for source, column in SOURCE_COLUMNS.items():
            if column not in reader.fieldnames:
                raise IntegrityError(f"missing {column} in {path.name}")
        for row in reader:
            model_id = row["ModelID"].strip()
            if not model_id or model_id in seen_all:
                raise IntegrityError(f"duplicate/blank ModelID in {path.name}: {model_id}")
            seen_all.add(model_id)
            if model_id not in target_ids:
                continue
            required_sources = required_sources_by_model[model_id]
            for source, column in SOURCE_COLUMNS.items():
                if source not in required_sources:
                    # Unpaired denominator records are source-specific. An
                    # opposite-source blank is expected and is never used.
                    continue
                raw = row[column].strip()
                if not raw:
                    raise IntegrityError(f"missing parameter: {path.name} {model_id} {source}")
                value = parse_float(raw, (path.name, model_id, source))
                if domain == "efficacy" and not (0 < value <= 1):
                    raise IntegrityError(f"efficacy domain drift: {model_id} {source}")
                if domain == "growth" and not (value > 0):
                    raise IntegrityError(f"growth domain drift: {model_id} {source}")
                values[(model_id, source)] = value
    expected_keys = {(row.model_id, row.source) for row in denominators}
    if set(values) != expected_keys:
        raise IntegrityError(f"parameter coverage drift: {path.name}")
    return values, {
        "sha256": actual,
        "unique_model_ids": len(seen_all),
        "mapped_source_model_values": len(values),
        "domain": domain,
    }


def within_stratum_percentiles(
    denominators: Sequence[Denominator], values: dict[tuple[str, str], float]
) -> dict[tuple[str, str], float]:
    grouped: dict[tuple[str, str], list[Denominator]] = defaultdict(list)
    for row in denominators:
        grouped[(row.source, row.tissue)].append(row)
    if {key: len(rows) for key, rows in grouped.items()} != EXPECTED_DENOMINATORS:
        raise IntegrityError("parameter percentile denominators drift")
    result = {}
    for key, rows in grouped.items():
        ordered = sorted(rows, key=lambda row: row.model_id)
        raw = np.asarray([values[(row.model_id, row.source)] for row in ordered], dtype=float)
        ranks = rankdata(raw, method="average")
        percentiles = (ranks - 1) / (len(raw) - 1)
        for row, percentile in zip(ordered, percentiles, strict=True):
            result[(row.model_id, row.source)] = float(percentile)
    if len(result) != sum(EXPECTED_DENOMINATORS.values()) or not all(math.isfinite(value) for value in result.values()):
        raise IntegrityError("parameter percentile coverage/value drift")
    return result


def tied_exposure_gate(values: Sequence[float], tissue: str, parameter: str) -> dict[str, object]:
    counts = Counter(values)
    distinct = len(counts)
    largest = max(counts.values())
    if distinct < MIN_DISTINCT or largest > MAX_TIE:
        raise IntegrityError(
            f"{parameter} exposure adequacy drift in {tissue}: distinct={distinct} largest_tie={largest}"
        )
    return {"distinct": distinct, "largest_tie": largest, "pairs": len(values)}


def build_parameter_rows(
    denominators: Sequence[Denominator],
    efficacy: dict[tuple[str, str], float],
    growth: dict[tuple[str, str], float],
    efficacy_q: dict[tuple[str, str], float],
    growth_q: dict[tuple[str, str], float],
) -> list[ParameterRow]:
    rows = [
        ParameterRow(
            model_id=row.model_id,
            source=row.source,
            tissue=row.tissue,
            raw_efficacy=efficacy[(row.model_id, row.source)],
            raw_growth_rate=growth[(row.model_id, row.source)],
            efficacy_percentile=efficacy_q[(row.model_id, row.source)],
            growth_percentile=growth_q[(row.model_id, row.source)],
        )
        for row in denominators
    ]
    if len(rows) != 103:
        raise IntegrityError("parameter ledger row drift")
    return rows


def write_rows(path: Path, fields: Sequence[str], rows: Sequence[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_parameter_ledger(path: Path, rows: Sequence[ParameterRow]) -> None:
    write_rows(path, list(ParameterRow.__dataclass_fields__), [row.__dict__ for row in rows])


def load_outcome(path: Path, pair_ids: set[str]) -> tuple[list[OutcomeRow], str]:
    actual = sha256(path)
    if actual != OUTCOME_SHA256:
        raise IntegrityError(f"outcome SHA-256 drift: {actual}")
    rows = []
    seen = set()
    counts = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            model_id = raw["model_id"].strip()
            tissue = raw["tissue"].strip()
            if model_id not in pair_ids or model_id in seen or tissue not in TISSUES:
                raise IntegrityError(f"invalid outcome identity: {model_id}")
            gap = parse_float(raw["absolute_percentile_gap"], (model_id, "gap"))
            flagged = parse_bool(raw["discordant_ge_0_25"], (model_id, "flag"))
            if flagged != (gap >= 0.25):
                raise IntegrityError(f"outcome flag drift: {model_id}")
            seen.add(model_id)
            counts[tissue] += 1
            rows.append(
                OutcomeRow(
                    model_id=model_id,
                    model_name=raw["model_name"].strip(),
                    tissue=tissue,
                    label=raw["label"].strip(),
                    gap=gap,
                    flagged=flagged,
                )
            )
    if set(seen) != pair_ids or dict(counts) != EXPECTED_PAIRS:
        raise IntegrityError(f"outcome population drift: rows={len(rows)} counts={dict(counts)}")
    return sorted(rows, key=lambda row: (row.tissue, row.model_id)), actual


def fixed_spearman(x: Sequence[float], y: Sequence[float]) -> float:
    x_rank = rankdata(np.asarray(x, dtype=float), method="average")
    y_rank = rankdata(np.asarray(y, dtype=float), method="average")
    return fixed_percentile_correlation(x_rank, y_rank)


def paired_exposure_rows(
    outcomes: Sequence[OutcomeRow],
    efficacy_q: dict[tuple[str, str], float],
    growth_q: dict[tuple[str, str], float],
) -> list[dict[str, object]]:
    rows = []
    for outcome in outcomes:
        avana_eff = efficacy_q[(outcome.model_id, "Avana")]
        ky_eff = efficacy_q[(outcome.model_id, "KY")]
        avana_growth = growth_q[(outcome.model_id, "Avana")]
        ky_growth = growth_q[(outcome.model_id, "KY")]
        rows.append(
            {
                "model_id": outcome.model_id,
                "model_name": outcome.model_name,
                "tissue": outcome.tissue,
                "label": outcome.label,
                "efficacy_exposure": abs(avana_eff - ky_eff),
                "growth_exposure": abs(avana_growth - ky_growth),
                "wrn_percentile_gap": outcome.gap,
                "wrn_gap_flagged": outcome.flagged,
                "avana_efficacy_percentile": avana_eff,
                "ky_efficacy_percentile": ky_eff,
                "avana_growth_percentile": avana_growth,
                "ky_growth_percentile": ky_growth,
            }
        )
    if len(rows) != 34:
        raise IntegrityError("paired exposure ledger drift")
    return rows


def arrays_by_tissue(
    paired_rows: Sequence[dict[str, object]], parameter: str
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    result = {}
    for tissue in TISSUES:
        selected = sorted(
            [row for row in paired_rows if row["tissue"] == tissue],
            key=lambda row: str(row["model_id"]),
        )
        x = np.asarray([float(row[f"{parameter}_exposure"]) for row in selected], dtype=float)
        y = np.asarray([float(row["wrn_percentile_gap"]) for row in selected], dtype=float)
        if len(x) != EXPECTED_PAIRS[tissue] or not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)):
            raise IntegrityError(f"paired array drift: {parameter} {tissue}")
        result[tissue] = (x, y)
    return result


def inference(
    paired_rows: Sequence[dict[str, object]],
    parameter: str,
    rng: np.random.Generator,
    *,
    inferential: bool,
) -> dict[str, object]:
    arrays = arrays_by_tissue(paired_rows, parameter)
    tissue_rho = {tissue: fixed_spearman(x, y) for tissue, (x, y) in arrays.items()}
    theta = float(np.mean(list(tissue_rho.values())))
    result = {
        "parameter": parameter,
        "tissue_rho": tissue_rho,
        "theta": theta,
    }
    if not inferential:
        return result
    frozen = {}
    for tissue, (x, y) in arrays.items():
        xr = rankdata(x, method="average")
        yr = rankdata(y, method="average")
        x_centered = (xr - xr.mean()) / np.sqrt(np.sum((xr - xr.mean()) ** 2))
        y_centered = (yr - yr.mean()) / np.sqrt(np.sum((yr - yr.mean()) ** 2))
        frozen[tissue] = (x_centered, y_centered)
    extreme = 0
    generated = 0
    batch_size = 2000
    while generated < PERMUTATIONS:
        batch = min(batch_size, PERMUTATIONS - generated)
        estimates = []
        for tissue in TISSUES:
            x_centered, y_centered = frozen[tissue]
            indices = np.argsort(rng.random((batch, len(y_centered))), axis=1)
            estimates.append(y_centered[indices] @ x_centered)
        extreme += int(np.count_nonzero(np.mean(np.vstack(estimates), axis=0) >= theta))
        generated += batch
    p_value = (1 + extreme) / (PERMUTATIONS + 1)
    bootstrap = np.empty(BOOTSTRAPS, dtype=float)
    for index in range(BOOTSTRAPS):
        correlations = []
        for tissue, (x, y) in arrays.items():
            xr = rankdata(x, method="average")
            yr = rankdata(y, method="average")
            sample = rng.integers(0, len(xr), size=len(xr))
            correlations.append(fixed_percentile_correlation(xr[sample], yr[sample]))
        bootstrap[index] = float(np.mean(correlations))
    ci_low, ci_high = np.quantile(bootstrap, [0.025, 0.975])
    result.update({
        "permutation_repeats": PERMUTATIONS,
        "permutation_extreme_count": extreme,
        "permutation_p_one_sided": p_value,
        "bootstrap_repeats": BOOTSTRAPS,
        "bootstrap_ci_95": [float(ci_low), float(ci_high)],
    })
    return result


def write_inference_rows(path: Path, efficacy: dict[str, object], growth: dict[str, object]) -> None:
    rows = []
    for result, inferential in ((efficacy, True), (growth, False)):
        for tissue in TISSUES:
            rows.append(
                {
                    "parameter": result["parameter"],
                    "tissue": tissue,
                    "n_pairs": EXPECTED_PAIRS[tissue],
                    "spearman_rho": result["tissue_rho"][tissue],
                    "equal_tissue_theta": result["theta"],
                    "inferential_primary": inferential,
                }
            )
    write_rows(
        path,
        ["parameter", "tissue", "n_pairs", "spearman_rho", "equal_tissue_theta", "inferential_primary"],
        rows,
    )


def summary_digest(result: dict[str, object]) -> str:
    payload = json.loads(json.dumps(result))
    payload["artifact_receipt_sha256"]["summary.json"] = ""
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()
    return hashlib.sha256(encoded).hexdigest()


def run(args: argparse.Namespace, output_dir: Path) -> dict[str, object]:
    denominators, denominator_receipt = load_denominators(Path(args.denominator_file))
    by_model: dict[str, list[Denominator]] = defaultdict(list)
    for row in denominators:
        by_model[row.model_id].append(row)
    paired_ids = set()
    for model_id, records in by_model.items():
        if len(records) == 2:
            if {record.source for record in records} != set(SOURCES) or len({record.tissue for record in records}) != 1:
                raise IntegrityError(f"invalid cross-source pair identity: {model_id}")
            paired_ids.add(model_id)
    if len(paired_ids) != 34:
        raise IntegrityError(f"paired model count drift: {len(paired_ids)}")
    efficacy, efficacy_receipt = load_parameter_file(
        Path(args.efficacy_file), EFFICIENCY_SHA256, denominators, "efficacy"
    )
    growth, growth_receipt = load_parameter_file(
        Path(args.growth_file), GROWTH_SHA256, denominators, "growth"
    )
    efficacy_q = within_stratum_percentiles(denominators, efficacy)
    growth_q = within_stratum_percentiles(denominators, growth)
    by_model: dict[str, list[Denominator]] = defaultdict(list)
    for row in denominators:
        by_model[row.model_id].append(row)
    adequacy = {"efficacy": {}, "growth": {}}
    for tissue in TISSUES:
        selected = [row for row in denominators if row.tissue == tissue and row.model_id in paired_ids]
        efficacy_exposure = [abs(efficacy_q[(row.model_id, "Avana")] - efficacy_q[(row.model_id, "KY")]) for row in selected]
        growth_exposure = [abs(growth_q[(row.model_id, "Avana")] - growth_q[(row.model_id, "KY")]) for row in selected]
        adequacy["efficacy"][tissue] = tied_exposure_gate(efficacy_exposure, tissue, "efficacy")
        adequacy["growth"][tissue] = tied_exposure_gate(growth_exposure, tissue, "growth")
    parameter_rows = build_parameter_rows(denominators, efficacy, growth, efficacy_q, growth_q)
    write_parameter_ledger(output_dir / "parameter_ledger.csv", parameter_rows)

    # The hash-locked WRN outcome is intentionally opened only after the complete
    # parameter ledger and all outcome-blind adequacy gates have passed.
    outcome, outcome_hash = load_outcome(Path(args.outcome_file), paired_ids)
    paired_rows = paired_exposure_rows(outcome, efficacy_q, growth_q)
    write_rows(
        output_dir / "paired_exposure_outcome.csv",
        [
            "model_id", "model_name", "tissue", "label", "efficacy_exposure", "growth_exposure",
            "wrn_percentile_gap", "wrn_gap_flagged", "avana_efficacy_percentile",
            "ky_efficacy_percentile", "avana_growth_percentile", "ky_growth_percentile",
        ],
        paired_rows,
    )
    rng = np.random.default_rng(SEED)
    efficacy_result = inference(paired_rows, "efficacy", rng, inferential=True)
    growth_result = inference(paired_rows, "growth", rng, inferential=False)
    write_inference_rows(output_dir / "inference.csv", efficacy_result, growth_result)
    primary = {
        "theta": efficacy_result["theta"],
        "tissue_rho": efficacy_result["tissue_rho"],
        "permutation_p_one_sided": efficacy_result["permutation_p_one_sided"],
        "bootstrap_ci_95": efficacy_result["bootstrap_ci_95"],
        "gates": {
            "theta_ge_0_40": efficacy_result["theta"] >= THETA_TARGET,
            "permutation_p_le_0_05": efficacy_result["permutation_p_one_sided"] <= P_MAX,
            "bootstrap_lower_gt_0_10": efficacy_result["bootstrap_ci_95"][0] > CI_LOW_MIN,
            "no_tissue_rho_below_minus_0_20": min(efficacy_result["tissue_rho"].values()) >= MIN_TISSUE_RHO,
        },
    }
    primary["pass"] = all(primary["gates"].values())
    artifact_receipt = {
        name: sha256(output_dir / name)
        for name in ("parameter_ledger.csv", "paired_exposure_outcome.csv", "inference.csv")
    }
    artifact_receipt["summary.json"] = ""
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "PASS_EFFICACY_ASSOCIATION" if primary["pass"] else "FAIL_EFFICACY_ASSOCIATION",
        "analysis_type": "preregistered_same_assay_model_parameter_association_after_endpoint_unsealing",
        "input_receipt": {
            "denominator": denominator_receipt,
            "efficacy": efficacy_receipt,
            "growth": growth_receipt,
            "outcome_sha256_after_adequacy": outcome_hash,
        },
        "adequacy": adequacy,
        "primary": primary,
        "growth_descriptive": {
            "theta": growth_result["theta"],
            "tissue_rho": growth_result["tissue_rho"],
            "p_values_computed": 0,
            "confidence_intervals_computed": 0,
            "can_rescue_primary": False,
        },
        "inference_receipt": {
            "seed": SEED,
            "permutations": PERMUTATIONS,
            "bootstraps": BOOTSTRAPS,
            "paired_model_unit": True,
            "raw_units_compared_across_sources": False,
            "zero_variance_bootstrap_redraws": 0,
        },
        "artifact_receipt_sha256": artifact_receipt,
        "overall_pass": primary["pass"],
        "claim_boundary": "frozen cohort-specific association between efficacy-rank discordance and WRN gap",
    }
    return result


EXPECTED_RESULT_FILES = {
    "summary.json", "parameter_ledger.csv", "paired_exposure_outcome.csv", "inference.csv"
}


def write_error(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False)
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def validate_staged(stage: Path, result: dict[str, object]) -> None:
    if {path.name for path in stage.iterdir() if path.is_file()} != EXPECTED_RESULT_FILES:
        raise IntegrityError("staged EXP013 file set drift")
    expected_parameter_fields = tuple(ParameterRow.__dataclass_fields__)
    with (stage / "parameter_ledger.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != expected_parameter_fields:
            raise IntegrityError("parameter ledger schema drift")
        parameter_rows = list(reader)
    if len(parameter_rows) != 103 or len({(r["model_id"], r["source"], r["tissue"]) for r in parameter_rows}) != 103:
        raise IntegrityError("parameter ledger identity drift")
    with (stage / "paired_exposure_outcome.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != (
            "model_id", "model_name", "tissue", "label", "efficacy_exposure", "growth_exposure",
            "wrn_percentile_gap", "wrn_gap_flagged", "avana_efficacy_percentile",
            "ky_efficacy_percentile", "avana_growth_percentile", "ky_growth_percentile",
        ):
            raise IntegrityError("paired ledger schema drift")
        paired_rows = list(reader)
    if len(paired_rows) != 34 or len({r["model_id"] for r in paired_rows}) != 34:
        raise IntegrityError("paired ledger identity drift")
    with (stage / "inference.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != (
            "parameter", "tissue", "n_pairs", "spearman_rho", "equal_tissue_theta", "inferential_primary"
        ):
            raise IntegrityError("inference schema drift")
        inference_rows = list(reader)
    if len(inference_rows) != 4 or len({(r["parameter"], r["tissue"]) for r in inference_rows}) != 4:
        raise IntegrityError("inference identity drift")
    for row in paired_rows:
        gap = parse_float(row["wrn_percentile_gap"], row["model_id"])
        if parse_bool(row["wrn_gap_flagged"], row["model_id"]) != (gap >= 0.25):
            raise IntegrityError("paired outcome flag drift")
        for field in ("efficacy_exposure", "growth_exposure", "avana_efficacy_percentile", "ky_efficacy_percentile", "avana_growth_percentile", "ky_growth_percentile"):
            parse_float(row[field], (row["model_id"], field))
    required_summary = {
        "experiment_id", "status", "analysis_type", "input_receipt", "adequacy", "primary",
        "growth_descriptive", "inference_receipt", "artifact_receipt_sha256", "overall_pass", "claim_boundary"
    }
    if set(result) != required_summary or result["experiment_id"] != EXPERIMENT_ID:
        raise IntegrityError("summary schema drift")
    if result["overall_pass"] != result["primary"]["pass"]:
        raise IntegrityError("summary pass drift")
    if set(result["artifact_receipt_sha256"]) != EXPECTED_RESULT_FILES:
        raise IntegrityError("artifact receipt schema drift")
    for name in EXPECTED_RESULT_FILES - {"summary.json"}:
        if result["artifact_receipt_sha256"][name] != sha256(stage / name):
            raise IntegrityError(f"artifact hash drift: {name}")
    if result["artifact_receipt_sha256"]["summary.json"] != summary_digest(result):
        raise IntegrityError("summary self-digest drift")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--efficacy-file", default="data/raw/depmap/23q4/CRISPRInferredModelEfficacy.csv")
    parser.add_argument("--growth-file", default="data/raw/depmap/23q4/CRISPRInferredModelGrowthRate.csv")
    parser.add_argument("--denominator-file", default="experiments/EXP-20260822-003/results/model_scores.csv")
    parser.add_argument("--outcome-file", default="experiments/EXP-20260822-005/results/model_percentile_gaps.csv")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-013/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-013/error_receipt.json")
    return parser


def publish(args: argparse.Namespace) -> int:
    target = Path(args.results_dir)
    error = Path(args.error_receipt)
    if target.exists():
        write_error(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_RESULTS_DIRECTORY_EXISTS", "results_written": False, "overall_pass": False})
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=target.parent, prefix=f".{target.name}.stage.") as temporary_name:
            stage = Path(temporary_name)
            result = run(args, stage)
            result["artifact_receipt_sha256"]["summary.json"] = summary_digest(result)
            (stage / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_staged(stage, result)
            if json.loads((stage / "summary.json").read_text()) != result:
                raise IntegrityError("summary round-trip drift")
            os.replace(stage, target)
    except Exception as exc:
        write_error(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_INTEGRITY", "error": str(exc), "error_type": type(exc).__name__, "results_written": False, "overall_pass": False})
        return 1
    if error.exists():
        error.unlink()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 2


def main() -> None:
    raise SystemExit(publish(build_parser().parse_args()))


if __name__ == "__main__":
    main()
