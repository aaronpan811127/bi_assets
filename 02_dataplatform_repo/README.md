# Data Platform — shared metric views

A standalone Databricks Asset Bundle for the **metric views shared across domains**. It is
treated as its own repo in the customer org, separate from `01_aibi_monorepo/`.

Shared metric views are manually maintained here. When the monorepo's `generate-dab` skill
generates a domain bundle, it only creates domain-specific metric views — anything declared as
a shared metric view is skipped, because it belongs to this bundle instead.

## Folder structure

```text
02_dataplatform_repo/
├── README.md
├── .gitignore
├── .github/                        # CI/CD pipeline (GitHub Actions)
│   ├── workflows/
│   │   ├── ci.yml                  # pull_request → validate the bundle
│   │   └── cd.yml                  # push to master → deploy the bundle
│   └── actions/
│       └── setup-databricks/       # composite action: install + auth the Databricks CLI
│           └── action.yml
├── assets/
│   └── metric_views/*.metric_view.yml  # ✍️  edit: shared metric view definitions
├── resources/
│   └── metric_views.yml            # ✍️  edit: Databricks shared metric view definitions
└── databricks.yml                  # bundle entrypoint
```

## CI/CD Pipeline

CI/CD runs on **GitHub Actions** (`.github/workflows/`). This repo is a single DAB bundle
rooted at the repo root, so — unlike the monorepo — there is no per-folder change detection.

The `dab_prehook` and `metric_view_deploy` steps come from the `bi-tools` package (published by
the `00_setup` setup process), installed via `pip install "bi-tools>=0.1.0"` by the
`setup-databricks` composite action.

### CI Behaviour

Defined in `.github/workflows/ci.yml`, triggered on pull requests to `master`.

- `dab_prehook` — rule-based config validation
- `databricks bundle validate` — schema and config validation
- `databricks bundle plan` — shows planned changes without applying

### CD Behaviour

Defined in `.github/workflows/cd.yml`, triggered on pushes (merges) to `master`.

- `dab_prehook` — rule-based config validation
- `databricks bundle validate` — schema and config validation
- `metric_view_deploy` — deploy the shared metric views

Shared metric views must be deployed **before** any domain bundle in `01_aibi_monorepo/` that
depends on them, since those domain assets may reference the shared metric views.
