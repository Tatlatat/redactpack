# RedactPack

RedactPack is a local-first CLI that turns sensitive logs and support/debug folders into sanitized, reviewable handoff packages.

It is built for support engineers, SREs, MSPs, and developers who need to share diagnostics with vendors, customers, contractors, or AI tools without sending obvious PII and secrets unchanged.

RedactPack reports are review aids, not safety guarantees. Always review sanitized output before sharing.

## Why RedactPack

- Works offline by default.
- Does not modify original files.
- Preserves folder structure in sanitized output.
- Replaces sensitive values with deterministic typed placeholders.
- Writes JSON and Markdown reports without raw sensitive values.
- Includes a benchmark corpus so detector recall can be measured and tracked.
- Avoids runtime dependencies in the MVP.

## Install

From source:

```bash
python -m pip install .
```

For development:

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

After release, the intended install path is:

```bash
pipx install redactpack
```

## Quickstart

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-out
```

Create a zip package:

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-out --zip
```

Dry-run review only:

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-review --dry-run
```

List detectors:

```bash
redactpack detectors
```

Run the published benchmark corpus:

```bash
redactpack benchmark
```

## Policy Example

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-out --policy examples/redactpack.policy.json
```

Policy files are JSON:

```json
{
  "disabled_detectors": ["ipv4"],
  "allowlist": ["example\\.internal"],
  "custom_literals": [
    {
      "literal": "ACME-CUSTOMER-123",
      "label": "customer_id",
      "severity": "medium"
    }
  ],
  "fail_on": "high"
}
```

## Built-In Detectors

- Email addresses.
- IPv4 addresses.
- Bearer tokens.
- AWS access key IDs.
- GitHub tokens.
- Stripe keys.
- Slack tokens.
- Generic API key assignments.
- Credit card numbers with Luhn validation.
- US SSN pattern.
- URLs with sensitive query parameters.

## Exit Codes

- `0`: scan completed and no findings met the configured failure threshold.
- `1`: scan completed and at least one finding met the configured failure threshold.
- `2`: user/configuration error.

Default failure threshold is `critical`.

## Reports

Each scan writes:

- `redactpack-report.json`
- `redactpack-summary.md`

Reports include detector counts, severity counts, skipped files, limitation notes, and finding metadata. They include placeholders and positions, not raw sensitive values or brute-forceable value hashes.

## Limitations

- Regex/checksum detectors can miss sensitive data.
- False positives can remove useful debugging context.
- Binary files are skipped by default.
- Symlinks are skipped by default so scans do not silently include files outside the input tree.
- Output directories must be outside the input directory.
- Non-UTF-8 text is decoded with replacement characters in the MVP.
- The MVP does not redact images, PDFs, screenshots, or OCR content.
- Reports help humans review risk; they do not prove an output is safe.

## Prior Art

RedactPack is ecosystem-neutral. It complements, rather than replaces:

- `sos clean` for sos report obfuscation.
- Replicated troubleshoot.sh redactors for Kubernetes support bundles.
- Yelp detect-secrets, gitleaks, and trufflehog for repository/secret scanning workflows.
- Microsoft Presidio for broad PII detection frameworks.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m redactpack.cli benchmark
```

## License

MIT. See `LICENSE`.
