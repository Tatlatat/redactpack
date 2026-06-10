from __future__ import annotations

import json

from .models import ScanReport


def render_json(report: ScanReport) -> str:
    return json.dumps(report.to_safe_dict(), indent=2, sort_keys=True) + "\n"


def render_markdown(report: ScanReport) -> str:
    lines = [
        "# RedactPack Summary",
        "",
        "This report is a review aid, not a safety guarantee.",
        "",
        f"- Input: `{report.input_path}`",
        f"- Output: `{report.output_path}`",
        f"- Dry run: `{str(report.dry_run).lower()}`",
        f"- Findings: `{len(report.findings)}`",
        f"- Skipped files: `{len(report.skipped_files)}`",
        "",
        "## Counts By Severity",
        "",
    ]
    for severity, count in report.counts_by_severity.items():
        lines.append(f"- {severity}: {count}")
    lines.extend(["", "## Counts By Detector", ""])
    if report.counts_by_detector:
        for detector, count in report.counts_by_detector.items():
            lines.append(f"- {detector}: {count}")
    else:
        lines.append("- none: 0")
    lines.extend(["", "## Limitations", ""])
    for limitation in report.limitations:
        lines.append(f"- {limitation}")
    return "\n".join(lines) + "\n"
