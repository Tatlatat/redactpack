# User Guide

Date: 2026-06-11

## Install

```bash
python -m pip install .
```

Developer install:

```bash
python -m pip install -e ".[dev]"
```

## Scan A Bundle

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-out
```

Outputs:

- sanitized files in `/tmp/redactpack-out`
- `/tmp/redactpack-out/redactpack-report.json`
- `/tmp/redactpack-out/redactpack-summary.md`

## Create A Zip

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-out --zip
```

Zip output is written next to the output directory, for example `/tmp/redactpack-out.zip`.

## Dry Run

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-review --dry-run
```

Dry-run writes reports but not sanitized files.

## Use A Policy

```bash
redactpack scan examples/sample-bundle --out /tmp/redactpack-out --policy examples/redactpack.policy.json
```

Policy files can disable detectors, add allowlist regexes, define custom literal redactions, and set `fail_on`.

## Benchmark Detectors

```bash
redactpack benchmark
```

The benchmark reports recall for the packaged corpus. It is a regression signal, not a safety guarantee.

## Review Before Sharing

Read the summary and inspect sanitized files before sending them outside your trusted boundary. RedactPack reports are review aids, not proof that a bundle is safe.
