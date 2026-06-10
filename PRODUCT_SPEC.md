# Product Spec

Date: 2026-06-10

Product: RedactPack

## One-Line Description

RedactPack is a local-first CLI that turns sensitive logs and support/debug folders into sanitized, reviewable handoff packages.

## Target Users

- B2B SaaS support engineers.
- DevOps/SRE teams escalating issues to vendors.
- MSPs handling client diagnostics.
- Developers preparing logs and config snippets for AI debugging.

## Core Workflow

1. User runs `redactpack scan INPUT --out OUTPUT`.
2. RedactPack walks files without modifying originals.
3. RedactPack detects common secrets and PII using conservative local detectors.
4. RedactPack writes a mirrored sanitized output directory.
5. RedactPack writes `redactpack-report.json` and `redactpack-summary.md`.
6. If `--zip` is passed, RedactPack creates a sanitized zip package.
7. If findings at or above `--fail-on` severity are found, RedactPack exits non-zero.

## Main Features

- Offline scanning by default.
- File and directory input.
- Deterministic typed placeholders, for example `[REDACTED:EMAIL:1]`.
- Built-in detectors for emails, IP addresses, URLs with sensitive query fields, bearer tokens, AWS keys, GitHub tokens, Stripe keys, Slack tokens, generic API keys, high-entropy tokens, credit cards with Luhn validation, and US SSNs.
- Policy file for detector toggles, allowlist regexes, custom literal redactions, and severity threshold.
- Dry-run mode that produces reports without writing sanitized files.
- Detection benchmark command with a published local corpus and measured recall.
- JSON and Markdown reports framed as review aids, never safety guarantees.

## Non-Goals

- No SaaS dashboard.
- No network calls.
- No LLM redaction.
- No OCR or image redaction in MVP.
- No reversible raw-value vault in MVP.
- No claim of complete sanitization.
- No dependency on Kubernetes, RHEL/sos, git repositories, or a ticket system.

## MVP Boundary

The MVP must be useful as a small CLI. It does not need a GUI or integrations. Quality is measured by deterministic behavior, clear reports, good tests, cross-platform packaging, and honest limitation language.

## Fable 5 Binding Conditions

- Competitor analysis must cover `sos clean`, troubleshoot.sh redactors, and Yelp `detect-secrets`.
- Trust verification must be product behavior: benchmark corpus, measured recall, dry-run reports, conservative defaults, and severity model.
- Manifests and risk reports must be described as review aids, not guarantees.
