# Problem Statement

Date: 2026-06-10

Technical teams need to share diagnostic material to solve customer and production issues, but that material often contains sensitive data. The current choices are bad:

- Manually scrub the files and risk missing secrets or PII.
- Share raw data and accept privacy/security risk.
- Use a cloud DLP or platform-specific redaction tool that may be expensive, unavailable for local bundles, or disallowed for raw customer data.
- Use generic scanners that find issues but do not create a clean shareable package.

## Core Job-To-Be-Done

When I need to share a log/support/debug bundle outside the trusted boundary, I want to locally generate a sanitized package with a redaction report so I can preserve debugging value without leaking sensitive data.

## Non-Goals For MVP

- Perfect PII detection.
- Full enterprise DLP replacement.
- Cloud dashboard.
- Ticket-system integrations.
- OCR/image/PDF deep parsing.
- LLM-based redaction.
- Reversible secret vault by default.

## Acceptance Criteria For The Future MVP

- Runs on macOS, Windows, and Linux.
- Works offline by default.
- Accepts files and directories.
- Produces sanitized outputs without modifying originals.
- Detects common secrets and PII patterns.
- Preserves file structure and debugging context.
- Produces JSON and human-readable reports.
- Exits non-zero when configured severity thresholds are exceeded.
- Has tests, docs, examples, and CI.
