# External Review Result — Checkpoint 3 Post-Fix Re-Review

Date: 2026-06-11
Reviewer: Claude Fable 5 (independent re-review, post-condition verification)
Scope: Verify the two code pre-tag conditions from the Checkpoint 3 PASS
(`EXTERNAL_REVIEW_CHECKPOINT_3_RESULT.md`), plus report path privacy.
Scope was not re-litigated.

## Verdict

PASS — both code pre-tag conditions are fixed with regression tests and
verified by independent reproduction. One pre-tag condition remains
outstanding by nature (CI matrix; see Remaining Release Blocker).

## Condition 1: Unreadable file inside bundle — FIXED, VERIFIED

- Code: `src/redactpack/scanner.py:85-89` — `_read_text_or_none` now
  wraps `path.read_bytes()` in `try/except OSError → None`, routing
  unreadable files through the same skip-and-report path already used
  for binary files and symlinks (`scanner.py:42-45`). This is exactly
  the mechanism the original review prescribed.
- Regression test:
  `tests/test_scanner_reports.py:108`
  `test_unreadable_files_are_skipped_and_reports_are_still_written`
  (monkeypatched `PermissionError`) — passes.
- Independent reproduction (real `chmod 000`, not monkeypatch):
  - Bundle containing a `chmod 000` file: scan completed, exit 0,
    both reports written, sanitized `app.log` written, `locked.txt`
    listed in `skipped_files`. No traceback, no partial output.
  - Single unreadable file as direct input: scan completed, exit 0,
    reports written. Consistent behavior.

## Condition 2: Non-object policy JSON — FIXED, VERIFIED

- Code: `src/redactpack/policy.py:45-46` —
  `if not isinstance(data, dict): raise ValueError("policy file must be
  a JSON object")`, mapped by the existing `cli.py:43-45` handler to a
  clean stderr message and exit 2.
- Regression tests:
  `tests/test_policy.py:44` `test_non_object_policy_json_is_rejected`
  and `tests/test_cli.py:32`
  `test_cli_rejects_non_object_policy_json_cleanly` — both pass.
- Independent reproduction (installed venv CLI): policy files containing
  `[]`, `"just a string"`, and `42` each produce
  `redactpack: policy file must be a JSON object` on stderr with
  exit 2, no traceback. No output directory is created (policy loads
  before the scan starts).

## Report Path Privacy (defect 4 of the original review) — ALSO FIXED

- Code: `scanner.py` `_display_path` returns `path.name or "."`;
  `input_path`/`output_path` in the report are now basenames.
- Reproduced: scan of `examples/sample-bundle` with an absolute input
  path records `input_path: "sample-bundle"` and
  `output_path: "rp_priv_out"`. Every member of the shareable zip was
  extracted and grepped for `/Users/` and the local username — zero
  matches. No absolute paths or username disclosure in shared artifacts.

## Additional Observations (no scope expansion)

- Defect 3 of the original review (CWD-relative fixture in
  `tests/test_benchmark.py`) is also fixed: the full suite passes from
  `/tmp` (previously 1 failed), and two new tests
  (`test_benchmark_default_corpus_works_outside_repo`,
  `test_cli_benchmark_default_corpus_works_outside_repo`) pin it.
- No regressions: full suite is 28/28 passed (was 25 at Checkpoint 3
  review; +3 net new regression tests covering the fixed defects).
- `python -m compileall -q src` passes; AST parse of all sources with
  `feature_version=(3,9)` passes — the fixes use no post-3.9 syntax.

## Remaining Release Blocker

Pre-tag condition 1 of the Checkpoint 3 PASS is still open and is the
only remaining blocker: the workspace is still not a git repository
(`git rev-parse` fails), so the configured GitHub Actions matrix
(`.github/workflows/ci.yml`, ubuntu/macos/windows × 3.9/3.12) has never
executed remotely. Windows and Linux remain verified by design review
and the 3.9 AST check only. **Do not tag v0.1.0 until the repository is
published and the CI matrix is fully green.** This is an operational
publish-time step, not a code defect; no code-level blockers remain.
