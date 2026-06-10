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
- `.venv/bin/python -m pytest tests -v`: 28 passed.
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

## Limitations

Remote CI has not been executed from this local workspace. Windows and Linux behavior is prepared through CI configuration and standard-library-only runtime design, but it is not claimed as remotely green until the workflow runs in GitHub Actions.

## Cross-Platform Design Choices

- Uses `pathlib`.
- Avoids shell commands in runtime.
- Uses deterministic sorted traversal.
- Avoids runtime dependencies and native extensions.
- Skips symlinks rather than following them.
- Uses UTF-8 read with replacement for non-UTF-8 text.
