# Decisions

Date: 2026-06-10

## D001 - Select RedactPack As The OSS Project Idea

Decision:

Build RedactPack, a local-first support/debug bundle sanitizer for logs, configs, tickets, text, JSON, CSV, and small archives.

Why:

- The pain is practical and repeated: support engineers, DevOps teams, MSPs, and small B2B SaaS teams often need to share logs or diagnostic bundles while avoiding PII, API keys, tokens, customer data, IPs, and account identifiers.
- Public evidence shows active concern around PII/secrets in logs, including Hacker News discussions on secrets in arbitrary strings and Reddit posts from developers building or asking for tools to strip PII/secrets before debugging or AI use.
- Commercial products validate willingness to pay for redaction and privacy workflows, but many are tied to SaaS platforms or cloud DLP rather than a simple local handoff package.
- Existing OSS is strong in adjacent layers but not exactly this workflow:
  - Presidio is a broad PII framework.
  - gitleaks and trufflehog are strong secret scanners, especially for repositories.
  - scrubadub is a PII text-cleaning library.
  - ScrubDuck is close, but RedactPack can differentiate with package-oriented output, manifest-first review, policy files, deterministic CI mode, and support handoff ergonomics.

Alternatives rejected:

- DMARC report analyzer: useful, but existing OSS such as parsedmarc and newer single-binary tools already cover much of the space.
- OpenAPI breaking-change checker: useful, but strong current alternatives exist and the market is more developer-tool saturated.
- PDF bank statement parser: real pain, but bank-specific parsing and financial-data correctness create a broad, brittle MVP.
- Security questionnaire answer assistant: high willingness to pay, but credible MVP needs knowledge-base integrations and LLM workflows that add scope and trust risk.

Evidence:

- Microsoft Presidio: https://github.com/microsoft/presidio
- Zendesk ADPP redaction: https://support.zendesk.com/hc/en-us/articles/9248330321050-Automatically-redacting-sensitive-information-in-tickets-using-triggers
- HN discussion on secrets in logs: https://news.ycombinator.com/item?id=45160774
- Reddit ScrubDuck post: https://www.reddit.com/r/devops/comments/1q6oe42/i_built_a_cli_tool_to_strip_piisecrets_from/
- Reddit observability thread: https://www.reddit.com/r/Observability/comments/1ovz7xt/how_do_you_handle_sensitive_data_in_your_logs_and/

## D002 - Keep MVP Dependency-Light

Decision:

The future MVP should start as a Python CLI using the standard library plus a minimal CLI/test stack, with deterministic regex/checksum detectors first and optional integrations later.

Why:

- Local-first privacy tooling should be easy to inspect and install.
- Heavy NLP dependencies would complicate cross-platform packaging.
- Regex/checksum/key-pattern detectors are enough to deliver practical first value for support bundles.

Rejected:

- Starting with Presidio as a core dependency: powerful but heavy for the lightweight MVP.
- Starting with an LLM redaction workflow: introduces privacy concerns and paid API requirements.

## D003 - Stop Before Checkpoint 2 Until External Review Passes

Decision:

Do not write implementation code yet.

Why:

- The attached goal explicitly says to start with Checkpoint 1 and not write code yet.
- The checkpoint system forbids moving to Checkpoint 2 before Claude Fable 5 passes Checkpoint 1.
- Claude Fable 5 is unavailable in this environment.
