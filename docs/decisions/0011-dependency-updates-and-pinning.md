# 0011. Dependabot updates and SHA-pinned actions

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
A bot checks every week for newer versions of everything the project depends on and opens pull requests to update them. Third-party CI actions are locked to exact versions so they cannot change underneath us.

## Context
Outdated dependencies are a common source of vulnerabilities, and CI actions referenced by movable tags are a supply-chain risk. Updates must still be reviewed like any other change.

## Decision
- Dependabot version updates run weekly for every ecosystem in each repository, grouping minor and patch updates into one PR per ecosystem and keeping major updates separate.
- Dependabot PR titles use `chore(deps)` and labels `type:chore`, `area:deps`, so they fit the naming rules. `pr-policy` exempts them from branch-name, template, and docs rules only.
- Dependabot security updates are enabled.
- Third-party actions are pinned to full commit SHAs with the version in a comment; Dependabot updates both.
- The project's own reusable workflows are referenced at `@main`, because they are reviewed through the same process.
- pre-commit hook versions are refreshed with `pre-commit autoupdate`.

## Consequences
- A steady trickle of small PRs to review; grouping keeps it manageable.
- Ecosystems with no manifest yet (for example `npm` before `package.json` exists) show a Dependabot error until the files are added; this is expected.

## Alternatives considered
- **Manual updates:** easy to forget, especially for security fixes.
- **Renovate:** more configurable, but an extra app to install when Dependabot is built in.
