import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from candrel.tp53_mdm2_replication import (
    Context,
    EXPOSED,
    REFERENCE,
    T0Stop,
    canonical_roster,
    classify_context_stop,
    delta_from_scores,
    grouped_contexts,
    normalized_receipt_sha256,
    permutation_deltas,
    verify_endpoint_hash,
)


def contexts() -> list[Context]:
    return [
        Context("Avana", "m2", "Bowel", ("s2",), EXPOSED, 0),
        Context("Avana", "m1", "Bowel", ("s1",), REFERENCE, 1),
        Context("Avana", "m3", "Lung", ("s3",), EXPOSED, 0),
        Context("Avana", "m4", "Lung", ("s4",), REFERENCE, 2),
    ]


def test_grouping_is_canonical_and_status_explicit():
    groups = grouped_contexts(contexts(), "Avana")
    assert list(groups) == ["Bowel", "Lung"]
    assert groups["Bowel"] == {EXPOSED: ["m2"], REFERENCE: ["m1"]}
    assert groups["Lung"] == {EXPOSED: ["m3"], REFERENCE: ["m4"]}


def test_lower_exposed_scores_have_negative_delta():
    groups = grouped_contexts(contexts(), "Avana")
    delta, lineage_deltas, pair_count = delta_from_scores(
        groups, {"m1": 0.0, "m2": -1.0, "m3": 0.0, "m4": 1.0}
    )
    assert delta == -1.0
    assert lineage_deltas == {"Bowel": -1.0, "Lung": -1.0}
    assert pair_count == 2


def test_permutation_is_seed_reproducible():
    groups = grouped_contexts(contexts(), "Avana")
    scores = {"m1": 0.0, "m2": -1.0, "m3": 0.0, "m4": 1.0}
    first = permutation_deltas(groups, scores, 32, np.random.default_rng(123))
    second = permutation_deltas(groups, scores, 32, np.random.default_rng(123))
    np.testing.assert_array_equal(first, second)


def test_canonical_roster_digest_is_stable():
    roster = canonical_roster(contexts())
    assert hashlib.sha256(roster.encode()).hexdigest() == hashlib.sha256(roster.encode()).hexdigest()
    assert roster.index('"model_id":"m1"') < roster.index('"model_id":"m2"')


def test_endpoint_hash_stop_does_not_open_values(tmp_path: Path):
    endpoint = tmp_path / "endpoint.csv"
    endpoint.write_text("not-the-frozen-endpoint\n", encoding="utf-8")
    with pytest.raises(T0Stop) as caught:
        verify_endpoint_hash(endpoint)
    assert caught.value.status == "T0_INPUT_HASH"
    assert caught.value.endpoint_opened is False


def test_metadata_stop_classifier_preserves_declared_phase():
    assert classify_context_stop(RuntimeError("Model.csv SHA-256 drift")) == "T0_INPUT_HASH"
    assert classify_context_stop(RuntimeError("TP53 matrix header drift")) == "T0_SCHEMA_HEADER"
    assert classify_context_stop(RuntimeError("TP53 matrix coverage drift")) == "T0_MATRIX_COVERAGE"
    assert classify_context_stop(RuntimeError("invalid eligible identity")) == "T0_IDENTITY_JOIN"


def test_normalized_receipt_digest_ignores_self_field(tmp_path: Path):
    receipt = tmp_path / "receipt.json"
    payload = {"receipt_sha256": "placeholder", "value": 7}
    receipt.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    expected = hashlib.sha256(
        (json.dumps({"receipt_sha256": "", "value": 7}, indent=2, sort_keys=True) + "\n").encode()
    ).hexdigest()
    assert normalized_receipt_sha256(receipt, "receipt_sha256") == expected
