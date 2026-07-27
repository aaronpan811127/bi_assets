"""dab_prehook — rule-based config validation for a DAB bundle.

PLACEHOLDER. Runs before `databricks bundle validate` in both the CI and CD
pipelines. Intended to enforce repo-specific conventions that the Databricks
schema validator does not, e.g.:

  - databricks.yml exists and its bundle name matches the folder name
  - every resources/*.yml referenced asset file actually exists
  - generated files (*.genie_space.json, resources/*.yml) are up to date
  - naming conventions for dashboards / genie spaces / metric views

Usage:
    dab_prehook [BUNDLE_DIR]

BUNDLE_DIR defaults to the current working directory (the pipeline invokes this
from inside each changed bundle folder). Exits non-zero if any rule fails.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _check_databricks_yml(bundle_dir: Path) -> list[str]:
    """Return a list of error strings (empty = pass)."""
    errors: list[str] = []
    dab = bundle_dir / "databricks.yml"
    if not dab.is_file():
        errors.append(f"{bundle_dir}: missing databricks.yml")
    # TODO: parse databricks.yml and assert bundle.name == bundle_dir.name, etc.
    return errors


def run_prehook(bundle_dir: Path) -> list[str]:
    """Run all rule checks against a bundle directory. Returns error strings."""
    errors: list[str] = []
    errors += _check_databricks_yml(bundle_dir)
    # TODO: add further rule-based checks here.
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dab_prehook", description=__doc__.splitlines()[0])
    parser.add_argument(
        "bundle_dir",
        nargs="?",
        default=".",
        help="Path to the DAB bundle folder (default: current directory).",
    )
    args = parser.parse_args(argv)

    bundle_dir = Path(args.bundle_dir).resolve()
    print(f"[dab_prehook] (placeholder) validating {bundle_dir} ...", flush=True)

    errors = run_prehook(bundle_dir)
    if errors:
        for e in errors:
            print(f"[dab_prehook] FAIL: {e}", file=sys.stderr, flush=True)
        return 1

    print("[dab_prehook] OK — no rule violations found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
