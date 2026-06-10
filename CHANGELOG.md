# Changelog

## 0.1.0 - Unreleased

- Initial RedactPack MVP.
- Local scan command for files and directories.
- Deterministic typed placeholders.
- JSON and Markdown review-aid reports.
- Built-in detectors for common PII and secret formats.
- Policy support for disabled detectors, allowlist regexes, custom literals, and severity threshold.
- Dry-run mode.
- Optional zip packaging.
- Benchmark command with published corpus and recall metrics.
- Cross-platform CI configuration.
- Fixed policy-file `fail_on` precedence so CLI defaults do not override explicit policy thresholds.
- Removed unsalted value hashes from reports.
- Added `generic_api_key` to the benchmark corpus and tightened corpus coverage tests.
- Added allowlist regex validation at policy load time.
- Hardened zip naming for output directories containing dots.
- Rejected output directories inside the input tree.
- Skipped symlink files instead of following them.
- Skipped unreadable files and still wrote reports.
- Rejected non-object policy JSON with a clean error.
- Removed absolute local input/output paths from shared reports.
