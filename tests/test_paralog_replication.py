from __future__ import annotations

import pytest

from candrel.paralog_replication import T0Stop, delta_from_scores, summary_digest


def test_delta_counts_lower_scores_as_negative_and_ties_as_zero() -> None:
    groups = {"Lung": {"damaging": ["d1", "d2"], "intact": ["i1", "i2"]}}
    scores = {"d1": -2.0, "d2": 0.0, "i1": -1.0, "i2": 0.0}
    delta, lineage, pair_count = delta_from_scores(groups, scores)
    assert pair_count == 4
    assert delta == pytest.approx(-0.25)
    assert lineage["Lung"] == pytest.approx(-0.25)


def test_delta_rejects_zero_comparison_population() -> None:
    groups = {"Lung": {"damaging": ["d1"], "intact": []}}
    with pytest.raises(RuntimeError, match="zero pair denominator"):
        delta_from_scores(groups, {"d1": -1.0})


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
