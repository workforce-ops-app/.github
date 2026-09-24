# 0029. Request approval routing

- **Status:** Accepted ("any denial ends the request" pending discussion)
- **Date:** 2026-09-23

## In short
Requests such as time off and shift coverage go to the managers whose scope covers the employee. A company can require more than one approval. Everyone else involved is kept informed, a request can never get stuck, and nobody can approve their own request.

## Context
The proposal routes requests to "the appropriate manager based on the employee's assigned management structure". With scoped role assignments ([0017](0017-scoped-role-assignments.md)), several managers can cover the same employee, which happens in real workplaces.

## Decision
- **Reviewers:** everyone holding the review permission whose scope covers the employee.
- **Required approvals:** a company setting per request type; **default 1**. Other covering managers are notified of every review and decision.
- **Denials (pending):** proposed that any denial ends the request.
- **Too few reviewers:** when the required count exceeds the available managers, administrators and higher are notified of the misconfiguration, and the requirement drops to all available managers; with no eligible reviewer at all, the request goes to administrators.
- **No self-review:** nobody reviews their own request; a manager's own requests go to their managers or administrators.
- **Re-check at approval** for coverage and swaps: eligibility is checked again at the moment of approval.

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Security tests cover self-approval and approval from outside scope.
- A "pending approvals" record is shared by time off, coverage, and sensitive actions.

## Alternatives considered
- **A single designated manager per employee:** simpler, but doesn't match scoped assignments or real practice.
- **Majority vote:** harder to explain and to audit.
