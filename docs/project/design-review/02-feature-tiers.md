# Design review 2: Feature tiers

**In short:** features are grouped into three tiers. **Core** must work by the midterm demo, **next** by the final demo, and **stretch** is done if time allows. Security audits are scheduled alongside: the backend audit happens before the midterm.

| # | Question | Answer | Status |
|---|---|---|---|
| 2.1 | What is core, next, and stretch? | See the tiers below. | answered; Corbin to confirm |
| 2.2 | Should time off be core? | **Yes**: small, and shows permissions and scope working in a real workflow. | answered |
| 2.3 | Should anything move between tiers? | Sensitive-action safeguards (waiting periods, second approvals) and draft-and-publish schedules move from stretch to **next**. Email delivery of setup/reset links is added to next at low priority (may slip to stretch). If development moves fast, next-tier work can start early. | answered |
| 2.4 | When do the security audits happen? | Threat model before coding; backend audit after the core backend and **before the midterm**; frontend audit once the frontend is built and connected; internal-user and external-attacker audits in the second half. | answered |

## Tiers

### Core: by the midterm demo
- Sign in and out, secure sessions, one-time setup and reset links ([authentication](04-api-and-authentication.md))
- Companies, departments, teams, users: basic administration
- Roles, permissions, ranks, and scoped role assignments ([authorization](03-authorization.md))
- Re-entering the password for sensitive actions
- **Schedules:** employees see their own shifts and their department's; managers create and edit shifts in their scope
- **Time off:** request, approve or deny, status shown on the page
- Audit log entries for everything above
- Demo data: two companies with several roles, to show company separation live
- Security tests for company separation from the start
- A basic blocklist check for common passwords

### Next: by the final demo
- Shift coverage and swaps
- Manager-arranged coverage and open shifts for approved time off
- Draft-and-publish schedules
- Shift tasks
- Announcements
- In-app notifications
- Configurable company rules: cutoffs, deadlines, reminders, automatic expiry, required approvals, security policies
- Sensitive-action safeguards: waiting periods, second approvals, notifications
- Audit log verification (nightly) and an owner-facing audit viewer
- Security page for owners and admins
- The detection study
- Backup and restore, with timed drills
- Email delivery of setup and reset links (low priority; may slip to stretch)

### Stretch: if time allows
- Platform support access
- Two-factor sign-in
- Email notifications
- Online hosting (unless needed earlier)
- Privacy data erasure
- Online check against leaked-password databases
- Shift qualifications (e.g. certifications required for a shift)
- Cross-company security view for platform staff

## Security audit schedule

| When | Activity |
|---|---|
| Before coding | Threat model ([security study](07-security-study.md)) |
| After the core backend, **before the midterm** | Backend audit: injection, authentication, sessions, company separation |
| Once the frontend is built and connected | Frontend audit: XSS, CSRF, hidden-button assumptions |
| Second half | Internal-user audit (malicious or compromised employee), then external-attacker audit |
| Throughout | Every finding logged when found |

Recorded as decision [0023](../../decisions/0023-feature-tiers-and-audit-schedule.md).
