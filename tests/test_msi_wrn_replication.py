import argparse
import csv
import hashlib
from pathlib import Path

import numpy as np
import pytest

from candrel.msi_wrn_replication import (
    IntegrityError,
    EligibleScreen,
    ModelScore,
    bootstrap_interval,
    evaluate_source,
    extract_endpoint,
    file_digest,
    pair_delta,
    run,
    sequential_effect_evaluation,
    stratified_delta,
    verify_input_hashes,
)
import candrel.msi_wrn_replication as replication


def _rows(strong: bool = True) -> list[ModelScore]:
    rows = []
    for tissue_index, tissue in enumerate(
        ("Large Intestine", "Ovary", "Endometrium", "Stomach")
    ):
        for label, values in (
            ("MSI", [-2.0, -1.8] if strong else [-1.0, 0.0]),
            ("MSS", [-0.2, 0.0] if strong else [-1.0, 0.0]),
        ):
            for index, value in enumerate(values):
                rows.append(
                    ModelScore(
                        model_id=f"ACH-{tissue_index}{label}{index}",
                        model_name=f"M{tissue_index}{label}{index}",
                        tissue=tissue,
                        label=label,
                        library="Avana",
                        screen_ids=f"SC-{tissue_index}{label}{index}",
                        score=value,
                    )
                )
    return rows


def test_pair_delta_direction() -> None:
    delta, differences = pair_delta(np.array([-2.0, -1.0]), np.array([0.0, 1.0]))
    assert delta == -1.0
    assert np.all(differences < 0)


def test_stratified_delta_excludes_cross_tissue_pairs() -> None:
    delta, by_tissue, shift = stratified_delta(_rows(strong=True))
    assert delta == -1.0
    assert set(by_tissue) == {"Large Intestine", "Ovary", "Endometrium", "Stomach"}
    assert all(value == -1.0 for value in by_tissue.values())
    assert shift < 0


def test_strong_synthetic_source_passes() -> None:
    result = evaluate_source(_rows(strong=True), "Avana", 200, 200, 17)
    assert result["pass"] is True
    assert result["stratified_delta"] == -1.0
    assert result["permutation_p_one_sided"] <= 0.05


def test_null_synthetic_source_fails() -> None:
    result = evaluate_source(_rows(strong=False), "Avana", 200, 200, 17)
    assert result["pass"] is False
    assert result["stratified_delta"] == 0.0


def test_bootstrap_is_seed_deterministic() -> None:
    first = bootstrap_interval(_rows(), 50, np.random.default_rng(5))
    second = bootstrap_interval(_rows(), 50, np.random.default_rng(5))
    assert first == second


def test_extract_endpoint_requires_exact_unique_column(tmp_path: Path) -> None:
    path = tmp_path / "scores.csv"
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["", "WRN (7486)", "OTHER (1)"])
        writer.writerow(["SC-1", "-1.5", "0"])
    assert extract_endpoint(path) == {"SC-1": -1.5}

    bad = tmp_path / "bad.csv"
    bad.write_text(",OTHER (1)\nSC-1,0\n")
    with pytest.raises(IntegrityError):
        extract_endpoint(bad)


def test_file_digest_known_fixture(tmp_path: Path) -> None:
    path = tmp_path / "fixture.txt"
    path.write_bytes(b"candrel\n")
    assert file_digest(path, "sha256") == (
        "6300681d1b4c542e234371c2b5a434dd883deddad5bc7800d83f1cfd52af1932"
    )


def test_discovery_failure_never_calls_confirmation_loader() -> None:
    called = False

    def forbidden_loader():
        nonlocal called
        called = True
        raise AssertionError("confirmation loader must remain sealed")

    discovery, confirmation, emitted = sequential_effect_evaluation(
        _rows(strong=False), forbidden_loader, 200, 200, 17
    )
    assert discovery["pass"] is False
    assert confirmation is None
    assert called is False
    assert all(row.library == "Avana" for row in emitted)


def test_verify_input_hashes_covers_every_frozen_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = {}
    expected_sha = {}
    for name in ("qc_file", "sequence_map_file", "model_file", "msi_file"):
        path = tmp_path / f"{name}.csv"
        path.write_bytes(f"{name}\n".encode())
        paths[name] = str(path)
        expected_sha[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    score = tmp_path / "scores.csv"
    score.write_bytes(b"score\n")
    monkeypatch.setattr(replication, "EXPECTED_SCORE_MD5", hashlib.md5(b"score\n").hexdigest())
    monkeypatch.setattr(replication, "EXPECTED_METADATA_SHA256", expected_sha)
    args = argparse.Namespace(score_file=str(score), **paths)
    receipt = verify_input_hashes(args)
    assert set(receipt) == {
        "score_file_md5",
        "qc_file_sha256",
        "sequence_map_file_sha256",
        "model_file_sha256",
        "msi_file_sha256",
    }


def test_run_discovery_failure_never_extracts_ky(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    eligible = []
    for library in ("Avana", "KY"):
        for tissue_index, tissue in enumerate(
            ("Large Intestine", "Ovary", "Endometrium", "Stomach")
        ):
            for label in ("MSI", "MSS"):
                for index in range(2):
                    token = f"{library}-{tissue_index}-{label}-{index}"
                    eligible.append(
                        EligibleScreen(
                            screen_id=f"SC-{token}",
                            model_id=f"ACH-{token}",
                            model_name=token,
                            tissue=tissue,
                            label=label,
                            library=library,
                            qc_status="PASS",
                        )
                    )
    extraction_calls = []

    def fake_extract(_path, column="WRN (7486)", include_screen_ids=None):
        extraction_calls.append(set(include_screen_ids))
        return {screen_id: 0.0 for screen_id in include_screen_ids}

    monkeypatch.setattr(replication, "verify_input_hashes", lambda _args: {"ok": "ok"})
    monkeypatch.setattr(replication, "load_eligible_screens", lambda *_args: eligible)
    monkeypatch.setattr(replication, "extract_endpoint", fake_extract)
    args = argparse.Namespace(
        score_file=str(tmp_path / "unused.csv"),
        qc_file="unused",
        model_file="unused",
        msi_file="unused",
        sequence_map_file="unused",
        model_output=str(tmp_path / "models.csv"),
        permutations=20,
        bootstraps=20,
        seed=7,
    )
    result = run(args)
    assert result["status"] == "FAIL_DISCOVERY"
    assert result["confirmation"] is None
    assert len(extraction_calls) == 1
    assert all("Avana" in screen_id for screen_id in extraction_calls[0])
