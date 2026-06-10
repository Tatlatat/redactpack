# External Review Result - Checkpoint 2 Re-Review

Date: 2026-06-11

Reviewer: Claude Fable 5 (independent senior OSS engineering review)

Scope: Re-review after the 2026-06-11 FAIL (score 6/10). Per the prior
review's re-review instructions, this review verifies the four required
changes, checks for regressions introduced by the fixes, and confirms the
overall quality bar. Scope and architecture are accepted as previously
reviewed and were not re-litigated. Inputs: `EXTERNAL_REVIEW_PACKET_CHECKPOINT_2.md`,
`CHECKPOINT_2_FIXES_AFTER_FABLE_FAIL.md`, full source/tests/docs, and
empirical verification in the project venv plus a fresh venv.

## Verdict

PASS

## Score

8/10

The two critical trust-path defects (C1, C2) are fixed, verified
empirically, and locked in with regression tests. The TEST_PLAN corpus
violation and the allowlist crash are also fixed with tests. The fixes are
minimal, well-scoped, and introduced no regressions. The score reflects a
genuinely solid MVP — clean architecture, zero runtime dependencies,
honest documentation, verified install path — held below 9 by the small
near-tautological benchmark corpus and a handful of known, documented-or-
acknowledged rough edges listed below.

## Required Fix Verification

### Fix 1 — Policy `fail_on` precedence (prior C1): COMPLETE

- `src/redactpack/cli.py:62-67`: `--fail-on` now has `default=None`.
- `src/redactpack/cli.py:20-27`: with no policy, the CLI uses the explicit
  flag or falls back to `critical`; with a policy, the policy's `fail_on`
  is rebuilt with the CLI value only when the flag was explicitly provided
  (`args.fail_on is not None`).
- Regression test `tests/test_cli.py::test_cli_honors_policy_fail_on_when_flag_is_omitted`
  exercises the exact failure shape from the prior review (policy
  `{"fail_on": "low"}`, medium-severity email, no flag, must exit 1).
- Empirical matrix (project venv, fresh tmp dirs):
  - policy `{"fail_on":"low"}`, no flag → exit 1 (policy honored; was exit 0 before the fix)
  - no policy, no flag → exit 0 (default `critical`, finding is medium)
  - policy `{"fail_on":"critical"}`, `--fail-on low` → exit 1 (CLI overrides policy)
  - no policy, `--fail-on low` → exit 1

### Fix 2 — Brute-forceable value hashes removed (prior C2): COMPLETE

- `src/redactpack/models.py`: `Finding.to_safe_dict()` no longer emits
  `value_hash`; `hashlib` is gone from the module. Repo-wide grep finds no
  `value_hash` in any source file (remaining mentions are review/history docs).
- Test `tests/test_models.py::test_finding_safe_dict_excludes_raw_value_and_bruteforceable_hash`
  asserts the serialized finding contains neither the raw value nor
  `value_hash`. Combined with
  `test_zip_output_contains_sanitized_files_and_reports` (the zip packages
  `redactpack-report.json`, which is rendered from `to_safe_dict`), the
  shared-artifact path is covered.
- Empirical leak check: scanned `examples/sample-bundle` with `--zip`,
  unzipped the artifact, and grepped every file for `value_hash` and all
  raw sample values (email, AWS key, Stripe key, bearer token,
  `secret123`): no matches.
- Documentation updated: README ("placeholders and positions, not raw
  sensitive values or brute-forceable value hashes"),
  SECURITY_PRIVACY.md Privacy Principles and Secret Handling ("Raw values
  and unsalted value hashes are not written to reports"), CHANGELOG.md.
  SECURITY.md's Security Model claims ("Reports do not contain raw
  sensitive values", "Raw values are kept only in process memory") are now
  actually true. Minor nit below on SECURITY.md wording.

### Fix 3 — Benchmark corpus completeness: COMPLETE

- A `generic_api_key` case exists in both `tests/fixtures/corpus.json` and
  `src/redactpack/data/corpus.json`; the two files are byte-identical
  (verified by diff).
- `tests/test_benchmark.py::test_benchmark_corpus_measures_recall` now
  asserts `set(result["recall_by_detector"])` equals the full set of
  built-in detector ids — the gap can no longer be invisible to CI.
- Empirical: `redactpack benchmark` run from `/tmp` reports
  `corpus: redactpack.data/corpus.json`, 11 expected labels, 11 detectors
  in `recall_by_detector`, overall recall 1.0, missed list empty.
  `redactpack detectors` lists 11 detectors — counts now agree.
- Bonus: the prior review's non-critical issue 3 (CWD-dependent default
  corpus resolution) was also fixed — `benchmark._load_corpus` no longer
  probes a CWD-relative path and always uses packaged data when no path is
  passed, with outside-repo tests at both the API and CLI level.

### Fix 4 — Allowlist regex validation at load: COMPLETE

- `src/redactpack/policy.py:66-71`: `_validate_allowlist` compiles each
  pattern and raises `ValueError` with the index and reason; it is invoked
  from `Policy.default` (line 29), which both `load_policy` and the CLI
  default path route through.
- Regression test
  `tests/test_policy.py::test_invalid_allowlist_regex_is_rejected_at_load`.
- Empirical: policy `{"allowlist": ["[unclosed"]}` exits 2 with
  `redactpack: allowlist[0] is not a valid regex: unterminated character
  set at position 0` — no traceback.

### Re-review housekeeping

- CHANGELOG.md updated with all four fixes, as the prior review required.
- Internal verification claims in the packet and fixes doc match what this
  review reproduced independently.

## Verification Performed

- `.venv/bin/python -m pytest tests -v` (Python 3.14.4): 22 passed in 0.04s,
  including the three new regression tests named in the fixes document.
- Fresh venv (`python3 -m venv`), `pip install <repo>`: install succeeded;
  installed `redactpack benchmark` from the venv tmp dir used packaged
  corpus at recall 1.0; installed `redactpack scan` redacted an email to
  `[REDACTED:EMAIL:1]` and honored `--fail-on low` with exit 1.
- `fail_on` precedence matrix: four scenarios, all correct (see Fix 1).
- Invalid allowlist regex: clean exit 2, no traceback (see Fix 4).
- Zip leak check: no `value_hash`, no raw sample values anywhere in the
  zip artifact (see Fix 2).
- `python -m compileall -q src`: passed. AST parse of all sources with
  `feature_version=(3,9)`: passed (CI matrix runs real 3.9 on three OSes).
- Code inspection of every file touched by the fixes (`cli.py`,
  `models.py`, `policy.py`, `benchmark.py`, both corpus files, all test
  files) plus `scanner.py`, README, SECURITY.md, SECURITY_PRIVACY.md,
  CHANGELOG.md for regressions: none found.

## New Blockers

None. The fixes are surgical and did not introduce new defects.

## Remaining Non-Critical Issues (carried over, all non-blocking)

1. `scanner.remove_output` (`scanner.py:94-97`) is still dead code wrapping
   `shutil.rmtree` of an arbitrary path — remove it or wire it up with tests.
2. `tests/test_benchmark.py:8` still resolves the fixture via a
   CWD-relative `Path("tests/fixtures/corpus.json")`; pytest invoked from
   outside the repo root would fail. Fine for CI (runs at repo root).
3. `_write_zip` still uses `output.with_suffix(".zip")`, which mangles
   dotted output directory names (`out.v1` → `out.zip`).
4. README Limitations still lacks entries for lossy non-UTF-8 decoding
   (`errors="replace"`) and silent symlink-following during traversal.
5. The benchmark corpus remains small (5 cases, 11 labels) and mirrors the
   unit-test strings; recall 1.0 is near-guaranteed by construction. It is
   a sound regression harness, not yet a meaningful quality metric.
6. `--out` inside the input directory remains unspecified and untested.
7. Version strings like `1.2.3.4` still false-positive as IPv4 (generic
   limitations coverage applies; a concrete README example would help).
8. Minor nit: SECURITY.md's Security Model could state the no-hash report
   behavior explicitly (the statement currently lives in
   SECURITY_PRIVACY.md and README); a one-line addition would make the
   security-facing doc self-contained.

## Recommended Improvements (non-blocking)

- Grow the corpus beyond unit-test mirrors: real-world log shapes,
  negative cases, and a precision metric alongside recall.
- Address remaining items 1-4 above in the next implementation pass; they
  are each small.
- Consider a direct test asserting the zip artifact (not just the
  serialized finding) contains no `value_hash`, to pin the shared-artifact
  guarantee end to end.

## Checkpoint 1 Binding Conditions Status

1. Competitor analysis amendment: **Met** (unchanged).
2. Trust verification first-class: **Met.** The severity model's policy
   surface now works as documented (C1 fixed), the corpus covers every
   built-in detector with CI enforcement (corpus gap fixed), and the
   shared artifact no longer partially undoes redaction (C2 fixed).
3. Review-aid framing: **Met** (unchanged).

## Conclusion

All four required changes from the 2026-06-11 FAIL are complete, correct,
empirically verified, and protected by regression tests. No new blockers.
Checkpoint 2 passes at 8/10. The project may proceed; the carried-over
non-critical items should be triaged into the next checkpoint's plan.
