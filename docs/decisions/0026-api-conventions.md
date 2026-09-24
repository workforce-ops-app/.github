# 0026. API conventions

- **Status:** Accepted (`/api/v1` prefix tentative)
- **Date:** 2026-09-23

## In short
The frontend and backend talk through one consistent set of rules: predictable addresses, one error format that never leaks internals, and paged lists. This makes the API easier to build, test, and audit.

## Context
Two people build both sides of every feature. Consistent conventions prevent every endpoint from inventing its own style, and several conventions are also security controls (error handling, status codes for other companies' data).

## Decision
- Addresses `/api/v1/…`, plural hyphenated resources, actions as sub-paths. **The version prefix is tentative** pending discussion between the teammates.
- JSON with `snake_case`; UUID strings; ISO 8601 UTC moments; `YYYY-MM-DD` dates ([0019](0019-uuidv7-ids.md), [0021](0021-time-handling.md)).
- RFC 9457 problem details for errors, never internal details; status codes:

| Code | Meaning |
|---|---|
| 400 | malformed request |
| 401 | not signed in |
| 403 | in your company, but not allowed |
| 404 | doesn't exist, **or belongs to another company** ([0016](0016-tenant-isolation.md)) |
| 409 | not allowed in the record's current state |
| 422 | invalid input |
| 429 | too many requests |

- Cursor pagination (default 50, max 200), plain filters, allow-listed sorting.

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- The frontend's `js/api/` layer handles one error format.
- Security tests can assert exact status codes, e.g. 404 (not 403) across companies.

## Alternatives considered
- **Page-number pagination:** simpler, but rows shift while data changes.
- **No version prefix:** simpler addresses; adding one later changes every frontend call.
