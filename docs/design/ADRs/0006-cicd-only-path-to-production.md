# 6. CI/CD is the only path to production

- Status: Accepted
- Deciders: Data platform team, BI teams, Platform engineers
- Related: [high-level-design.md](../high-level-design.md#git-repositories)

## Context

Both the data platform and BI asset flows promote work into higher environments
(Stg, Prod, Consumption). We need to decide how changes reach those promoted
environments and how standards and policies are enforced along the way.

## Considered options

1. **Manual promotion** — engineers hand-edit or hand-deploy to Stg/Prod and the
   Consumption Workspace as needed.
2. **CI/CD-only promotion** — every change to a promoted environment flows through
   a pipeline driven from its Git repo, with standards enforced by automation and
   review.
3. **Hybrid** — CI/CD for routine changes, with a documented manual override for
   urgent fixes.

## Decision

Adopt **option 2**: **CI/CD is the only writer** of Stg, Prod, and the Consumption
Workspace. No persona hand-edits a promoted environment.

## Rationale

- Manual promotion (option 1) has no reliable audit trail, is easy to get wrong,
  and lets un-reviewed changes reach production.
- A hybrid with manual overrides (option 3) tends to normalise the override path;
  the "emergency" edit becomes routine and erodes the guarantee.
- Pipeline-only promotion makes the Git repo the single source of truth, enforces
  standards and policies through automation and review, and gives platform
  engineers a clean, auditable promotion mechanism they own.

## Consequences

- Platform engineers own the promotion pipelines and pipeline configuration for
  both the Data platform repo and the BI asset repo.
- Getting a change to production requires committing to the appropriate repo — see
  [ADR 1](0001-two-repos-two-cadences.md).
- Breakglass/emergency changes, if ever needed, must be an explicit, audited
  exception rather than a standing capability.
