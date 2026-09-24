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
- **Company security settings:** every setting has a platform default and limit; companies may only move settings in the stricter direction, within the limits listed in [design review 3](../project/design-review/03-authorization.md#company-security-settings-stricter-only). Changes require password re-entry and notify owners.

## Consequences
- The lockout maximum of 1 hour cannot be exceeded even by a stricter company, so lockouts cannot be turned into a denial-of-service tool.
- Safeguards need a small "pending approval / waiting" mechanism, shared by all sensitive actions.

## Alternatives considered
- **Safeguards by role only** (e.g. owners skip checks): contradicts the proposal and leaves a compromised owner account unchecked.
- **Fully configurable security settings:** a single careless owner could disable protections for their whole company.
