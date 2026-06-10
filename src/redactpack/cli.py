from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from .benchmark import run_benchmark
from .detectors import default_detectors
from .policy import Policy, load_policy
from .scanner import scan_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        if args.command == "scan":
            policy = load_policy(args.policy) if args.policy else Policy.default(fail_on=args.fail_on or "critical")
            if args.policy and args.fail_on is not None:
                policy = Policy.default(
                    disabled_detectors=policy.disabled_detectors,
                    allowlist=policy.allowlist_patterns,
                    custom_literals=policy.custom_literals,
                    fail_on=args.fail_on,
                )
            result = scan_path(args.input, args.out, policy, dry_run=args.dry_run, make_zip=args.zip)
            print(f"Wrote review-aid reports to {Path(args.out)}")
            if result.zip_path:
                print(f"Wrote sanitized zip to {result.zip_path}")
            return result.exit_code
        if args.command == "detectors":
            for detector in default_detectors():
                print(f"{detector.spec.id}\t{detector.spec.severity}\t{detector.spec.description}")
            return 0
        if args.command == "benchmark":
            result = run_benchmark(args.corpus)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0
        parser.print_help()
        return 2
    except (FileNotFoundError, ValueError) as exc:
        print(f"redactpack: {exc}", file=sys.stderr)
        return 2


def main_entry() -> None:
    raise SystemExit(main())


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="redactpack", description="Sanitize local support/debug bundles.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan = subparsers.add_parser("scan", help="Scan and sanitize a file or directory")
    scan.add_argument("input", help="Input file or directory")
    scan.add_argument("--out", required=True, help="Output directory for sanitized files and reports")
    scan.add_argument("--policy", help="Optional JSON policy file")
    scan.add_argument("--dry-run", action="store_true", help="Write reports without sanitized files")
    scan.add_argument("--zip", action="store_true", help="Create a zip archive next to the output directory")
    scan.add_argument(
        "--fail-on",
        choices=("low", "medium", "high", "critical"),
        default=None,
        help="Return non-zero when findings meet this severity threshold",
    )

    subparsers.add_parser("detectors", help="List built-in detectors")

    benchmark = subparsers.add_parser("benchmark", help="Run detection benchmark corpus")
    benchmark.add_argument("--corpus", default=None, help="Path to benchmark corpus JSON")

    return parser


if __name__ == "__main__":
    main_entry()
