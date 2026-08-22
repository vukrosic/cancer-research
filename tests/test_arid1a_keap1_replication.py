from __future__ import annotations

import csv
import inspect
import json
import subprocess
from pathlib import Path

import pytest

from candrel.arid1a_keap1_replication import (
    Context,
    IntegrityError,
    T0Stop,
    classify_context_stop,
    sha256,
    verify_endpoint_input_hash,
    verify_implementation_boundary,
    write_endpoint_rows,
)
from candrel import arid1a_replication as base


def bound_manifest(tmp_path: Path) -> Path:
    manifest_path = Path("experiments/EXP-20260822-016/manifest.json")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    base_commit = payload["implementation_boundary"]["required_base_commit"]
    implementation_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], check=True, capture_output=True, text=True
    ).stdout.strip()
    module_path = Path("src/candrel/arid1a_keap1_replication.py")
    if subprocess.run(
        ["git", "show", f"{implementation_commit}:{module_path}"],
        check=False,
        capture_output=True,
    ).returncode != 0:
        pytest.skip("EXP016 implementation commit not created yet")
    payload["implementation_boundary"] = {
        "required_base_commit": base_commit,
        "implementation_commit": implementation_commit,
        "implementation_module": {
            "path": str(module_path),
            "sha256": sha256(module_path),
        },
        "verify_uv_lock_sha256": True,
        "verify_manifest_identifiers": True,
    }
    output = tmp_path / "manifest.json"
    output.write_text(json.dumps(payload), encoding="utf-8")
    return output


def test_bound_implementation_manifest_passes_and_threshold_drift_stops(tmp_path) -> None:
    manifest = bound_manifest(tmp_path)
    assert verify_implementation_boundary(manifest)["experiment_id"] == "EXP-20260822-016"
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["inference"]["delta_target"] = -0.99
    manifest.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(T0Stop) as raised:
        verify_implementation_boundary(manifest)
    assert raised.value.status == "T0_IMPLEMENTATION_BOUNDARY"
    assert raised.value.endpoint_opened is False


def test_endpoint_hash_drift_stops_before_endpoint_values(tmp_path) -> None:
    changed = tmp_path / "endpoint.csv"
    changed.write_text("not the frozen endpoint\n", encoding="utf-8")
    with pytest.raises(T0Stop) as raised:
        verify_endpoint_input_hash(changed)
    assert raised.value.status == "T0_INPUT_HASH"
    assert raised.value.endpoint_opened is False


def test_endpoint_scores_remain_source_specific(tmp_path) -> None:
    contexts = [
        Context("Avana", "M1", "Lung", ("S1",), "intact", 0),
        Context("KY", "M1", "Lung", ("S2",), "intact", 0),
    ]
    output = tmp_path / "endpoint_scores.csv"
    write_endpoint_rows(output, contexts, {("Avana", "M1"): -1.0, ("KY", "M1"): -2.0})
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [(row["source"], row["target_score"]) for row in rows] == [
        ("Avana", "-1.0"),
        ("KY", "-2.0"),
    ]


def test_shared_analysis_call_contract_is_explicit() -> None:
    assert list(inspect.signature(base.design_sensitivity).parameters) == [
        "contexts", "source", "rng"
    ]
    assert list(inspect.signature(base.inference_for).parameters) == [
        "contexts", "scores", "source", "rng"
    ]


def test_context_integrity_errors_have_named_t0_stops() -> None:
    assert classify_context_stop(IntegrityError("Model.csv SHA-256 drift")) == "T0_INPUT_HASH"
    assert classify_context_stop(IntegrityError("Model.csv header drift")) == "T0_SCHEMA_HEADER"
    assert classify_context_stop(IntegrityError("duplicate ModelID")) == "T0_MATRIX_COVERAGE"
