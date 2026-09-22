# Dependencies

**In short:** Dependabot checks weekly for new versions of our libraries, Docker images, and CI actions, and opens pull requests for them. They are reviewed and merged like any other PR. Major upgrades arrive one at a time so they get proper attention.

## Pinned versions

| Component | Version | Changed by |
|---|---|---|
| Python | 3.13 | a decision (Dependabot does not move it) |
| MySQL | 8.4 LTS | a decision; Dependabot applies 8.4.x patches only |
| Node.js | 22 LTS (tooling only) | a decision |
| Python / npm packages | pinned in lock files | Dependabot |
| Docker base images | pinned tags | Dependabot, within the versions above |
| GitHub Actions | pinned to exact commit SHAs, with the version in a comment | Dependabot |
| pre-commit hooks | `rev:` in `.pre-commit-config.yaml` | `pre-commit autoupdate` (monthly, in a `chore(deps)` PR) |

Actions are pinned to commit SHAs instead of tags like `@v7` because a tag can be moved to different code. This protects the supply chain.

## Dependabot configuration

Each repository has `.github/dependabot.yml`:

- **Schedule:** weekly on Monday.
- **Grouping:** minor and patch updates for an ecosystem arrive as one PR; major updates get their own PR.
- **Format:** titles are `chore(deps): …` (or `chore(deps-dev): …`) with labels `type:chore` and `area:deps`, so they pass `pr-policy`.
- **Ecosystems:** backend `pip`, `docker`, `docker-compose`, `github-actions`; frontend `npm`, `docker`, `github-actions`; `.github` `pip`, `github-actions`.

Dependabot security updates are also enabled; those PRs arrive whenever an advisory is published.

## Reviewing a Dependabot PR

1. Read the release notes Dependabot includes, especially for major versions.
2. Check the CI report. Dependabot PRs are exempt from branch-name, template, and docs rules, but every other check applies.
3. Approve and squash-merge. For a major upgrade that needs code changes, push the fixes to the Dependabot branch or close it and do the upgrade in a normal branch.

## Changing Python, MySQL, or Node versions

Write a decision record, then update the `ignore` rules in `dependabot.yml`, the Docker base images, the versions in the reusable CI workflow, and [local setup](local-setup.md) in one PR.
