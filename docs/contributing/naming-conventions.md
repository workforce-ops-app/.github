# Naming conventions

**In short:** issues, pull requests, and commits all use the same title format, `<type>(<area>): <summary>`. Branches use `<type>/<issue#>-<slug>`. Local hooks and CI enforce both.

## Types

| Type | Use for |
|---|---|
| `feat` | New functionality or a user-visible change |
| `fix` | Something that was broken |
| `security` | A security control, hardening, or a fix for a security finding |
| `refactor` | Restructuring with no behavior change |
| `test` | Tests only |
| `docs` | Documentation only |
| `chore` | Tooling, CI, dependencies, maintenance |

## Titles (issues, PRs, commit subjects)

```
<type>(<area>): <summary>
feat(time-off): add request submission endpoint
fix(auth): reject expired sessions
chore(deps): bump ruff from 0.16.7 to 0.16.8
```

- `area` is lowercase with hyphens: a module (`time-off`, `schedules`), a concern (`auth`, `authz`, `tenancy`, `audit`, `ci`, `docs`), or `ui` for shared frontend pieces.
- The summary is an imperative phrase ("add", "fix", "remove") and has no trailing period.
- Add `!` after the area for a breaking change: `feat(api)!: rename shift fields`.

## Branches

```
<type>/<issue#>-<slug>
feat/14-time-off-requests
security/31-csrf-on-logout
```

- The issue number is strongly encouraged; a branch without one gets a warning.
- The slug is lowercase words joined by hyphens.
- Reserved: `main`, `production`, `review/*`. Dependabot uses `dependabot/*`.

## Commit messages

```
feat(time-off): add request model and migration

Optional body explaining why, wrapped at ~72 characters.

Refs #14
```

- Subject in the title format, then a blank line, then an optional body.
- Reference the issue or PR with `Refs #N` (related) or `Closes #N` (completes it). Use `Refs workforce-ops-app/<repo>#N` for the other repository.
- `Co-authored-by` trailers are not used.

## Labels

Defined in [`labels.yml`](../../labels.yml):

| Group | Examples |
|---|---|
| `type:*` | matches the title type |
| `area:*` | module or concern; add new ones to `labels.yml` when a module is added |
| `priority:*` | `high`, `medium`, `low` |
| Security | `security` (touches a control), `security-finding` (audit result) |
| Process | `docs:not-needed`, `bypass:<check>`, `post-merge-review` |
