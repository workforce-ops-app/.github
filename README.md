# .github — shared project configuration

**In short:** this repository holds what every Workforce Operations Application repository shares: the issue and pull request templates, the CI pipeline, the git hooks, the labels, and the team's contributor guide and decision records. Change a rule here and every repository picks it up.

## What is here

| Path | Purpose |
|---|---|
| `.github/ISSUE_TEMPLATE/`, `.github/PULL_REQUEST_TEMPLATE.md` | Default templates for every repository in the organization |
| `.github/workflows/reusable-*.yml` | The shared CI/CD steps; each repository calls them from short workflow files |
| `.github/workflows/ci.yml` (and the other non-`reusable` files) | This repository's own CI, using the same shared steps |
| `scripts/` | CI runner, report builder, PR policy, review-branch rebuild, follow-up issues, label sync |
| `hooks/`, `.pre-commit-hooks.yaml` | Git hooks (commit message, branch name) used by every repository via pre-commit |
| `labels.yml` | Shared labels, applied with `python scripts/sync_labels.py` |
| `docs/contributing/` | How we work: workflow, naming, CI, reviews, dependencies, documentation |
| `docs/decisions/` | Decision records: what we decided and why |
| `docs/templates/` | Starting points for feature docs, decision records, user guides, runbooks |
| `profile/README.md` | The organization's public landing page |
| `CONTRIBUTING.md`, `SECURITY.md` | Defaults shown by GitHub for every repository |

## Working on this repository

It follows the same workflow as the application repositories ([contributor guide](docs/contributing/README.md)). Its checks run with:

```
python -m pip install -r requirements-dev.txt
python scripts/ci_runner.py
```

Changes to `hooks/` reach the other repositories when a new tag is created (for example `v0.2.0`) and their `.pre-commit-config.yaml` is updated to it. Changes to `scripts/` and reusable workflows apply to every repository as soon as they merge to `main`.
