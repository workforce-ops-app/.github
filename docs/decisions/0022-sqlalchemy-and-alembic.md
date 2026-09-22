# 0022. SQLAlchemy 2.0 and Alembic for database access

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
The backend talks to MySQL through SQLAlchemy, a widely used Python database library, and changes the database structure through Alembic migrations. Every query is parameterized automatically, and the company filter can be applied in one central place.

## Context
The proposal requires parameterized queries to prevent SQL injection. The tenant filter ([0016](0016-tenant-isolation.md)) and the inactive-record filter ([0020](0020-status-over-deletion.md)) need a central hook that sees every query.

## Decision
- **SQLAlchemy 2.0** (ORM with typed models) for all database access, with a MySQL driver.
- Raw SQL strings are not used. Where a hand-written query is unavoidable it uses bound parameters (`text()` with `:name` placeholders) and is reviewed as security-sensitive.
- **Alembic** manages the schema: one migration per PR ([modularity guide](../contributing/modularity.md)); CI checks for a single head and runs upgrade/downgrade on a fresh MySQL.
- Only `repository.py` modules issue queries ([0004](0004-backend-feature-modules.md)).
- The exact driver and whether to use async sessions are decided when the backend is scaffolded.

## Consequences
- The ORM's global query hooks give one place to enforce tenancy and hide inactive records.
- Contributors need to learn SQLAlchemy 2.0's style; the contributor docs will include examples.

## Alternatives considered
- **Hand-written SQL with a driver:** full control, but every query is a chance to forget a parameter or a tenant filter.
- **A lighter query builder:** fewer features and no equivalent central hook.
