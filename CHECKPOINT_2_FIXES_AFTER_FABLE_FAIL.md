# Checkpoint 2 Fixes After Fable FAIL

Date: 2026-06-11

External review result: FAIL, score 6/10.

## Required Fixes Completed

1. Policy `fail_on` precedence
   - Fixed CLI behavior so `--fail-on` defaults to `None`.
   - Policy file thresholds are honored when the flag is omitted.
   - Added regression test `test_cli_honors_policy_fail_on_when_flag_is_omitted`.

2. Brute-forceable value hashes
   - Removed `value_hash` from report output.
   - Reports now include placeholders and positions, not raw values or unsalted hashes.
   - Updated README, technical spec, architecture, security/privacy docs, and implementation plan.

3. Benchmark corpus completeness
   - Added `generic_api_key` to `tests/fixtures/corpus.json`.
   - Added `generic_api_key` to packaged `src/redactpack/data/corpus.json`.
   - Strengthened benchmark tests to assert every built-in detector appears in recall metrics.

4. Allowlist regex validation
   - Added regex validation at policy load/default construction time.
   - Invalid allowlist regexes now return clean CLI exit code 2 through the existing ValueError path.
   - Added regression test `test_invalid_allowlist_regex_is_rejected_at_load`.

## Verification After Fixes

- `.venv/bin/python -m compileall -q src`: passed.
- `.venv/bin/python -m pytest tests -v`: 22 passed.
- Fresh install with `python -m pip install .`: passed.
- Installed CLI benchmark from `/tmp`: passed, used `redactpack.data/corpus.json`, 11/11 labels matched, 1.0 recall.
- Policy `{"fail_on":"low"}` with medium email finding exits 1.
- Invalid allowlist regex exits 2 with clean message.
- Sample zip report contains no `value_hash` and no raw sample email/token/provider keys.
