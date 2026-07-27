# Databricks notebook source
# MAGIC %md
# MAGIC # generate_dab
# MAGIC
# MAGIC **PLACEHOLDER** — supporting utility used by the `generate-dab` agent skill.
# MAGIC
# MAGIC For a given domain folder, this notebook:
# MAGIC
# MAGIC 1. Converts each native `assets/genie_agents/*.geniespace.json` into a
# MAGIC    deployable `*.genie_space.json`.
# MAGIC 2. Generates the DAB resource files:
# MAGIC    - `resources/dashboards.yml`
# MAGIC    - `resources/genie_agents.yml`
# MAGIC    - `resources/metric_views.yml` (domain-specific metric views only —
# MAGIC      metric views declared in `01_shared_metric_views` are skipped)
# MAGIC 3. Generates the `databricks.yml` bundle entrypoint.
# MAGIC
# MAGIC Deploy this notebook to the dev workspace, e.g. `/Workspace/shared_bi_utilities`.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Parameters

# COMMAND ----------

dbutils.widgets.text("domain_path", "", "Path to the domain folder, e.g. finance_operations")
dbutils.widgets.text("shared_metric_views_path", "01_shared_metric_views", "Path to shared metric views bundle")

domain_path = dbutils.widgets.get("domain_path")
shared_metric_views_path = dbutils.widgets.get("shared_metric_views_path")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Implementation (placeholder)
# MAGIC
# MAGIC TODO: implement generation logic.

# COMMAND ----------

def generate_dab(domain_path: str, shared_metric_views_path: str = "01_shared_metric_views") -> None:
    """Generate deployable Genie definitions + DAB resource yml + databricks.yml."""
    raise NotImplementedError("Placeholder — implement DAB generation logic.")


if __name__ != "__main__":
    print(f"[placeholder] generate_dab(domain_path={domain_path!r}, "
          f"shared_metric_views_path={shared_metric_views_path!r})")
