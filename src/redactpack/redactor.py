from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, List

from .detectors import RegexDetector, scan_text
from .models import Finding, severity_rank
from .policy import Policy


@dataclass
class RedactionResult:
    text: str
    findings: List[Finding]


def redact_text(text: str, detectors: Iterable[RegexDetector], policy: Policy, file: str = "<text>") -> RedactionResult:
    enabled_detectors = [detector for detector in detectors if policy.is_enabled(detector.spec.id)]
    findings = scan_text(text, enabled_detectors, file=file)
    findings.extend(_custom_literal_findings(text, policy, file))
    findings = [finding for finding in findings if not _is_allowlisted(finding.value, policy)]
    findings = _resolve_overlaps(findings)
    findings = _assign_placeholders(findings)

    redacted = text
    for finding in sorted(findings, key=lambda item: item.start, reverse=True):
        redacted = redacted[: finding.start] + finding.placeholder + redacted[finding.end :]
    return RedactionResult(text=redacted, findings=sorted(findings, key=lambda item: (item.file, item.start, item.end)))


def _custom_literal_findings(text: str, policy: Policy, file: str) -> List[Finding]:
    findings: List[Finding] = []
    for item in policy.custom_literals:
        literal = item["literal"]
        detector = item.get("label", "custom_literal")
        severity = item.get("severity", "medium")
        for match in re.finditer(re.escape(literal), text):
            findings.append(
                Finding(
                    detector=detector,
                    label=detector.replace("_", " ").title(),
                    severity=severity,
                    confidence=1.0,
                    file=file,
                    line=text.count("\n", 0, match.start()) + 1,
                    start=match.start(),
                    end=match.end(),
                    value=literal,
                )
            )
    return findings


def _is_allowlisted(value: str, policy: Policy) -> bool:
    return any(re.search(pattern, value) for pattern in policy.allowlist_patterns)


def _resolve_overlaps(findings: List[Finding]) -> List[Finding]:
    chosen: List[Finding] = []
    for finding in sorted(
        findings,
        key=lambda item: (-severity_rank(item.severity), -(item.end - item.start), item.start, item.detector),
    ):
        if any(_overlaps(finding, existing) for existing in chosen):
            continue
        chosen.append(finding)
    return sorted(chosen, key=lambda item: (item.start, item.end, item.detector))


def _overlaps(left: Finding, right: Finding) -> bool:
    return left.file == right.file and left.start < right.end and right.start < left.end


def _assign_placeholders(findings: List[Finding]) -> List[Finding]:
    counters: dict[str, int] = {}
    by_value: dict[tuple[str, str], str] = {}
    assigned: List[Finding] = []
    for finding in findings:
        key = (finding.detector, finding.value)
        if key not in by_value:
            counters[finding.detector] = counters.get(finding.detector, 0) + 1
            by_value[key] = f"[REDACTED:{finding.detector.upper()}:{counters[finding.detector]}]"
        assigned.append(finding.with_placeholder(by_value[key]))
    return assigned
