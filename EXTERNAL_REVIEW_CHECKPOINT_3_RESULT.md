# External Review Result - Checkpoint 3

Date: 2026-06-11

Reviewer: Claude Fable 5 (independent OSS release readiness review)

Scope: Release readiness per `EXTERNAL_REVIEW_PACKET_CHECKPOINT_3.md` —
stability, cross-platform readiness, installation, runtime usability,
documentation, codebase maturity, test confidence, deployability, UX, and
fitness for publication as a serious OSS project.

## Verdict

PASS — with binding pre-tag release conditions (see Release Blockers).

## Score

8/10

The codebase is small, clean, dependency-free, deterministic, and honestly
documented. Every claim in the internal verification summary reproduced
exactly in this review. Most of the eight non-critical items carried over
from the Checkpoint 2 re-review were genuinely fixed, each with a
regression test. The score is held below 9 by two ungraceful crash paths
found by adversarial probing, the still-unexecuted remote CI matrix (so
Windows/Linux remain design-verified, not empirically verified), a
near-tautological benchmark corpus, and local-path metadata embedded in
shareable reports.

## Verification Performed (all reproduced independently)

- `.venv/bin/python -m pytest tests -v` (Python 3.14.4): **25 passed**,
  including the new hardening regression tests
  (`test_zip_name_appends_suffix_for_dotted_output_directory`,
  `test_output_directory_inside_input_is_rejected`,
  `test_symlink_files_are_skipped_not_followed`).
- `python -m compileall -q src`: passed. AST parse of all sources with
  `feature_version=(3,9)`: passed.
- Fresh venv (`python3 -m venv` + `pip install <repo>`): install succeeded.
- Installed `redactpack benchmark` run from `/tmp`: uses
  `redactpack.data/corpus.json`, 11 detectors in `recall_by_detector`,
  overall recall 1.0, missed list empty.
- Installed `redactpack scan examples/sample-bundle --policy
  examples/redactpack.policy.json --zip`: correct sanitized output for all
  six seeded values (email, IPv4, bearer token, sensitive-query URL, AWS
  key, Stripe key) plus the custom literal (`[REDACTED:CUSTOMER_ID:1]`).
- Zip leak check: extracted every member of `out.zip` and searched for all
  raw sample values, `value_hash`, and the seeded IP — **zero leaks**.
- `fail_on` precedence matrix (installed CLI, 4 scenarios): policy
  `low`/no flag → 1; no policy/no flag → 0; policy `critical` + `--fail-on
  low` → 1; no policy + `--fail-on low` → 1. All correct.
- Error paths: missing input → clean exit 2 message; malformed (non-JSON)
  policy → clean exit 2 message; output dir inside input dir → clean
  rejection; binary file and symlink skipped and listed in
  `skipped_files`; non-UTF-8 file lossy-decoded as documented; dotted
  output dir `out.v1` zips to `out.v1.zip`; single-file scan works.
- Performance probe: 9.6 MB log (121k lines), scan completed in 1.5 s with
  360 findings. Adequate for the documented input envelope.
- Carried-over fix audit (Checkpoint 2 re-review items): dead
  `scanner.remove_output` removed; `_write_zip` dotted-name mangling fixed
  (`scanner.py:96`); `--out` inside input now rejected (`scanner.py:32-33`);
  symlinks skipped and reported (`scanner.py:39-41`); README Limitations
  now covers lossy non-UTF-8 decoding and symlink skipping; SECURITY.md
  Security Model now states the no-raw-values/no-unsalted-hashes behavior
  itself. All confirmed in code and by test or probe.

## Defects Found in This Review

None are data-safety defects; no path examined leaks sensitive values.

1. **Unreadable file inside the bundle crashes the scan with a raw
   traceback** (`scanner.py:86` — `path.read_bytes()` has no
   `OSError`/`PermissionError` handling; `cli.py:43` catches only
   `FileNotFoundError` and `ValueError`). Reproduced with a `chmod 000`
   file: traceback, exit 1, partially written output directory with **no
   reports**. Support bundles extracted from other systems routinely
   contain unreadable or root-owned files; the tool already has the
   correct mechanism (skip-and-report, used for binary files and
   symlinks) and should route unreadable files through it.
2. **Policy file containing valid JSON of the wrong shape crashes with a
   raw traceback** (`policy.py:45` — `data.get` on a non-dict, e.g. a
   policy file containing `[]`, raises uncaught `AttributeError`).
   Violates the technical spec's "invalid policy exits 2 with the exact
   invalid field." A type check with a `ValueError` is a three-line fix.
3. **`tests/test_benchmark.py:8` still resolves the fixture via a
   CWD-relative path** — `pytest` invoked from outside the repo root
   fails this test (reproduced: 1 failed, 24 passed from `/tmp`). This
   was explicitly listed as carried-over item 2 in the Checkpoint 2
   re-review and was not fixed during final hardening. Harmless in the
   current CI (runs at repo root), but it will bite downstream
   packagers/distro test runners.
4. **Shareable reports embed absolute local paths** — `input_path` in
   `redactpack-report.json` (inside the shareable zip) records e.g.
   `/Users/<name>/...`, disclosing the local username and directory
   layout. For a privacy-positioning tool, the shared artifact should
   carry relative or basename paths.

## Release Blockers (binding pre-tag conditions of this PASS)

The checkpoint passes; the **v0.1.0 tag must not be created** until:

1. The GitHub Actions matrix (ubuntu/macos/windows × 3.9/3.12) has been
   pushed and is fully green. This is the project's own open checklist
   item; the workspace is not yet a git repository, so no remote CI run
   exists. Windows and Linux are currently verified by design review
   only.
2. Defect 1 (unreadable-file crash) is fixed as skip-and-report with a
   regression test.
3. Defect 2 (non-object policy JSON traceback) is fixed as clean exit 2
   with a regression test.

## Major Risks

- **Detector false negatives remain the core product risk.** Detection is
  regex/checksum-based and conservative; recall 1.0 on a 5-case,
  11-label corpus that mirrors the unit-test strings is near-guaranteed
  by construction and must not be read as a quality metric. The docs say
  this honestly, which is the saving grace.
- **Windows behavior is unproven empirically** (path semantics, console
  encoding, zip handling) until the CI matrix runs. The stdlib-only,
  pathlib-based design makes failure unlikely but not impossible.
- **Crash-path coverage is thin**: two ungraceful crash paths were found
  within minutes of adversarial probing; others likely exist (e.g.,
  output-write `OSError`s, Windows long paths/locked files). A top-level
  "unexpected error" handler that still reports cleanly would cap this
  class.
- **False positives redact debugging context** (e.g., version string
  `1.2.3.4` is redacted as IPv4 — reproduced). Documented generically;
  the concrete example recommended at Checkpoint 2 is still absent from
  README.
- **Metadata disclosure in shared artifacts** (defect 4) is a reputation
  risk for a privacy tool even though no secret values leak.

## Required Fixes

Not applicable — verdict is PASS. The three binding pre-tag conditions
above are mandatory before tagging/announcing v0.1.0; defects 3 and 4 and
the README false-positive example are strongly recommended for v0.1.x.

## Assessment Against the Ten Review Criteria

1. Stability: good on all documented paths; two ungraceful crash edges
   (gated above).
2. Cross-platform readiness: well-designed; macOS empirically verified;
   Windows/Linux pending the CI gate.
3. Installation experience: verified clean from a fresh venv; pipx path
   documented for post-release.
4. Runtime usability: clear CLI, correct exit codes, readable errors on
   documented failure paths, useful reports.
5. Documentation completeness: strong — README, USER_GUIDE, SECURITY,
   CONTRIBUTING, CHANGELOG, examples, honest limitations throughout.
6. Codebase maturity: small, modular, dependency-free, deterministic;
   prior review debt actually paid down.
7. Test coverage/confidence: 25 focused tests covering every prior
   regression; gaps only at the crash edges named above.
8. Practical deployability: yes, contingent on the standard push-and-CI
   step that publication itself requires.
9. User experience: good for the target persona; report metadata nit
   noted.
10. Ready to publish as a serious OSS project: yes, under the binding
    conditions above.

## Final Approval Statement

Checkpoint 3 is APPROVED. RedactPack is stable on its documented paths,
usable, honestly and thoroughly documented, and practically deployable as
a v0.1.0 alpha. This approval is conditional in exactly one operational
sense: the v0.1.0 release tag must not be cut until the cross-platform CI
matrix is green on the published repository and the two crash-path fixes
(unreadable input files; non-object policy JSON) have landed with
regression tests. With those conditions met, this project meets the bar
for publication as a serious open-source project.
