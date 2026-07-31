# 1. Two repos, two cadences

- Status: Accepted
- Deciders: Data platform team, BI teams
- Related: [high-level-design.md](../high-level-design.md#git-repositories)

## Context

BI assets (dashboards, Genie agents, metric views) and the enterprise data
platform (pipelines, medallion tables, data products, semantic layer) evolve at
very different speeds and carry very different blast radii. BI teams want to ship
a dashboard tweak in minutes; a change to a governed production data product must
move slowly through Dev → Stg → Prod. We need to decide how source control is
organised across these two kinds of work.

## Considered options

1. **One monorepo for everything** — data platform code and BI assets share a
   single repo and CI/CD pipeline.
2. **Two independent repos** — a Data platform repo and a BI asset repo, each with
   its own CI/CD promotion flow.
3. **A repo per team** — every domain team gets its own standalone repo for both
   its data and BI work.

## Decision

Adopt **option 2**: split source control into a **Data platform repo** and a **BI
asset repo**, each the source of truth for its own environment and CI/CD flow.

## Rationale

- A single monorepo (option 1) couples the two release cadences: every BI change
  would ride the data platform's slower, higher-governance pipeline, defeating the
  self-service goal.
- A repo per team (option 3) fragments shared tooling, CI/CD, and standards, and
  makes shared assets (e.g. cross-domain metric views) hard to home.
- Two repos give the fast-moving BI work its own low-friction cadence while keeping
  the high-blast-radius platform work behind a hardened pipeline — the boundary
  matches the real difference in risk and speed.

## Consequences

- BI teams ship on their own schedule without waiting on the data platform release
  cycle.
- Cross-repo dependencies (BI assets reading platform data) must be managed
  explicitly rather than resolved within a single build.
- See [ADR 6](0006-cicd-only-path-to-production.md) for how promotion is governed
  in each repo.
