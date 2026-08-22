from candrel import pbrm1_arid2_parp1_replication as module


def test_experiment_contract() -> None:
    assert module.EXPERIMENT_ID == "EXP-20260822-039"
    assert module.PAIR_ID == "PBRM1_or_ARID2_damaging_to_PARP1"
    assert module.STATUS_COLUMNS == ("PBRM1 (55193)", "ARID2 (196528)")
    assert module.TARGET_COLUMN == "PARP1 (142)"
    assert module.EXPECTED_STATUS_COUNTS == {
        "Avana": {"damaging": 49, "matrix_intact": 926},
        "KY": {"damaging": 22, "matrix_intact": 293},
    }


def test_composite_loader_is_bound_to_two_columns() -> None:
    assert module.base._load_composite_status_matrix is module._load_composite_status_matrix
    assert module.base.STATUS_LABEL == "PBRM1_or_ARID2_composite"
    assert module.base.load_context is module._load_context
