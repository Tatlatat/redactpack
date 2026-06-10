# Contributing

Thanks for considering a contribution to RedactPack.

## Local Setup

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## Development Rules

- Write tests before behavior changes.
- Keep runtime dependencies minimal.
- Do not add network calls to scan behavior.
- Do not write raw sensitive values to reports.
- Describe reports as review aids, not safety guarantees.
- Add benchmark corpus cases when adding detectors.

## Adding A Detector

1. Add corpus examples to `tests/fixtures/corpus.json` and `src/redactpack/data/corpus.json`.
2. Add tests in `tests/test_detectors.py`.
3. Implement the detector in `src/redactpack/detectors.py`.
4. Run `python -m pytest` and `python -m redactpack.cli benchmark`.

## Pull Request Checklist

- Tests pass.
- Benchmark recall has not regressed.
- README or docs are updated when user-facing behavior changes.
- New reports do not include raw sensitive values.
