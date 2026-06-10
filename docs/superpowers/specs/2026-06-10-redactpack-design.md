# RedactPack Design

Date: 2026-06-10

User instruction: proceed autonomously and do not ask follow-up questions.

## Approved Direction

Build RedactPack as a local-first, dependency-light Python CLI for sanitizing support/debug bundles. This is the selected Checkpoint 1 idea and Claude Fable 5 approved it with a score of 7/10.

## Design

RedactPack scans files and directories, applies deterministic detectors and redaction, writes a mirrored sanitized output, and emits JSON/Markdown reports. Reports are always review aids, never safety guarantees.

The CLI supports `scan`, `detectors`, and `benchmark`. The benchmark command runs a published corpus and reports recall to make trust verification a first-class product feature.

## Architecture

- `models`: typed data model.
- `detectors`: built-in detector registry.
- `redactor`: deterministic placeholder and overlap logic.
- `policy`: JSON policy loader.
- `scanner`: filesystem orchestration.
- `reports`: JSON and Markdown renderers.
- `benchmark`: detection corpus metrics.
- `cli`: argparse interface.

## Fable 5 Conditions

- Add direct prior art for `sos clean`, troubleshoot.sh redactors, and detect-secrets.
- Publish a benchmark corpus and measured recall.
- Avoid safety-guarantee language.

## Self-Review

No placeholders remain. Scope is a single CLI MVP. The architecture matches the product spec and Checkpoint 2 artifacts.
