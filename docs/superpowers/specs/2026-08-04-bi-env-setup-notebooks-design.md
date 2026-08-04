# Design — BI Dev & Consumption environment setup notebooks

Adds the provisioning automation that `00_setup/` is missing today. `00_setup/setup-guide.md`
currently tells an admin to create catalogs, groups and grants by hand with inline SQL, and its
object model predates
[detailed-design-bi-dev-consumption.md](../../design/detailed-design-bi-dev-consumption.md) — the
guide creates a `finance_operations` catalog with a `presentation` schema and a single
`bi-admins` group, while the design specifies `<domain>_team` catalogs with `prototype` /
`incubation` schemas and a two-layer group model. This work implements the **design's** model
and updates the guide to match.

## Goals

- One re-runnable, reviewable path to stand up the BI Development Env and the Consumption Env.
- Implement the design's access model exactly: entitlement groups carry no UC grants; UC access
  groups own the grants; entitlement groups are nested into them.
- Safe against live workspaces: dry-run by default, additive only, never revokes.

## Non-goals

Explicitly out of scope, and why:

| Not done here | Owner |
|---|---|
| `CAN_RUN` on published assets | CD, declared on the `presentation` target (ADR-0006). |
| Creating Prod catalog / schemas | Data Platform Env. These notebooks only grant read on what exists. |
| Importing `00_setup/notebooks/` and `00_setup/skills/` | Stays manual — steps 4–5 of `setup-guide.md`. |
| Fixing the `supply_chain` bundle-name mismatch | Tracked separately in `TODO.md`. |

## Architecture

Two admin notebooks, kept out of `00_setup/notebooks/` (that folder is agent-skill helpers
deployed to `/Workspace/shared_bi_utilities`; this is one-time provisioning):

```
00_setup/
├── env_setup/
│   ├── README.md                    # purpose, run order, required rights, smoke test
│   ├── environments.yml             # the one file an admin edits
│   ├── setup_bi_dev_env.py          # run FIRST  — owns UC + BI Dev workspace
│   └── setup_consumption_env.py     # run SECOND — Consumption workspace only
└── tools/bi_tools/
    └── env_plan.py                  # config resolution + planning (pure, unit-tested)
```

Each notebook is uploaded to the workspace it configures and run there, authenticating as the
admin's own identity from the notebook context. Planning logic lives in `bi_tools.env_plan` and
is imported by both notebooks, so the tested code is not in notebook cells and the two notebooks
cannot drift apart.

Both notebooks obtain `bi_tools` with a first cell running `%pip install "bi-tools>=0.1.0"`,
matching how the monorepo CI installs it (`setup-guide.md` step 6 publishes the package).
Because that publishing step may not have happened when an admin first runs these notebooks, the
cell falls back to a `%pip install` from a widget-supplied workspace path to the wheel, and fails
with a message pointing at step 6 if neither source resolves.

### Division of labour

Both workspaces share one metastore, so UC objects are created once, by the dev notebook.

| Concern | `setup_bi_dev_env` | `setup_consumption_env` |
|---|---|---|
| UC catalogs / schemas | `<domain>_team` + `prototype`, `incubation` | — |
| UC access groups + grants | `<domain>_team_rw`, `<domain>_team_read`, `prod_<domain>_read` | — |
| Entitlement group + nesting | `<domain>_developers` → `_team_rw`, `prod_<domain>_read` | `<domain>_consumers` → `_team_read`, `prod_<domain>_read` |
| Workspace entitlements | developers: workspace + SQL access | consumers: SQL access only |
| Consumption-only | — | `/Workspace/Shared/presentation_bi_assets` + per-domain dirs; warehouse `CAN_USE` |

## Configuration — `environments.yml`

Naming is template-driven with per-domain overrides, because the design's worked example uses
`prod_finance_read`, which does not fall out of `prod_{domain}_read`.

```yaml
naming:
  team_catalog:     "{domain}_team"
  team_schemas:     [prototype, incubation]
  developers_group: "{domain}_developers"
  consumers_group:  "{domain}_consumers"
  team_rw_group:    "{domain}_team_rw"
  team_read_group:  "{domain}_team_read"
  prod_read_group:  "prod_{domain}_read"

workspaces:
  bi_dev:
    host: https://<dev-workspace>.cloud.databricks.com
  consumption:
    host: https://<consumption-workspace>.cloud.databricks.com
    warehouse_id: ""                                  # consumers get CAN_USE
    assets_root: /Workspace/Shared/presentation_bi_assets

shared_groups:
  admins: bi-admins                                   # verified, never created here

domains:
  - name: finance_operations
    prod:
      catalog: prod_catalog
      schemas: [finance]
    # groups: { prod_read_group: prod_finance_read }  # optional override
  - name: supply_chain
    prod: { catalog: prod_catalog, schemas: [supply_chain] }
  - name: data_platform
    prod: { catalog: prod_catalog, schemas: [core] }
```

The three domains match `01_aibi_monorepo/` so the file is a working example as shipped. `host`
is informational for execution — each notebook runs inside its workspace — but is asserted
against the notebook's actual workspace URL so the consumption notebook cannot be run in the dev
workspace by mistake. The config path is a widget, defaulting to the notebook's own directory.

## Execution model

Both notebooks run the same five ordered phases; grants depend on objects, nesting depends on
groups.

1. **Load & validate config** — parse YAML, resolve naming templates and overrides to concrete
   names, assert required fields. All config errors are collected and raised together.
2. **Preflight** — assert the expected workspace; detect whether account-level auth is available;
   verify prerequisites exist (Prod catalog/schemas, warehouse, `bi-admins`).
3. **Plan** — diff desired against actual state, producing typed actions (`CREATE CATALOG`,
   `CREATE SCHEMA`, `GRANT`, `ADD MEMBER`, `SET ENTITLEMENT`, `MKDIRS`), each tagged
   `create` / `already-present` / `drift-warning`.
4. **Report** — print the plan grouped by domain, with counts.
5. **Apply** — only when the `apply` widget is `true`; otherwise print "dry run — nothing
   changed" and stop.

**Reconcile semantics:** additive only — create-if-missing, add-missing grants and members.
Never revoke, drop, or remove. Extra grants or members found in the workspace are reported as
`drift-warning` and left in place. The `apply` widget defaults to `false`, so "Run all" on a
fresh open is a no-op report.

**Groups:** Databricks groups are account-level. With account-level auth the notebook creates and
reconciles groups and nesting. Without it, the notebook verifies each required group exists and,
if any are missing, fails at the end of the plan phase with a copy-pasteable list of the groups
and memberships an account admin must create.

**Idempotency:** a second run of either notebook must plan zero `create` actions. This is the
primary acceptance criterion for the live paths.

## Error handling

| Tier | Example | Behaviour |
|---|---|---|
| Config error | empty `warehouse_id`, bad YAML, unknown key | Raised together at end of phase 1. Nothing touched. |
| Missing prerequisite or rights | Prod catalog absent, `bi-admins` missing, no account auth with groups missing, `PERMISSION_DENIED` in preflight | Fails at end of plan phase, listing what is missing and who must supply it (account admin / metastore admin / data platform team). Nothing touched. |
| Apply-time failure | one `GRANT` fails mid-run | Per-action try/except: record, continue remaining actions, then raise a summary of failed vs succeeded. |

Apply-phase failures deliberately do not abort the run. Halting on the first failure would leave
a half-built environment with no clear resume point; because every action is additive and
idempotent, "fix the cause and re-run" is the recovery path.

## Testing

Only the pure logic is unit tested; the SDK-calling apply layer is covered by a manual smoke
test, since mocking the SDK there would only test the mock. This adds the first `tests/`
directory for `bi_tools`, establishing the test setup that `TODO.md`'s existing "add tests for
`bi_tools`" item (about `dab_prehook` and `metric_view_deploy`) can then build on.

`pytest` tests in `00_setup/tools/tests/test_env_plan.py`:

- naming-template resolution, including per-domain overrides
- each config-validation error case
- plan construction against a faked current state (dict of existing catalogs / groups / grants),
  asserting correct `create` vs `already-present` vs `drift-warning`
- idempotency: planning against the state the first plan would produce yields zero creates

Manual smoke test, documented in `00_setup/env_setup/README.md`: dry-run in both workspaces →
apply in dev → apply in consumption → re-run both dry-run and confirm zero creates.

## Documentation changes

- `00_setup/setup-guide.md` — replace the hand-written SQL in steps 2 and 3 with the notebook
  workflow, and correct the object model to `<domain>_team` catalogs, `prototype` / `incubation`
  schemas, and the two-layer group model.
- Root `README.md` — add `env_setup/` to the `00_setup/` branch of the folder tree.
- `TODO.md` — add follow-ups discovered during implementation (the existing `bi_tools` tests item
  stays open; it covers `dab_prehook` / `metric_view_deploy`, not `env_plan`).

## Related

- [Detailed design — BI Development & Consumption Environments](../../design/detailed-design-bi-dev-consumption.md)
- ADRs [0002](../../design/ADRs/0002-shared-workspace-per-team-catalogs.md),
  [0004](../../design/ADRs/0004-read-only-production-for-bi.md),
  [0005](../../design/ADRs/0005-consumers-strictly-read.md),
  [0006](../../design/ADRs/0006-cicd-only-path-to-production.md)
