from __future__ import annotations

from pathlib import Path
import zipfile
from typing import List

from .detectors import default_detectors
from .models import Finding, ScanReport, ScanResult, severity_meets_threshold
from .policy import Policy
from .redactor import redact_text
from .reports import render_json, render_markdown


REPORT_JSON = "redactpack-report.json"
REPORT_MARKDOWN = "redactpack-summary.md"


def scan_path(
    input_path: str | Path,
    output_path: str | Path,
    policy: Policy,
    *,
    dry_run: bool = False,
    make_zip: bool = False,
) -> ScanResult:
    source = Path(input_path)
    output = Path(output_path)
    if not source.exists():
        raise FileNotFoundError(f"input path does not exist: {source}")
    if output.exists() and not output.is_dir():
        raise ValueError(f"output path must be a directory: {output}")
    if source.is_dir() and _is_inside(output, source):
        raise ValueError("output path must be outside the input directory")
    output.mkdir(parents=True, exist_ok=True)

    findings: List[Finding] = []
    skipped: List[str] = []
    for path, relative in _iter_candidates(source):
        if path.is_symlink():
            skipped.append(relative.as_posix())
            continue
        text = _read_text_or_none(path)
        if text is None:
            skipped.append(relative.as_posix())
            continue
        result = redact_text(text, default_detectors(), policy, file=relative.as_posix())
        findings.extend(result.findings)
        if not dry_run:
            destination = output / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(result.text.encode("utf-8"))

    report = ScanReport(
        input_path=_display_path(source),
        output_path=_display_path(output),
        dry_run=dry_run,
        findings=sorted(findings, key=lambda item: (item.file, item.start, item.end, item.detector)),
        skipped_files=sorted(skipped),
    )
    (output / REPORT_JSON).write_text(render_json(report), encoding="utf-8")
    (output / REPORT_MARKDOWN).write_text(render_markdown(report), encoding="utf-8")
    zip_path = _write_zip(output) if make_zip else None
    exit_code = 1 if any(severity_meets_threshold(finding.severity, policy.fail_on) for finding in findings) else 0
    return ScanResult(report=report, exit_code=exit_code, zip_path=zip_path)


def _iter_candidates(source: Path) -> list[tuple[Path, Path]]:
    if source.is_file():
        return [(source, Path(source.name))]
    if source.is_symlink():
        return [(source, Path(source.name))]
    candidates: list[tuple[Path, Path]] = []
    for path in sorted(source.rglob("*")):
        if path.is_symlink() or path.is_file():
            candidates.append((path, path.relative_to(source)))
    return candidates


def _is_inside(candidate: Path, parent: Path) -> bool:
    candidate_resolved = candidate.resolve(strict=False)
    parent_resolved = parent.resolve(strict=False)
    return candidate_resolved == parent_resolved or parent_resolved in candidate_resolved.parents


def _read_text_or_none(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def _write_zip(output: Path) -> Path:
    zip_path = Path(f"{output}.zip")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(output.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(output).as_posix())
    return zip_path


def _display_path(path: Path) -> str:
    return path.name or "."
