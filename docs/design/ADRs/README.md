# Architecture Decision Records

Each ADR captures one design decision for the self-service BI platform: the
context, the options considered, the decision, and its rationale. They record the
"why" behind the [high-level design](../high-level-design.md).

| ADR | Decision |
|---|---|
| [0001](0001-two-repos-two-cadences.md) | Two repos, two cadences |
| [0002](0002-shared-workspace-per-team-catalogs.md) | One shared workspace, per-team catalogs |
| [0003](0003-team-catalog-as-incubator.md) | Team catalog as an incubator |
| [0004](0004-read-only-production-for-bi.md) | Read-only production data for BI |
| [0005](0005-consumers-strictly-read.md) | Consumers are strictly read-only |
| [0006](0006-cicd-only-path-to-production.md) | CI/CD is the only path to production |

## Format

Each ADR is a numbered Markdown file (`NNNN-short-title.md`) with: Status, Context,
Considered options, Decision, Rationale, and Consequences. New decisions get the
next number and are added to the table above.
