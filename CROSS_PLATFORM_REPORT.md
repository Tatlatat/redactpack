# Cross-Platform Report

Date: 2026-06-11

## Supported Targets

- macOS with Python 3.9+
- Linux with Python 3.9+
- Windows with Python 3.9+

## Local Verification

Environment:

- macOS
- Python 3.14.4 local venv

Verified locally:

- `python -m compileall -q src`: passed.
- `.venv/bin/python -m pytest tests -v`: 29 passed.
- Fresh source install in `/tmp/redactpack-install-venv`: passed.
- Installed `redactpack benchmark` from `/tmp`: passed.
- Installed `redactpack scan` sample bundle with zip: passed.

## CI Readiness

`.github/workflows/ci.yml` defines a matrix for:

- `ubuntu-latest`
- `macos-latest`
- `windows-latest`
- Python `3.9`
- Python `3.12`

The workflow installs the package, runs tests, and runs the packaged benchmark.

## Hosted CI Evidence

Repository: `https://github.com/Tatlatat/redactpack`

Run: `https://github.com/Tatlatat/redactpack/actions/runs/27295074259`

Commit: `720577c1d436eefffb3b39aa76acf92557461374`

Result: passed.

Jobs passed:

- Python 3.9 on `ubuntu-latest`.
- Python 3.12 on `ubuntu-latest`.
- Python 3.9 on `macos-latest`.
- Python 3.12 on `macos-latest`.
- Python 3.9 on `windows-latest`.
- Python 3.12 on `windows-latest`.

## Limitations

No platform blocker is known after hosted CI. Remaining cross-platform risk is ordinary MVP coverage risk: future detector additions and file handling changes should continue to run through the hosted matrix.

## Cross-Platform Design Choices

- Uses `pathlib`.
- Avoids shell commands in runtime.
- Uses deterministic sorted traversal.
- Avoids runtime dependencies and native extensions.
- Skips symlinks rather than following them.
- Uses UTF-8 read with replacement for non-UTF-8 text.
