# 0004. Organize the backend by feature module

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Each backend feature (schedules, time off, tasks, and so on) lives in its own folder with everything it needs. A change to time off touches only the time-off folder, which keeps PRs small and conflict-free.

## Context
Organizing by layer (all routers together, all models together) means almost every feature PR edits the same shared files. The project also needs strong, auditable security checks on every endpoint.

## Decision
```
app/
├── main.py        app factory; discovers routers in modules/
├── core/          config, logging, security headers, errors
├── db/            engine, session, base model
├── auth/          password hashing, sessions, CSRF, re-authentication
├── authz/         permission registry, scope resolution, authorize()
├── tenancy/       company context, tenant-scoped query helpers
├── audit/         append-only, hash-chained audit writer
├── detection/     pattern-based detectors → security_events
├── jobs/          scheduler and background jobs
└── modules/<feature>/
    ├── router.py       HTTP only
    ├── schemas.py      request/response models
    ├── service.py      business rules; calls authorize()
    ├── repository.py   the only code that talks to the database
    ├── models.py       tables
    └── permissions.py  permissions this module defines
```
Tests mirror this under `tests/{unit,integration,security}/`.

## Consequences
- Security review has clear places to look: every service call goes through `authorize()`, every query through a repository.
- Shared layers must offer registration points (see [0012](0012-extensibility-patterns.md)) so modules never need to edit them.
- The data model is recorded in [0016](0016-tenant-isolation.md)–[0022](0022-sqlalchemy-and-alembic.md); authorization details and API conventions will get their own records.

## Alternatives considered
- **Layered structure:** familiar, but causes conflicts and scatters each feature across the codebase.
