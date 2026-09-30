# 0025. Safeguards for sensitive actions and "stricter only" company security settings

- **Status:** Accepted
- **Date:** 2026-09-23 (revised 2026-09-28 at sign-off)

## In short
Risky actions such as transferring ownership or removing an administrator need the password re-entered. Waiting periods, second approvals, and notifications are planned as a later addition if time allows. Companies can tighten their own security settings, but can never loosen them below the platform's.

## Context
The proposal asks for protections "based on the sensitivity of the action rather than simply the user's position in the hierarchy", and lets owners configure company security policies. Letting owners weaken security would undermine the whole platform.

## Decision
- **Core:** password re-entry for ownership transfer, admin-level changes, role permission changes, reporting line changes ([0024](0024-authorization-model.md)), and security setting changes; a confirmation showing the count for schedule changes of **10+ shifts**.
- **Core, from [0032](0032-delegation-limits.md):** approval from above for same-level role grants, and agreement of the other owners for owner changes.
- **Stretch:** a **48-hour** cancellable wait for ownership transfer; a second approval for removing an administrator or changing admin-level permissions, and for bulk schedule changes above a company-set limit; notifications to owners, admins, and affected people.
- **Company security settings:** every setting has a platform default and limit; companies may only move settings in the stricter direction, within these limits. Changes require password re-entry.

| Setting | Platform default | Companies may set |
|---|---|---|
| Idle sign-out (no activity) | 1 h ([0027](0027-authentication-and-sessions.md)) | shorter, not below 5 min |
| Maximum session (time since sign-in, even if active) | 30 days ([0027](0027-authentication-and-sessions.md)) | shorter, not below 1 h |
| Failed attempts before lock | 5 | fewer, not below 3 |
| Lock duration | 15 min → 30 min → 1 h | longer first steps, never over the 1 h maximum |
| Minimum password length | 15 | longer, up to 64 |
| Setup/reset link validity | 48 h | shorter, not below 1 h |
| Ownership transfer wait (stretch) | 48 h | longer, up to 7 days |
| Second approval for bulk schedule changes (stretch) | 10+ shifts | a lower number, not below 2 |
| Actions requiring password re-entry | platform list | add actions, never remove |

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- The lockout maximum of 1 hour cannot be exceeded even by a stricter company, so lockouts cannot be turned into a denial-of-service tool.
- Until the stretch safeguards exist, a compromised administrator account that knows its own password can make admin-level changes immediately; the audit log still records every one. The report states this as a known limit.
- The stretch safeguards would need a small "pending approval / waiting" mechanism shared by all sensitive actions.

## Alternatives considered
- **Safeguards by role only** (e.g. owners skip checks): contradicts the proposal and leaves a compromised owner account unchecked.
- **Fully configurable security settings:** a single careless owner could disable protections for their whole company.
- **Waiting periods and second approvals in the next tier:** stronger, but the team gave the demo features priority.
