# Security policy

**In short:** if you find a way to get at data or actions you should not have access to, report it privately — not in a public issue — so it can be fixed before anyone else learns about it.

## Reporting a vulnerability

Use GitHub's private reporting on the affected repository: **Security → Report a vulnerability**.

- [Report for the backend](https://github.com/workforce-ops-app/workforce-ops-backend/security/advisories/new)
- [Report for the frontend](https://github.com/workforce-ops-app/workforce-ops-frontend/security/advisories/new)

Please include what you found, how to reproduce it, and what an attacker could do with it. You will get a response within a few days.

## What happens next

1. The report is confirmed and given a severity.
2. The fix is developed and merged. Where possible it includes a regression test in `tests/security/`.
3. After the fix is released, the advisory may be published and the finding is added to the project's security findings log.

## Scope

This is an academic project that is not deployed for real customers yet. Reports about the application code, CI configuration, and dependencies are all welcome.
