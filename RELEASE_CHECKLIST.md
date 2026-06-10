# Release Checklist

Date: 2026-06-11

## Required Assets

- [x] Source code
- [x] Tests
- [x] README
- [x] LICENSE
- [x] CONTRIBUTING
- [x] CHANGELOG
- [x] SECURITY policy
- [x] Examples
- [x] Configuration example
- [x] CI workflow
- [x] Installation guide
- [x] User guide
- [x] Security/privacy review
- [x] Benchmark corpus

## Verification

- [x] `python -m compileall -q src`
- [x] `.venv/bin/python -m pytest tests -v` passes with 28 tests
- [x] Fresh venv install from source works
- [x] Installed CLI benchmark works outside repo
- [x] Sample scan works
- [x] Zip output works
- [x] Policy `fail_on` works
- [x] Invalid allowlist error is clean
- [x] Output-inside-input guard works
- [x] Symlink skip behavior is tested
- [x] Dotted output zip naming is tested
- [x] Unreadable file skip-and-report is tested
- [x] Non-object policy JSON clean error is tested
- [x] Shared reports avoid absolute local input/output paths

## Release Blockers

- [ ] Remote GitHub Actions matrix has not been executed in this local workspace.
- [x] Unreadable-file crash fixed and post-fix reviewed by Fable.
- [x] Non-object policy JSON crash fixed and post-fix reviewed by Fable.

## Pre-Tag Command Set

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m redactpack.cli benchmark
python -m redactpack.cli scan examples/sample-bundle --out /tmp/redactpack-release-smoke --zip
```
