# 3. Team catalog as an incubator

- Status: Accepted
- Deciders: Data platform team, BI teams
- Related: [high-level-design.md](../high-level-design.md#bi-development-env)

## Context

BI developers and citizen developers often need to create new data products and
semantic models (tables, views, metric views) to build their dashboards and Genie
agents. Some of these are throwaway experiments; others turn out to be valuable
enough to become governed, enterprise-wide assets. We need a path that lets teams
move fast without either blocking on the data platform team or creating permanent
ungoverned shadow data.

## Considered options

1. **All data products must be created by the data platform team** — BI developers
   file a request and wait for a governed asset in the Prod Catalog.
2. **Team catalog as an incubator** — teams create data products and semantic
   models in their own team catalog first, then transfer production-worthy ones to
   the Data Platform catalog.
3. **Permanent self-service** — teams create and keep data products in their team
   catalog indefinitely, with no graduation path to the governed platform.

## Decision

Adopt **option 2**: teams **prototype in their team catalog first**, and
**transfer** enterprise-ready or production-worthy assets to the Data Platform
catalog for governed ownership.

## Rationale

- Requiring the platform team to create everything (option 1) reintroduces the
  bottleneck that self-service exists to remove.
- Permanent self-service (option 3) leads to ungoverned shadow data: valuable
  assets stay outside the enterprise semantic layer, with no ownership, lineage, or
  quality guarantees.
- The incubator model gives a fast, low-governance space to prototype and a clear
  graduation route from experiment to governed enterprise asset — self-service
  without permanent shadow data.

## Consequences

- A transfer/graduation process (ownership handoff to the data platform team) must
  exist and be maintained.
- Assets in a team catalog are understood to be pre-production until graduated.
- Reinforces [ADR 2](0002-shared-workspace-per-team-catalogs.md): the team catalog
  is both the isolation boundary and the incubation space.
