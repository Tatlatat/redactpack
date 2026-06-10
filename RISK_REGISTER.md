# Risk Register

Date: 2026-06-10

| ID | Risk | Likelihood | Impact | Mitigation | Status |
| --- | --- | --- | --- | --- | --- |
| R001 | Existing tools already solve enough of the problem. | Medium | High | Keep RedactPack focused on support handoff bundles, review manifests, risk reports, and deterministic package outputs rather than generic PII detection. | Open |
| R002 | False negatives could cause users to leak sensitive data. | High | High | Treat trust verification as product behavior: conservative defaults, dry-run risk reports, explicit severity model, detection corpus with measured recall, checksum validation, high-signal detectors, and clear "review aid, not safety guarantee" language. | Open |
| R003 | False positives could make sanitized logs useless for debugging. | Medium | Medium | Use typed placeholders, deterministic IDs, preserve structure, and support allow rules. | Open |
| R004 | Cross-platform packaging could become fragile. | Medium | Medium | Prefer Python standard library, CLI-first design, no native dependencies in MVP, CI matrix for macOS/Windows/Linux later. | Open |
| R005 | Optional reversible mapping could create a sensitive local vault. | Medium | High | Make reversible mode opt-in, encrypt or avoid storing raw values in MVP, and clearly separate non-reversible default mode. | Open |
| R006 | The market may see the product as a feature rather than standalone tool. | Medium | Medium | Target pre-send workflows for support, vendor escalation, contractor handoff, and AI debugging where a standalone local tool has natural value. | Open |
| R007 | Claude Fable 5 external review is unavailable through native Codex tool discovery. | Medium | High | Use Claude Code through tmux with `--model fable` after updating Claude Code to 2.1.170+. | Mitigated for Checkpoint 1 |
| R008 | Prior art in support-bundle ecosystems weakens differentiation. | Medium | High | Position RedactPack as general-purpose and ecosystem-neutral; explicitly compare against `sos clean`, troubleshoot.sh redactors, and detect-secrets in docs and specs. | Open |
