# 0027. Authentication, sessions, and onboarding

- **Status:** Accepted
- **Date:** 2026-09-23 (revised 2026-09-28 at sign-off)

## In short
People sign in with a password of at least 15 characters, stored with Argon2id. Sessions live on the server behind a tightly locked cookie. Repeated wrong guesses cause short, escalating lockouts. New employees and forgotten passwords use one-time links that an administrator passes on, so no email service is needed at first.

## Context
Session hijacking and CSRF are course topics, and credential protection is a security proposal goal. NIST SP 800-63B revision 4 sets current expectations for password-only sign-in. The project has no email service in the core tier.

## Decision
- **Passwords:** minimum 15, allow at least 64 (spaces and all printable characters), no truncation, no composition or rotation rules; common-password blocklist (core); online leaked-password check (stretch); Argon2id at about 0.5 s.
- **Sessions:** server-side; `__Host-session` cookie with `Secure; HttpOnly; SameSite=Strict; Path=/`; new ID at sign-in and on privilege or password change; password change signs out other devices.
- **Session timeouts:** a session ends at whichever limit comes first:
  - **Idle timeout: 1 hour**, the same for everyone. Every action restarts it. Protects computers left signed in.
  - **Maximum session length: 30 days** since sign-in, however active the user is. Limits how long a stolen session stays useful, and matches NIST's recommendation to re-authenticate password-only sessions at least every 30 days.

  Companies may shorten both ([0025](0025-sensitive-actions-and-security-settings.md)).
- **CSRF:** per-session token in `X-CSRF-Token`, plus SameSite and an Origin check.
- **Lockouts:** 5 failures → 15 min, 10 → 30 min, 15+ → 1 h (maximum); reset after success or 24 h; admin unlock (audited); alerts on repeats; 20 sign-in attempts per minute per address; 300 requests per minute per session.
- **Onboarding:** companies created by platform staff; admins create accounts and get a one-time setup link (48 h, single use); resets use the same mechanism; links stored as hashes; email delivery next tier (low priority).

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Phone demos need HTTPS for the `__Host-` cookie to work ([0031](0031-demo-environment-and-data.md)).
- A 15-character minimum is stricter than many sites; the sign-up and reset screens should explain it (a passphrase works well).
- Company security settings may only make these stricter ([0025](0025-sensitive-actions-and-security-settings.md)).

## Alternatives considered
- **Token-based sessions (JWT in the browser):** harder to revoke, and storing them in JavaScript exposes them to XSS.
- **8- or 12-character minimum:** friendlier, but below NIST's current recommendation for password-only sign-in.
- **Permanent lockouts:** let attackers lock real users out indefinitely.
- **A 24-hour maximum session, or shorter limits for owners and administrators:** safer against stolen sessions, but daily sign-ins add friction the team judged unnecessary for a scheduling application.
- **No maximum session length:** most convenient, but a stolen session could be kept alive forever, beyond NIST's 30-day limit.
