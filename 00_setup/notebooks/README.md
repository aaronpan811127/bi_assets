# notebooks

Supporting utilities used by the agent skills in `skills`. Deploy these to the
dev workspace, e.g. `/Workspace/shared_bi_utilities`.

| Notebook | Purpose |
| --- | --- |
| `sync_genie_space.py` | Create/update Genie agents from `*.genie_space.json` (or export a live space back to `*.geniespace.json`). |
| `generate_dab.py` | Generate `*.genie_space.json` from `*.geniespace.json`, and generate `resources/*.yml` + `databricks.yml` for a domain bundle. |

> ⚠️ These are **placeholders** — the generation/sync logic is stubbed with
> `NotImplementedError`. Fill in the implementation using the Databricks SDK and
> Genie APIs.
