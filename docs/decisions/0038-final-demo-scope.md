# 0038. Final demo scope: five web features, the security study kept

- **Status:** Accepted
- **Date:** 2026-11-04

## In short
The final demo of the web course shows five things: a calendar-style department view, announcements, time-off requests, shift swaps and coverage requests, and screens suited to each permission level, including companies signing up and setting up their own people and roles. The work the security report depends on stays planned. Every other next-tier and remaining core feature moves to stretch.

## Context
[0023](0023-feature-tiers-and-audit-schedule.md) planned a large next tier for the final demo, and [0036](0036-midterm-scope-schedules.md) moved most of the core tier to after the midterm. Together that is far more than two people can finish safely in the weeks left. The two courses need different things: the web course grades the finished application in a live demo; the security course grades a research report built on audits, a detection study, and recovery evidence ([report plan](../project/report-plan.md)).

## Decision
- **Web features for the final demo:**
  - **Department view like a calendar:** times down the side, each shift drawn as a bar as long as the shift, people or days across.
  - **Announcements:** people who manage others post announcements to the people they manage, within the scope they manage (team, department, or company).
  - **Time-off requests:** employees ask for time off; their managers in the reporting chain approve or deny it; requests nobody reviews in time are declined automatically, so none get stuck; approved time off opens the employee's shifts ([0029](0029-request-approval-routing.md)). The number of approvals comes from company settings, which are stored with safe defaults (one approval); a screen to change them stays stretch.
  - **Shift swaps and coverage requests:** employees coordinate changes through the application, as set out in 0029: coworkers answer first, then the manager approves. They reuse the approval routing that time off builds first.
  - **Screens for each permission level:** employees see their own shifts, requests, and announcements; managers also see what they manage and act on it; owners and administrators manage people, roles, and permissions.
- **Companies sign up themselves:** a public sign-up page creates a company and its owner account. It is open to anyone, rate limited per address, and uses the existing password rules. This replaces "companies created by platform staff" in [0027](0027-authentication-and-sessions.md); the seed script still creates the demo companies.
- **Owners and administrators set up their company:** they add employees, create roles, and choose each role's permissions, within the existing delegation limits ([0032](0032-delegation-limits.md)). A new employee gets a one-time setup link (48 hours, single use, as in 0027) that the administrator hands over; the administrator never knows the password. Email delivery stays stretch.
- **Reporting chain kept, three levels for the demo:** owner, then managers, then employees. Deeper chains are supported by the design ([0024](0024-authorization-model.md)) but are only shown if time allows.
- **Security-report work stays planned:** the detection study and security page, audit log verification and viewer, backup and restore, lockouts and rate limits, separate database users, and the audits planned in 0023 (frontend, internal user, external attacker).
- **Supporting pieces stay planned** because the features above need them: password re-entry for sensitive actions, setup and reset links, the reporting chain, people, roles, and reporting-line management.
- **Moved to stretch:** changing your own name or email, the company settings screen and logo, draft-and-publish schedules, shift tasks with photos, in-app notifications, working-hour limits across shifts, and everything already in stretch.
- **Design before code:** time off already has its design page; announcements, swaps and coverage, and company sign-up each get one (with their threat model rows) before their code slices start.

## Consequences
- The final demo shows a complete path: a company signs up, sets up its people and roles, plans the week, posts an announcement, and an employee arranges a swap.
- Public sign-up adds an endpoint anyone can call, so mass sign-ups and guessing which emails exist need threat rows and tests.
- Time off is built before swaps and coverage: it is the simpler flow (employee, then manager) and already designed, so it builds the shared approval routing of 0029, and coverage only adds the coworker step.
- The secure file upload feature (photos on task notes) is stretch, so the report covers file upload risks only if time allows.
- Issues for the moved features go to a **Stretch** milestone in each repository rather than being closed.

## Alternatives considered
- **Keep the full next tier:** not achievable in the weeks left alongside the audits and the report.
- **Time off in stretch** (the first version of this decision, revised the same day): fewer slices, but coverage would have had to build the approval routing alone, and the demo would lack the path from approved time off to an open shift.
- **Move the security-report work to stretch too:** the report would have no data for research question RQ1 and no recovery evidence.
- **Sign-up with an invite code:** blocks mass fake companies, but adds a step to the demo; rate limits cover the main risk.
- **Temporary passwords for new employees:** quicker to build, but the administrator would know the employee's password until it is changed.
- **Scopes only, without the reporting chain:** less work, but peers could act on each other (threats E3 and E4), and coverage approval needs to know each employee's manager.
