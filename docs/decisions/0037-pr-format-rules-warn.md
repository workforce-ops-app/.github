# 0037. PR format rules warn instead of failing CI

- **Status:** Accepted
- **Date:** 2026-10-11

## In short
CI no longer fails a pull request because of how it is written. A title, branch name, or description that does not follow the conventions now shows as a warning in the CI report. CI still fails on the rules that protect the project: where a pull request may be merged, no `Co-authored-by` trailers, and a written reason for any bypass.

## Context
`pr-policy` ([0008](0008-ci-pipeline-and-report.md)) failed a pull request whose title, branch name, or `## Summary`, `## What changed`, or `## Details` section did not follow the conventions. In practice this blocked finished work over wording, and the author had to edit the description and wait for CI again before review could start. Every pull request is already read and approved by the other teammate, who can ask for a missing section in review. The same check also enforces rules that review alone could miss, such as a pull request opened from a `review/*` branch.

## Decision
- **Warnings (shown in the report, never block merging):** the title format `<type>(<area>): <summary>`, the branch name `<type>/<issue#>-<slug>`, the filled-in `## Summary`, `## What changed`, and `## Details` sections (`## Summary` for promotions), plus the existing warnings (no linked issue, code changed without docs).
- **Errors (still fail `ci / overall`):** a pull request from a `review/*` branch; anything other than `main` into `production`; a target other than `main` or `production`; a `Co-authored-by` trailer in any commit; a `bypass:*` label without a written *Bypass justification*.
- The conventions themselves do not change ([naming](../contributing/naming.md), [issues and PRs](../contributing/issues-and-prs.md)). The reviewer asks for fixes, and the local commit-message hook still checks commit subjects.
- `pr-policy` still cannot be bypassed ([0009](0009-ci-bypass-policy.md)).

## Consequences
- A pull request can be reviewed and merged with a non-standard title or an incomplete description, so the reviewer has to check them. On `main` the squash commit takes the pull request title, so a wrong title ends up in the history unless it is fixed before merging.
- Fewer CI reruns for wording changes.

## Alternatives considered
- **Remove `pr-policy` entirely:** would also drop the only CI check for `review/*` branches, the production flow, and `Co-authored-by` trailers, which the local hooks catch only on machines where they are installed.
- **Keep everything as errors:** blocks finished work over wording that review already covers.
