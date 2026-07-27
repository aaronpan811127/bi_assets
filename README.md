# Self-serve BI Assets — workspace

This workspace has two independent parts:

| Folder | What it is | Audience |
| --- | --- | --- |
| [`01_aibi_monorepo/`](01_aibi_monorepo/) | The **self-serve BI monorepo** — domain bundles (dashboards, genie agents, metric views), the shared metric views bundle, and the CI/CD pipeline. Treated as its own repo in the customer org. | BI developers |
| [`00_setup/`](00_setup/) | **Setup tooling** used once to stand up `aibi_monorepo` in a customer environment — the admin [setup guide](00_setup/setup-guide.md), Genie Code notebooks & skills, and the `bi-tools` CI package. | Platform / workspace admins |

## Where to start

- 🛠️ **Standing up a new customer environment?** Follow **[`00_setup/setup-guide.md`](00_setup/setup-guide.md)**.
- 📖 **Developing BI assets?** See **[`01_aibi_monorepo/README.md`](01_aibi_monorepo/README.md)** and its [user guide](01_aibi_monorepo/user-guide.md).

## Folder structure

```text
bi_assets/                             (this dev workspace)
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
└── 01_aibi_monorepo/                  # the independent BI monorepo (customer runs this day-to-day)
    ├── README.md                      #   monorepo docs
    ├── user-guide.md                  #   getting-started guide & Genie Code cheat sheet
    ├── .gitignore
    ├── .github/                       #   CI/CD pipeline (GitHub Actions)
    │   ├── workflows/{ci.yml,cd.yml}
    │   ├── actions/setup-databricks/action.yml
    │   └── scripts/detect-changed-dabs.sh
    ├── shared_metric_views/           #   metric views shared across domains (manual)
    ├── finance_operations/            #   domain bundle
    └── supply_chain/                  #   domain bundle
```

## How the two parts relate

`00_setup/` is used once by an admin to configure a customer environment: it deploys the
`notebooks/` and `skills/` into the workspace (so Genie Code can generate and sync assets) and
publishes the `bi-tools` package (so the monorepo's CI can install `dab_prehook` and
`metric_view_deploy`). After that, all day-to-day work happens inside `01_aibi_monorepo/`,
which is self-contained and validated/deployed by its own pipeline.
