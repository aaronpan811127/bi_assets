# Setup Guide

One-time steps for an **administrator** to stand up the **`aibi_monorepo`** repo in a new
customer environment, before BI developers can follow the
[User Guide](../01_aibi_monorepo/user-guide.md).

> Audience: platform / workspace admin. Developers do **not** need to do any of this.
>
> This `00_setup/` folder is the setup tooling — notebooks, Genie Code skills, and the
> `bi-tools` package. It is **not** part of the customer's `aibi_monorepo` repo; it is used
> once to configure the environment that repo runs in.

## Prerequisites

- A Databricks workspace with **Unity Catalog** enabled.
- Workspace admin (or metastore admin) rights to create catalogs, schemas, groups and grants.
- A running **SQL warehouse** to back dashboards and genie spaces.
- Git provider access (this repo lives on GitHub) and permission to add repo secrets.
- Local tooling for the person running CLI steps: `git`, the
  [Databricks CLI](https://docs.databricks.com/dev-tools/cli/) (v0.240+), and Python 3.10+.

## 1. Create the `aibi_monorepo` repo in the customer org

1. Create a repo from the contents of `01_aibi_monorepo/` in the customer's GitHub org.
2. Add it as a **Databricks Git folder** (Repos) in the workspace so Genie Code can edit it.

## 2. Create Unity Catalog objects

The workspace is shared across teams, but **each team owns its own team catalog** so assets,
data, and grants stay isolated. Create one catalog/schema per team/domain (names should match
the `catalog`/`schema` used in the domain's generated resources):

```sql
-- Example for the finance_operations team catalog
CREATE CATALOG IF NOT EXISTS finance_operations;
CREATE SCHEMA  IF NOT EXISTS finance_operations.presentation;
-- Repeat for supply_chain, data_platform, and any future team/domain.
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
of `00_setup/notebooks/` to the path the skills expect (default `/Workspace/shared_bi_utilities`):

```bash
databricks workspace import-dir 00_setup/notebooks /Workspace/shared_bi_utilities --overwrite
```

> These notebooks are **placeholders** — implement their logic (Databricks SDK / Genie APIs)
> before the `generate-dab` and `sync-genie-space` skills will do real work.

## 5. Install the Genie Code skills

Install the skills under `00_setup/skills/` at the location Genie Code loads from
(`/Workspace/.assistance/skills/`):

```bash
databricks workspace import-dir 00_setup/skills /Workspace/.assistance/skills --overwrite
```

## 6. Publish the CI/CD helper tools

The `aibi_monorepo` pipeline uses `dab_prehook` and `metric_view_deploy` from the `bi-tools`
package, installed in CI via `pip install "bi-tools>=0.1.0"`. Build and publish it from
`00_setup/tools/` to the index the pipeline can reach (PyPI or an internal index):

```bash
pip install build
python -m build 00_setup/tools          # produces a wheel + sdist in 00_setup/tools/dist/
# then upload dist/* to your package index (e.g. twine upload ...)
```

> The tools are **placeholders** — implement their logic before relying on the pipeline for
> real validation/deploys. During development you can instead `pip install ./00_setup/tools`.

## 7. Configure the DAB deployment target

Edit each domain's `databricks.yml` (and `02_dataplatform_repo/databricks.yml`) so the
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

The environment is ready. Point BI developers at the
**[User Guide](../01_aibi_monorepo/user-guide.md)** to start building dashboards, genie agents
and metric views.
