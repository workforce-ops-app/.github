# 0031. Demo environment, demo data, and logging

- **Status:** Accepted (phone connection method pending)
- **Date:** 2026-09-23

## In short
The application runs on a laptop for the demos with made-up demo data, works on phones and computers, and keeps its logs free of personal details.

## Context
The web course grades live demos in midterm and final weeks. There is no hosting decision yet, and using real people's data would bring privacy obligations and email delivery into scope.

## Decision
- **Demo data only**; a seed script creates at least two companies with several roles.
- **Laptop demos** with Docker Compose; hosting is decided later ([0023](0023-feature-tiers-and-audit-schedule.md) lists it as stretch unless needed earlier).
- **Phones and computers**, WCAG 2.2 AA, current Chrome/Edge/Firefox/Safari.
- **Phone access (pending):** local HTTPS (preferred), a temporary tunnel, or the browser's phone view, decided before the midterm.
- **Logs:** structured JSON, IDs/actions/errors only, no personal details, kept 30 days.

Details: [design review 8](../project/design-review/08-building-and-running.md).

## Consequences
- Security features (audit viewer, lockouts, company separation) can be demonstrated live without privacy concerns.
- The local HTTPS setup must be tested well before the midterm demo.

## Alternatives considered
- **Hosting for the midterm:** adds cost and operational work before any feature is finished.
- **Real pilot users:** realistic, but requires privacy handling and email that the core tier doesn't have.
