from __future__ import annotations

import csv

import pytest

from candrel.arid1a_replication import (
    Context,
    T0Stop,
    delta_from_scores,
    summary_digest,
    write_endpoint_rows,
)


def test_delta_counts_lower_scores_as_negative_and_ties_as_zero() -> None:
    groups = {"Lung": {"damaging": ["d1", "d2"], "intact": ["i1", "i2"]}}
    scores = {"d1": -2.0, "d2": 0.0, "i1": -1.0, "i2": 0.0}
    delta, lineage, pair_count = delta_from_scores(groups, scores)
    assert pair_count == 4
    assert delta == pytest.approx(-0.25)
    assert lineage["Lung"] == pytest.approx(-0.25)


def test_summary_digest_normalizes_self_receipt() -> None:
    result = {"artifact_receipt_sha256": {name: "" for name in {
        "context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv", "summary.json"
    }}}
    digest = summary_digest(result)
    result["artifact_receipt_sha256"]["summary.json"] = digest
    assert summary_digest(result) == digest


def test_t0_stop_preserves_protocol_status_and_endpoint_boundary() -> None:
    context_stop = T0Stop("T0_CONTEXT_ADEQUACY", False, "not enough status groups")
    endpoint_stop = T0Stop("T0_ENDPOINT_COMPLETENESS", True, "missing target score")
    assert context_stop.status == "T0_CONTEXT_ADEQUACY"
    assert context_stop.endpoint_opened is False
    assert endpoint_stop.status == "T0_ENDPOINT_COMPLETENESS"
    assert endpoint_stop.endpoint_opened is True


def test_endpoint_scores_remain_separate_for_same_model_in_each_source(tmp_path) -> None:
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
