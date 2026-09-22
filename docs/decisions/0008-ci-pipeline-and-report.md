# 0008. Shared CI pipeline with a single PR report comment

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Every pull request runs one standard set of checks, and the results appear as a single table comment on the PR that updates with each push. Contributors can run the exact same checks on their own machine first.

## Context
Problems that slip past local work should be caught before merging, and results should be easy to read for both team members. The checks are also evidence for the project's security write-up.

## Decision
- A reusable workflow in `.github` runs `pr-policy` plus every operation listed in the calling repository's `ci.toml`, using one runner script (`scripts/ci_runner.py`) that also runs locally.
- Operations whose required files do not exist yet are skipped with the reason shown, so checks switch on as the code grows.
- One job, `overall`, builds the report and fails if anything failed; **`ci / overall` is the only required status check**.
- A separate `workflow_run` workflow posts or updates the PR comment (identified by a hidden marker). It runs apart from CI so it can post on PRs whose CI token is read-only (Dependabot), and it verifies that the report belongs to the PR's current commit before posting.
- The naming and message rules live in one Python module shared by the local git hooks and `pr-policy`.
- A `deploy` workflow exists for `production` but performs a dry run until a hosting target is chosen and `DEPLOY_ENABLED` is set.

## Consequences
- Adding a check means adding an entry to `ci.toml` (and a `bypass:` label).
- Changing the pipeline in `.github` changes it for every repository at once, so pipeline PRs deserve careful review.
- Security checks (secret scanning, dependency audit, security lint rules, security tests) are part of every PR by default.

## Alternatives considered
- **One workflow job per check:** GitHub shows each natively, but the report would need to collect results from many jobs, and local runs would differ from CI.
- **A third-party CI service:** another account and configuration to manage for no clear gain.
