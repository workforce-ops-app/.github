# 0027. Authentication, sessions, and onboarding

- **Status:** Accepted (session timeouts pending: option A or B)
- **Date:** 2026-09-23

## In short
People sign in with a password of at least 15 characters, stored with Argon2id. Sessions live on the server behind a tightly locked cookie. Repeated wrong guesses cause short, escalating lockouts. New employees and forgotten passwords use one-time links that an administrator passes on, so no email service is needed at first.

## Context
Session hijacking and CSRF are course topics, and credential protection is a security proposal goal. NIST SP 800-63B revision 4 sets current expectations for password-only sign-in. The project has no email service in the core tier.

## Decision
- **Passwords:** minimum 15, allow at least 64 (spaces and all printable characters), no truncation, no composition or rotation rules; common-password blocklist (core); online leaked-password check (stretch); Argon2id at about 0.5 s.
- **Sessions:** server-side; `__Host-session` cookie with `Secure; HttpOnly; SameSite=Strict; Path=/`; new ID at sign-in and on privilege or password change; password change signs out other devices.
- **Session timeouts: pending.** Option A: 1 h idle / 24 h maximum for everyone. Option B: the same for employees and managers, 30 min / 12 h for owners and administrators.
- **CSRF:** per-session token in `X-CSRF-Token`, plus SameSite and an Origin check.
- **Lockouts:** 5 failures → 15 min, 10 → 30 min, 15+ → 1 h (maximum); reset after success or 24 h; admin unlock (audited); alerts on repeats; 20 sign-in attempts per minute per address; 300 requests per minute per session.
- **Onboarding:** companies created by platform staff; admins create accounts and get a one-time setup link (48 h, single use); resets use the same mechanism; links stored as hashes; email delivery next tier (low priority).

Details: [design review 4](../project/design-review/04-api-and-authentication.md).

## Consequences
- Phone demos need HTTPS for the `__Host-` cookie to work ([design review 8](../project/design-review/08-building-and-running.md)).
- A 15-character minimum is stricter than many sites; the sign-up and reset screens should explain it (a passphrase works well).
- Company security settings may only make these stricter ([0025](0025-sensitive-actions-and-security-settings.md)).

## Alternatives considered
- **Token-based sessions (JWT in the browser):** harder to revoke, and storing them in JavaScript exposes them to XSS.
- **8- or 12-character minimum:** friendlier, but below NIST's current recommendation for password-only sign-in.
- **Permanent lockouts:** let attackers lock real users out indefinitely.
