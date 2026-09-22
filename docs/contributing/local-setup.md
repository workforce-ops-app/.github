# Local setup

**In short:** clone all three repositories side by side into one folder, install the listed tools, and run `pre-commit install` in each clone. Then the same checks that run on pull requests also run on your machine.

## Tools

| Tool | Version | Used for |
|---|---|---|
| Git | recent | version control |
| Python | 3.13 | backend, CI runner, git hooks |
| Node.js | 22 LTS | frontend tooling only (formatting, linting, tests) |
| Docker Desktop | recent | MySQL, image builds, integration tests, secret scanning |
| pre-commit | latest (`python -m pip install pre-commit`) | local git hooks |
| GitHub CLI (`gh`) | recent | issues, PRs, branch cleanup |

## Folder layout

Clone the repositories next to each other. The CI runner is referenced by relative path, so this layout matters:

```
workforce-ops/                  any name
├── .github/                    git clone https://github.com/workforce-ops-app/.github
├── workforce-ops-backend/      git clone https://github.com/workforce-ops-app/workforce-ops-backend
└── workforce-ops-frontend/     git clone https://github.com/workforce-ops-app/workforce-ops-frontend
```

## Git hooks

In each application repository:

```
pre-commit install
```

This installs three hook types, configured in `.pre-commit-config.yaml`:

| When | What it checks |
|---|---|
| On commit | formatting, lint, whitespace/line endings, large files, secrets |
| On the commit message | `<type>(<area>): <summary>` format and no `Co-authored-by` trailers; adds `Refs #N` from the branch name if missing |
| On push | branch name format; blocks direct pushes to `main` and `production` |

Hooks can be skipped with `--no-verify`, but CI runs the same rules and will fail the pull request.

## Running the CI checks locally

From a repository root:

```
python ../.github/scripts/ci_runner.py              # everything
python ../.github/scripts/ci_runner.py --only lint  # one operation
```

Locally the runner does not install dependencies; use your own virtual environment (`python -m venv .venv`) or `npm ci`. Operations that need files that do not exist yet are skipped with the reason shown.

## Line endings on Windows

Every repository has a `.gitattributes` that stores text files with LF line endings. Leave `core.autocrlf` at its default; the attributes file takes precedence.
