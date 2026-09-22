# CI and the PR report

**In short:** every pull request runs the same set of checks. The results appear as one comment on the PR that updates with each push. A PR can merge only when the overall result is green. Bypassing a check is possible but discouraged, needs a written reason and the teammate's approval, and always leaves a record.

## The report comment

```
workforce-ops-backend — CI Report
python · commit 1e39397 · run log

| Operation        | Status | Summary                          | Time  |
| pr-policy        | ✅     | title, branch, description …     | 0.4s  |
| secret-scan      | ✅     | no secrets found                 | 3.1s  |
| audit            | ✅     | no known vulnerabilities         | 6.2s  |
| format-check     | ✅     | 42 files already formatted       | 0.3s  |
| lint             | ✅     | All checks passed!               | 0.5s  |
| typecheck        | ⏭️     | no app                           | —     |
| …                                                                         |
Overall: ✅ 5 passed · 0 failed · 3 skipped
```

| Icon | Meaning |
|---|---|
| ✅ | passed |
| ❌ | failed — blocks merging |
| ⏭️ | skipped — the files it needs do not exist yet (the summary says which) |
| ⚠️ | failed but bypassed with a label |

Warnings (for example "no linked issue" or "code changed but docs did not") are listed under the table and do not block merging.

## Operations

| Operation | Backend | Frontend |
|---|---|---|
| pr-policy | title, branch name, template sections, bypass justification, no `Co-authored-by`, not from `review/*` | same |
| secret-scan | gitleaks over the full history | same |
| audit | pip-audit | npm audit (high and critical) |
| format-check | ruff format | prettier |
| lint | ruff (includes security rules) | eslint, stylelint, html-validate |
| typecheck | mypy | tsc on JSDoc types |
| unit-test | pytest `tests/unit` | vitest |
| migration-check | one Alembic head; upgrade/downgrade on a fresh MySQL | — |
| security-test | pytest `tests/security` (cross-tenant, escalation) | header/CSP checks |
| build | Docker image | Docker image (nginx) |
| integration-test | compose up, health check, pytest `tests/integration` | Playwright |

Each repository lists its operations in `ci.toml` at its root. An operation switches on by itself once the files in its `requires` list exist, so nobody has to remember to enable checks as the project grows.

## How it is wired

- `.github/workflows/ci.yml` in each repository calls the shared `reusable-ci.yml` from the `.github` repository.
- **The one required status check is `ci / overall`.** It fails if any operation failed.
- `ci-comment.yml` posts the report as a PR comment after the run finishes. It runs separately so it can post even on Dependabot PRs, and it checks that the report belongs to the PR's current commit.
- `deploy.yml` runs on pushes to `production`. Until a hosting target exists it builds the image and reports a dry run. Setting the repository variable `DEPLOY_ENABLED` to `true` switches to the real deployment step once one is written.

## Adding or changing a check

Edit `ci.toml` in the repository:

```toml
[[operation]]
name = "lint"                    # also the bypass label: bypass:lint
run = "ruff check ."             # {repo} expands to the repository root
requires = ["pyproject.toml"]    # skipped until these exist
pass_summary = "0 problems"      # optional; default is the last line of output
local = true                     # false = CI only
timeout_minutes = 15
```

A new operation name also needs a `bypass:<name>` label in `labels.yml`.

## Bypassing a check

Bypasses are **strongly discouraged** and are for cases like a broken third-party tool or a known false positive, not for merging failing code.

1. Add the label `bypass:<operation>` (for example `bypass:typecheck`).
2. Fill in **Bypass justification** in the PR description: what failed, why it is safe to merge anyway, and the follow-up issue.
3. The teammate's approval covers the bypass. They should comment that they agree.

The operation still runs. The report shows ⚠️ and the overall check can pass. `pr-policy` and `secret-scan` cannot be bypassed.

## Emergency merges

If something must merge while the teammate is unavailable, an organization admin can use the ruleset bypass on the PR. GitHub logs every ruleset bypass.

After any merge with a `bypass:*` label or without an approving review, a workflow opens a **`post-merge-review`** issue for the teammate. That issue must be worked through like any other.
