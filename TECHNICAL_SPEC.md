# Technical Spec

Date: 2026-06-10

## Tech Stack

- Language: Python 3.9+
- Packaging: `pyproject.toml` with setuptools
- Runtime dependencies: none outside the Python standard library
- Test dependencies: pytest
- CLI entrypoint: `redactpack`

## Commands

```bash
redactpack scan INPUT --out OUTPUT [--policy POLICY] [--dry-run] [--zip] [--fail-on low|medium|high|critical]
redactpack benchmark [--corpus PATH]
redactpack detectors
```

## Data Model

Finding:

- `detector`: stable detector id.
- `label`: human-readable category.
- `severity`: `low`, `medium`, `high`, or `critical`.
- `confidence`: float from 0.0 to 1.0.
- `file`: relative file path.
- `line`: 1-based line number.
- `start`: 0-based character offset in the full text.
- `end`: 0-based exclusive character offset.
- `placeholder`: deterministic redaction placeholder.

Report:

- input path.
- output path.
- dry-run boolean.
- generated timestamp.
- counts by detector and severity.
- finding metadata with placeholders and positions, never raw sensitive values or brute-forceable value hashes.
- limitations and review warnings.

Policy:

- enabled detector ids.
- disabled detector ids.
- allowlist regexes.
- custom literal redactions.
- fail-on severity.

## Severity Model

- `critical`: credential formats likely to grant access, such as bearer tokens and cloud/provider keys.
- `high`: financial or regulated identifiers, such as credit cards and SSNs.
- `medium`: personal or infrastructure identifiers, such as emails and IPs.
- `low`: context identifiers with lower standalone risk.

Default fail threshold: `critical`.

## Error Handling

- Missing input exits 2 with a readable message.
- Existing output path is allowed only when it is a directory; files are rejected.
- Binary or unsupported files are copied only when `--copy-unsupported` is set; MVP default skips them and reports skipped files.
- Invalid policy exits 2 with the exact invalid field.
- Unexpected runtime errors exit 1.

## Cross-Platform Strategy

- Use `pathlib`.
- Avoid shell commands in runtime.
- Use UTF-8 with `errors="replace"` for text input.
- Use deterministic sorting for file traversal and report output.
- CI must run on Ubuntu, macOS, and Windows.

## Trust Verification

The `benchmark` command runs against a packaged local corpus containing known sensitive values and expected detector ids. It reports recall by detector and overall recall. The project publishes the same corpus in `tests/fixtures/corpus.json` and `src/redactpack/data/corpus.json` so users and reviewers can inspect the benchmark.
