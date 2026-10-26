# Midterm presentation plan

**In short:** how we present the application at the midterm: who presents which part, in what order, the questions we expect with short answers, and how we practise. The demo itself is in the [demo script](demo-script.md); what the midterm covers is in [decision 0036](../decisions/0036-midterm-scope-schedules.md). Questions can come at any point, so each of us must be able to explain every part, not only the parts we built.

**Draft:** the split and timings below are a proposal to agree together. The presentation length and the date are not confirmed yet; adjust the timings once the instructor announces them.

## Outline and who presents

Each of us presents the parts we built, so the explanations come first-hand.

| Part | Time | Presents | Content |
|---|---|---|---|
| 1. The project | 1 min | Corbin | What the application does and for whom; the two courses it serves |
| 2. The security approach | 2 min | Michael | Security built in from the start: companies kept apart, sign-in, permissions with scopes, a signed audit log; the threat model behind it |
| 3. Live demo | 8 min | both | [Demo script](demo-script.md): Corbin drives the screens (steps 1 to 6), Michael the attacks and the audit log (steps 7 to 10) |
| 4. How we work | 1 min | Corbin | Small pull requests, review by the other teammate, automatic checks (tests, security tests, secret scan, dependency audit) |
| 5. What comes next | 1 min | Michael | Time off, administration, coverage and swaps, file uploads, the detection study |
| 6. Questions | rest | both | The person who built the part answers first; the other adds |

Slides are optional: a title slide, one with the system diagram and the security model from the [design overview](design-overview.md), and one with what comes next are enough. The demo is the main part.

## Who explains which code

Everyone reads every midterm slice before the presentation (the "Explain in the presentation" note in each issue names its course topic). Each slice's builder explains it first:

| Slice | Course topic | Builder |
|---|---|---|
| Company filter (T1) | SQL injection and safe queries | Michael |
| Company and people tables (O1), seed data (O2) | SQL tables and foreign keys | Corbin |
| Signed audit log (L1) | integrity, hashing with a secret key | Michael |
| Password hashing (S1) | password hashing | Corbin |
| Sign-in and sessions (S2) | sessions | Michael |
| CSRF protection (S3) | CSRF | Corbin |
| Permissions and scopes (Z1) | access control | Michael |
| Shifts (SC1, SC2, SD1) | REST, SQL JOINs | Michael |
| Session state and screens (UI1 to UI4) | AJAX, CSRF, XSS | Corbin |
| nginx and security headers (F3) | Content Security Policy, XSS | Corbin |

## Likely questions, with short answers

Answers name the place in the code, so either of us can show it. Parts marked *(when built)* describe the design; check them against the code once the slice merges.

**SQL injection and safe queries**
- *How do you prevent SQL injection?* Every query is built with SQLAlchemy, which sends values as bound parameters, like a PDO prepared statement in PHP. A value can never change the query. Repositories never build SQL text, and the lint rules flag SQL built from strings.
- *What if someone changes `company_id` in a request?* The company never comes from the request; it comes from the server-side session. The company filter (`app/tenancy/filter.py`) adds `company_id = <session's company>` to every query, and refuses saving a row for another company.
- *What if a developer forgets the company condition?* They do not write it: the filter adds it automatically. A test fails if any table with `company_id` is not covered, and shortcuts that would skip it (bulk changes, the raw table) are refused.
- *Why 404 and not 403 for another company's record?* A 403 would confirm the record exists. A 404 is the same answer as for an ID that does not exist, so it reveals nothing.

**XSS**
- *A shift note contains `<script>`. What happens?* It shows as plain text. Pages only put data on the page through `js/core/dom.js`, which uses `textContent`, never `innerHTML`; lint fails the build on `innerHTML` with data.
- *And if HTML got in anyway?* The Content Security Policy from nginx blocks inline scripts and event attributes, a second, independent defense *(when built, F3)*.
- *Can an error message reflect input back?* No. The API never copies submitted values into error answers.

**CSRF**
- *How do you stop a forged request from another site?* Three defenses: the session cookie is `SameSite=Strict`; every change must carry an `Origin` header equal to our own address; and every change must send a token (`X-CSRF-Token`) that only our pages can read *(when built, S3)*.
- *Why three?* So one mistake or one browser quirk is not enough to get through.

**Sessions**
- *How does sign-in keep you signed in?* The server creates 32 random bytes as the session token and sends it in a `__Host-session` cookie that is `Secure`, `HttpOnly` (scripts cannot read it), and `SameSite=Strict`. The database stores only its SHA-256 hash *(when built, S2)*.
- *Why store a hash of the token?* Someone who copies the database cannot use the hashes to sign in.
- *When does a session end?* After 1 hour without activity, after 30 days at most, or at sign-out. A new token is created at every sign-in, so an old one cannot be planted (session fixation).

**Password hashing**
- *How are passwords stored?* As Argon2id hashes, deliberately slow and memory-hungry, so guessing passwords from a stolen database is expensive *(when built, S1)*.
- *Why not SHA-256 for passwords?* It is built to be fast; an attacker could try billions of guesses per second.
- *Password rules?* At least 15 characters, no forced symbols, and the most common passwords are refused (NIST guidance).
- *Does sign-in reveal whether an email exists?* No. Every failure gets the same message, in similar time.

**REST and AJAX**
- *How is the API organised?* Resources under `/api`, standard methods (GET to read, POST to create, PATCH to change), standard status codes, and one error format for every error (RFC 9457 problem details).
- *How do pages call it?* Through `js/api/client.js`: `fetch` with JSON, the session cookie only to our own address, the CSRF token on changes, and one error type for error answers and another for network failures.

**SQL JOINs**
- *Where do you use joins?* Listing shifts for a manager whose scope is a team joins shifts to the team's members; the scope filter turns a person's role assignments into that condition, so rows outside their scope are never loaded *(when built, SC1)*.

**Access control**
- *How is a request checked?* Every service function calls `authorize(user, permission, target)`: the person needs a role that grants the permission, with a scope (company, department, team, or one person) that covers the target. Everything is denied unless a rule allows it *(when built, Z1)*.
- *The employee has no edit button; is that the protection?* No, only a convenience. The server checks every request; the demo shows a direct API call answering 403.

**Audit log**
- *How do you know the log was not edited?* Each entry is signed with HMAC-SHA256 over its content plus the previous entry's signature, with a key kept outside the database. Changing, removing, or inserting an entry breaks the chain *(when built, L1)*.
- *Can someone with database access just fix the chain?* Not without the key. Automatic checking of the chain comes with the next tier.

**Errors and logs**
- *What does a user see when something breaks?* A generic message and a reference number. The log has the same number, the error type, and where it happened, but never the error's message, which could contain secrets ([decision 0035](../decisions/0035-logging-unexpected-errors.md)).

**How we work**
- *How do you make sure both of you know the code?* Every change is a small pull request that the other must approve, and both of us review the whole project before presentations.
- *What runs automatically?* Formatting, lint (with security rules), type checks, unit and security tests, a secret scan, a dependency audit, the database migration check, the image build, and an integration test, on every pull request.

## Practice

- [ ] Agree on the outline, the split, and the timings above.
- [ ] Each of us reads every midterm slice and answers the questions above out loud for the parts the other built.
- [ ] Practice run 1, with the [demo script](demo-script.md), timed. Note problems as issues.
- [ ] Practice run 2 on a fresh setup (`docker compose down --volumes` first), recorded as the fallback video.
- [ ] The day before: pull `main`, fresh setup, quick run through.
