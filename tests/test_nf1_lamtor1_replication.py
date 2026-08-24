from candrel import nf1_lamtor1_replication as module


def test_experiment_contract() -> None:
    assert module.EXPERIMENT_ID == "EXP-20260822-040"
    assert module.PAIR_ID == "NF1_damaging_to_LAMTOR1"
    assert module.STATUS_COLUMN == "NF1 (4763)"
    assert module.TARGET_COLUMN == "LAMTOR1 (55004)"
    assert module.EXPECTED_STATUS_COUNTS == {
        "Avana": {"damaging": 57, "matrix_intact": 918},
        "KY": {"damaging": 21, "matrix_intact": 294},
    }


def test_screen_map_contract_uses_frozen_digest() -> None:
    assert module.EXPECTED_HASHES["screen_map"] == "1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad"
