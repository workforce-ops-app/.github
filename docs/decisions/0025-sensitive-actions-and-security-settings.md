# 0025. Safeguards for sensitive actions and "stricter only" company security settings

- **Status:** Accepted
- **Date:** 2026-09-23

## In short
Risky actions such as transferring ownership or removing an administrator need extra steps depending on how risky they are: re-entering the password, a waiting period, a second approval, notifications. Companies can tighten their own security settings, but can never loosen them below the platform's.

## Context
The proposal asks for protections "based on the sensitivity of the action rather than simply the user's position in the hierarchy", and lets owners configure company security policies. Letting owners weaken security would undermine the whole platform.

## Decision
- **Core:** password re-entry for ownership transfer, admin-level changes, role permission changes, and security setting changes; a confirmation showing the count for schedule changes of **10+ shifts**.
- **Next:** a **48-hour** cancellable wait for ownership transfer; a second approval for removing an administrator or changing admin-level permissions, and for bulk schedule changes above a company-set limit; notifications to owners, admins, and affected people.
- **Company security settings:** every setting has a platform default and limit; companies may only move settings in the stricter direction, within these limits. Changes require password re-entry and notify owners.

| Setting | Platform default | Companies may set |
|---|---|---|
| Idle sign-out (no activity) | per [0027](0027-authentication-and-sessions.md) | shorter, not below 5 min |
| Maximum session (time since sign-in, even if active) | per [0027](0027-authentication-and-sessions.md) | shorter, not below 1 h |
| Failed attempts before lock | 5 | fewer, not below 3 |
| Lock duration | 15 min → 30 min → 1 h | longer first steps, never over the 1 h maximum |
| Minimum password length | 15 | longer, up to 64 |
| Setup/reset link validity | 48 h | shorter, not below 1 h |
| Ownership transfer wait | 48 h | longer, up to 7 days |
| Second approval for bulk schedule changes | 10+ shifts | a lower number, not below 2 |
| Actions requiring password re-entry | platform list | add actions, never remove |

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- The lockout maximum of 1 hour cannot be exceeded even by a stricter company, so lockouts cannot be turned into a denial-of-service tool.
- Safeguards need a small "pending approval / waiting" mechanism, shared by all sensitive actions.

## Alternatives considered
- **Safeguards by role only** (e.g. owners skip checks): contradicts the proposal and leaves a compromised owner account unchecked.
- **Fully configurable security settings:** a single careless owner could disable protections for their whole company.
