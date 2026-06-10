# Security Policy

## Supported Versions

RedactPack is pre-1.0. Security fixes target the latest unreleased main branch until the first tagged release.

## Reporting A Vulnerability

Open a private security advisory in the hosting platform if available. If private advisories are unavailable, open a public issue with minimal detail and offer to share sensitive reproduction data privately.

Do not include real secrets, customer data, or unredacted logs in public issues.

## Security Model

RedactPack is a local review aid. It does not guarantee that output is safe to share.

Expected behavior:

- No network calls during scans.
- Input files are not modified.
- Reports do not contain raw sensitive values or unsalted value hashes.
- Raw values are kept only in process memory during a scan.
- Symlink files are skipped rather than followed.

Known limitations:

- Detectors can miss sensitive data.
- Binary, image, and PDF content are not deeply inspected in the MVP.
- Custom policies can disable important protection.
