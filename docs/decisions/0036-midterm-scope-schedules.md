# 0036. Midterm demo: schedules on the security pieces it needs

- **Status:** Accepted
- **Date:** 2026-10-01

## In short
The midterm demo shows one complete feature, schedules, instead of the whole core tier. Underneath it are only the security pieces schedules need: keeping companies apart, signing in, protection against forged requests, roles with scopes, and the signed audit log. Everything else planned for the midterm moves to after it, and time is set aside to prepare and practise the presentation.

## Context
[0023](0023-feature-tiers-and-audit-schedule.md) put the whole core tier in front of the midterm: sign-in, company structure and administration, roles and reporting lines with approvals, schedules, time off, and a backend audit. Broken into pull requests that is about 35 pieces of work, with about two weeks left and the presentation still to prepare. The midterm grades a live demo of the application's progress ([project overview](../project/README.md)); a smaller demo that works end to end, and that both teammates can explain and answer questions about at any point, serves that better than many unfinished parts.

Schedules are the most central feature, and they need less of the security foundation than the others: editing shifts is a permission with a scope (company, department, team), so it does not need the reporting chain, approvals, or the administration screens. The demo data creates the companies and people.

## Decision
- **Midterm scope:**
  - **Finish Phase 1:** database layer, Docker Compose, the frontend page structure, nginx.
  - **Security base:** the automatic company filter and cross-company tests ([0016](0016-tenant-isolation.md)), the tables for companies and people, the demo seed script, the signed audit log ([0018](0018-audit-log-chains.md)), password hashing, sign-in and sessions, CSRF protection ([0027](0027-authentication-and-sessions.md)), and permissions and roles with scopes ([0017](0017-scoped-role-assignments.md)).
  - **Schedules:** creating, viewing, assigning, and cancelling shifts, changing several at once, and demo shifts.
  - **Screens:** session state and permission-aware navigation, sign-in, my shifts and the department week, and the manager's edit mode.
  - **Audit and presentation:** an audit of what is built against OWASP ASVS Level 2, a demo script, and presentation practice.
- **After the midterm, before the next tier:** everything else from the core tier. That covers:
  - separate database users and insert-only audit rights;
  - lockouts, password re-entry, and setup and reset links;
  - the reporting chain, administration endpoints, role approvals, and owner changes;
  - company settings and changing your own name;
  - time off;
  - the administration, account, and time-off screens.
- **The demo shows the security story, not only the screens:** a request for the other company's shift answers 404, an employee calling the edit endpoint directly gets 403, and every change is in the audit log.
- **Audits:** the pre-midterm backend audit covers what is built by then; the rest of the core is covered by the audits already planned for the second half (0023).
- If time is short after the midterm, next-tier features move to stretch before any remaining core feature does.

## Consequences
- About 15 pieces of work before the midterm instead of about 35, with time left for the presentation.
- The midterm shows fewer features; the account and administration screens, time off, and approvals are explained as planned work rather than demonstrated.
- The second half carries more: the rest of the core plus the next tier. The next tier is re-planned after the midterm.
- Without setup links, demo accounts get their passwords from the seed script (from an environment variable, never the repository).
- Without separate database users at the midterm, the application's database user can still change audit entries directly; the signatures still detect any change. Insert-only rights follow after the midterm.

## Alternatives considered
- **Keep the full core tier:** not achievable in two weeks alongside presentation preparation; risks an unfinished demo.
- **Schedules as plain create, read, update, and delete without the security base:** faster, but the project is also a security study; a schedule anyone can edit, or one that shows another company's shifts, would undercut the demo.
- **Time off instead of schedules:** depends on schedules (approved time off opens shifts) and on the reporting chain and approvals, so it needs more of the foundation first.
