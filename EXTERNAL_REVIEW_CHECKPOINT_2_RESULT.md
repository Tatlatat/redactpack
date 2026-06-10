# External Review Result - Checkpoint 2

Date: 2026-06-11

Reviewer: Claude Fable 5 (independent senior OSS engineering review)

Scope: Full Checkpoint 2 packet — all listed memory/research docs, specs,
repository assets, source, tests, fixtures, examples, CI, and release files.
Verification was performed empirically in a fresh virtual environment.

## Verdict

FAIL

## Score

6/10

This is a near-pass. The architecture, code style, documentation honesty,
and installation experience are genuinely good. The FAIL rests on two
defects that sit directly in the product's core trust path — the same trust
path that Checkpoint 1 made a binding condition — plus a verifiable
violation of the project's own TEST_PLAN. All required changes are small
and well-scoped; this should pass quickly on re-review once fixed.

## Verification Performed

All commands run against a fresh venv (`python3 -m venv`, Python 3.14.4):

- `pip install ".[dev]"` from repo root: succeeded.
- `python -m pytest tests -q`: 20 passed in 0.04s.
- `redactpack benchmark` from `/tmp` (outside repo): used packaged
  `redactpack.data/corpus.json`, overall recall 1.0, 10 expected labels.
- `redactpack detectors`: lists 11 detectors.
- `redactpack scan examples/sample-bundle --out ... --zip`: exit 1 as
  expected (critical findings at default threshold); sanitized files,
  JSON/Markdown reports, and zip all produced correctly.
- Leak check: grep for all raw sample values (email, AWS key, Stripe key,
  bearer token, `secret123`) across the entire output directory: no raw
  values present in sanitized files or reports.
- Scan with `examples/redactpack.policy.json`: custom literal
  `ACME-CUSTOMER-123` correctly redacted as `[REDACTED:CUSTOMER_ID:1]`;
  allowlist honored.
- Dry-run: reports written, no sanitized files, exit 1 on critical finding.
- Error handling: missing input exits 2 with a clean message; invalid
  `fail_on` in policy exits 2 with a clean message.
- AST parse of all sources with `feature_version=(3,9)`: OK (3.9 syntax
  compatibility plausible; not executed on a real 3.9 interpreter locally —
  CI matrix covers it).
- Targeted bug probes (see Critical Issues): policy `fail_on` precedence
  and invalid allowlist regex.

## Criteria Assessment

| # | Criterion | Assessment |
| --- | --- | --- |
| 1 | Code quality | Good. Small, typed, idiomatic modules; one real CLI logic bug. |
| 2 | Architecture | Good. Pure core, thin CLI, clean separation exactly as documented. |
| 3 | Maintainability | Good. ~670 LOC source, focused tests, clear contribution path. |
| 4 | Simplicity | Very good. No framework, no abstraction tax. |
| 5 | Dependency choices | Excellent. Zero runtime deps; pytest dev-only. |
| 6 | Test quality | Good but with gaps. 20 meaningful tests; missing CLI-level fail_on/policy precedence test; corpus missing one detector. |
| 7 | Documentation quality | Good. Honest limitations, review-aid framing consistent; README documents a policy feature that does not work (see C1). |
| 8 | Installation experience | Very good. Fresh install verified; entry point and packaged data work outside repo. |
| 9 | Runtime usability | Good. Clear output, sensible exit codes, dry-run, zip; one ungraceful crash path. |
| 10 | Solves intended problem | Yes, for the MVP definition — with the trust-path caveats below. |

## Critical Issues

### C1. Policy file `fail_on` is silently ignored by the CLI

`src/redactpack/cli.py:21-27`: after loading a policy, the code rebuilds it
with `fail_on=args.fail_on` whenever `args.policy and args.fail_on` is
truthy. Because `--fail-on` has `default="critical"` (`cli.py:62-67`),
`args.fail_on` is always truthy, so the CLI default always overwrites the
policy file's `fail_on` — even when the user never passed `--fail-on`.

Empirically verified: a policy of `{"fail_on": "low"}` scanning a file
containing one email (medium severity) exits 0; the identical scan with
`--fail-on low` on the CLI exits 1. The README's Policy Example documents
`"fail_on": "high"` in policy JSON as a supported feature; it has no
effect.

Why this is critical rather than cosmetic: exit-code gating is the
enforcement mechanism this tool offers for CI and scripted workflows, and
the severity model was part of Checkpoint 1's binding condition to make
trust verification first-class. A user who encodes a stricter threshold in
a shared team policy file silently gets `critical` instead — the failure
mode is silent under-enforcement of a documented control. Unit tests cover
`load_policy` parsing `fail_on` correctly, but no test exercises the CLI
path, which is exactly where it breaks.

### C2. Shareable zip contains unsalted SHA-256 fingerprints of every redacted value

`src/redactpack/models.py:24-25, 55-67`: `Finding.to_safe_dict()` emits
`value_hash = sha256(value)` for every finding, this lands in
`redactpack-report.json`, and `scanner._write_zip` packages that report
into the zip the product positions as the sanitized artifact to share
(verified: the produced zip contains the JSON report with 7 `value_hash`
entries for the sample bundle).

Unsalted hashes of low-entropy values are recoverable by offline brute
force: the US SSN space is ~10^9, credit card numbers are Luhn- and
BIN-constrained, and emails fall to dictionary attacks. For these PII
classes the report partially undoes the redaction in the very artifact the
recipient gets. The hash is also unnecessary for its apparent purpose —
correlation of repeated values is already provided by deterministic
placeholders (`[REDACTED:EMAIL:1]`).

This does not match the project's own security model ("Raw values are kept
only in process memory during a scan" — SECURITY.md): a brute-forceable
fingerprint is a partial persistence of the value.

## Non-Critical Issues

1. **Benchmark corpus violates TEST_PLAN.** TEST_PLAN.md requires the
   corpus to "include labeled examples for every MVP detector."
   `generic_api_key` has no corpus case: the benchmark reports 10
   detectors, `redactpack detectors` lists 11. The corpus test asserts
   only `total_expected >= 8`, so the gap is invisible to CI. The internal
   review's claim that binding condition 2 is fully met is therefore
   slightly overstated.
2. **Invalid allowlist regex crashes with a raw traceback.** A policy with
   `"allowlist": ["[unclosed"]` produces an unhandled `re.PatternError`
   traceback mid-scan instead of the clean exit-2 path used for other
   policy errors. Allowlist patterns are not validated at load time
   (`policy.py:39-56`; failure occurs later in `redactor._is_allowlisted`).
3. **Benchmark default corpus resolution is CWD-dependent.**
   `benchmark._load_corpus` checks `Path("tests/fixtures/corpus.json")`
   relative to the current working directory before falling back to
   packaged data. An installed CLI run from any directory that happens to
   contain `tests/fixtures/corpus.json` (the user's own project) silently
   benchmarks against the wrong file.
4. **Dead code.** `scanner.remove_output` (`scanner.py:94-97`) is never
   used, imported, or tested, and wraps `shutil.rmtree` of an arbitrary
   path.
5. **False positive on version strings.** `version 1.2.3.4` is redacted as
   an IPv4 address (verified). Acceptable regex tradeoff and generically
   covered by the limitations section, but worth a concrete README example
   plus the `disabled_detectors`/allowlist remedy.
6. **Whole-file reads and lossy non-UTF-8 handling.** `_read_text_or_none`
   reads entire files into memory and decodes non-UTF-8 text with
   `errors="replace"`, silently mojibake-ing legacy-encoded logs in the
   sanitized output. Fine for MVP; should be listed in Limitations.
7. **Zip naming edge case.** `output.with_suffix(".zip")` mangles output
   directories containing dots (`out.v1` becomes `out.zip`).
8. **No guard against `--out` inside the input directory.** No data-loss
   today because the file listing is snapshotted before writes, but the
   interaction is unspecified and untested.
9. **Symlinks are followed silently** during traversal, so a bundle
   containing a symlink can pull in files from outside the input tree
   (they do get sanitized, but inclusion may surprise users).
10. **Benchmark is near-tautological.** Four cases, ten labels, all
    mirroring the unit-test strings; recall 1.0 is guaranteed by
    construction. No negative cases, no precision signal. Acceptable as a
    regression harness for the MVP, but it should not be presented as a
    meaningful quality metric until the corpus grows.
11. **`tests/test_benchmark.py` uses a CWD-relative fixture path**, which
    breaks if pytest is invoked from outside the repo root.
12. **Minor duplication.** Line-number computation exists in
    `detectors._line_number` and inline in
    `redactor._custom_literal_findings`.

## Required Changes (to convert FAIL to PASS)

1. **Fix `fail_on` precedence (C1).** Make `--fail-on` default to `None`;
   apply CLI value only when explicitly provided, otherwise honor the
   policy file, otherwise default to `critical`. Add a CLI-level
   regression test: policy `{"fail_on": "low"}` with a medium-severity
   finding must exit 1 without any `--fail-on` flag.
2. **Stop shipping brute-forceable fingerprints (C2).** Either remove
   `value_hash` from reports (placeholders already correlate repeats), or
   replace it with an HMAC keyed by a random per-run salt that is not
   stored in the output, or exclude the JSON findings detail from the zip
   by default. Document the chosen behavior in SECURITY.md and add a test
   asserting the shared artifact contains no unsalted value hashes.
3. **Complete the corpus per TEST_PLAN.** Add a `generic_api_key` case to
   both `tests/fixtures/corpus.json` and `src/redactpack/data/corpus.json`,
   and strengthen the benchmark test to assert every built-in detector id
   appears in `recall_by_detector`.
4. **Validate allowlist regexes at policy load** and route failures
   through the existing clean exit-2 error path, with a test.

## Recommended Improvements (non-blocking)

- Remove `scanner.remove_output` or wire it to a real code path with tests.
- Make benchmark default-corpus resolution explicit: prefer packaged data
  unless a path is passed; drop the CWD-relative repo fallback (point the
  repo's own CI/tests at the fixture path explicitly instead).
- Add Limitations entries for non-UTF-8 lossy decoding and symlink
  traversal; consider a `--no-follow-symlinks` default in a future release.
- Guard or document `--out` inside the input tree; fix `with_suffix(".zip")`
  for dotted directory names (append `.zip` instead).
- Grow the corpus beyond unit-test mirrors: real-world log shapes, negative
  cases, and a precision metric alongside recall.
- Use `importlib.resources` consistently and stream large files or cap file
  size with a skip-and-report behavior.

## What Is Genuinely Good

- Module boundaries match ARCHITECTURE.md exactly; the redaction core is
  pure and the CLI is a thin layer, which made this review easy to verify.
- Zero runtime dependencies, ~670 LOC of source, fast tests — the
  lightweight claim is real, not aspirational.
- Deterministic typed placeholders with stable numbering are well designed
  and well tested.
- Overlap resolution (severity-then-length) is correct and deterministic.
- Review-aid framing (Checkpoint 1 binding condition 3) is consistent
  across README, reports, SECURITY.md, and report text — verified in the
  generated artifacts themselves.
- Competitor analysis now covers sos `clean`, troubleshoot.sh, and
  detect-secrets with honest positioning (binding condition 1 met).
- Installation experience is clean and was verified end-to-end, including
  packaged-data behavior outside the repo.

## Checkpoint 1 Binding Conditions Status

1. Competitor analysis amendment: **Met.**
2. Trust verification first-class: **Substantially met, with defects.**
   The benchmark, corpus, dry-run, severity model, and conservative
   defaults exist; however C1 breaks the severity model's policy surface
   and the corpus misses one detector, so this condition is not yet met to
   the standard the wording demanded.
3. Review-aid framing: **Met.**

## Re-Review Instructions

Address required changes 1-4, update CHANGELOG.md, re-run the internal
verification suite, and resubmit. No re-litigation of scope or
architecture is needed; this review accepts both.
