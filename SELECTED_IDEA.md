# Selected Idea

Date: 2026-06-10

## Working Name

RedactPack

## One-Line Description

A local-first CLI that turns sensitive logs and support/debug bundles into sanitized packages with review-aid reports for human approval before sharing.

## Target Users

- Support engineers at B2B SaaS companies.
- DevOps and SRE teams escalating issues to vendors.
- MSPs handling client logs and configs.
- Small regulated teams that need to share diagnostics without leaking PII or secrets.
- Developers preparing log context for AI debugging tools.

## Problem

Teams need to share diagnostic files quickly, but logs and support bundles often contain emails, names, IPs, tokens, API keys, account IDs, internal hostnames, URLs with secrets, stack traces, and customer data. Manual scrubbing is slow and unreliable. Cloud DLP tools may be too expensive, too platform-specific, or unacceptable for sensitive local files.

## Product Wedge

Support handoff package, not generic PII detection.

The MVP creates a sanitized output package and a reviewable manifest:

- Preserve directory/file structure.
- Replace sensitive values with typed placeholders.
- Produce a review-aid risk report and redaction counts.
- Allow custom policy rules.
- Run fully offline.

## OSS Advantage

Users can inspect the detectors, run locally, extend policies for their own data formats, and integrate the tool into scripts without sending raw logs to a vendor.

## Why Users Care

- Avoid accidental leakage of customer data and secrets.
- Reduce time spent manually scrubbing logs.
- Keep debugging value by preserving structure and typed placeholders.
- Provide an artifact showing what was redacted.
- Fit into vendor escalation and AI debugging workflows.

## Why Companies Might Pay Around This Problem

- Compliance obligations and customer contracts often require safe handling of sensitive support data.
- A leak through support logs can cause incident response, customer trust loss, and audit findings.
- Commercial products already sell support redaction, DLP, and compliance automation.
- Paid opportunities could include hosted policy management, team reporting, enterprise detectors, signed binaries, support, or integrations while keeping the core OSS local-first.

## Long-Term Potential

RedactPack can grow into a respected OSS project for privacy-preserving support workflows:

- CLI MVP.
- HTML review reports.
- Pre-send hooks for support tooling.
- GitHub Action / CI mode.
- Optional local web review UI.
- Policy packs for common vendors and frameworks.
- Enterprise extensions for team policy distribution and audit trails.
