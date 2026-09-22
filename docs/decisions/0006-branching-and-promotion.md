# 0006. `main` → `production` with squash merges into `main`

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Work is merged into `main` one squashed commit per pull request. When `main` is ready to release, it is promoted to `production` with a regular merge. There is no staging branch.

## Context
Two developers need a simple flow with a clear history, and every change should trace back to an issue and a reviewed PR.

## Decision
- Topic branches `<type>/<issue#>-<slug>` → PR into `main`, **squash merge** (one commit per PR, message = PR title and description).
- `main` → PR into `production`, **merge commit** only. Squashing a promotion would rewrite its commits, so `production` would drift from `main` and every later promotion would show old changes again.
- Direct pushes and force-pushes to `main` and `production` are blocked by rulesets in each repository.
- Hotfixes use a normal `fix/*` branch into `main`, then a promotion.
- Local branches are cleaned up at the start of each task; remote branches are deleted automatically on merge.

## Consequences
- `main`'s history reads as a list of PR titles, which is also what release notes are generated from.
- A promotion PR lists exactly what will ship.
- There is no separate environment for pre-release testing; `review/integration` (see [0007](0007-review-integration-branch.md)) and CI fill that role for now.

## Alternatives considered
- **`main` → `staging` → `production`:** an extra promotion step without a staging environment to justify it yet.
- **Rebase merging:** keeps individual commits, but produces noisier history and is harder for beginners to recover from.
