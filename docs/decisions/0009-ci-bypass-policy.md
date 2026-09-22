# 0009. Bypasses allowed but discouraged, justified, and followed up

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
A failing check can be bypassed only with a written reason and the teammate's approval. In a true emergency an admin can merge without approval. Either way, a follow-up issue makes sure someone looks at it afterwards.

## Context
The team wants CI to be strict, but a broken third-party tool or an urgent fix must not block all work. Bypasses must be visible and rare.

## Decision
- **Normal bypass:** a `bypass:<operation>` label. The PR description must include a *Bypass justification* (`pr-policy` fails otherwise), and the required approval from the teammate covers it. The operation still runs and shows ⚠️ in the report.
- `pr-policy` and `secret-scan` cannot be bypassed.
- **Emergency:** organization admins are on the ruleset bypass list in "pull requests only" mode, so even emergencies go through a PR. GitHub logs every ruleset bypass.
- **Follow-up:** any merge with a `bypass:*` label or without an approving review automatically opens a `post-merge-review` issue.

## Consequences
- Every bypass leaves three traces: the label, the justification, and (for emergencies) a follow-up issue.
- Labels can be applied by anyone with write access; the approval requirement, not the label, is the real control.

## Alternatives considered
- **No bypass at all:** safest on paper, but a tooling outage would block all merges.
- **Bypass by admins only:** no record of reasoning, and nothing prompts a later review.
