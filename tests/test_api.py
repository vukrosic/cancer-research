import hashlib
import json

import pytest

from candrel.api import ApiError, CachedApi


def test_cached_input_must_match_receipt(tmp_path):
    target = tmp_path / "locked.json"
    target.write_text(json.dumps({"data": [1]}, sort_keys=True))
    expected = hashlib.sha256(target.read_bytes()).hexdigest()
    api = CachedApi(tmp_path, expected_hashes={"locked.json": expected})
    payload, observed_path = api.get("/unused", {}, "locked")
    assert payload == {"data": [1]}
    assert observed_path == target


def test_cached_input_drift_stops_run(tmp_path):
    (tmp_path / "locked.json").write_text("{}")
    api = CachedApi(tmp_path, expected_hashes={"locked.json": "0" * 64})
    with pytest.raises(ApiError, match="Input drift"):
        api.get("/unused", {}, "locked")
