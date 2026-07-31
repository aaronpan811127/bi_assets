# 4. Read-only production data for BI

- Status: Accepted
- Deciders: Data platform team, BI teams
- Related: [high-level-design.md](../high-level-design.md#bi-developer)

## Context

BI developers build dashboards and Genie agents that must reflect real production
data. At the same time, the enterprise data platform team must retain sole control
over governed production data products. We need to decide what access BI
developers get to the Prod Catalog.

## Considered options

1. **No production access** — BI developers work only against copies or sample data
   in their team catalog.
2. **Read-only production access** — BI developers can read from the Prod Catalog
   but cannot write to it.
3. **Read + write production access** — BI developers can create or modify objects
   directly in the Prod Catalog.

## Decision

Adopt **option 2**: BI developers get **read-only** access to the **Prod Catalog**.

## Rationale

- Working only against copies (option 1) means dashboards can drift from production
  truth and forces error-prone data duplication.
- Write access to production (option 3) breaks the governance model — the platform
  team would no longer have sole control over governed data, and blast radius from
  BI mistakes would reach production.
- Read-only access lets dashboards and Genie agents reflect production truth while
  the platform team retains sole write control over governed data.

## Consequences

- New production-grade data products still flow through the incubation and transfer
  path in [ADR 3](0003-team-catalog-as-incubator.md), not by direct BI writes.
- BI developers must have write access somewhere for their own derived objects —
  that is their team catalog (see [ADR 2](0002-shared-workspace-per-team-catalogs.md)).
