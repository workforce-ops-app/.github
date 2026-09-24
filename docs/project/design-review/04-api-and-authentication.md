# Design review 4: API conventions and authentication

**In short:** this covers how the frontend and backend talk to each other (addresses, errors, long lists) and how people get in and stay signed in (accounts, passwords, sessions, lockouts, and forged-request protection). Passwords follow NIST's current guidance: at least 15 characters, checked against a blocklist. **The session timeouts are still to be decided between two options.**

| # | Question | Answer | Status |
|---|---|---|---|
| 4.1 | Versioned API addresses? | `/api/v1/…` | **tentative: Michael and Corbin to discuss** |
| 4.2 | Error format? | RFC 9457 problem details; no internal details leaked. | answered |
| 4.3 | Long lists? | Cursor pagination, default 50, max 200. | answered |
| 4.4 | Session timeouts? | **Option A or B, below.** | **for Corbin and Michael to decide** |
| 4.5 | Forged-request (CSRF) protection? | Per-session token in a header, plus SameSite cookies and an Origin check. | answered |
| 4.6 | Lockout rules? | Escalating: 15 min → 30 min → **1 hour maximum**. | answered |
| 4.7 | Password rules? | **Minimum 15 characters** (NIST SP 800-63B rev. 4), plus blocklist. | answered; Corbin to confirm |
| 4.8 | How are companies created? | By platform staff only; no public sign-up (may revisit later). | answered |
| 4.9 | How do employees get accounts? | Admin creates the account; the system shows a **one-time setup link** passed on in person or by text. | answered |
| 4.10 | Forgotten passwords? | Admin generates a fresh one-time link; email delivery is next tier, low priority. | answered |

## API conventions

- **Addresses:** `/api/v1/…`, plural resource names with hyphens (`/api/v1/time-off-requests`), and actions as sub-paths (`POST …/{id}/approve`). `v1` lets a future breaking change ship as `v2` alongside; it costs little now and is expensive to add later. Tentative.
- **Data:** JSON with `snake_case` fields; IDs as UUID strings; moments in ISO 8601 UTC (`2026-10-01T14:00:00Z`); calendar dates as `YYYY-MM-DD`.
- **Errors:** RFC 9457 problem details (type, title, status, detail, per-field errors); never stack traces or SQL.

| Code | Meaning |
|---|---|
| 400 | malformed request |
| 401 | not signed in |
| 403 | in your company, but not allowed |
| 404 | doesn't exist, **or belongs to another company** |
| 409 | not allowed in the record's current state |
| 422 | invalid input |
| 429 | too many requests |

- **Lists:** `?limit=50&cursor=…` (max 200); IDs are time-ordered, so cursors never skip or repeat rows. Filters as plain parameters; `?sort=` from a per-resource allow-list.

## Sessions

- Session data stays on the server; the browser holds a random ID in a cookie named **`__Host-session`**. The name prefix forces: secure connections only, no JavaScript access, never sent by other sites (`Secure; HttpOnly; SameSite=Strict; Path=/`).
- A new session ID at sign-in and whenever permissions or the password change; a password change signs out all other devices.

**Timeouts: to decide.**

| Option | Employees and managers | Owners and administrators |
|---|---|---|
| **A: uniform** | 1 h idle / 24 h maximum | 1 h idle / 24 h maximum |
| **B: split** | 1 h idle / 24 h maximum | **30 min idle / 12 h maximum** |

Both are acceptable under NIST guidance for password-only sign-in. Option B limits the damage if a high-privilege account is left signed in on a shared computer. Michael finds B fair; the decision is left to both teammates.

## CSRF protection

- A per-session secret token, given to the frontend when it loads the session, sent in an `X-CSRF-Token` header on every state-changing request.
- Plus `SameSite=Strict` cookies and a check that requests come from our own origin.

## Lockouts and rate limits

| Failed sign-ins in a row | Locked for |
|---|---|
| 5 | 15 minutes |
| 10 | 30 minutes |
| 15 and above | **1 hour** each time (maximum) |

- The count resets after a successful sign-in, or after 24 hours with no failures.
- Administrators can unlock early (audited). Repeated lockouts alert administrators and are logged for the detection study.
- No permanent lockouts, which would let attackers lock real users out on purpose.
- At most 20 sign-in attempts per minute from one network address; 300 requests per minute per session in general.

## Passwords

- **Minimum 15 characters**, per NIST SP 800-63B revision 4 for password-only sign-in. Allow at least **64**, including spaces and all printable characters; never truncate.
- No forced mixes of symbols; no forced periodic changes.
- New passwords are checked against a **blocklist of common passwords** (core). An online check against leaked-password databases is stretch.
- Stored with **Argon2id**, tuned to about half a second per check. The hash has a fixed size whatever the password length.

## Accounts and onboarding

- **Companies** are created by platform staff only; no public sign-up, which would bring spam and fake-company abuse into scope.
- **New employees:** an administrator creates the account; the system shows a **one-time setup link** (valid 48 hours, single use) that the administrator passes on in person or by text. The employee sets their own password; the administrator never knows it.
- **Forgotten passwords:** an administrator generates a fresh one-time link; the request is audited and the employee's other sessions are signed out.
- Links are stored only as hashes (`one_time_tokens`: purpose, expiry, used time).
- **Email delivery** of these links: next tier, low priority, may slip to stretch.

Recorded as decisions [0026](../../decisions/0026-api-conventions.md) and [0027](../../decisions/0027-authentication-and-sessions.md).
