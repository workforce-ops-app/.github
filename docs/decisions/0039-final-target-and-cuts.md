# 0039. Finish the demo and the report by Dec 8, and move four items to stretch

- **Status:** Accepted
- **Date:** 2026-11-19

## In short
The final presentation is on 2026-12-08 and the security report is due 2026-12-10. The team finishes both by 2026-12-08. To fit, four items that neither course requires move to stretch: automatic decline of time-off requests, the audit log viewer, the department calendar on phones, and a days-down calendar prototype. The five demo features of [0038](0038-final-demo-scope.md) and every piece of evidence the [report plan](../project/report-plan.md) names stay. Slices may be built ahead of review.

## Context
On 2026-11-19 about 25 to 30 pull requests remained for the demo, plus three audits and their fixes, the detection scoring, the restore drill, and most of the report's results sections. Most pull requests take two or three review rounds, so with 19 days left the plan needed about two merges a day. The Roadmap (#24) already listed cuts to make "if time runs short".

The report has a hard internal deadline of its own: each teammate critiques the full draft and the weaknesses are fixed before submission, so a complete draft is needed several days before it is due.

## Decision
- **Target:** the demo and the report are both finished by 2026-12-08. The order of the remaining work is free, as long as every requirement below is covered.
- **Moved to stretch:**
  - **Automatic decline** of time-off requests nobody reviewed in time (workforce-ops-app/workforce-ops-backend#65). Requests stay pending until a manager in the chain reviews them or the employee cancels.
  - **The audit log viewer** (workforce-ops-app/workforce-ops-frontend#64). Audit log verification (workforce-ops-app/workforce-ops-backend#58) is built and gives the report its evidence.
  - **The department calendar on phones** (CAL4, workforce-ops-app/workforce-ops-frontend#84). The calendar is shown on laptop and desktop screens in the demo.
  - **A days-down calendar prototype** (each day a row, hours across), considered on 2026-11-17 for crowded days. The calendar keeps the layout in 0038.
- **Stays, for the web course:** the five features of 0038 (department calendar with the people menu, announcements, time off with approval through the reporting chain, swaps and coverage, company sign-up and screens for each permission level), the security page, and a demo that shows AJAX.
- **Stays, for the security course:** the three audits (frontend, internal user, external attacker) and their fixes, the detection study (datasets, scoring, results), the timed restore drill, the queued security fixes for the course topics in the report plan (including the memory-safety check of native code), and the report with both critiques.
- **Building ahead of review:** a slice may start on the branch of the slice it depends on before that one is reviewed. Its pull request still targets main and names the pull request to merge first. Unmerged work is combined in a `review/*` branch for testing (see [0007](0007-review-integration-branch.md)). Merging still needs the other teammate's approval and passing CI. The audits and the detection scoring may run against a `review/*` branch, recording the commit they tested.
- **Adjusting the plan:** either teammate may propose changes in review; changes to scope are recorded as decisions.

## Consequences
- The demo path of 0038 is unchanged: a company signs up, sets up its people and roles, plans the week, posts an announcement, and an employee arranges a swap.
- A time-off request can stay pending if nobody reviews it. The demo shows requests being reviewed, and the report lists automatic decline as future work.
- Stacked branches need updating from main after each merge below them, so reviews work best in batches, merged from the bottom of the stack up.
- Audit findings found against a `review/*` branch are fixed on the branch of the slice they belong to, or in their own fix slice.
- Issues for the moved items go to the **Stretch** milestone rather than being closed.

## Alternatives considered
- **Keep the full 0038 scope:** needs about two merges a day with no slack for audit findings or the report critiques.
- **Cut the memory-safety check** (workforce-ops-app/workforce-ops-backend#107): small, and the report plan names memory safety as a course topic the report covers.
- **Cut backup and restore** (workforce-ops-app/workforce-ops-backend#117): the restore drill times are evidence for research question RQ3.
- **Wait for each review before starting the next slice:** leaves days idle while reviews are pending.
