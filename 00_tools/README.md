# tools — CI/CD helper commands

Installable Python package (`bi-tools`) exposing two console scripts used by the
GitHub Actions pipelines:

| Command | Where it runs | Purpose |
| --- | --- | --- |
| `dab_prehook` | CI + CD | Rule-based config validation of a DAB bundle (runs before `databricks bundle validate`). |
| `metric_view_deploy` | CD | Deploy metric views for a bundle (runs before `databricks bundle deploy`). |

> ⚠️ These are **placeholders**. Argument handling and a runnable skeleton exist,
> but the real validation / deployment logic is stubbed with TODOs.

## Install

```bash
pip install ./00_tools
```

This puts `dab_prehook` and `metric_view_deploy` on `PATH`. Both accept an optional
bundle directory (default: current directory), so the pipeline runs them from inside
each changed bundle folder:

```bash
cd finance_operations
dab_prehook
metric_view_deploy
```

`metric_view_deploy --dry-run` lists what would be deployed without applying changes.
