# Repository setup

**In short:** the one-time steps to create the organization and repositories and switch on the protections the workflow relies on. Follow them in order. The first commit goes straight to `main`; after the rules are switched on, everything goes through pull requests.

## 1. Organization

1. Create the organization. Display name: **Workforce Operations Application**. URL name: `workforce-ops-app`.
2. Add both team members as **owners**.
3. Create a team named **`maintainers`** containing both members. `CODEOWNERS` requests reviews from it.
4. **Settings → Actions → General**
   - Workflow permissions: **Read repository contents and packages permissions**. Each workflow asks for more only where it needs it.
   - **Allow GitHub Actions to create and approve pull requests: off.** Automation must never be able to approve a PR.
5. **Settings → Repository → default labels:** optional; labels are synced from `labels.yml` instead.

## 2. Repositories

Create three **public** repositories with no license: `.github`, `workforce-ops-backend`, `workforce-ops-frontend`. For each:

1. Push the initial scaffold straight to `main` (the only direct push).
2. **Settings → General → Pull Requests**
   - Allow merge commits: **on** (used only for `main` → `production`)
   - Allow squash merging: **on**, default message **Pull request title and description**
   - Allow rebase merging: **off**
   - Always suggest updating pull request branches: **on**
   - **Automatically delete head branches: on**
3. Application repositories only: create the `production` branch from `main`. The `.github` repository has no `production` branch, because other repositories use its workflows and hooks straight from `main` (and from tags).
4. **Settings → Code security**: turn on
   - Dependency graph, Dependabot alerts, Dependabot security updates
   - Secret scanning and **push protection**
   - Code scanning → CodeQL **default setup** (languages: Python, JavaScript, Actions)
   - **Private vulnerability reporting**
5. **Settings → Secrets and variables → Actions → Variables**: add `DEPLOY_ENABLED` = `false` (application repositories).
6. **Settings → Environments**: `production` is created on the first deploy run; no protection rules are needed yet.

## 3. Rulesets (organization level)

**Organization Settings → Repository → Rulesets.** Target all three repositories.

**`main`**: target branch `main`
- Restrict deletions; block force pushes
- Require a pull request before merging
  - Required approvals: **1**
  - Dismiss stale approvals when new commits are pushed
  - Require review from Code Owners
  - Require approval of the most recent reviewable push
  - Require conversation resolution
  - Allowed merge methods: **Squash**
- Require status checks to pass: **`ci / overall`**, and require branches to be up to date
- Bypass list: **Organization admins, mode "For pull requests only"** (the emergency path; it is logged)

**`production`**: target branch `production`
- Same as `main`, except allowed merge methods: **Merge** only

`review/*` branches have **no** ruleset: the automation force-pushes `review/integration`.

**`.github` tags**: in the `.github` repository, a tag ruleset on `v*` that restricts updates and deletions, because other repositories pin hooks to these tags.

## 4. Shared pieces

1. In the `.github` repository, create tag **`v0.1.0`**. The application repositories' `.pre-commit-config.yaml` pins it.
2. Sync labels: `gh auth login`, then `python scripts/sync_labels.py`.
3. Clone the repositories side by side and run `pre-commit install` in each ([local setup](local-setup.md)).

## 5. Check it works

Open a small test PR in each repository (for example a docs typo) and confirm:
- the CI report comment appears and `ci / overall` is required;
- merging is blocked until the teammate approves;
- `review/integration` is created and shows the PR;
- after merging, the remote branch is deleted automatically.

## Renaming the organization later

The display name can change at any time. Changing the **URL name** (`workforce-ops-app`) redirects repository links, but these references must be updated by hand:

| Where | What |
|---|---|
| `.github/workflows/*.yml` in each application repository | `uses: workforce-ops-app/.github/...` |
| `.pre-commit-config.yaml` in each application repository | `repo: https://github.com/workforce-ops-app/.github` |
| `.github/CODEOWNERS` in each repository | `@workforce-ops-app/maintainers` |
| `.github/workflows/post-merge-review.yml` in each repository | `review-team:` input |
| `scripts/sync_labels.py` | `ORG` |
| `.github/ISSUE_TEMPLATE/config.yml`, `SECURITY.md`, `CONTRIBUTING.md`, `profile/README.md`, docs | links |

Search all three repositories for `workforce-ops-app` to find every occurrence.
