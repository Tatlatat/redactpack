# Review Log

Date: 2026-06-10

## Checkpoint 1 Internal Review

Reviewer: Codex self-review

STATUS: PASSED_INTERNAL_REVIEW

Summary:

The selected idea, RedactPack, is strong enough for external review. It targets a specific operational pain: preparing logs and debug bundles for safe sharing. The niche is credible, self-installation is natural because raw diagnostic data is sensitive, and commercial redaction/DLP products validate willingness to pay. The primary risk is adjacency to existing OSS and a newer close project, so differentiation must remain focused on support handoff packages, review manifests, risk reports, deterministic policies, and local-first operation.

Artifacts reviewed:

- `MARKET_RESEARCH.md`
- `COMPETITOR_ANALYSIS.md`
- `IDEA_SCORECARD.md`
- `SELECTED_IDEA.md`
- `USER_PERSONAS.md`
- `PROBLEM_STATEMENT.md`
- `MVP_SCOPE.md`
- `REJECTED_IDEAS.md`
- `CHECKPOINT_1_INTERNAL_REVIEW.md`

## Checkpoint 1 External Review Attempt

Reviewer required: Claude Code Team Mode using Claude Fable 5

STATUS: BLOCKED_EXTERNAL_REVIEW_UNAVAILABLE

Finding:

Claude Code Team Mode / Claude Fable 5 is not available in the current environment. Tool discovery exposed GPT-based multi-agent tools and installable plugins such as GitHub, Slack, Drive, and OpenAI Developers, but no Claude Fable 5 tool or plugin.

Second availability check:

On the continuation turn, tool discovery again exposed automation and GPT multi-agent tools, but no Claude Code Team Mode or Claude Fable 5 reviewer. This repeats the same external-review blocker.

Required manual action:

Send `EXTERNAL_REVIEW_PACKET_CHECKPOINT_1.md` to Claude Fable 5 manually.

Exact prompt:

```text
You are Claude Fable 5 acting as an independent OSS product strategy reviewer.

Review Checkpoint 1 for this AI-developed OSS project.

Evaluate:
1. Is the selected idea strong?
2. Is there evidence of real users?
3. Does it solve a painful practical problem?
4. Is the target user specific enough?
5. Is the niche large enough?
6. Is the market already saturated?
7. Is the differentiation clear?
8. Is OSS a good distribution model for this?
9. Is self-installation realistic?
10. Is there long-term potential?

You must be strict.

Return:
- PASS or FAIL.
- A score from 1 to 10.
- The strongest reasons for your decision.
- The biggest risks.
- Required changes if FAIL.

Only pass the checkpoint if the idea is genuinely strong, differentiated, useful, and feasible.
```

## Checkpoint 1 External Review

Date: 2026-06-10

Reviewer: Claude Fable 5 (independent OSS product strategy review)

STATUS: PASS

Score: 7 / 10

Summary:

RedactPack passes Checkpoint 1. The problem is real, recurring, and
high-consequence; local-first OSS is structurally the right distribution
model; the support-handoff-package wedge is correctly framed; and the MVP
scope is disciplined and feasible. The pass carries three binding
conditions for Checkpoint 2: (1) amend the competitor analysis to cover
missed prior art (sos `clean`, troubleshoot.sh redactors, detect-secrets)
and reposition as ecosystem-neutral; (2) make trust verification a
first-class MVP feature with a published detection test corpus and measured
recall as a Checkpoint 2 deliverable; (3) frame manifests and risk reports
as review aids, never safety guarantees.

Full review: `EXTERNAL_REVIEW_CHECKPOINT_1_RESULT.md`

## Checkpoint 2 Internal Review

Date: 2026-06-10

Reviewer: Codex self-review

STATUS: PASSED_INTERNAL_REVIEW

Summary:

RedactPack MVP is implemented and internally verified. The implementation uses no runtime dependencies, has separated modules, includes a packaged detection benchmark corpus, writes review-aid reports without raw sensitive values, and provides docs/examples/CI/release assets required by Checkpoint 2. Fable 5's Checkpoint 1 binding conditions have been addressed.

Verification:

- `.venv/bin/python -m pytest tests -v`: 20 passed.
- Fresh install with `python -m pip install .`: passed.
- Installed CLI benchmark from `/tmp`: passed and used packaged corpus.
- Sample scan with zip output: passed, exit 1 as expected because critical findings met the default threshold.

## Checkpoint 2 External Review

Date: 2026-06-11

Reviewer: Claude Fable 5 (independent external review)

STATUS: FAILED_EXTERNAL_REVIEW

Verdict: FAIL. Score: 6/10.

Summary:

The implementation is architecturally clean, dependency-free, well
documented, and installs and runs correctly (verified in a fresh venv:
20/20 tests pass, benchmark works outside the repo via packaged corpus,
sample scan produces correct sanitized output with no raw values in
reports). The FAIL rests on two trust-path defects and one test-plan
violation, all empirically verified:

1. CRITICAL: Policy file `fail_on` is silently ignored — the CLI's
   `--fail-on` default ("critical") always overwrites it (`cli.py:21-27`).
   A documented README feature; policy `{"fail_on": "low"}` exits 0 where
   `--fail-on low` exits 1 on identical input.
2. CRITICAL: The shareable zip's JSON report contains unsalted SHA-256
   `value_hash` fingerprints of every redacted value; low-entropy PII
   (SSNs, credit cards, emails) is recoverable by offline brute force.
3. Benchmark corpus omits `generic_api_key`, violating TEST_PLAN's
   "every MVP detector" requirement (10 labels vs 11 detectors).
4. Invalid allowlist regex in a policy crashes with a raw traceback
   instead of the clean exit-2 error path.

Required changes: fix fail_on precedence (CLI default None, policy honored,
regression test); remove/salt value hashes in shared artifacts; complete
the corpus and tighten the benchmark test; validate allowlist regexes at
load. Recommended improvements and full evidence are recorded in the result
file. Re-review expected to pass once the four required changes land.

Full review: `EXTERNAL_REVIEW_CHECKPOINT_2_RESULT.md`

## Checkpoint 2 Fix Loop After External FAIL

Date: 2026-06-11

Reviewer: Codex implementation loop

STATUS: READY_FOR_EXTERNAL_REVIEW_AFTER_FIXES

Summary:

All four required changes from Claude Fable 5's Checkpoint 2 FAIL were implemented and verified.

Fixes:

- `fail_on` policy precedence fixed; CLI default is now `None`, policy value is honored unless the flag is explicitly supplied.
- `value_hash` removed from report output; reports include placeholders/positions but not raw values or unsalted hashes.
- `generic_api_key` added to both benchmark corpora; tests now require every built-in detector to appear in recall metrics.
- Allowlist regexes are validated at policy load time and invalid regexes return clean exit code 2.

Verification:

- `.venv/bin/python -m pytest tests -v`: 22 passed.
- Fresh installed CLI benchmark from `/tmp`: 11/11 expected labels, overall recall 1.0.
- Policy `{"fail_on":"low"}` with an email finding exits 1.
- Invalid allowlist regex exits 2 with a clean message.
- Sample zip report contains no `value_hash` and no raw sample secrets.

## Checkpoint 2 External Re-Review

Date: 2026-06-11

Reviewer: Claude Fable 5 (independent senior OSS engineering review)

STATUS: PASS

Score: 8/10

Summary:

All four required changes from the Checkpoint 2 FAIL are complete, correct,
and empirically verified. No new blockers were found.

1. `fail_on` precedence fixed: `--fail-on` defaults to `None`; policy file
   thresholds are honored when the flag is omitted, CLI flag overrides when
   given. Verified with a four-scenario exit-code matrix plus the new
   regression test `test_cli_honors_policy_fail_on_when_flag_is_omitted`.
2. `value_hash` removed from all report output; zip artifact verified free
   of value hashes and raw sample values; docs updated; unit regression
   test in place.
3. `generic_api_key` added to both corpora (byte-identical files); the
   benchmark test now requires every built-in detector in
   `recall_by_detector`; installed benchmark from `/tmp` reports 11/11
   labels at recall 1.0. The CWD-dependent corpus fallback was also removed.
4. Allowlist regexes are validated at policy load; invalid patterns exit 2
   with a clean message (no traceback), with a regression test.

Verification: 22/22 tests pass; fresh-venv install and installed-CLI smoke
test pass; compileall and 3.9 AST checks pass; CHANGELOG.md updated as
required. Carried-over non-critical items (dead `remove_output`,
CWD-relative test fixture path, dotted-dir zip naming, limitations doc
gaps, small benchmark corpus) remain non-blocking and are listed in the
result file for the next checkpoint's triage.

Full review: `EXTERNAL_REVIEW_CHECKPOINT_2_REREVIEW_RESULT.md`

## Checkpoint 3 Internal Review

Date: 2026-06-11

Reviewer: Codex self-review

STATUS: PASSED_INTERNAL_REVIEW

Summary:

Final hardening completed and release-readiness artifacts prepared. Local verification passed: 28 tests, compileall, Python 3.9 AST parse, fresh install, packaged benchmark, sample scan with zip, zipped report leak/path check, unreadable-file skip-and-report, and non-object policy clean error. Cross-platform CI matrix is configured but not remotely executed from this local workspace.

Full review: `CHECKPOINT_3_INTERNAL_REVIEW.md`

## Checkpoint 3 External Review

Date: 2026-06-11

Reviewer: Claude Fable 5 (independent OSS release readiness review)

STATUS: PASS

Verdict: PASS. Score: 8/10. Binding pre-tag conditions apply.

Summary:

All internal verification claims reproduced independently: 25/25 tests,
compileall and 3.9 AST checks, fresh-venv install, installed benchmark
from `/tmp` (11 detectors, recall 1.0), sample scan with policy and zip
(all seeded secrets plus custom literal redacted), zip leak check clean
(no raw values, no `value_hash`), four-scenario `fail_on` matrix correct,
and a 9.6 MB performance probe at 1.5 s. The Checkpoint 2 carried-over
hardening items (dead `remove_output`, dotted-dir zip naming,
output-inside-input guard, symlink skipping, README/SECURITY doc gaps)
are verified fixed with regression tests.

Adversarial probing found two ungraceful crash paths (no data leaks):
an unreadable file inside a bundle raises an unhandled `PermissionError`
traceback and leaves partial output without reports; a policy file
containing valid JSON of non-object shape (e.g. `[]`) raises an unhandled
`AttributeError` traceback. Also noted: `tests/test_benchmark.py:8` still
fails when pytest runs outside the repo root (carried item not fixed),
and shareable reports embed absolute local input paths (username
disclosure in a privacy tool).

Binding pre-tag conditions: do not tag v0.1.0 until (1) the GitHub
Actions matrix is green on the published repository (the workspace is not
yet a git repo; Windows/Linux remain design-verified only), (2) the
unreadable-file crash is fixed as skip-and-report with a regression test,
and (3) non-object policy JSON is rejected with a clean exit 2 and a
regression test.

Full review: `EXTERNAL_REVIEW_CHECKPOINT_3_RESULT.md`

## Checkpoint 3 Post-Fix Re-Review

Date: 2026-06-11

Reviewer: Claude Fable 5 (independent post-condition re-review)

STATUS: PASS

Summary:

Both code pre-tag conditions of the Checkpoint 3 PASS are verified
fixed. (1) Unreadable files now route through the existing
skip-and-report path (`scanner.py` `_read_text_or_none` catches
`OSError`); reproduced with real `chmod 000` files in a bundle and as
direct input — exit 0, reports written, file listed in `skipped_files`;
regression test passes. (2) Non-object policy JSON (`[]`, string,
number) now exits 2 with a clean "policy file must be a JSON object"
message and no traceback; two regression tests pass. Report path
privacy (defect 4) is also fixed: reports carry basenames via
`_display_path`, and a zip-member grep found no absolute paths or
username. Defect 3 (CWD-relative test fixture) fixed as well — 28/28
tests pass from `/tmp` and from repo root; compileall and 3.9 AST checks
pass. Remaining release blocker: pre-tag condition 1 only — the
workspace is still not a git repository, so the CI matrix
(ubuntu/macos/windows × 3.9/3.12) has not run; do not tag v0.1.0 until
it is green on the published repository.

Full review: `EXTERNAL_REVIEW_CHECKPOINT_3_POSTFIX_RESULT.md`

## Hosted CI Release Gate

Date: 2026-06-11

Reviewer: GitHub Actions hosted matrix

STATUS: PASS

Summary:

The public repository was published at `https://github.com/Tatlatat/redactpack`. GitHub Actions run `27295074259` passed on commit `720577c1d436eefffb3b39aa76acf92557461374` across Ubuntu, macOS, and Windows for Python 3.9 and 3.12. Each job installed the package, ran the test suite, and ran the packaged benchmark.

Full run: `https://github.com/Tatlatat/redactpack/actions/runs/27295074259`
