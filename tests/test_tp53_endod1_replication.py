from pathlib import Path

import pytest

from candrel import arid1a_atr_replication as template
from candrel import tp53_mdm2_replication as engine
from candrel.tp53_endod1_replication import ANALYSIS_EXPOSED, ANALYSIS_REFERENCE, Context, T0Stop, TARGET_COLUMN, grouped_contexts, verify_endpoint_hash


def test_analysis_groups_use_endod1_labels():
    contexts = [Context("Avana", "m1", "Bowel", ("s1",), ANALYSIS_EXPOSED, 1), Context("Avana", "m2", "Bowel", ("s2",), ANALYSIS_REFERENCE, 0)]
    groups = grouped_contexts(contexts, "Avana")
    assert groups["Bowel"][ANALYSIS_EXPOSED] == ["m1"]
    assert groups["Bowel"][ANALYSIS_REFERENCE] == ["m2"]


def test_wrapper_restores_template_globals():
    before = (template.EXPERIMENT_ID, template.PAIR_ID, template.STATUS_COLUMN, template.TARGET_COLUMN)
    grouped_contexts([], "Avana")
    assert (template.EXPERIMENT_ID, template.PAIR_ID, template.STATUS_COLUMN, template.TARGET_COLUMN) == before


def test_configuration_restores_engine_globals():
    before = (engine.EXPERIMENT_ID, engine.PAIR_ID, engine.STATUS_COLUMN, engine.TARGET_COLUMN)
    grouped_contexts([], "Avana")
    assert (engine.EXPERIMENT_ID, engine.PAIR_ID, engine.STATUS_COLUMN, engine.TARGET_COLUMN) == before


def test_endpoint_hash_stop_is_pre_value(tmp_path: Path):
    endpoint = tmp_path / "endpoint.csv"
    endpoint.write_text("not-frozen\n", encoding="utf-8")
    with pytest.raises(T0Stop) as caught:
        verify_endpoint_hash(endpoint)
    assert caught.value.status == "T0_INPUT_HASH"
    assert caught.value.endpoint_opened is False


def test_endod1_target_is_bound_in_module():
    assert TARGET_COLUMN == "ENDOD1 (23052)"
