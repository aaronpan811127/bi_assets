"""bi_tools — CI/CD helper commands for the self-serve BI monorepo.

Exposes two console scripts (see pyproject.toml):

    dab_prehook        rule-based config validation for a DAB bundle
    metric_view_deploy deploy metric views for a bundle

Both are PLACEHOLDERS — they implement argument handling and a runnable skeleton,
but the real validation / deployment logic is stubbed out with TODOs.
"""

__version__ = "0.1.0"
