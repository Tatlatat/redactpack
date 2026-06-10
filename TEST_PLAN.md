# Test Plan

Date: 2026-06-10

## Test Strategy

RedactPack must be tested at three levels:

- Unit tests for detectors, redaction, policy loading, and severity logic.
- Integration tests for scanning directories and generating reports.
- CLI tests for real command workflows through `redactpack.cli.main`.

## Required Coverage

- Detector coverage for each built-in detector.
- Redaction overlap handling.
- Deterministic placeholder assignment.
- Reports do not include raw sensitive values.
- Dry-run writes reports but not sanitized files.
- Fail-on severity returns non-zero for configured thresholds.
- Binary files are skipped and reported.
- Zip output contains sanitized files and reports.
- Benchmark command returns measured recall.

## Benchmark Corpus

`tests/fixtures/corpus.json` must include labeled examples for every MVP detector. The benchmark command must report:

- total expected labels.
- matched labels.
- missed labels.
- overall recall.
- recall by detector.

The benchmark is not a safety guarantee. It is a visible quality signal and regression check.

## Commands

```bash
python -m pytest
python -m redactpack.cli detectors
python -m redactpack.cli benchmark
python -m redactpack.cli scan examples/sample-bundle --out /tmp/redactpack-out --dry-run
```
