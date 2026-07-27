# Setup Guide

One-time steps for an **administrator** to stand up this repo in a new customer
environment, before BI developers can follow the [User Guide](user-guide.md).

> Audience: platform / workspace admin. Developers do **not** need to do any of this.

## Prerequisites

- A Databricks workspace with **Unity Catalog** enabled.
- Workspace admin (or metastore admin) rights to create catalogs, schemas, groups and grants.
- A running **SQL warehouse** to back dashboards and genie spaces.
- Git provider access (this repo lives on GitHub) and permission to add repo secrets.
- Local tooling for the person running CLI steps: `git`, the
  [Databricks CLI](https://docs.databricks.com/dev-tools/cli/) (v0.240+), and Python 3.10+.

## 1. Fork / clone the repo into the customer org

1. Create the repo in the customer's GitHub org (or fork this one).
2. Add it as a **Databricks Git folder** (Repos) in the workspace so Genie Code can edit it.

## 2. Create Unity Catalog objects

Each domain bundle expects a catalog/schema to hold its assets. Create one per domain
(names should match the `catalog`/`schema` used in the domain's generated resources):

```sql
-- Example for the finance_operations domain
CREATE CATALOG IF NOT EXISTS finance_operations;
CREATE SCHEMA  IF NOT EXISTS finance_operations.presentation;
-- Repeat for supply_chain, and any future domain.
```

## 3. Create groups and grants

```sql
-- Admin group referenced by the bundle permissions (databricks.yml -> group_name: bi-admins)
-- Create the `bi-admins` group in the account console / SCIM, then grant it access:
GRANT USE CATALOG, USE SCHEMA, CREATE TABLE ON CATALOG finance_operations TO `bi-admins`;
GRANT SELECT ON CATALOG finance_operations TO `bi-admins`;
```

Adjust group names and privileges to the customer's governance model. Ensure BI developers
are members of the group(s) that own the domains they work on.

## 4. Deploy the shared utilities (notebooks)

The Genie Code skills call notebooks that must exist in the workspace. Deploy the contents
of `00_notebooks/` to the path the skills expect (default `/Workspace/shared_bi_utilities`):

```bash
databricks workspace import-dir 00_notebooks /Workspace/shared_bi_utilities --overwrite
```

> These notebooks are **placeholders** — implement their logic (Databricks SDK / Genie APIs)
> before the `generate-dab` and `sync-genie-space` skills will do real work.

## 5. Install the Genie Code skills

Install the skills under `00_skills/` at the location Genie Code loads from
(`/Workspace/.assistance/skills/`):

```bash
databricks workspace import-dir 00_skills /Workspace/.assistance/skills --overwrite
```

## 6. Install the CI/CD helper tools

The pipeline uses `dab_prehook` and `metric_view_deploy` from the `bi-tools` package.
CI installs these automatically (`pip install ./00_tools`), but implement their logic
(currently placeholders) before relying on the pipeline for real validation/deploys.

## 7. Configure the DAB deployment target

Edit each domain's `databricks.yml` (and `01_shared_metric_views/databricks.yml`) so the
`presentation` target points at the customer workspace:

- `workspace.host` — replace `https://<your-workspace>.cloud.databricks.com` with the real URL.
- `workspace.root_path` — the path bundles deploy under.
- `permissions.group_name` — the admin group created in step 3.
- `variables.warehouse_id` — set (or override at deploy time) to the SQL warehouse id.

## 8. Configure GitHub Actions CI/CD

In the GitHub repo settings, add:

| Kind | Name | Value |
| --- | --- | --- |
| Variable | `DATABRICKS_HOST` | Workspace URL, e.g. `https://<workspace>.cloud.databricks.com` |
| Secret | `DATABRICKS_TOKEN` | A PAT / service-principal token with deploy rights |
| Environment | `presentation` | Guards the CD deploy jobs (add reviewers/protection as needed) |

Use a **service principal** (not a personal token) for `DATABRICKS_TOKEN` in production, and
grant it the same group membership/privileges as `bi-admins`.

## 9. Smoke test

1. Locally (or in a Git folder) run a validation against a sample domain:

   ```bash
   cd finance_operations
   dab_prehook
   databricks bundle validate
   ```

2. Open a small PR and confirm the **CI** workflow runs and comments results.
3. Merge to `master` and confirm the **CD** workflow deploys the changed bundle.

## Done

The environment is ready. Point BI developers at the **[User Guide](user-guide.md)** to start
building dashboards, genie agents and metric views.
