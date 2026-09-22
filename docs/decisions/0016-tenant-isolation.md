# 0016. Keep companies separate in one shared database

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
All companies' data lives in the same database, and every company-owned row is labeled with its company. Four independent layers make sure one company can never see or change another company's data, so a single bug is not enough to cause a leak.

## Context
Preventing cross-tenant access is the first goal in the security proposal. MySQL has no built-in row-level security, so isolation has to be enforced by the application and the schema. A separate database per company would isolate data strongly but multiplies migrations, connections, and backups for a two-person project.

## Decision
**Shared schema.** Every company-owned table has a non-null `company_id`.

**Layer 1: automatic filter.** A SQLAlchemy hook adds `company_id = <current company>` to every query on a company-owned model. The current company comes only from the server-side session, never from request data. Running such a query with no company set raises an error instead of returning all rows. Only platform code (clearly separated, and audited) may run cross-company queries.

**Layer 2: company-aware links.** Company-owned tables have a unique key on `(company_id, id)`, and references between company-owned tables use composite foreign keys that include `company_id`. The database itself then rejects a row that points at another company's data.

**Layer 3: tests.**
- A security test suite seeds at least two companies and, for every endpoint, requests the other company's records as a signed-in user. Each must behave as if the record does not exist.
- A test fails if any model with a `company_id` column is not covered by the automatic filter.

**Layer 4: "not found", not "forbidden".** Requests for another company's records return 404, so responses do not reveal which IDs exist.

**Accounts.** A user account belongs to exactly one company. A person working for two companies has two accounts. Platform personnel are stored separately and never belong to a company (support access is a separate, audited mechanism).

## Consequences
- The automatic filter must be documented clearly (`docs/architecture/tenancy.md` in the backend), because it is invisible in individual queries.
- Composite keys make company-owned foreign keys wider.
- Background jobs must set the company explicitly for each unit of work.

## Alternatives considered
- **Database per company:** strongest isolation, much more operational work.
- **Filtering by hand in every query:** one forgotten filter becomes a data leak.
- **Database views per company:** MySQL views cannot take the session's company as a parameter safely; complicated for little gain.
