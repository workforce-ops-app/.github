# 0020. Change status instead of deleting records

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Business records are never erased. A user who leaves is deactivated, and a shift that is not needed is cancelled. Only temporary data such as expired sessions is actually deleted. This keeps the full history the audit log refers to.

## Context
Audit entries point at users, shifts, and requests. Deleting those rows would break the history and weaken the "what happened" story the security study relies on.

## Decision
- **Users:** deactivated with `deactivated_at`; never deleted. Deactivated users cannot sign in, and their sessions are revoked.
- **Business records** (shifts, requests, tasks, announcements, roles, departments, teams): use explicit states such as `cancelled` or `archived`, or an `archived_at` timestamp.
- **Hard-deleted data:** expired sessions, used or expired one-time tokens, and security events past retention.
- **Retention:**

| Data | Kept |
|---|---|
| Audit log | indefinitely |
| Security events (detection) | 1 year |
| Sessions | until expiry, then removed |
| One-time tokens | until used or expired, then removed |

- **Privacy erasure** (stretch goal): personal fields of a user are replaced in place with anonymous values; rows are kept so references stay valid.

## Consequences
- Queries must exclude inactive records by default. The same mechanism as the company filter ([0016](0016-tenant-isolation.md)) provides this, with an explicit opt-in to include them.
- Tables grow over time; archived data can be moved out later if needed.

## Alternatives considered
- **Hard deletes everywhere:** simplest, but breaks audit references.
- **A generic `deleted_at` on every table:** hides meaning. A shift being *cancelled* is different from a role being *archived*.
