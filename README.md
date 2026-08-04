# Databricks Enterprise Self-Service BI Reference Implementation

This is a **worked example of a self-service BI setup on Databricks**. It is not a product or a
framework — it is a complete example, with **architecture, design, working code, and user
guides**, that a team can read, adapt, and use to set up self-service BI in their own Databricks
account.

It makes specific choices on purpose (a shared BI development workspace, one Unity Catalog per
team, a monorepo of domain bundles, and CI/CD as the only way to reach production) and explains
*why* in the [ADRs](docs/design/ADRs/README.md), so you can take a default as-is or change it on
purpose.

## Why this exists — the problem it solves

Companies want business teams and non-specialist developers to build and ship their own BI
assets (dashboards, Genie agents, metric views) **without waiting on the central data platform
team**. Without structure, that quickly gets messy:

- **No isolation.** Teams overwrite each other's data and grants in shared catalogs, or the org
  ends up with too many one-off workspaces to manage.
- **Ungoverned data.** Prototypes never become owned, governed assets, so important reports run
  on data nobody is responsible for.
- **Unsafe promotion.** Assets reach production by hand, with no review, audit trail, or repeatable
  path — and BI work gets tied to the slow, risky data platform release cycle.
- **No shared blueprint.** Every team reinvents the structure, tooling, and CI/CD, and nobody
  writes down why the environment is set up the way it is.

This reference implementation solves those problems with one clear blueprint: a **shared BI
development workspace** where **each team gets its own Unity Catalog** (so assets, data, and
grants never mix), a path that turns team prototypes into governed data platform assets, and
**CI/CD as the only way to reach production** — all captured as architecture docs, ADRs, runnable
code (DABs and pipelines), and step-by-step authoring guides.

## Why it matters — driving adoption and scale

This blueprint helps teams **adopt and scale Databricks BI products** — AI/BI Dashboards, Genie,
and Metric Views — across a company by answering the setup, governance, and CI/CD questions up
front, so each team doesn't have to. That helps both sides:

### For the customer

- **Faster first dashboard.** A new team gets a proven workspace layout, catalog isolation,
  tooling, and pipeline on day one instead of spending weeks building them.
- **Scales to many teams without sprawl.** One catalog per team and a monorepo of domain bundles
  let the environment grow to dozens of teams while staying governed and easy to maintain.
- **A paved road.** The defaults and ADRs give every team a consistent, well-reasoned starting
  point, so good practice spreads by copy-and-adapt instead of word of mouth.
- **Governance without slowing teams down.** Self-service authoring plus CI/CD-only promotion
  give the platform team control and auditability while teams keep shipping fast.

### For Databricks

- **More adoption of Databricks BI products.** Making it easier to safely build and ship
  Dashboards, Genie agents, and Metric Views means more of the business builds on the Databricks
  Data Intelligence Platform instead of outside BI tools.
- **More platform usage.** More teams building governed BI on Unity Catalog means more use of
  Databricks compute, storage, and the semantic layer in each account.
- **A reusable field asset.** The same blueprint works across customers, so it saves time on
  "how should we structure self-service BI?" and helps land and expand accounts.

The implementation is split into three independent **repos/tooling parts**, a set of
**authoring guides**, and the **architecture docs**:

| Folder | What it is | Audience |
| --- | --- | --- |
| [`00_setup/`](00_setup/) | **Setup tooling** used once to set up `aibi_monorepo` in a customer environment — the admin [setup guide](00_setup/setup-guide.md), Genie Code notebooks and skills, and the `bi-tools` CI package. | Platform / workspace admins |
| [`01_aibi_monorepo/`](01_aibi_monorepo/) | The **self-serve BI monorepo** — domain bundles (dashboards, genie agents, metric views) and the CI/CD pipeline. Its own repo in the customer org. | BI developers / Platform |
| [`02_dataplatform_repo/`](02_dataplatform_repo/) | The **shared metric views bundle** — metric views used by more than one domain, with its own CI/CD pipeline. Its own repo, deployed before the domain bundles that depend on it. | Data platform team / Platform |
| [`03_metric_views_guide/`](03_metric_views_guide/) | Authoring guide for **metric views**. | BI developers / Data Engineers |
| [`04_genie_agents_guide/`](04_genie_agents_guide/) | Authoring guide for **genie agents**. | BI developers |
| [`05_dashboards_guide/`](05_dashboards_guide/) | Authoring guide for **dashboards**. | BI developers |
| [`docs/`](docs/) | **Architecture docs** — the [high-level design](docs/design/high-level-design.md) and the [ADRs](docs/design/ADRs/README.md) that record each design decision. | Architects / anyone onboarding |

## Where to start

- 🧭 **Understanding the architecture?** Read **[`docs/design/high-level-design.md`](docs/design/high-level-design.md)** and the **[ADRs](docs/design/ADRs/README.md)**.
- 🛠️ **Standing up a new customer environment?** Follow **[`00_setup/setup-guide.md`](00_setup/setup-guide.md)**.
- 📖 **Developing BI assets?** See **[`01_aibi_monorepo/README.md`](01_aibi_monorepo/README.md)** and its [user guide](01_aibi_monorepo/user-guide.md).

## Folder structure

```text
databricks-selfservice-bi-reference/   (this reference implementation)
├── README.md                          # this file
├── .gitignore
│
├── 00_setup/                          # setup tooling — configures the environment ONCE (admins)
│   ├── setup-guide.md                 #   one-time admin steps for a new customer environment
│   ├── notebooks/                     #   utilities called by the Genie Code skills
│   │   ├── README.md
│   │   ├── generate_dab.py
│   │   └── sync_genie_space.py
│   ├── skills/                        #   Genie Code skills (call notebooks/)
│   │   ├── generate-dab/SKILL.md
│   │   └── sync-genie-space/SKILL.md
│   └── tools/                         #   bi-tools package → published for the monorepo's CI
│       ├── README.md
│       ├── pyproject.toml
│       └── bi_tools/
│           ├── dab_prehook.py         #     rule-based config validation (CI + CD)
│           └── metric_view_deploy.py  #     deploy metric views (CD)
│
├── 01_aibi_monorepo/                  # the independent BI monorepo (customer runs this day-to-day)
│   ├── README.md                      #   monorepo docs
│   ├── user-guide.md                  #   getting-started guide & Genie Code cheat sheet
│   ├── .gitignore
│   ├── .github/                       #   CI/CD pipeline (GitHub Actions)
│   │   ├── workflows/{ci.yml,cd.yml}
│   │   ├── actions/setup-databricks/action.yml
│   │   └── scripts/detect-changed-dabs.sh
│   ├── finance_operations/            #   domain bundle
│   │   ├── assets/{dashboards,genie_agents,metric_views}/
│   │   ├── resources/{dashboards,genie_agents,metric_views}.yml
│   │   └── databricks.yml
│   ├── supply_chain/                  #   domain bundle (same layout)
│   └── data_platform/                 #   domain bundle (same layout)
│
├── 02_dataplatform_repo/              # shared metric views bundle (its own repo)
│   ├── .gitignore
│   ├── README.md
│   ├── .github/                       #   CI/CD pipeline (GitHub Actions)
│   │   ├── workflows/{ci.yml,cd.yml}
│   │   └── actions/setup-databricks/action.yml
│   ├── assets/metric_views/*.metric_view.yml  # shared metric views (manual)
│   ├── resources/metric_views.yml     #   Databricks shared metric view definitions
│   └── databricks.yml                 #   bundle entrypoint
│
├── 03_metric_views_guide/             # authoring guide: metric views
├── 04_genie_agents_guide/             # authoring guide: genie agents
├── 05_dashboards_guide/               # authoring guide: dashboards
│
└── docs/                              # architecture docs
    └── design/
        ├── high-level-design.md       #   environments, personas, git repos
        ├── ADRs/                      #   one numbered ADR per design decision
        │   ├── README.md
        │   └── 000N-*.md
        └── images/architecture.png    #   topology diagram
```

## How the parts relate

An admin runs `00_setup/` once to set up a customer environment: it deploys the `notebooks/` and
`skills/` into the workspace (so Genie Code can generate and sync assets) and publishes the
`bi-tools` package (so the monorepo's CI can install `dab_prehook` and `metric_view_deploy`).
After that, all day-to-day work happens inside `01_aibi_monorepo/`, which is self-contained and
validated and deployed by its own pipeline.

`02_dataplatform_repo/` holds the metric views used by more than one domain. It is its own repo
with the same CI/CD pattern, deployed separately from — and before — the domain bundles in
`01_aibi_monorepo/` that depend on those shared metric views.

The `03_`–`05_` guides show how to author each asset type (metric views, genie agents,
dashboards). `docs/design/` records the architecture: the [high-level design](docs/design/high-level-design.md)
and the [ADRs](docs/design/ADRs/README.md) that capture each design decision and why it was made.
