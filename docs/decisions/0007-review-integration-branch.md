# 0007. Automatically rebuilt `review/integration` branch

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
A branch called `review/integration` always holds `main` plus every open pull request that is ready for review, merged together. The team can test everything at once, and clashes between PRs show up early. It is maintained automatically and can never be merged.

## Context
PRs are kept small and topic-focused, but they still need to be tested together, and conflicts between them are cheaper to fix early. Keeping a combined branch up to date by hand would drift.

## Decision
- A workflow rebuilds the branch from scratch on every push to `main` and whenever a PR into `main` is opened, updated, reopened, closed, or marked ready or draft.
- Ready PRs are merged onto `main` in PR-number order; drafts and PRs from forks are excluded.
- A PR that conflicts is left out and gets a comment naming what it conflicts with; the comment updates when it becomes clean.
- After pushing, the workflow dispatches CI on the branch, so the combination is tested.
- Other combinations go in separate `review/<purpose>` branches, created only when explicitly requested.
- `pr-policy` fails any PR whose head is a `review/*` branch. Git cannot block creating such a PR, but it can never pass the required check.

## Consequences
- The branch is force-pushed constantly; users update it with `git reset --hard`, never commit to it, and it has no branch protection.
- The rebuild job runs with write access, so it only performs git merges and never executes PR code; CI on the result runs separately with read-only access.

## Alternatives considered
- **Updating the branch by hand:** error-prone and quickly out of date.
- **Incremental merges instead of rebuilding:** closed or merged PRs would linger and history would grow tangled.
