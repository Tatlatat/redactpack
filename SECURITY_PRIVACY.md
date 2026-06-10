# Security And Privacy

Date: 2026-06-10

## Privacy Principles

- RedactPack runs locally.
- RedactPack makes no network calls.
- RedactPack never modifies input files.
- Reports include placeholders and positions, not raw sensitive values or brute-forceable value hashes.
- Manifests and risk reports are review aids, not safety guarantees.
- Symlink files are skipped rather than followed.

## Main Risks

- False negatives can leave sensitive data in output.
- False positives can remove debugging context.
- Custom policies can disable important detectors.
- Reversible mapping files would become sensitive artifacts; MVP does not create them.
- Non-UTF-8 text is decoded with replacement characters.

## Mitigations

- Conservative built-in detector defaults.
- Explicit severity model.
- `--dry-run` mode for review before writing sanitized packages.
- Detection benchmark corpus with measured recall.
- Clear limitations in README and reports.
- Non-zero exit threshold for high-risk findings.

## Dependency Policy

Runtime dependencies are avoided in the MVP. This keeps installation easy and reduces supply-chain risk.

## Secret Handling

Detector findings keep raw values only in process memory during a scan. Raw values and unsalted value hashes are not written to reports.
