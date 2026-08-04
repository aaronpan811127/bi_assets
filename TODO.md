# TODO — open work to complete this reference implementation

Tracks what is left to finish the repo described in [`README.md`](README.md). Grouped by area.
Check items off as they land. "Done" items are listed at the bottom for context.

## Design

- [ ] Review whether the six ADRs cover every choice the README makes (e.g. "monorepo of
      domain bundles", "team catalog as incubator") — add a new numbered ADR for any decision
      that is implied but not yet recorded.
- [ ] Confirm `docs/design/images/architecture.png` matches the current three-repo layout
      (`00_setup`, `01_aibi_monorepo`, `02_dataplatform_repo`) and regenerate if stale.
- [ ] Sanity-check the high-level design against the actual folder structure so the docs and
      code agree (naming, targets, promotion path).

## Build

### Setup tooling (`00_setup/`) — currently all placeholders

- [ ] Implement `bi_tools/dab_prehook.py` — parse `databricks.yml`, assert
      `bundle.name == <folder name>`, and add the remaining rule-based validation checks
      (currently a stub).
- [ ] Implement `bi_tools/metric_view_deploy.py` — deploy metric views via the Databricks SDK
      (Unity Catalog metric views API); remove the `NotImplementedError` placeholder.
- [ ] Implement `notebooks/generate_dab.py` — DAB generation logic (currently raises
      `NotImplementedError`).
- [ ] Implement `notebooks/sync_genie_space.py` — Genie Space sync via the Databricks SDK /
      Genie API (currently raises `NotImplementedError`).
- [ ] Verify the `generate-dab` and `sync-genie-space` skills work end-to-end once their
      backing notebooks are implemented.
- [ ] Add tests for `bi_tools` (prehook validation + metric view deploy) so CI actually
      exercises them.

### Monorepo (`01_aibi_monorepo/`)

- [ ] Fix the `supply_chain` bundle: `databricks.yml` and `asset_objects.yaml` are named
      `data_governance` but the folder is `supply_chain` — align the bundle name with the folder.
- [ ] Remove the duplicate Genie agent file in `supply_chain/assets/genie_agents/`
      (`sample_agent.genie_space.json` vs `sample_agent.geniespace.json`) and keep one
      consistent extension across all domains.
- [ ] Make `supply_chain` match the standard domain layout: add
      `assets/metric_views/` and `resources/metric_views.yml`.
- [ ] Fill in the `data_platform` domain — its `assets/{dashboards,genie_agents,metric_views}/`
      folders only contain `.gitkeep`; add sample assets (or document why it is intentionally
      empty).
- [ ] Confirm every domain's `resources/*.yml` references assets that actually exist.

### Pipelines (CI/CD)

- [ ] End-to-end test the monorepo CI/CD (`.github/workflows/{ci,cd}.yml`) including
      `detect-changed-dabs.sh` against a real workspace.
- [ ] End-to-end test the `02_dataplatform_repo` CI/CD and confirm it deploys ahead of the
      domain bundles that depend on the shared metric views.
- [ ] Verify the `setup-databricks` composite action and required secrets/vars are documented.

## Documentation

- [ ] Keep the top-level `README.md` folder tree in sync as domains and guides are filled in.
- [ ] Document the `bi-tools` package publishing step referenced by the monorepo CI (where it
      is published, how CI installs it).
- [ ] Cross-link the finished `03_`–`05_` guides from `01_aibi_monorepo/user-guide.md` and the
      README once written.

## User guides (authoring guides) — not yet written

- [ ] Write `03_metric_views_guide/` — how to author metric views (currently only `.gitkeep`).
- [ ] Write `04_genie_agents_guide/` — how to author Genie agents (currently only `.gitkeep`).
- [ ] Write `05_dashboards_guide/` — how to author dashboards (currently only `.gitkeep`).
- [ ] Ensure each guide uses the matching sample assets in `01_aibi_monorepo/` as worked
      examples.

## Done (for reference)

- [x] Top-level `README.md` written and structured.
- [x] Six ADRs written and Accepted; `docs/design/ADRs/README.md` index in place.
- [x] `docs/design/high-level-design.md` written.
- [x] `01_aibi_monorepo/README.md` and `user-guide.md` written.
- [x] `02_dataplatform_repo/README.md` and shared metric views (`customer`, `product`) in place.
- [x] `00_setup/setup-guide.md` written.
- [x] `finance_operations` domain populated with sample dashboard, agent, and metric views.
- [x] CI/CD workflow scaffolding for both repos in place.
