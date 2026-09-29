# 0031. Demo environment, demo data, and logging

- **Status:** Accepted
- **Date:** 2026-09-23 (revised 2026-09-28 at sign-off)

## In short
The application runs on a laptop for the demos with made-up demo data, works on phones and computers, and keeps its logs free of personal details.

## Context
The web course grades live demos in midterm and final weeks. There is no hosting decision yet, and using real people's data would bring privacy obligations and email delivery into scope.

## Decision
- **Demo data only**; a seed script creates at least two companies with several roles.
- **Laptop demos** with Docker Compose; hosting is decided later ([0023](0023-feature-tiers-and-audit-schedule.md) lists it as stretch unless needed earlier). Whether a local deployment over HTTPS meets the web course's deployment requirement is still to be confirmed with the instructor.
- **Phones and computers**, WCAG 2.2 AA, current Chrome/Edge/Firefox/Safari.
- **Phone view:** the phone layout is demonstrated with the browser's phone view on the laptop. A real phone reaching the laptop over Wi-Fi would need HTTPS, because the `__Host-` session cookie only works over HTTPS.
- **Logs:** structured JSON, IDs/actions/errors only, no personal details, kept 30 days.

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Security features (audit viewer, lockouts, company separation) can be demonstrated live without privacy concerns.
- No certificates or tunnels to set up; the phone layout is still tested at phone sizes, but not on a physical phone.

## Alternatives considered
- **Hosting for the midterm:** adds cost and operational work before any feature is finished.
- **Real pilot users:** realistic, but requires privacy handling and email that the core tier doesn't have.
- **Local HTTPS for a real phone** (a tool such as mkcert): shows a real phone, but needs a certificate installed on every phone used.
- **A temporary tunnel** (such as Cloudflare Tunnel): easy, but makes the demo briefly reachable from the internet.
