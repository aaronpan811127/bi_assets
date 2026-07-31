# 5. Consumers are strictly read-only

- Status: Accepted
- Deciders: Data platform team, BI teams
- Related: [high-level-design.md](../high-level-design.md#consumption-env)

## Context

Business end users consume finished BI assets — viewing dashboards and querying
Genie agents. We need to decide what surface they access and what they can do,
balancing ease of consumption against keeping authoring and governance surfaces
protected.

## Considered options

1. **Consumers use the shared BI Development Workspace** — end users view assets in
   the same workspace where BI developers build them.
2. **Dedicated Consumption Workspace, consumer-only entitlement** — a separate
   workspace hosting only published, production-grade assets, with read-only
   consumer access.
3. **Direct catalog access for consumers** — end users query the Prod/Team catalogs
   directly with read grants, without a curated consumption surface.

## Decision

Adopt **option 2**: a dedicated **Consumption Workspace** with a **consumer-only
entitlement** (read/view only).

## Rationale

- Letting consumers into the development workspace (option 1) exposes authoring
  surfaces and half-finished assets to end users and blurs the promotion boundary.
- Direct catalog access (option 3) gives no curated, production-grade surface and
  pushes governance onto every consumer grant.
- A dedicated consumption surface with a consumer-only entitlement keeps end users
  away from any authoring surface and gives the platform team a clean, well-defined
  promotion target.

## Consequences

- Assets reach consumers only via CI/CD promotion into the Consumption Workspace
  (see [ADR 6](0006-cicd-only-path-to-production.md)).
- Consumers have no write access anywhere and no access to development or platform
  environments.
