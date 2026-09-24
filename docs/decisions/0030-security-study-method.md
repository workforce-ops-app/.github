# 0030. Security study method

- **Status:** Accepted
- **Date:** 2026-09-23

## In short
Security is audited against a recognised checklist with standard tools, only on our own test copies, with teammates attacking each other's work. A separate detection study measures pattern matching fairly. Everything found is recorded with its fix, as evidence for the research report.

## Context
The security course grades a research report with methodology, findings, and threats to validity. The instructor's field values standard, justified tools, documented data selection, replicability, and claims proportionate to the evidence.

## Decision
- **Checklist:** OWASP ASVS Level 2, applicable chapters only, with course topics mapped to checks.
- **Tools:** OWASP ZAP, sqlmap, Burp Suite Community, plus the CI security checks.
- **Scope:** local and test copies only.
- **Roles:** cross-attacking per phase; the external phase together.
- **Findings:** template → private advisory until fixed → findings log (tool, vulnerability, fix, regression test).
- **Detection study:** public attack collections plus tricky benign input; documented selection; tuned and scored on separate sets; precision/recall/F1 per type, confusion matrix, timing; log only.
- **Threat model:** STRIDE on a data-flow diagram with four attacker profiles, before coding.
- **Research questions:** RQ2 split into published prevalence and our own case-study findings.
- **Artifacts** go to the public `workforce-ops-research` repository as a replication package.

Details: [design review 7](../project/design-review/07-security-study.md) and the [report plan](../project/report-plan.md).

## Consequences
- The audits produce a steady stream of issues and fixes, visible in the repositories for grading and peer evaluation.
- The attacker profiles make RQ2's case-study data consistent.

## Alternatives considered
- **OWASP Top 10 only:** quicker, but a list of risk categories rather than testable requirements.
- **Self-auditing only:** people miss flaws in their own code.
