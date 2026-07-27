# Self-serve BI Assets — workspace

This workspace has two independent parts:

| Folder | What it is | Audience |
| --- | --- | --- |
| [`01_aibi_monorepo/`](01_aibi_monorepo/) | The **self-serve BI monorepo** — domain bundles (dashboards, genie agents, metric views), the shared metric views bundle, and the CI/CD pipeline. Treated as its own repo in the customer org. | BI developers |
| [`00_setup/`](00_setup/) | **Setup tooling** used once to stand up `aibi_monorepo` in a customer environment — the admin [setup guide](00_setup/setup-guide.md), Genie Code notebooks & skills, and the `bi-tools` CI package. | Platform / workspace admins |

## Where to start

- 🛠️ **Standing up a new customer environment?** Follow **[`00_setup/setup-guide.md`](00_setup/setup-guide.md)**.
- 📖 **Developing BI assets?** See **[`01_aibi_monorepo/README.md`](01_aibi_monorepo/README.md)** and its user guide.

## How the two parts relate

```text
bi_assets/                     (this dev workspace)
├── 00_setup/                  setup tooling — configures the environment ONCE
│   ├── setup-guide.md
│   ├── notebooks/             utilities called by the Genie Code skills
│   ├── skills/                Genie Code skills (generate-dab, sync-genie-space)
│   └── tools/                 bi-tools package (dab_prehook, metric_view_deploy) → published for CI
│
└── 01_aibi_monorepo/          the independent BI monorepo (what the customer runs day-to-day)
    ├── .github/               CI/CD pipeline
    ├── user-guide.md
    ├── shared_metric_views/   metric views shared across domains
    ├── finance_operations/    domain bundle
    └── supply_chain/          domain bundle
```

`00_setup/` deploys the notebooks/skills into the workspace and publishes `bi-tools`, so the
`aibi_monorepo` repo can be developed via Genie Code and validated/deployed by its own pipeline.
