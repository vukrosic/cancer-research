from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Sequence

import numpy as np

from . import arid1a_replication as base


EXPERIMENT_ID = "EXP-20260822-016"
TARGET_COLUMN = "KEAP1 (9817)"
PAIR_ID = "ARID1A_to_KEAP1"
SOURCES = ("Avana", "KY")
DESIGN_SEEDS = {"Avana": 20261630, "KY": 20261730}
INFERENCE_SEEDS = {"Avana": 20271630, "KY": 20271730}
EXPECTED_RESULT_FILES = {
    "context_ledger.csv",
    "design_sensitivity.csv",
    "endpoint_scores.csv",
    "inference.csv",
    "summary.json",
}
EXPECTED_MODULE_PATH = "src/candrel/arid1a_keap1_replication.py"


IntegrityError = base.IntegrityError
T0Stop = base.T0Stop
Context = base.Context


def sha256(path: Path) -> str:
    return base.sha256(path)


def classify_context_stop(error: IntegrityError) -> str:
    message = str(error).lower()
    if "sha-256" in message:
        return "T0_INPUT_HASH"
    if "header" in message or "column" in message:
        return "T0_SCHEMA_HEADER"
    if "coverage" in message or "duplicate" in message:
        return "T0_MATRIX_COVERAGE"
    return "T0_IDENTITY_JOIN"


def git_command(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def git_blob_sha256(commit: str, path: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        raise ValueError(f"implementation module is absent at commit: {commit}")
    return hashlib.sha256(result.stdout).hexdigest()


def verify_implementation_boundary(manifest_path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        boundary = manifest["implementation_boundary"]
        base_commit = boundary["required_base_commit"]
        implementation_commit = boundary["implementation_commit"]
        module = boundary["implementation_module"]
        if manifest["experiment_id"] != EXPERIMENT_ID:
            raise ValueError("manifest experiment identity drift")
        if manifest["entrypoint"] != "uv run candrel-arid1a-keap1-replication":
            raise ValueError("manifest entrypoint drift")
        if manifest["inputs"]["endpoint"]["target_column"] != TARGET_COLUMN:
            raise ValueError("manifest endpoint target drift")
        if manifest["inputs"]["damaging_matrix"]["status_column"] != base.STATUS_COLUMN:
            raise ValueError("manifest status column drift")
        if manifest["inputs"]["damaging_matrix"]["status_threshold"] != 1:
            raise ValueError("manifest status threshold drift")
        manifest_hashes = {
            "endpoint": manifest["inputs"]["endpoint"]["sha256"],
            "screen_qc": manifest["inputs"]["screen_qc"]["sha256"],
            "screen_map": manifest["inputs"]["screen_map"]["sha256"],
            "model": manifest["inputs"]["model"]["sha256"],
            "damaging": manifest["inputs"]["damaging_matrix"]["sha256"],
        }
        if manifest_hashes != base.EXPECTED_HASHES:
            raise ValueError("manifest input hash contract drift")
        if manifest["eligibility"]["libraries"] != list(SOURCES):
            raise ValueError("manifest source contract drift")
        if manifest["eligibility"]["pass_qc"] is not True or manifest["eligibility"]["can_include"] is not True:
            raise ValueError("manifest eligibility contract drift")
        adequacy = manifest["adequacy"]
        if adequacy["min_damaging_models_per_source"] != base.MIN_LOSS:
            raise ValueError("manifest damaging adequacy drift")
        if adequacy["min_intact_models_per_source"] != base.MIN_INTACT:
            raise ValueError("manifest intact adequacy drift")
        if adequacy["min_lineages_with_both_statuses"] != base.MIN_LINEAGES:
            raise ValueError("manifest lineage adequacy drift")
        if manifest["primary_pair"] != "ARID1A_matrix_damaging_status_to_KEAP1_dependency":
            raise ValueError("manifest primary pair drift")
        if manifest["analysis_type"] != "preregistered_source_specific_lineage_stratified_arid1a_keap1_replication":
            raise ValueError("manifest analysis type drift")
        if manifest["design_sensitivity"]["mean_shift"] != base.NORMAL_MEAN_SHIFT:
            raise ValueError("manifest design shift drift")
        if manifest["design_sensitivity"]["null_permutations"] != base.PERMUTATIONS:
            raise ValueError("manifest design permutation drift")
        if manifest["design_sensitivity"]["alternative_simulations"] != base.DESIGN_SIMULATIONS:
            raise ValueError("manifest design simulation drift")
        if manifest["design_sensitivity"]["minimum_power_for_confirmatory_label"] != base.MIN_CONFIRMATORY_POWER:
            raise ValueError("manifest confirmatory power threshold drift")
        if manifest["design_sensitivity"]["planning_power_seeds"] != DESIGN_SEEDS:
            raise ValueError("manifest planning seed drift")
        if manifest["design_sensitivity"]["confirmatory_claim_enabled"] is not False:
            raise ValueError("manifest confirmatory claim drift")
        if manifest["inference"]["design_seeds"] != DESIGN_SEEDS:
            raise ValueError("manifest design seed drift")
        if manifest["inference"]["inference_seeds"] != INFERENCE_SEEDS:
            raise ValueError("manifest inference seed drift")
        if manifest["inference"]["permutations"] != base.PERMUTATIONS or manifest["inference"]["bootstraps"] != base.BOOTSTRAPS:
            raise ValueError("manifest inference repeat drift")
        if manifest["inference"]["delta_target"] != base.DELTA_TARGET:
            raise ValueError("manifest delta threshold drift")
        if manifest["inference"]["permutation_p_max"] != base.P_MAX:
            raise ValueError("manifest permutation threshold drift")
        if manifest["inference"]["bootstrap_upper_max"] != base.BOOTSTRAP_UPPER_MAX:
            raise ValueError("manifest bootstrap threshold drift")
        if manifest["inference"]["max_lineage_delta"] != base.MAX_LINEAGE_DELTA:
            raise ValueError("manifest lineage threshold drift")
        if not implementation_commit or not isinstance(module, dict):
            raise ValueError("implementation receipt is not bound")
        if module["path"] != EXPECTED_MODULE_PATH:
            raise ValueError("implementation module path drift")
        for commit in (base_commit, implementation_commit):
            resolved = git_command("rev-parse", "--verify", f"{commit}^{{commit}}")
            if resolved.returncode != 0:
                raise ValueError(f"unresolvable commit: {commit}")
        head = git_command("rev-parse", "HEAD")
        if head.returncode != 0:
            raise ValueError("cannot resolve current HEAD")
        for ancestor in (base_commit, implementation_commit):
            relation = git_command("merge-base", "--is-ancestor", ancestor, "HEAD")
            if relation.returncode != 0:
                raise ValueError(f"required commit is not an ancestor: {ancestor}")
        module_path = Path(module["path"])
        if sha256(module_path) != module["sha256"]:
            raise ValueError("implementation module SHA-256 drift")
        if git_blob_sha256(implementation_commit, module["path"]) != module["sha256"]:
            raise ValueError("implementation module commit-content drift")
        lock_path = Path("uv.lock")
        if sha256(lock_path) != manifest["uv_lock_sha256"]:
            raise ValueError("uv.lock SHA-256 drift")
        census = Path(manifest["candidate_census"]["path"])
        if sha256(census) != manifest["candidate_census"]["sha256"]:
            raise ValueError("candidate census SHA-256 drift")
        if manifest["design_sensitivity"]["frozen_label"] != "FEASIBILITY_ONLY":
            raise ValueError("feasibility label drift")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise T0Stop("T0_IMPLEMENTATION_BOUNDARY", False, str(exc)) from exc
    return manifest


def verify_endpoint_input_hash(path: Path) -> None:
    actual = sha256(path)
    if actual != base.EXPECTED_HASHES["endpoint"]:
        raise T0Stop("T0_INPUT_HASH", False, f"endpoint SHA-256 drift: {actual}")


def load_endpoint(
    path: Path, contexts: Sequence[base.Context]
) -> tuple[dict[tuple[str, str], float], dict[str, object]]:
    actual = sha256(path)
    if actual != base.EXPECTED_HASHES["endpoint"]:
        raise T0Stop("T0_ENDPOINT_COMPLETENESS", True, f"endpoint SHA-256 drift: {actual}")
    screen_to_context = {
        screen_id: context
        for context in contexts
        for screen_id in context.screen_ids
    }
    values: dict[tuple[str, str], list[float]] = defaultdict(list)
    seen_screens: set[str] = set()
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            if header is None or not header or header[0] != "":
                raise ValueError("endpoint header drift")
            if header.count(TARGET_COLUMN) != 1:
                raise ValueError(f"missing/duplicate endpoint column: {TARGET_COLUMN}")
            index = header.index(TARGET_COLUMN)
            for row in reader:
                if not row:
                    continue
                screen_id = row[0].strip()
                if screen_id not in screen_to_context:
                    continue
                if screen_id in seen_screens:
                    raise ValueError(f"duplicate endpoint ScreenID: {screen_id}")
                seen_screens.add(screen_id)
                if index >= len(row) or not row[index].strip():
                    continue
                context = screen_to_context[screen_id]
                values[(context.source, context.model_id)].append(
                    base.parse_float(row[index], (screen_id, TARGET_COLUMN))
                )
    except (OSError, ValueError, IntegrityError) as exc:
        raise T0Stop("T0_ENDPOINT_COMPLETENESS", True, str(exc)) from exc

    model_scores: dict[tuple[str, str], float] = {}
    missing = []
    for context in contexts:
        key = (context.source, context.model_id)
        if not values[key]:
            missing.append(key)
        else:
            model_scores[key] = float(median(values[key]))
    if missing:
        raise T0Stop(
            "T0_ENDPOINT_COMPLETENESS",
            True,
            f"endpoint completeness failure: {len(missing)} missing source/model values",
        )
    for source in SOURCES:
        groups = base.grouped_contexts(contexts, source)
        for lineage, by_status in groups.items():
            for status in ("damaging", "intact"):
                if by_status[status] and any(
                    (source, model_id) not in model_scores
                    for model_id in by_status[status]
                ):
                    raise T0Stop(
                        "T0_ENDPOINT_COMPLETENESS",
                        True,
                        f"endpoint group completeness failure: {source}/{lineage}/{status}",
                    )
    return model_scores, {
        "sha256": actual,
        "eligible_screens_seen": len(seen_screens),
        "eligible_screens_expected": len(screen_to_context),
        "model_values": len(model_scores),
        "median_collapse": True,
    }


def write_endpoint_rows(
    path: Path,
    contexts: Sequence[base.Context],
    scores: dict[tuple[str, str], float],
) -> None:
    fields = ["pair_id", "source", "model_id", "lineage", "status", "target_score"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            {
                "pair_id": PAIR_ID,
                "source": context.source,
                "model_id": context.model_id,
                "lineage": context.lineage,
                "status": context.status,
                "target_score": scores[(context.source, context.model_id)],
            }
            for context in contexts
        )


def summary_digest(result: dict[str, object]) -> str:
    return base.summary_digest(result)


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
    base.write_json_atomic(path, payload)


def run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    manifest = verify_implementation_boundary(Path(args.manifest_file))
    verify_endpoint_input_hash(Path(args.endpoint_file))
    try:
        contexts, context_receipt = base.load_context(
            Path(args.qc_file),
            Path(args.screen_map_file),
            Path(args.model_file),
            Path(args.damaging_file),
        )
    except T0Stop:
        raise
    except IntegrityError as exc:
        raise T0Stop(classify_context_stop(exc), False, str(exc)) from exc
    base.write_context_ledger(stage / "context_ledger.csv", contexts)
    context_receipt["context_ledger_sha256"] = sha256(stage / "context_ledger.csv")
    design_rows = []
    for source in SOURCES:
        row = base.design_sensitivity(
            contexts,
            source,
            np.random.default_rng(DESIGN_SEEDS[source]),
        )
        row["pair_id"] = PAIR_ID
        design_rows.append(row)
    base.write_design_rows(stage / "design_sensitivity.csv", design_rows)
    design_receipt = {
        "design_sensitivity_sha256": sha256(stage / "design_sensitivity.csv"),
        "minimum_confirmatory_power": base.MIN_CONFIRMATORY_POWER,
        "frozen_label": "FEASIBILITY_ONLY",
        "confirmatory_claim_enabled": False,
        "all_primary_sources_power_adequate": all(
            row["confirmatory_power_adequate"] for row in design_rows
        ),
    }
    pre_endpoint_payload = {
        "experiment_id": EXPERIMENT_ID,
        "context_ledger_sha256": context_receipt["context_ledger_sha256"],
        "design_sensitivity_sha256": design_receipt["design_sensitivity_sha256"],
    }
    pre_endpoint_receipt = {
        **pre_endpoint_payload,
        "receipt_sha256": hashlib.sha256(
            (json.dumps(pre_endpoint_payload, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "sealed_before_endpoint": True,
    }
    write_json_atomic(Path(args.pre_endpoint_receipt), pre_endpoint_receipt)
    scores, endpoint_receipt = load_endpoint(Path(args.endpoint_file), contexts)
    write_endpoint_rows(stage / "endpoint_scores.csv", contexts, scores)
    results = []
    for source in SOURCES:
        row = base.inference_for(
            contexts,
            scores,
            source,
            np.random.default_rng(INFERENCE_SEEDS[source]),
        )
        row["pair_id"] = PAIR_ID
        results.append(row)
    base.write_inference(stage / "inference.csv", results)
    nominal_pass = all(row["pass"] for row in results)
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "FEASIBILITY_ONLY_NOMINAL_GATES_PASS" if nominal_pass else "FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE",
        "analysis_label": "FEASIBILITY_ONLY",
        "confirmatory_claim": False,
        "analysis_type": "preregistered_source_specific_lineage_stratified_arid1a_keap1_replication",
        "claim_eligibility": {
            "primary_confirmatory": False,
            "design_sensitivity_label": "FEASIBILITY_ONLY",
            "nominal_primary_gates_pass": nominal_pass,
        },
        "context_receipt": context_receipt,
        "design_sensitivity": design_receipt,
        "pre_endpoint_receipt": pre_endpoint_receipt,
        "endpoint_receipt": endpoint_receipt,
        "primary": results,
        "inference_receipt": {
            "design_seeds": DESIGN_SEEDS,
            "inference_seeds": INFERENCE_SEEDS,
            "permutations": base.PERMUTATIONS,
            "bootstraps": base.BOOTSTRAPS,
            "bootstrap_interval": "percentile_95_linear_quantile",
            "unit": "collapsed_source_model_id",
            "cross_source_raw_score_comparison": False,
        },
        "implementation_receipt": {
            "manifest_path": args.manifest_file,
            "required_base_commit": manifest["implementation_boundary"]["required_base_commit"],
            "implementation_commit": manifest["implementation_boundary"]["implementation_commit"],
            "implementation_module": manifest["implementation_boundary"]["implementation_module"],
            "uv_lock_sha256": manifest["uv_lock_sha256"],
        },
        "artifact_receipt_sha256": {
            name: sha256(stage / name)
            for name in ("context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv")
        } | {"summary.json": ""},
        "overall_pass": False,
        "claim_boundary": "matrix-defined damaging ARID1A status association with source-specific KEAP1 dependency in frozen 23Q4 cell-line screen cohorts; no biological independence or clinical claim",
    }
    return result


def validate_staged(stage: Path, result: dict[str, object]) -> None:
    if {path.name for path in stage.iterdir() if path.is_file()} != EXPECTED_RESULT_FILES:
        raise IntegrityError("EXP016 staged file set drift")
    with (stage / "context_ledger.csv").open(newline="", encoding="utf-8") as handle:
        context_rows = list(csv.DictReader(handle))
    if len(context_rows) != sum(base.EXPECTED_SOURCE_MODELS.values()):
        raise IntegrityError("context ledger count drift")
    if len({(row["source"], row["model_id"]) for row in context_rows}) != len(context_rows):
        raise IntegrityError("context ledger identity drift")
    with (stage / "design_sensitivity.csv").open(newline="", encoding="utf-8") as handle:
        design_rows = list(csv.DictReader(handle))
    if len(design_rows) != len(SOURCES) or {row["source"] for row in design_rows} != set(SOURCES):
        raise IntegrityError("design sensitivity receipt drift")
    with (stage / "endpoint_scores.csv").open(newline="", encoding="utf-8") as handle:
        endpoint_rows = list(csv.DictReader(handle))
    if len(endpoint_rows) != sum(base.EXPECTED_SOURCE_MODELS.values()):
        raise IntegrityError("endpoint ledger count drift")
    with (stage / "inference.csv").open(newline="", encoding="utf-8") as handle:
        inference_rows = list(csv.DictReader(handle))
    if len(inference_rows) != len(SOURCES) or {row["source"] for row in inference_rows} != set(SOURCES):
        raise IntegrityError("inference receipt drift")
    if any(row["primary_confirmatory"] != "False" for row in inference_rows):
        raise IntegrityError("feasibility-only CSV claim drift")
    expected_keys = {
        "experiment_id", "status", "analysis_label", "confirmatory_claim", "analysis_type",
        "claim_eligibility", "context_receipt", "design_sensitivity", "pre_endpoint_receipt",
        "endpoint_receipt", "primary", "inference_receipt", "implementation_receipt",
        "artifact_receipt_sha256", "overall_pass", "claim_boundary",
    }
    if set(result) != expected_keys or result["experiment_id"] != EXPERIMENT_ID:
        raise IntegrityError("summary schema drift")
    if result["analysis_label"] != "FEASIBILITY_ONLY" or result["confirmatory_claim"] is not False:
        raise IntegrityError("terminal feasibility label drift")
    if result["overall_pass"] is not False or result["claim_eligibility"]["primary_confirmatory"] is not False:
        raise IntegrityError("terminal confirmatory claim drift")
    if result["pre_endpoint_receipt"]["sealed_before_endpoint"] is not True:
        raise IntegrityError("pre-endpoint receipt seal drift")
    if set(result["artifact_receipt_sha256"]) != EXPECTED_RESULT_FILES:
        raise IntegrityError("artifact receipt key drift")
    for name in EXPECTED_RESULT_FILES - {"summary.json"}:
        if result["artifact_receipt_sha256"][name] != sha256(stage / name):
            raise IntegrityError(f"artifact hash drift: {name}")
    if result["artifact_receipt_sha256"]["summary.json"] != summary_digest(result):
        raise IntegrityError("summary normalized self-digest drift")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv")
    parser.add_argument("--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv")
    parser.add_argument("--screen-map-file", default="data/raw/depmap/23q4/CRISPRScreenMap.csv")
    parser.add_argument("--model-file", default="data/raw/depmap/23q4/Model.csv")
    parser.add_argument("--damaging-file", default="data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv")
    parser.add_argument("--manifest-file", default="experiments/EXP-20260822-016/manifest.json")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-016/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-016/error_receipt.json")
    parser.add_argument("--pre-endpoint-receipt", default="experiments/EXP-20260822-016/pre_endpoint_receipt.json")
    return parser


def publish(args: argparse.Namespace) -> int:
    target = Path(args.results_dir)
    error = Path(args.error_receipt)
    if target.exists():
        write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_RESULTS_DIRECTORY_EXISTS", "results_written": False})
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=target.parent, prefix=f".{target.name}.stage.") as temporary_name:
            stage = Path(temporary_name)
            try:
                result = run(args, stage)
            except T0Stop as exc:
                preserved_path = None
                if any(stage.iterdir()):
                    preserved = target.parent / "t0_provenance"
                    if preserved.exists():
                        raise IntegrityError(f"T0 provenance directory already exists: {preserved}")
                    os.replace(stage, preserved)
                    preserved_path = str(preserved)
                write_json_atomic(error, {
                    "experiment_id": EXPERIMENT_ID,
                    "status": exc.status,
                    "analysis_label": "FEASIBILITY_ONLY",
                    "confirmatory_claim": False,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                    "t0": True,
                    "endpoint_opened": exc.endpoint_opened,
                    "results_written": False,
                    "preserved_path": preserved_path,
                })
                return 2
            result["artifact_receipt_sha256"]["summary.json"] = summary_digest(result)
            (stage / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_staged(stage, result)
            if json.loads((stage / "summary.json").read_text(encoding="utf-8")) != result:
                raise IntegrityError("summary round-trip drift")
            os.replace(stage, target)
    except Exception as exc:
        write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_INTEGRITY", "error": str(exc), "error_type": type(exc).__name__, "results_written": False})
        return 1
    if error.exists():
        error.unlink()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 2


def main() -> None:
    raise SystemExit(publish(build_parser().parse_args()))


if __name__ == "__main__":
    main()
