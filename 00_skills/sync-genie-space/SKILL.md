---
name: sync-genie-space
description: >-
  Create or update Genie agents (Genie Spaces) from a deployable
  *.genie_space.json file, or export a live Genie Space back to a native
  *.geniespace.json for local editing. Use when a user edits a genie agent
  definition and wants it pushed to / pulled from the workspace.
---

# sync-genie-space

**PLACEHOLDER skill.** Wraps the `/Workspace/shared_bi_utilities/sync_genie_space`
notebook (source: `00_notebooks/sync_genie_space.py`).

## When to use

- After editing a `*.geniespace.json` / `*.genie_space.json` and wanting the change
  reflected in the workspace.
- To pull an existing workspace Genie Space down into a native `*.geniespace.json`.

## Inputs

| Input | Description |
| --- | --- |
| `genie_space_json` | Path to the `*.genie_space.json` file. |
| `mode` | `upsert` (push to workspace) or `export` (pull to `*.geniespace.json`). |
| `warehouse_id` | Optional SQL warehouse id override. |

## How it runs

Invokes the shared notebook, e.g. via the Databricks CLI:

```bash
databricks jobs submit --json '{
  "run_name": "sync-genie-space",
  "tasks": [{
    "task_key": "sync",
    "notebook_task": {
      "notebook_path": "/Workspace/shared_bi_utilities/sync_genie_space",
      "base_parameters": {
        "genie_space_json": "<path>",
        "mode": "upsert"
      }
    }
  }]
}'
```

> TODO: implement the notebook logic (currently raises `NotImplementedError`).
