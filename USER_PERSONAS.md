# User Personas

Date: 2026-06-10

## Persona 1 - B2B SaaS Support Engineer

Name: Maya

Context:

Maya handles technical escalations for a small SaaS product. Customers send logs and exports. Maya often needs to forward a bundle to engineering, a cloud provider, or an AI assistant.

Pain:

- Logs include customer emails, account IDs, URLs, bearer tokens, and internal hostnames.
- Manual review is slow and inconsistent.
- She needs to preserve enough context for debugging.

Success:

- Run one command on a support bundle.
- Get a sanitized zip and an HTML/JSON report.
- Share the result with confidence.

## Persona 2 - DevOps Engineer Escalating Vendor Issues

Name: Andre

Context:

Andre runs infrastructure for a 40-person company. When a vendor asks for logs, he needs to package config files and service logs.

Pain:

- Vendor support wants raw diagnostic bundles.
- Configs may include API keys or credentials.
- Cloud upload to a redaction SaaS is not allowed.

Success:

- Redact locally.
- Fail the package if high-risk secrets remain.
- Keep a manifest for internal audit.

## Persona 3 - Managed Service Provider

Name: Linh

Context:

Linh supports multiple clients and routinely collects logs from client machines.

Pain:

- Each client has different sensitive identifiers.
- A mistake could violate client trust.
- She needs repeatable policies across technicians.

Success:

- Use a shared policy file.
- Generate client-safe packages.
- Keep a clear record of redaction counts and risk.

## Persona 4 - Developer Using AI Debugging

Name: Sam

Context:

Sam wants to paste stack traces, logs, and config snippets into an AI assistant.

Pain:

- It is easy to miss a token or customer email.
- Existing secret scanners do not produce a clean sanitized prompt file.

Success:

- Pipe a file or paste text through the tool.
- Get deterministic placeholders.
- Copy the sanitized output into an AI tool.
