# Installation Plan

Date: 2026-06-10

## Supported Platforms

- macOS with Python 3.9+
- Windows with Python 3.9+
- Linux with Python 3.9+

## Install From Source

```bash
python -m pip install .
```

## Developer Install

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Recommended User Install After Release

```bash
pipx install redactpack
```

## Upgrade

```bash
pipx upgrade redactpack
```

## Uninstall

```bash
pipx uninstall redactpack
```

## Cross-Platform CI

GitHub Actions must run tests on:

- `ubuntu-latest`
- `macos-latest`
- `windows-latest`

Python versions:

- 3.9
- 3.12
