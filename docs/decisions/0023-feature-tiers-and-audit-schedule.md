# 0023. Feature tiers and security audit schedule

- **Status:** Accepted
- **Date:** 2026-09-23 (revised 2026-09-28 at sign-off)

## In short
Features are built in three tiers matched to the course deadlines: core for the midterm demo, next for the final demo, stretch if time allows. Security audits are scheduled so the backend is audited before the midterm.

## Context
The web course grades two live demos (midterm and final weeks); the security course grades a report built on audits and a detection study. The proposal describes more features than two people can finish safely, so an order is needed that always leaves a demonstrable, secure application.

## Decision
- **Core** (midterm): authentication and sessions, company structure and users, roles and permissions with scopes and reporting lines, password re-entry for sensitive actions, approval from above for same-level role grants and owner changes ([0032](0032-delegation-limits.md)), schedules, time off, audit entries, demo data, tenancy security tests, common-password blocklist.
- **Next** (final): coverage and swaps (coworkers first, then the manager), manager-arranged coverage and open shifts, draft-and-publish schedules, tasks with photos on task notes (the secure file upload feature), announcements with acknowledgement nudges, in-app notifications, company display name and logo, configurable company rules, audit verification and viewer, security page, detection study, backup and restore, email delivery of setup/reset links (low priority).
- **Stretch:** sensitive-action safeguards beyond password re-entry (waiting periods, second approvals, notifications), attachments on time-off requests, repository mirror and GitHub export, support access, two-factor sign-in, email notifications, hosting, privacy erasure, online leaked-password check, shift qualifications, cross-company security view.
- Next-tier work may start early if core is finished.
- **Audits:** threat model before coding → backend audit before the midterm → frontend audit once connected → internal-user then external-attacker audits in the second half.

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Every demo shows a complete, secure slice rather than many unfinished features.
- The detection study and restore drills land in the second half, so the report's results depend on next-tier work finishing on time.

## Alternatives considered
- **Build everything in parallel:** risks having nothing complete at the midterm.
- **Sensitive-action safeguards in next:** stronger against a compromised administrator, but less important for the demos than the features above; password re-entry already covers the core risk.
- **Audit only at the end:** findings would arrive too late to fix, and the report would have no "found and fixed" evidence.
