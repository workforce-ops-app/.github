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
- RFC 9457 problem details for errors, never internal details; status codes 400/401/403/404/409/422/429 as listed in [design review 4](../project/design-review/04-api-and-authentication.md#api-conventions), with 404 for other companies' records ([0016](0016-tenant-isolation.md)).
- Cursor pagination (default 50, max 200), plain filters, allow-listed sorting.

## Consequences
- The frontend's `js/api/` layer handles one error format.
- Security tests can assert exact status codes, e.g. 404 (not 403) across companies.

## Alternatives considered
- **Page-number pagination:** simpler, but rows shift while data changes.
- **No version prefix:** simpler addresses; adding one later changes every frontend call.
