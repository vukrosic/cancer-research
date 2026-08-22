from pathlib import Path

import pytest

from candrel.pten_pik3cb_replication import (
    ANALYSIS_EXPOSED,
    ANALYSIS_REFERENCE,
    Context,
    T0Stop,
    classify_context_stop,
    grouped_contexts,
    verify_implementation_boundary,
    verify_endpoint_hash,
)


def test_analysis_groups_use_damaging_as_exposure():
    contexts = [
        Context("Avana", "m1", "Bowel", ("s1",), ANALYSIS_EXPOSED, 1),
        Context("Avana", "m2", "Bowel", ("s2",), ANALYSIS_REFERENCE, 0),
    ]
    groups = grouped_contexts(contexts, "Avana")
    assert groups["Bowel"][ANALYSIS_EXPOSED] == ["m1"]
    assert groups["Bowel"][ANALYSIS_REFERENCE] == ["m2"]


def test_endpoint_hash_stop_is_pre_value(tmp_path: Path):
    endpoint = tmp_path / "endpoint.csv"
    endpoint.write_text("not-frozen\n", encoding="utf-8")
    with pytest.raises(T0Stop) as caught:
        verify_endpoint_hash(endpoint)
    assert caught.value.status == "T0_INPUT_HASH"
    assert caught.value.endpoint_opened is False


def test_matrix_parse_stop_is_matrix_coverage():
    assert classify_context_stop(ValueError("non-numeric value for ('m1', 'PTEN (5728)')")) == "T0_MATRIX_COVERAGE"


def test_manifest_binds_pre_endpoint_implementation_boundary():
    manifest = verify_implementation_boundary(Path("experiments/EXP-20260822-019/manifest.json"))
    assert manifest["claim_contract"] == {"analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "overall_pass": False}
