"""metric_view_deploy — deploy metric views for a bundle.

PLACEHOLDER. Runs in the CD pipeline for both the shared metric views bundle and
each domain bundle, before `databricks bundle deploy`. Metric views are deployed
separately (rather than as ordinary DAB resources) so that shared metric views
land before the domain assets that depend on them.

Usage:
    metric_view_deploy [BUNDLE_DIR] [--dry-run]

BUNDLE_DIR defaults to the current working directory (the pipeline invokes this
from inside each bundle folder). Discovers assets/metric_views/*.metric_view.*
and creates/updates the corresponding Unity Catalog metric views. Exits non-zero
on failure.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def discover_metric_views(bundle_dir: Path) -> list[Path]:
    """Find metric view definition files in a bundle."""
    mv_dir = bundle_dir / "assets" / "metric_views"
    if not mv_dir.is_dir():
        return []
    # Definitions may be authored as *.metric_view.json or *.metric_view.yml.
    return sorted(
        p for p in mv_dir.iterdir()
        if p.is_file() and (".metric_view." in p.name)
    )


def deploy_metric_view(path: Path, dry_run: bool = False) -> None:
    """Create or update a single metric view from its definition file."""
    action = "would deploy" if dry_run else "deploying"
    print(f"[metric_view_deploy] {action}: {path.name}")
    if dry_run:
        return
    # TODO: implement using the Databricks SDK (Unity Catalog metric views API).
    raise NotImplementedError("Placeholder — implement metric view deploy logic.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="metric_view_deploy", description=__doc__.splitlines()[0]
    )
    parser.add_argument(
        "bundle_dir",
        nargs="?",
        default=".",
        help="Path to the bundle folder (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be deployed without applying changes.",
    )
    args = parser.parse_args(argv)

    bundle_dir = Path(args.bundle_dir).resolve()
    views = discover_metric_views(bundle_dir)

    if not views:
        print(f"[metric_view_deploy] no metric views found in {bundle_dir} — nothing to do.")
        return 0

    print(f"[metric_view_deploy] (placeholder) {len(views)} metric view(s) in {bundle_dir}")
    try:
        for v in views:
            deploy_metric_view(v, dry_run=args.dry_run)
    except NotImplementedError as e:
        print(f"[metric_view_deploy] {e}", file=sys.stderr)
        # Placeholder returns success on --dry-run, failure otherwise so the stub
        # does not silently pass in a real pipeline.
        return 0 if args.dry_run else 1

    print("[metric_view_deploy] done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
