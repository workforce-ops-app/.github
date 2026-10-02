# Issues and pull requests

**In short:** every issue and pull request starts with a plain-language explanation anyone could follow, then a *Details* section for the technical specifics. The templates provide this structure; keep it even when writing from the command line.

## The shared structure

```
## Summary            ← plain language: what and for whom
## Why it matters     ← plain language (issues)   /   ## What changed (PRs)
---
## Details            ← technical specifics, as subsections
```

Plain language means no jargon a non-developer would stumble on. "Employees can now ask for days off and see whether their manager approved" rather than "Adds POST /api/time-off with state machine".

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

## Slices and tracker issues

- **A slice** is one issue that becomes one pull request: one topic, small enough to review in one sitting, and at most one database migration.
- **A tracker issue** groups the slices of a larger piece of work, such as a phase or a feature. It lists each slice as a checkbox with a link, says in which order they go and what depends on what, and is closed by hand once its last slice merges. Nobody works on a tracker directly, and no pull request closes one.
- **Design before code:** the first slice of a feature is its design page (the backend feature page, plus a short frontend page for its screens). Code slices start once that page has merged.
- **The overall plan** (phases, what each phase must prove before the next starts, and each phase's tracker) is the pinned **Roadmap** issue in this repository.

## Issues that depend on other work

Issues can be filed before the work they need has merged, as long as they say what they wait for. Nobody starts an issue until everything it depends on has merged.

In the issue's *Related* section, one line per dependency:

```
Depends on #29 (in review as #36)            ← must merge before work on this issue starts
Depends on workforce-ops-app/workforce-ops-backend#30
Refs workforce-ops-app/.github#22            ← the tracker this slice belongs to
```

- **Link the issue, not only the pull request.** The issue number never changes; a pull request can be closed and replaced. Mention the pull request in parentheses when one is open.
- **Say why in plain language** in the issue's notes, for example "needs the database layer to store sessions", so the reason makes sense to someone who isn't a developer.
- **Keep the tracker in order.** The tracker lists the slice after the slices it depends on.
- A pull request whose issue had dependencies says in *Merge notes* which pull requests must merge first, if any are still open.

## Closing issues from a pull request

In *Related issues*:

```
Closes #14                                   ← this PR finishes the issue; merging closes it
Closes workforce-ops-app/workforce-ops-backend#3   ← same, in another repository
Refs #22                                     ← related but not finished: a tracker, the design sign-off, the other repository's twin issue
```

Squash merges use the PR description as the commit message, so the keyword in the PR description is what closes the issue. When a slice merges, tick its box in the tracker.

## Linking across repositories

A feature that spans both repositories gets an issue in each, and each links to the other in *Related*:

```
Refs workforce-ops-app/workforce-ops-frontend#12
```

Merge the backend PR first when the frontend depends on a new endpoint, and say so in *Merge notes*.
