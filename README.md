# Databricks Enterprise Self-Service BI Reference Implementation

This is an **opinionated reference implementation of a self-service BI environment on the
Databricks platform**. It is not a product or a framework — it is a worked example, complete
with **reference architecture, design, working code, and user guides**, that a team
can read, adapt, and adopt to stand up self-service BI in their own Databricks account.

It is opinionated on purpose: rather than cataloguing every option, it makes concrete choices
(shared BI development workspace, per-team Unity Catalog isolation, monorepo of domain bundles,
CI/CD-only promotion) and documents *why* each choice was made in the [ADRs](docs/design/ADRs/README.md)
so you can accept a default or knowingly diverge from it.

## Why this exists — the problem it solves

Enterprises want business domains and citizen developers to build and ship their own BI assets
(dashboards, Genie agents, metric views) **without waiting on the central data platform team**.
Done ad hoc, that self-service quickly turns into a mess:

- **No isolation.** Teams step on each other's data and grants in shared catalogs, or the org
  sprawls into an unmanageable number of one-off workspaces.
- **Ungoverned shadow data.** Prototypes never graduate to governed, owned assets, so critical
  reports run on data nobody stands behind.
- **Unsafe promotion.** Assets reach production by hand-editing, with no review, audit trail, or
  repeatable path — and BI work gets coupled to the slow, high-blast-radius data platform release
  cycle.
- **No shared blueprint.** Every team reinvents structure, tooling, and CI/CD, and there is no
  written record of why the environment is laid out the way it is.

This reference implementation answers those problems with a single opinionated blueprint: one
**shared BI development workspace** with **per-team Unity Catalog isolation** (each team owns its
own catalog, so assets, data, and grants never mix), a **team-catalog-as-incubator** path that
graduates prototypes into the governed data platform, and **CI/CD as the only path to
production** — all captured as architecture docs, ADRs, runnable code (DABs + pipelines), and
step-by-step authoring guides.

## Why it matters — accelerating adoption and scale

The point of this blueprint is to **accelerate the adoption and scale of Databricks BI products**
— AI/BI Dashboards, Genie, and Metric Views — across an enterprise, by removing the setup,
governance, and CI/CD questions that every team would otherwise have to answer from scratch.
That creates value on both sides:

### For the customer

- **Shortens time-to-first-dashboard.** A new domain team gets a proven workspace layout,
  catalog isolation, tooling, and pipeline on day one instead of spending weeks designing them.
- **Scales to many teams without sprawl.** Per-team catalog isolation and a monorepo of domain
  bundles let the environment grow to dozens of domains while staying governed and maintainable.
- **Encodes the paved road.** The opinionated defaults and ADRs give every team a consistent,
  well-reasoned starting point, so good practice scales by copy-and-adapt rather than tribal
  knowledge.
- **Governance without slowing teams down.** Self-service authoring and CI/CD-only promotion
  give the platform team control and auditability while domain teams keep shipping fast.

### For Databricks

- **Drives adoption of Databricks BI products.** Lowering the barrier to safely author and ship
  Dashboards, Genie agents, and Metric Views means more of the business builds on the Databricks
  Data Intelligence Platform rather than external BI tools.
- **Deepens platform consumption.** More teams building governed BI on Unity Catalog increases
  usage of Databricks compute, storage, and the semantic layer — expanding the footprint within
  each account.
- **A repeatable field asset.** The same blueprint can be reused across customers to
  short-circuit "how should we structure self-service BI?" engagements and accelerate landing
  and expansion.

The implementation is organised into three independent **repos/tooling parts**, a set of
**asset-authoring guides**, and the **architecture docs**:

| Folder | What it is | Audience |
| --- | --- | --- |
| [`00_setup/`](00_setup/) | **Setup tooling** used once to stand up `aibi_monorepo` in a customer environment — the admin [setup guide](00_setup/setup-guide.md), Genie Code notebooks & skills, and the `bi-tools` CI package. | Platform / workspace admins |
| [`01_aibi_monorepo/`](01_aibi_monorepo/) | The **self-serve BI monorepo** — domain bundles (dashboards, genie agents, metric views) and the CI/CD pipeline. Treated as its own repo in the customer org. | BI developers / Platform |
| [`02_dataplatform_repo/`](02_dataplatform_repo/) | The **shared metric views bundle** — metric views shared across domains, with its own CI/CD pipeline. Treated as its own repo, deployed before domain bundles that depend on it. | Data platform team / Platform |
| [`03_metric_views_guide/`](03_metric_views_guide/) | Authoring guide for **metric views**. | BI developers / Data Engineers |
| [`04_genie_agents_guide/`](04_genie_agents_guide/) | Authoring guide for **genie agents**. | BI developers |
| [`05_dashboards_guide/`](05_dashboards_guide/) | Authoring guide for **dashboards**. | BI developers |
| [`docs/`](docs/) | **Architecture docs** — the [high-level design](docs/design/high-level-design.md) and the [ADRs](docs/design/ADRs/README.md) recording each design decision. | Architects / anyone onboarding |

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

`00_setup/` is used once by an admin to configure a customer environment: it deploys the
`notebooks/` and `skills/` into the workspace (so Genie Code can generate and sync assets) and
publishes the `bi-tools` package (so the monorepo's CI can install `dab_prehook` and
`metric_view_deploy`). After that, all day-to-day work happens inside `01_aibi_monorepo/`,
which is self-contained and validated/deployed by its own pipeline.

`02_dataplatform_repo/` holds the metric views shared by more than one domain. It is its own
repo with the same CI/CD pattern, deployed independently of (and ahead of) the domain bundles
in `01_aibi_monorepo/` that depend on those shared metric views.

The `03_`–`05_` guides document how to author each asset type (metric views, genie agents,
dashboards). `docs/design/` records the architecture: the [high-level design](docs/design/high-level-design.md)
and the [ADRs](docs/design/ADRs/README.md) that capture each design decision and its rationale.
