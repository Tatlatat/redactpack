from pathlib import Path

from redactpack.benchmark import run_benchmark
from redactpack.detectors import default_detectors


def test_benchmark_corpus_measures_recall():
    result = run_benchmark(Path(__file__).parent / "fixtures" / "corpus.json")

    expected_detector_ids = {detector.spec.id for detector in default_detectors()}
    assert set(result["recall_by_detector"]) == expected_detector_ids
    assert result["matched_expected"] == result["total_expected"]
    assert result["overall_recall"] == 1.0
    assert result["missed"] == []


def test_benchmark_default_corpus_works_outside_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    result = run_benchmark()

    expected_detector_ids = {detector.spec.id for detector in default_detectors()}
    assert set(result["recall_by_detector"]) == expected_detector_ids
    assert result["overall_recall"] == 1.0
