# Issues and pull requests

**In short:** every issue and pull request starts with a plain-language explanation anyone could follow, then a *Details* section for the technical specifics. The templates provide this structure; keep it even when writing from the command line.

## The shared structure

```
## Summary            ← plain language: what and for whom
## Why it matters     ← plain language (issues)   /   ## What changed (PRs)
---
## Details            ← technical specifics, as subsections
```

Plain language means no jargon a non-developer would stumble on. "Employees can now ask for days off and see whether their manager approved" rather than "Adds POST /api/v1/time-off with state machine".

## Issue templates

| Template | Title starts with | Labels |
|---|---|---|
| Feature | `feat(<area>):` | `type:feat` |
| Bug | `fix(<area>):` | `type:fix` |
| Security finding | `security(<area>):` | `type:security`, `security-finding` |
| Chore / docs / refactor | `chore(<area>):` (or `docs`, `refactor`, `test`) | `type:chore` |

Add an `area:*` label and a `priority:*` label when filing. Blank issues are disabled.

From the command line, use the template file as the body so the structure stays identical:

```
gh issue create --template "Feature" --title "feat(time-off): add request submission"
```

**Security findings:** the repositories are public. An exploitable finding that is not fixed yet goes in a private advisory ([SECURITY.md](../../SECURITY.md)); file the public issue after the fix merges.

## Pull request template

Sections, in order:

| Section | Required | Notes |
|---|---|---|
| Summary | yes (CI checks) | plain language |
| What changed | yes (CI checks) | plain-language bullets |
| Details → Technical changes | yes | |
| Database / migrations | leave "None" if none | one migration per PR |
| API contract changes | leave "None" if none | the frontend depends on this |
| Security checklist | tick or strike through | |
| Documentation | tick what was updated | or apply `docs:not-needed` |
| How to test | yes | steps for the reviewer |
| Merge notes | "None" if none | dependencies on other PRs, conflict risk |
| Bypass justification | only with a `bypass:*` label | CI fails if a bypass label has no justification |
| Related issues | encouraged | `Closes #N` / `Refs #N` |

Promotion PRs (`main` → `production`) need only a `## Summary` listing the PRs included.

## Linking across repositories

A feature that spans both repositories gets an issue in each, and each links to the other in *Related*:

```
Refs workforce-ops-app/workforce-ops-frontend#12
```

Merge the backend PR first when the frontend depends on a new endpoint, and say so in *Merge notes*.
