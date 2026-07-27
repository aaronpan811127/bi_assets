# Databricks notebook source
# MAGIC %md
# MAGIC # sync_genie_space
# MAGIC
# MAGIC **PLACEHOLDER** — supporting utility used by the `sync-genie-space` agent skill.
# MAGIC
# MAGIC Creates or updates Genie agents (Genie Spaces) from a deployable
# MAGIC `*.genie_space.json` file, and can round-trip a live space back into a
# MAGIC native `*.geniespace.json` for local editing.
# MAGIC
# MAGIC Deploy this notebook to the dev workspace, e.g. `/Workspace/shared_bi_utilities`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parameters

# COMMAND ----------

dbutils.widgets.text("genie_space_json", "", "Path to *.genie_space.json")
dbutils.widgets.dropdown("mode", "upsert", ["upsert", "export"], "upsert=push to workspace, export=pull to *.geniespace.json")
dbutils.widgets.text("warehouse_id", "", "SQL warehouse id (optional override)")

genie_space_json = dbutils.widgets.get("genie_space_json")
mode = dbutils.widgets.get("mode")
warehouse_id = dbutils.widgets.get("warehouse_id")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Implementation (placeholder)
# MAGIC
# MAGIC TODO: implement using the Databricks SDK / Genie API.
# MAGIC
# MAGIC - `upsert`: read `genie_space_json`, create the Genie Space if it does not
# MAGIC   exist, otherwise update it in place.
# MAGIC - `export`: fetch the live Genie Space and write the native
# MAGIC   `*.geniespace.json` next to the source file for local editing.

# COMMAND ----------

from databricks.sdk import WorkspaceClient  # noqa: F401

def sync_genie_space(path: str, mode: str = "upsert", warehouse_id: str | None = None) -> None:
    """Create/update (or export) a Genie Space from a *.genie_space.json file."""
    raise NotImplementedError("Placeholder — implement Genie Space sync logic.")


if __name__ != "__main__":
    # Notebook entrypoint: run when invoked via %run / dbutils / job.
    print(f"[placeholder] sync_genie_space(path={genie_space_json!r}, mode={mode!r}, "
          f"warehouse_id={warehouse_id!r})")
