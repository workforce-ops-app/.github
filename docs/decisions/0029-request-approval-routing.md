# 0029. Request approval routing

- **Status:** Accepted
- **Date:** 2026-09-23 (revised 2026-09-28 at sign-off)

## In short
Requests such as time off and shift coverage go to the employee's direct managers in the reporting chain. A company can require more than one approval. If the managers disagree, the request moves up to the nearest manager above all of them. A request can never get stuck, and nobody can approve their own request.

## Context
The proposal routes requests to "the appropriate manager based on the employee's assigned management structure". Reporting lines ([0024](0024-authorization-model.md)) record that structure, and a person can report to several managers, which happens in real workplaces.

## Decision
- **Reviewers:** the employee's **direct managers** in the reporting chain who hold the review permission. They are notified of every request. Anyone higher in the chain may also step in, but isn't notified of every request.
- **Required approvals:** a company setting per request type; **default 1**; counted among the direct managers. The other direct managers are notified of every review and decision.
- **Disagreement:** when the direct managers' decisions conflict, the request goes to their **nearest shared manager**, the lowest person above all of the disagreeing managers in the chain. That person's decision settles it. With no shared manager, the Owner decides. If several shared managers are equally near, all of them receive it and the first decision settles it.
- **Too few reviewers:** when the required count exceeds the direct managers available, administrators are notified of the misconfiguration and the requirement drops to all available direct managers; with no eligible reviewer at all, the request goes to administrators.
- **No self-review:** nobody reviews their own request; a manager's own requests go to their own managers in the chain.
- **Coverage requests, coworkers first:** the employee sends the request to eligible coworkers, who each answer **accept**, **swap** (offering one of their shifts in exchange), or **decline**. The list of answers, even an empty one, goes to the reviewers when everyone asked has answered or at a company-set deadline before the shift, whichever comes first; the employee may send it early. The manager chooses from the list, or finds coverage if the list is empty. The schedule does not change until the manager approves.
- **Re-check at approval** for coverage and swaps: eligibility is checked again at the moment of approval.

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Security tests cover self-approval, approval by someone not above the employee, and disagreement escalation.
- Finding the nearest shared manager walks the reporting chain upwards from each disagreeing manager.
- A "pending approvals" record is shared by time off and coverage.

## Alternatives considered
- **Everyone whose scope covers the employee reviews:** the original design; replaced because reporting lines say more precisely who manages whom.
- **Any denial ends the request:** lets one manager overrule the others and causes friction between managers.
- **Hold until the managers agree:** can stall a request until the shift has passed.
- **Majority vote:** harder to explain and to audit.
- **Managers find coverage themselves:** puts the whole burden on managers; coworkers who know their own availability respond faster.
