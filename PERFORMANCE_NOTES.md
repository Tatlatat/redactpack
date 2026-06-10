# Performance Notes

Date: 2026-06-11

## Expected Input Sizes

MVP target:

- Small and medium support bundles.
- Text/config/log files from kilobytes to tens of megabytes.
- Directory trees with hundreds to low thousands of files.

## Complexity

- File traversal is linear in number of files.
- Detector scanning is approximately linear in text length times detector count.
- Redaction sorts findings per file to resolve overlaps.
- Reports are proportional to finding count.

## Current Boundaries

- Files are read fully into memory.
- Zip creation writes a complete archive after scan output is generated.
- Benchmark corpus is small and intended for regression, not load testing.

## Future Improvements

- Stream large files by chunks with overlap windows.
- Add file-size caps with skip-and-report behavior.
- Add performance benchmark fixtures.
- Add precision metrics and larger real-world corpus examples.
