# Rejected Ideas

Date: 2026-06-10

## DMARC Report Analyzer

Rejected because parsedmarc already provides a mature Python CLI/module and self-hosted alternative to commercial DMARC processors. Newer tools also target lightweight single-binary DMARC dashboards. Differentiation would be hard without building a broad email-security product.

Evidence:

- parsedmarc docs: https://domainaware.github.io/parsedmarc/

## OpenAPI Breaking-Change Reviewer

Rejected despite real pain. Optic being archived creates churn, but active alternatives such as openapi-changes and oasdiff already cover the core CLI/CI workflow. Differentiation would require a more ambitious product than this goal should start with.

Evidence:

- openapi-changes: https://github.com/pb33f/openapi-changes
- Optic migration discussion: https://specshield.io/blog/optic-is-dead-migration-guide

## PDF Bank Statement Parser

Rejected because the pain is real but the MVP is brittle. Bank PDF formats vary, correctness requirements are high, and many recent OSS projects already target this niche.

Evidence:

- Bank Statement Parser: https://github.com/sebastienrousseau/bankstatementparser
- Singapore bank parser Reddit post: https://www.reddit.com/r/singaporefi/comments/1ephb6v/i_built_a_bank_statement_parser_for_singapore/

## Security Questionnaire Assistant

Rejected for MVP scope. The market is attractive and willingness to pay is high, but useful implementation requires knowledge-base ingestion, source-of-truth governance, security review UX, and often AI. Commercial products are already strong.

Evidence:

- HyperComply: https://www.hypercomply.com/questionnaire-automation
- Conveyor comparison pages and security questionnaire automation market content show a crowded commercial space.

## Docker Compose / Env Drift Auditor

Rejected because the pain is plausible but weaker and less urgent. Many linters and security scanners already exist, and willingness to pay is less clear.

## Stripe Webhook Contract Tester

Rejected because the niche is too narrow and Stripe CLI already addresses much of the local workflow.

## Incident Evidence Pack Builder

Rejected because scope can explode into forensics, chain of custody, timeline generation, and compliance reporting. It may become a future adjacent product, but it is not the best first OSS wedge.

## Data Retention Map Generator

Rejected because the problem is valuable but vague. A credible MVP would require integrations with SaaS apps, databases, and policy workflows.

## SQLite/Postgres Restore Drill Verifier

Not selected but kept as runner-up. The idea is practical and less saturated, but RedactPack has clearer public pain evidence and a stronger local-first privacy reason.
