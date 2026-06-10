# RedactPack Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the RedactPack MVP as a dependency-light Python CLI for local support-bundle sanitization.

**Architecture:** A pure detector/redactor core feeds a scanner and report writer. The CLI is a thin argparse layer over the core so behavior can be tested without shelling out.

**Tech Stack:** Python 3.9+, setuptools, pytest, GitHub Actions matrix for macOS, Windows, and Linux.

---

### Task 1: Package Skeleton And Tests

**Files:**

- Create `pyproject.toml`
- Create `src/redactpack/__init__.py`
- Create `src/redactpack/models.py`
- Create `tests/test_models.py`

- [ ] Write tests for severity ordering and report-safe metadata that excludes raw values and brute-forceable hashes.
- [ ] Run `python -m pytest tests/test_models.py -v` and verify failure before implementation.
- [ ] Implement dataclasses and severity helper.
- [ ] Run the test and verify pass.

### Task 2: Detector Registry

**Files:**

- Create `src/redactpack/detectors.py`
- Create `tests/test_detectors.py`

- [ ] Write tests for built-in detector hits: email, IPv4, bearer token, AWS key, GitHub token, Stripe key, Slack token, API key assignment, credit card Luhn, SSN.
- [ ] Run detector tests and verify failure before implementation.
- [ ] Implement detector specs and scan function.
- [ ] Run tests and verify pass.

### Task 3: Redactor

**Files:**

- Create `src/redactpack/redactor.py`
- Create `tests/test_redactor.py`

- [ ] Write tests for deterministic typed placeholders, repeated-value stability, overlap resolution, allowlist skipping, and no raw values in findings.
- [ ] Run tests and verify failure before implementation.
- [ ] Implement redaction.
- [ ] Run tests and verify pass.

### Task 4: Policy Loader

**Files:**

- Create `src/redactpack/policy.py`
- Create `tests/test_policy.py`
- Create `examples/redactpack.policy.json`

- [ ] Write tests for default policy, disabling detectors, allowlist regexes, custom literals, and invalid severity.
- [ ] Run tests and verify failure before implementation.
- [ ] Implement JSON policy loader.
- [ ] Run tests and verify pass.

### Task 5: Scanner And Reports

**Files:**

- Create `src/redactpack/scanner.py`
- Create `src/redactpack/reports.py`
- Create `tests/test_scanner_reports.py`

- [ ] Write tests for directory mirroring, dry-run behavior, report files, skipped binary files, zip output, and fail-on threshold.
- [ ] Run tests and verify failure before implementation.
- [ ] Implement scanner and report rendering.
- [ ] Run tests and verify pass.

### Task 6: CLI And Benchmark

**Files:**

- Create `src/redactpack/cli.py`
- Create `src/redactpack/benchmark.py`
- Create `tests/test_cli.py`
- Create `tests/test_benchmark.py`
- Create `tests/fixtures/corpus.json`

- [ ] Write tests for `scan`, `detectors`, and `benchmark` commands.
- [ ] Run tests and verify failure before implementation.
- [ ] Implement argparse CLI and benchmark recall metrics.
- [ ] Run tests and verify pass.

### Task 7: Documentation, CI, And Review

**Files:**

- Create `README.md`
- Create `LICENSE`
- Create `CONTRIBUTING.md`
- Create `CHANGELOG.md`
- Create `SECURITY.md`
- Create `.github/workflows/ci.yml`
- Create `CHECKPOINT_2_INTERNAL_REVIEW.md`

- [ ] Document install, quickstart, examples, policy, benchmark, limitations, and review-aid language.
- [ ] Add CI matrix for Ubuntu, macOS, and Windows.
- [ ] Run full test suite.
- [ ] Run local CLI smoke test.
- [ ] Complete internal review.
- [ ] Invoke Claude Fable 5 external Checkpoint 2 review through tmux.
