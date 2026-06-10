from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Dict, List, Sequence, Set

from .models import SEVERITIES


@dataclass(frozen=True)
class Policy:
    disabled_detectors: Set[str] = field(default_factory=set)
    allowlist_patterns: List[str] = field(default_factory=list)
    custom_literals: List[Dict[str, str]] = field(default_factory=list)
    fail_on: str = "critical"

    @classmethod
    def default(
        cls,
        *,
        disabled_detectors: Sequence[str] | None = None,
        allowlist: Sequence[str] | None = None,
        custom_literals: Sequence[Dict[str, str]] | None = None,
        fail_on: str = "critical",
    ) -> "Policy":
        _validate_severity(fail_on, "fail_on")
        _validate_allowlist(allowlist or [])
        return cls(
            disabled_detectors=set(disabled_detectors or []),
            allowlist_patterns=list(allowlist or []),
            custom_literals=list(custom_literals or []),
            fail_on=fail_on,
        )

    def is_enabled(self, detector_id: str) -> bool:
        return detector_id not in self.disabled_detectors


def load_policy(path: str | Path | None) -> Policy:
    if path is None:
        return Policy.default()
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("policy file must be a JSON object")
    fail_on = data.get("fail_on", "critical")
    _validate_severity(fail_on, "fail_on")
    custom_literals = data.get("custom_literals", [])
    for index, item in enumerate(custom_literals):
        severity = item.get("severity", "medium")
        _validate_severity(severity, f"custom_literals[{index}].severity")
        if not item.get("literal"):
            raise ValueError(f"custom_literals[{index}].literal must be non-empty")
    return Policy.default(
        disabled_detectors=data.get("disabled_detectors", []),
        allowlist=data.get("allowlist", []),
        custom_literals=custom_literals,
        fail_on=fail_on,
    )


def _validate_severity(value: str, field_name: str) -> None:
    if value not in SEVERITIES:
        raise ValueError(f"{field_name} must be one of {', '.join(SEVERITIES)}")


def _validate_allowlist(patterns: Sequence[str]) -> None:
    for index, pattern in enumerate(patterns):
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"allowlist[{index}] is not a valid regex: {exc}") from exc
