# Idea Scorecard

Date: 2026-06-10

Scoring: 1 to 5. Pass requires average >= 4.0, real user pain >= 4, differentiation >= 4, OSS suitability >= 4, technical feasibility >= 4, and low saturation >= 3.

| Idea | Pain | Market | OSS Fit | Self-Install | Differentiation | Feasibility | MVP Clarity | Long-Term | Pay | Low Saturation | Avg | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| RedactPack: local support/debug bundle sanitizer | 5 | 4 | 5 | 5 | 4 | 5 | 5 | 4 | 4 | 3 | 4.4 | SELECT |
| Restore drill verifier for small databases | 4 | 4 | 4 | 5 | 4 | 4 | 4 | 4 | 4 | 4 | 4.1 | Runner-up |
| OpenAPI breaking-change reviewer | 4 | 4 | 4 | 5 | 3 | 4 | 4 | 4 | 4 | 2 | 3.8 | Reject: crowded |
| Docker Compose/env drift auditor | 3 | 4 | 4 | 5 | 3 | 5 | 4 | 3 | 3 | 3 | 3.7 | Reject: weaker pain |
| Data retention map generator | 4 | 4 | 4 | 4 | 3 | 4 | 3 | 4 | 4 | 3 | 3.7 | Reject: vague MVP |
| DMARC report analyzer | 4 | 4 | 4 | 4 | 2 | 4 | 4 | 3 | 3 | 2 | 3.4 | Reject: saturated |
| PDF bank-statement parser | 4 | 4 | 4 | 5 | 3 | 2 | 3 | 4 | 4 | 3 | 3.6 | Reject: brittle MVP |
| Security questionnaire assistant | 5 | 5 | 3 | 3 | 3 | 2 | 2 | 5 | 5 | 2 | 3.5 | Reject: broad and crowded |
| Stripe webhook contract tester | 3 | 3 | 4 | 5 | 3 | 4 | 4 | 3 | 3 | 3 | 3.5 | Reject: narrow |
| Incident evidence pack builder | 4 | 4 | 4 | 4 | 3 | 2 | 2 | 4 | 4 | 3 | 3.4 | Reject: scope risk |

## Selected Candidate Pass Check

RedactPack:

- Average score: 4.4
- Real user pain: 5
- Differentiation: 4
- OSS suitability: 5
- Technical feasibility: 5
- Low saturation: 3

Result: PASS internal score threshold.

## Why RedactPack Won

RedactPack has the best combination of painful workflow, local-first need, small MVP, cross-platform feasibility, and commercial validation. Its risk is saturation in general PII/secret scanning, but the support handoff package wedge is specific enough to defend.
