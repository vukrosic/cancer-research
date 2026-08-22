import numpy as np

from candrel.smoke import evaluate_gates, paired_scores, summarize


def record(model: str, source: str, score: float, qc: bool = True) -> dict:
    return {
        "attributes": {"source": source, "fc_clean_qn": score, "qc_pass": qc},
        "relationships": {"model": {"data": {"id": model}}},
    }


def test_paired_scores_uses_only_qc_paired_sources_and_median_duplicates():
    records = [
        record("M1", "Broad", -1.0),
        record("M1", "Broad", -0.8),
        record("M1", "Sanger", -0.7),
        record("M2", "Broad", 0.1),
        record("M3", "Broad", 0.2, qc=False),
        record("M3", "Sanger", 0.2),
    ]
    broad, sanger = paired_scores(records)
    assert np.allclose(broad, [-0.9])
    assert np.allclose(sanger, [-0.7])


def test_summary_detects_monotonic_signal():
    broad = np.linspace(-2, 1, 120)
    sanger = broad * 0.8 + np.sin(np.arange(120)) * 0.01
    result = summarize("TEST", broad, sanger, 7, repeats=50)
    assert result["eligible"] is True
    assert result["spearman_rho"] > 0.99
    assert result["permutation_p_one_sided"] < 0.05
    assert sum(result["threshold_contingency_counts"].values()) == len(broad)


def test_aggregate_gates_are_exactly_locked():
    genes = [
        {"eligible": True, "spearman_rho": value}
        for value in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    ]
    aggregate, gates = evaluate_gates(genes)
    assert aggregate["median_spearman"] == 0.35
    assert all(gates.values())
