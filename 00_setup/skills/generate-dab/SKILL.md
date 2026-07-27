---
name: generate-dab
description: >-
  Generate deployable Databricks Asset Bundle files for a domain: convert native
  *.geniespace.json into *.genie_space.json, and (re)generate resources/dashboards.yml,
  resources/genie_agents.yml, resources/metric_views.yml and databricks.yml. Use
  after adding or editing dashboards, genie agents, or metric views in a domain folder.
---

# generate-dab

**PLACEHOLDER skill.** Wraps the `/Workspace/shared_bi_utilities/generate_dab`
notebook (source: `notebooks/generate_dab.py`).

## When to use

- After adding/editing a `*.lvdash.json`, `*.geniespace.json`, or metric view in a
  domain folder, to regenerate the deployment files.
- Never hand-edit generated files — run this skill instead.

## What it generates

- `assets/genie_agents/*.genie_space.json` (from `*.geniespace.json`)
- `resources/dashboards.yml`
- `resources/genie_agents.yml`
- `resources/metric_views.yml` (domain-specific metric views only; shared metric
  views in `01_shared_metric_views` are skipped)
- `databricks.yml`

## Inputs

| Input | Description |
| --- | --- |
| `domain_path` | Path to the domain folder, e.g. `finance_operations`. |
| `shared_metric_views_path` | Path to the shared metric views bundle (default `01_shared_metric_views`). |

## How it runs

Invokes the shared notebook, e.g. via the Databricks CLI:

```bash
databricks jobs submit --json '{
  "run_name": "generate-dab",
  "tasks": [{
    "task_key": "generate",
    "notebook_task": {
      "notebook_path": "/Workspace/shared_bi_utilities/generate_dab",
      "base_parameters": {
        "domain_path": "finance_operations"
      }
    }
  }]
}'
```

> TODO: implement the notebook logic (currently raises `NotImplementedError`).
