from __future__ import annotations

import json
from pathlib import Path
from importlib import resources
from typing import Any, Dict, List

from .detectors import default_detectors, scan_text


DEFAULT_CORPUS = None


def run_benchmark(corpus_path: str | Path | None = DEFAULT_CORPUS) -> Dict[str, Any]:
    corpus_name, corpus = _load_corpus(corpus_path)
    total = 0
    matched = 0
    missed: List[Dict[str, str]] = []
    by_detector: Dict[str, Dict[str, int]] = {}

    for case in corpus:
        text = _case_text(case)
        found = {finding.detector for finding in scan_text(text, default_detectors(), file=case["name"])}
        for detector in case["expected_detectors"]:
            total += 1
            stats = by_detector.setdefault(detector, {"expected": 0, "matched": 0})
            stats["expected"] += 1
            if detector in found:
                matched += 1
                stats["matched"] += 1
            else:
                missed.append({"case": case["name"], "detector": detector})

    recall_by_detector = {
        detector: (stats["matched"] / stats["expected"] if stats["expected"] else 1.0)
        for detector, stats in sorted(by_detector.items())
    }
    return {
        "corpus": corpus_name,
        "total_expected": total,
        "matched_expected": matched,
        "missed": missed,
        "overall_recall": matched / total if total else 1.0,
        "recall_by_detector": recall_by_detector,
    }


def _load_corpus(corpus_path: str | Path | None) -> tuple[str, List[Dict[str, Any]]]:
    if corpus_path is not None:
        path = Path(corpus_path)
        return str(path), json.loads(path.read_text(encoding="utf-8"))
    with resources.files("redactpack.data").joinpath("corpus.json").open("r", encoding="utf-8") as handle:
        return "redactpack.data/corpus.json", json.load(handle)


def _case_text(case: Dict[str, Any]) -> str:
    if "text" in case:
        return str(case["text"])
    if "text_parts" in case:
        return "".join(str(part) for part in case["text_parts"])
    raise ValueError(f"benchmark case {case.get('name', '<unnamed>')} must define text or text_parts")
