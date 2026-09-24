# Design review 7: Security study

**In short:** how the application's security is tested and measured for the research report. Audits follow an industry checklist (OWASP ASVS Level 2) using standard free tools, with each teammate attacking the other's features. A detection study measures how well pattern matching spots attacks. A threat model written before coding guides it all.

| # | Question | Answer | Status |
|---|---|---|---|
| 7.1 | What yardstick do the audits use? | **OWASP ASVS Level 2**, limited to the chapters that apply (authentication, sessions, access control, input handling, cryptography, logging), with each course topic mapped to its checks. | answered |
| 7.2 | Which tools? | OWASP ZAP (automated scanning), sqlmap (injection), Burp Suite Community (manual probing), plus CI: security lint rules, CodeQL, dependency audits, secret scanning. | answered |
| 7.3 | What may be attacked? | **Only our own local or test copies.** Never anything real or anyone else's. | answered |
| 7.4 | Who attacks what? | **Cross-attacking:** in each phase, each teammate attacks the features the other built; the external-attacker phase is done together. | answered; Corbin to confirm |
| 7.5 | How are findings handled? | Security-finding issue template; private advisory until fixed; then the findings log, recording **tool → vulnerability → code fix → regression test**. | answered |
| 7.6 | How is the detection study designed? | See below. | answered |
| 7.7 | Where do detection alerts go? | A **Security page** for owners and administrators (their company's events); in-app notifications for serious events (next); a cross-company view for platform staff and email alerts (stretch). | answered |
| 7.8 | Threat model format? | **STRIDE** on a data-flow diagram, with four attacker profiles; written before coding. | answered |
| 7.9 | How far does "availability" go? | **In:** rate limits, lockouts, list and request size caps, query timeouts, safe regular expressions, backup and restore. **Out:** network-flooding attacks (a hosting-provider concern), stated in the report's threats to validity. | answered |

## Detection study (research question 1)

- **Attack examples:** public collections such as PayloadsAllTheThings and SecLists (licenses checked), covering SQL injection, cross-site scripting, path traversal, and command injection.
- **Normal examples:** realistic everyday input, **including tricky harmless text** (names like *O'Brien*, notes like "please *select* a new shift" or "I'll *drop* by at 5"), because false alarms are what make pattern matching look bad.
- **Selection documented:** exactly how and why each example set was chosen, to address selection bias.
- **Fair scoring:** patterns are tuned on one set and scored on a separate, unseen set.
- **Measures:** precision, recall, and F1 per attack type; a confusion matrix; time taken per pattern (a slow pattern can freeze the server on crafted input, so this doubles as a safety check).
- **Log only, never block.** The real protection is how the application is built.

## Attacker profiles

| Profile | Examples | Research question 2 |
|---|---|---|
| Outside attacker | credential guessing, injection, scraping | external |
| Malicious employee | reading coworkers' data, approving their own requests | internal |
| Compromised manager or admin account | escalation, mass changes, audit tampering | internal (via stolen credentials) |
| Rogue platform staff | reading customer data without support access | internal (platform) |

## Research questions

| RQ | Answered by |
|---|---|
| 1. What can pattern matching detect reliably? | the detection study |
| 2. Internal vs external threats | (a) published breach data for real-world prevalence; (b) our findings by attacker profile, as a case study |
| 3. Most vulnerable part of the system | the findings log, by component and severity |

RQ2 was split because the application alone can't measure real-world prevalence. Consider a short note to the instructor about the refined wording.

## Course alignment

The report names and tests the course's web security topics (SQL injection, session hijacking, CSRF, XSS) and its cryptography (HMAC audit chains, Argon2id). See the [report plan](../report-plan.md#course-alignment).

Recorded as decision [0030](../../decisions/0030-security-study-method.md).
