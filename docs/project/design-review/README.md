# Design review

**In short:** before writing code, the team worked through every open question about the project: how it's scoped, secured, and built, and what the research report needs. Each page below lists the questions, the answers, and the design that follows. Anything still undecided is collected at the bottom.

Answers were agreed on 2026-09-23 by Michael and are confirmed by Corbin through the review of this document.

| Page | Covers |
|---|---|
| [1. Project and team](01-project-and-team.md) | courses, deliverables, division of work, project board, demo setup, research repository |
| [2. Feature tiers](02-feature-tiers.md) | what's built for the midterm, the final, and if time allows; audit schedule |
| [3. Authorization](03-authorization.md) | permissions, ranked roles, escalation rules, sensitive actions, company security settings |
| [4. API conventions and authentication](04-api-and-authentication.md) | addresses, errors, lists, sessions, CSRF, lockouts, passwords, onboarding |
| [5. Backup and recovery](05-backup-and-recovery.md) | limiting damage, backups, recovery targets, drills, repository mirrors |
| [6. Feature details](06-feature-details.md) | schedules, time off, coverage and swaps, approvals, notifications, tasks, announcements |
| [7. Security study](07-security-study.md) | audit method, tools, detection study, threat model, research questions |
| [8. Building and running](08-building-and-running.md) | demo data, devices, accessibility, logs, demo setup |

Related: [project overview](../README.md) · [report plan](../report-plan.md) · decisions [0016–0022](../../decisions/README.md) (data model) and [0023–0031](../../decisions/README.md) (this review).

## For Corbin to decide or confirm

| # | Item | Options or proposal |
|---|---|---|
| 4.4 | Session timeouts | **A:** 1 h idle / 24 h max for everyone. **B:** same for employees and managers; 30 min / 12 h for owners and administrators. |
| 4.1 | `/api/v1` version prefix | keep (tentative) or drop |
| 4.7 | 15-character password minimum (NIST) | confirm |
| 6.18 | Any denial ends a multi-approval request | confirm or change |
| 5.6 | Where repository mirrors and exports are stored | both teammates' machines, or a dedicated server or computer |
| 6.23–6.26 | Shift task design | review |
| 7.4 | Cross-attacking between teammates | confirm |
| 2.1 | Feature tiers | confirm |

## Still open (either teammate)

| # | Item |
|---|---|
| 1.1 | Presentation and report dates, once announced |
| 8.4 | Application name and logo |
| 8.7 | How a phone connects to the laptop for demos (local HTTPS preferred) |
| 7 | Whether to tell the instructor about the refined research question 2 |

## What happens after approval

- Backend architecture and feature pages are written from the approved design: authorization, authentication, schedules, time off, coverage, tasks, announcements, backup and restore runbooks.
- The `workforce-ops-research` repository is created.
- The project board is set up.
