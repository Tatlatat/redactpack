from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Callable, Iterable, List, Pattern
from urllib.parse import parse_qsl, urlsplit

from .models import DetectorSpec, Finding


Validator = Callable[[str], bool]


@dataclass(frozen=True)
class RegexDetector:
    spec: DetectorSpec
    pattern: Pattern[str]
    validator: Validator | None = None
    group: int = 0

    def scan(self, text: str, file: str) -> Iterable[Finding]:
        for match in self.pattern.finditer(text):
            value = match.group(self.group)
            if self.validator and not self.validator(value):
                continue
            start, end = match.span(self.group)
            yield Finding(
                detector=self.spec.id,
                label=self.spec.label,
                severity=self.spec.severity,
                confidence=self.spec.confidence,
                file=file,
                line=_line_number(text, start),
                start=start,
                end=end,
                value=value,
            )


def default_detectors() -> List[RegexDetector]:
    return [
        RegexDetector(
            DetectorSpec("email", "Email address", "medium", 0.95, "Email address"),
            re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        ),
        RegexDetector(
            DetectorSpec("ipv4", "IPv4 address", "medium", 0.85, "IPv4 address"),
            re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
            validator=_valid_ipv4,
        ),
        RegexDetector(
            DetectorSpec("bearer_token", "Bearer token", "critical", 0.98, "Authorization bearer token"),
            re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/=-]{20,}\b"),
        ),
        RegexDetector(
            DetectorSpec("aws_access_key", "AWS access key id", "critical", 0.98, "AWS access key id"),
            re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        ),
        RegexDetector(
            DetectorSpec("github_token", "GitHub token", "critical", 0.97, "GitHub personal access token"),
            re.compile(r"\bgithub_(?:pat|oauth|app)_[A-Za-z0-9_]{20,}\b"),
        ),
        RegexDetector(
            DetectorSpec("stripe_key", "Stripe key", "critical", 0.98, "Stripe API key"),
            re.compile(r"\b[rs]k_(?:live|test)_[A-Za-z0-9]{16,}\b"),
        ),
        RegexDetector(
            DetectorSpec("slack_token", "Slack token", "critical", 0.95, "Slack token"),
            re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
        ),
        RegexDetector(
            DetectorSpec("generic_api_key", "Generic API key assignment", "critical", 0.75, "Generic key assignment"),
            re.compile(r"(?i)\b(?:api[_-]?key|token|secret|password)\b\s*[:=]\s*[\"']?([A-Za-z0-9_./+=-]{20,})[\"']?"),
            group=1,
        ),
        RegexDetector(
            DetectorSpec("credit_card", "Credit card number", "high", 0.90, "Credit card number passing Luhn check"),
            re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
            validator=_valid_luhn,
        ),
        RegexDetector(
            DetectorSpec("us_ssn", "US Social Security number", "high", 0.85, "US SSN pattern"),
            re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        ),
        RegexDetector(
            DetectorSpec("url_sensitive_query", "URL with sensitive query", "critical", 0.86, "URL containing sensitive query parameter"),
            re.compile(r"https?://[^\s\"'<>]+"),
            validator=_url_has_sensitive_query,
        ),
    ]


def scan_text(text: str, detectors: Iterable[RegexDetector], file: str = "<text>") -> List[Finding]:
    findings: List[Finding] = []
    for detector in detectors:
        findings.extend(detector.scan(text, file))
    return sorted(findings, key=lambda finding: (finding.start, finding.end, finding.detector))


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _valid_ipv4(value: str) -> bool:
    return all(0 <= int(part) <= 255 for part in value.split("."))


def _valid_luhn(value: str) -> bool:
    digits = [int(ch) for ch in value if ch.isdigit()]
    if len(digits) < 13:
        return False
    checksum = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


def _url_has_sensitive_query(value: str) -> bool:
    sensitive_names = {"token", "api_key", "apikey", "key", "secret", "password", "access_token"}
    try:
        query = parse_qsl(urlsplit(value).query, keep_blank_values=True)
    except ValueError:
        return False
    return any(name.lower() in sensitive_names and bool(param_value) for name, param_value in query)
