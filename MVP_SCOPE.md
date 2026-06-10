# MVP Scope

Date: 2026-06-10

## Product Name

RedactPack

## MVP Goal

Create a dependency-light local CLI that sanitizes common diagnostic files and produces a reviewable package.

## In Scope

- CLI command: `redactpack scan INPUT --out OUTPUT`
- Inputs:
  - Plain text logs.
  - JSON files.
  - CSV files.
  - `.env` and common config files.
  - Directories containing supported files.
- Detectors:
  - Email addresses.
  - IPv4 and IPv6 addresses.
  - URLs with query tokens.
  - Bearer tokens.
  - AWS access key IDs.
  - GitHub tokens.
  - Stripe keys.
  - Slack tokens.
  - Generic API keys and long high-entropy tokens.
  - Credit card numbers with Luhn validation.
  - US SSN pattern.
- Outputs:
  - Sanitized files in mirrored directory structure.
  - `redactpack-report.json`.
  - `redactpack-summary.md`.
  - Optional zip archive.
- Configuration:
  - YAML or TOML policy file.
  - Detector enable/disable.
  - Allowlist patterns.
  - Severity threshold for non-zero exit.
- Safety:
  - Never modify original files.
  - No network calls.
  - Clear limitation warnings.

## Out Of Scope For MVP

- GUI.
- SaaS dashboard.
- Ticket-system connectors.
- OCR or image redaction.
- PDFs beyond text extraction.
- NLP name/address detection.
- Automatic upload to vendors.
- Reversible mapping vault.
- Multi-user policy management.

## Why This Scope Is Realistic

The MVP can be built with a small, testable core:

- File walker.
- Type-aware readers/writers.
- Detector registry.
- Redaction engine.
- Report generator.
- CLI wrapper.

It avoids heavy dependencies, accounts, paid APIs, and complex infrastructure.
