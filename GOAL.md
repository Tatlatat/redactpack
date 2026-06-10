# Goal

Date started: 2026-06-10

Build an open-source software project developed through loop engineering, from market research through implementation, QA, documentation, review, and release readiness.

The attached goal requires three mandatory checkpoints:

1. Research and idea selection.
2. Product design and implementation.
3. Final review, hardening, and release readiness.

Each checkpoint must pass internal review and independent external review by Claude Code Team Mode using Claude Fable 5 before the next checkpoint can begin.

## Current Status

STATUS: PASSED_ALL_FABLE_CHECKPOINTS_REMOTE_CI_GATE_REMAINS

Checkpoint 1 passed internal review and external Claude Fable 5 review on 2026-06-10. Claude Code was updated to 2.1.170 and invoked through tmux with `--model fable`; Fable returned PASS with score 7/10. Checkpoint 2 passed Claude Fable 5 re-review on 2026-06-11 with score 8/10 after the required fix loop. Checkpoint 3 passed Claude Fable 5 with score 8/10, and the post-fix re-review confirmed no code-level blockers remain.

Checkpoint 1 external pass conditions that must be satisfied in Checkpoint 2:

- Amend competitor analysis to cover `sos clean`, troubleshoot.sh redactors, and Yelp `detect-secrets`.
- Make trust verification a first-class MVP feature with a detection test corpus, measured recall, dry-run reports, conservative defaults, and an explicit severity model.
- Frame manifests and risk reports as review aids, not safety guarantees.

## Selected Project Idea

Working name: RedactPack

RedactPack is a local-first CLI that turns messy support/debug bundles into sanitized, shareable packages. It scans logs, JSON, CSV, text, config files, and small archives for PII and secrets, writes a redacted output bundle, and generates a reviewable manifest plus risk report so support engineers and small B2B SaaS teams can share diagnostics with vendors, customers, contractors, or AI tools without leaking sensitive data.

## Completion Conditions

The full goal is complete only after:

- A differentiated idea is selected.
- The product is implemented and tested.
- Documentation and release artifacts are complete.
- CI covers macOS, Windows, and Linux.
- Claude Fable 5 approves Checkpoints 1, 2, and 3.

As of this file, all three Claude Fable 5 checkpoint reviews are approved. The remaining release gate is operational: publish the repository and run the configured GitHub Actions matrix green before tagging v0.1.0. This local workspace cannot prove remote Windows/Linux CI execution until that hosted run exists.
