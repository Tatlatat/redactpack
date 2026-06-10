from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


SEVERITIES = ("low", "medium", "high", "critical")


def severity_rank(severity: str) -> int:
    try:
        return SEVERITIES.index(severity)
    except ValueError as exc:
        raise ValueError(f"unknown severity: {severity}") from exc


def severity_meets_threshold(severity: str, threshold: str) -> bool:
    return severity_rank(severity) >= severity_rank(threshold)


@dataclass(frozen=True)
class Finding:
    detector: str
    label: str
    severity: str
    confidence: float
    file: str
    line: int
    start: int
    end: int
    value: str
    placeholder: str = ""

    def with_placeholder(self, placeholder: str) -> "Finding":
        return Finding(
            detector=self.detector,
            label=self.label,
            severity=self.severity,
            confidence=self.confidence,
            file=self.file,
            line=self.line,
            start=self.start,
            end=self.end,
            value=self.value,
            placeholder=placeholder,
        )

    def to_safe_dict(self) -> Dict[str, Any]:
        return {
            "detector": self.detector,
            "label": self.label,
            "severity": self.severity,
            "confidence": self.confidence,
            "file": self.file,
            "line": self.line,
            "start": self.start,
            "end": self.end,
            "placeholder": self.placeholder,
        }


@dataclass(frozen=True)
class DetectorSpec:
    id: str
    label: str
    severity: str
    confidence: float
    description: str


@dataclass
class ScanReport:
    input_path: str
    output_path: str
    dry_run: bool
    findings: List[Finding] = field(default_factory=list)
    skipped_files: List[str] = field(default_factory=list)
    generated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    limitations: List[str] = field(
        default_factory=lambda: [
            "RedactPack reports are review aids, not safety guarantees.",
            "Regex and checksum detectors can miss sensitive data; review sanitized output before sharing.",
        ]
    )

    @property
    def counts_by_detector(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for finding in self.findings:
            counts[finding.detector] = counts.get(finding.detector, 0) + 1
        return dict(sorted(counts.items()))

    @property
    def counts_by_severity(self) -> Dict[str, int]:
        counts = {severity: 0 for severity in SEVERITIES}
        for finding in self.findings:
            counts[finding.severity] += 1
        return counts

    def to_safe_dict(self) -> Dict[str, Any]:
        return {
            "input_path": self.input_path,
            "output_path": self.output_path,
            "dry_run": self.dry_run,
            "generated_at": self.generated_at,
            "counts_by_detector": self.counts_by_detector,
            "counts_by_severity": self.counts_by_severity,
            "skipped_files": self.skipped_files,
            "limitations": self.limitations,
            "findings": [finding.to_safe_dict() for finding in self.findings],
        }


@dataclass
class ScanResult:
    report: ScanReport
    exit_code: int
    zip_path: Optional[Path] = None
