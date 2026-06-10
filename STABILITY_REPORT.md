# Stability Report

Date: 2026-06-11

## Stable Behaviors Verified

- Detector registry returns expected built-in detectors.
- Redaction uses deterministic typed placeholders.
- Repeated values share placeholders.
- Overlap resolution favors higher severity and longer matches.
- Policy files can disable detectors, allowlist values, define custom literals, and set failure thresholds.
- Invalid policy severity and invalid allowlist regex produce clean errors.
- Non-object policy JSON produces a clean error.
- Directory scans mirror structure.
- Dry-run writes reports but not sanitized files.
- Binary files and symlinks are skipped and reported.
- Unreadable files are skipped and reported.
- Zip packages include sanitized files and reports.
- Output directories inside input directories are rejected.

## Test Evidence

`.venv/bin/python -m pytest tests -v`: 29 passed.

## Known Limits

- Detector coverage is intentionally conservative and incomplete.
- Non-UTF-8 logs may contain replacement characters in sanitized output.
- Very large files are read into memory in MVP.
- OCR, screenshots, images, PDFs, and binary deep inspection are out of scope.

## Stability Verdict

Stable enough for an initial OSS MVP release candidate. External Checkpoint 3 review passed, post-fix re-review passed, and hosted cross-platform CI passed.
