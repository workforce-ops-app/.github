# 0013. Four documentation categories, docs in the same PR

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Every repository documents its architecture, how to contribute, how to use it, and what features it has. Documentation is updated in the same pull request as the change it describes.

## Context
Documentation written after the fact is often never written. The project also needs security and decision documentation for its write-up.

## Decision
- Each application repository has `docs/architecture/`, `docs/contributing/`, `docs/user/`, and `docs/features/`. The backend adds `docs/api/`, `docs/security/`, and `docs/operations/`.
- Shared material (contributor guide, decision records, templates) lives in `.github/docs/`.
- Every document opens with a plain-language **In short:** paragraph.
- One file per feature, decision, and guide page; diagrams in Mermaid.
- The PR template includes a documentation checklist; `pr-policy` warns (does not fail) when code changes without docs, unless the PR has the `docs:not-needed` label.
- Release notes are generated from PR titles instead of a hand-edited changelog.

## Consequences
- Reviewers check docs as part of every review.
- Security findings are added to the findings log only after the fix merges, because the repositories are public.

## Alternatives considered
- **A separate documentation site or wiki:** drifts from the code and is not reviewed through PRs.
- **Failing CI when docs are missing:** too blunt; many changes legitimately need none.
