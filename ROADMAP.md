# Roadmap

Date: 2026-06-10

STATUS: PASSED_ALL_FABLE_CHECKPOINTS_REMOTE_CI_GATE_REMAINS

Checkpoint 1 was independently approved by Claude Fable 5 on 2026-06-10. Checkpoint 2 passed Claude Fable 5 re-review on 2026-06-11. Checkpoint 3 passed Claude Fable 5 on 2026-06-11 and post-fix re-review confirmed no code-level blockers remain.

## Phase 0 - Checkpoint 1 External Approval

Completed:

- Send `EXTERNAL_REVIEW_PACKET_CHECKPOINT_1.md` to Claude Fable 5.
- Record the review in `REVIEW_LOG.md`.
- Claude Code was updated to 2.1.170 and invoked through tmux with `--model fable`.
- Fable returned PASS, score 7/10.

Exit criteria:

- Complete.

Fable conditions carried into Checkpoint 2:

- Cover `sos clean`, troubleshoot.sh redactors, and Yelp `detect-secrets`.
- Include a detection test corpus with measured recall.
- Avoid safety-guarantee language around manifests and risk reports.

## Phase 1 - MVP Design

Planned artifacts:

- `PRODUCT_SPEC.md`
- `TECHNICAL_SPEC.md`
- `ARCHITECTURE.md`
- `IMPLEMENTATION_PLAN.md`
- `TEST_PLAN.md`
- `SECURITY_PRIVACY.md`
- `INSTALLATION_PLAN.md`

Core decisions to validate:

- CLI-first product.
- Python package with minimal dependencies.
- Standard-library redaction core where practical.
- No network calls by default.
- Deterministic placeholder generation.
- JSON and Markdown reports.

Exit criteria:

- Checkpoint 2 specs are complete and internally reviewed.

## Phase 2 - MVP Implementation

Planned core modules:

- CLI entrypoint.
- File discovery and input classification.
- Detector registry.
- Redaction engine.
- Policy/config loader.
- Report generator.
- Package writer.

Planned repository assets:

- Source code.
- Tests for core behavior and edge cases.
- README.
- License.
- Contributing guide.
- Security policy.
- Changelog.
- Examples.
- Cross-platform CI for macOS, Windows, and Linux.

Exit criteria:

- Complete. Claude Fable 5 passed Checkpoint 2 at 8/10 after the fix loop.

## Phase 3 - Release Hardening

Planned artifacts:

- `FINAL_REVIEW.md`
- `RELEASE_CHECKLIST.md`
- `CROSS_PLATFORM_REPORT.md`
- `STABILITY_REPORT.md`
- `PERFORMANCE_NOTES.md`
- `USER_GUIDE.md`
- `FINAL_SUMMARY.md`
- `CHECKPOINT_3_INTERNAL_REVIEW.md`

Verification:

- Install instructions for macOS, Windows, and Linux.
- Fresh install workflow.
- Example workflow.
- Failure-mode documentation.
- Performance notes for expected file sizes.
- Security/privacy review.

Exit criteria:

- Complete for local/code readiness.
- Remaining pre-tag gate: publish the repository and run the GitHub Actions matrix green on Ubuntu/macOS/Windows.
