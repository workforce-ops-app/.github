# Research report plan

**In short:** the security course requires a final report of at most 10 pages in IEEE conference format. This page lists each section, what it should contain, and where the evidence comes from, so the evidence is collected while the application is built instead of reconstructed at the end.

## Format

- IEEE conference proceedings template, **at most 10 pages**, PDF or Word.
- File name: `DescriptivePhrase ProjReport.pdf`, e.g. `Secure Workforce Operations ProjReport.pdf`.
- **Structured abstract:** Context, Goal, Method, Results, Conclusions (4–6 sentences).
- Each team member submits their own copy.

## Research questions

| # | Question | Answered by |
|---|---|---|
| RQ1 | What types of attacks can pattern-based (regular expression) inspection of input detect reliably? | the detection study: precision, recall, and F1 per attack type on a held-out test set |
| RQ2 | Are internal or external threats more common? | two parts: **(a)** real-world prevalence from published breach data (e.g. the Verizon Data Breach Investigations Report); **(b)** in our audits, findings by attacker profile, presented as a case study, not a general claim |
| RQ3 | What part of the system is the most vulnerable? | the findings log, grouped by component and severity |

RQ2 was refined from the proposal's wording, because the application alone cannot measure real-world prevalence.

## Sections and evidence

| Section | Content | Evidence source |
|---|---|---|
| Title, authors | both team members | |
| Abstract | structured, see above | |
| Introduction | problem, motivation, the three research questions and why we expect what we expect | security proposal |
| Background | multi-tenant SaaS, RBAC with scopes, the web attacks covered in the course | course material |
| Related work | secure development and testing practice | textbooks and references below; published breach data |
| Methodology | how the application was designed, audited, and measured: threat model, ASVS Level 2 audits, tools, cross-attacking, detection study design, **how test data was selected** | threat model; design review; decision records |
| Evaluation / findings | results per research question | findings log; detection study results; CI reports; restore drill times |
| Threats to validity | selection of test data, pattern tuning, lab (not production) environment, small team, out-of-scope network attacks, design choices such as the password policy | detection study notes; decision records |
| Discussion | what the results mean, limits of each claim | |
| Conclusion and future work | claims matched to the strength of the evidence | |
| Citations | | |

## Course alignment

The course topics that apply to a web application are tested and discussed by name:

| Course topic | Where it shows up |
|---|---|
| SQL injection | database access through SQLAlchemy only; sqlmap and ZAP testing; detection study |
| Session hijacking | server-side sessions, `__Host-` cookie, ID rotation, idle and maximum timeouts |
| Cross-site request forgery | CSRF tokens, SameSite cookies, Origin checks |
| Cross-site scripting | safe rendering, plain text plus bold announcements, Content Security Policy |
| Cryptography | HMAC-signed audit chains; Argon2id password hashing |
| Secure coding, defense mechanisms | layered tenant isolation, escalation rules, static analysis in CI |

Low-level topics (buffer overflows, return-oriented programming, memory safety) do not apply to a Python and JavaScript application; the report says so in one sentence.

Each finding in the log records **tool → vulnerability → code fix → regression test**, which demonstrates the course outcomes directly (apply tools, spot vulnerabilities, mitigate by refining code).

## Candidate references

- Mark Stamp, *Information Security: Principles and Practice*
- Wenliang Du, *Computer & Internet Security: A Hands-on Approach*
- Gary McGraw, *Software Security: Building Security In*
- Brian Chess and Jacob West, *Secure Programming with Static Analysis*
- OWASP Application Security Verification Standard (ASVS) 4.x/5.x
- NIST SP 800-63B, revision 4 (authentication)
- Verizon Data Breach Investigations Report (latest edition)

## Quality check before submitting

Lessons from reviews of research papers in this field:
- **Explain how test data was chosen** (selection bias is a common criticism).
- **Keep claims proportionate** to the evidence; avoid words like "substantially".
- **Answer each research question exactly as asked**, with its limits stated.
- **Motivate each research question.**
- **Make it replicable:** publish datasets, scripts, and instructions in the research repository.

Before submission, each teammate writes a critique of the draft in the course's critique format (short summary, at least three strengths, at least three weaknesses), and the weaknesses are fixed.
