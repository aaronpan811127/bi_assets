# 2. One shared workspace, per-team catalogs

- Status: Accepted
- Deciders: Data platform team, BI teams
- Related: [high-level-design.md](../high-level-design.md#bi-development-env)

## Context

Multiple business domains and teams — finance operations, supply chain, the data
platform team, and future domains — all need a place to develop BI assets. We must
decide how to give each team an isolated build surface without multiplying the
operational overhead of standing up and maintaining environments.

## Considered options

1. **A separate BI development workspace per team** — each team gets its own
   Databricks workspace.
2. **One shared workspace, isolation via per-team Unity Catalog catalogs** — a
   single BI Development Workspace shared by all teams, with each team owning its
   own team catalog.
3. **One shared workspace and one shared catalog** — all teams share both, relying
   on schema-level or naming conventions for separation.

## Decision

Adopt **option 2**: a single shared **BI Development Workspace**, with **every team
owning its own team catalog** in Unity Catalog.

## Rationale

- A workspace per team (option 1) duplicates setup, tooling, Genie Code skills, and
  CI/CD wiring for every team — high operational cost that grows with each new
  domain.
- A shared catalog (option 3) provides no real isolation boundary: a team's tables,
  views, and grants could collide with another's, and access control becomes a
  fragile convention rather than an enforced boundary.
- Sharing the workspace keeps tooling and onboarding in one place, while the team
  catalog is the natural Unity Catalog isolation boundary — data products, semantic
  models, and grants stay scoped to a team and never cross into another's.

## Consequences

- New teams onboard by getting a catalog and grants, not a whole new workspace.
- Workspace-level resources (compute, skills, config) are shared and must be sized
  for aggregate use.
- Per-team write access is scoped to the team's own catalog; see the access matrix
  in the [high-level design](../high-level-design.md#access-matrix).
