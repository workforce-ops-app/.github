# 0002. Separate backend and frontend repositories plus a shared `.github` repository

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
The backend and frontend live in separate repositories so their changes stay independent. A third repository, `.github`, holds what both share: templates, CI, hooks, labels, and the contributor guide.

## Context
The team wants modular pull requests that rarely conflict. The two halves use different toolchains (Python and JavaScript) and can be reviewed separately. Shared process rules must not drift between repositories.

## Decision
- A GitHub organization, `workforce-ops-app`, owns three public repositories: `workforce-ops-backend`, `workforce-ops-frontend`, and `.github`.
- GitHub uses the `.github` repository's issue templates, PR template, `CONTRIBUTING.md`, and `SECURITY.md` as defaults for every repository in the organization. The name must be exactly `.github` and the repository must be public.
- CI logic lives in reusable workflows and scripts in `.github`; each application repository has short caller workflows and a `ci.toml`.
- Both members are organization owners; a `maintainers` team owns review requests.

## Consequences
- Backend and frontend PRs never conflict with each other.
- A feature spanning both needs an issue in each, linked together, and the API contract must be documented (PR template section *API contract changes*).
- Workflows and templates are not inherited automatically; each repository calls the shared workflows explicitly, which also makes each repository's CI visible in its own files.
- Renaming the organization's URL name requires updating references (see [repository setup](../contributing/repository-setup.md#renaming-the-organization-later)).

## Alternatives considered
- **One repository (monorepo):** simpler cross-cutting changes, but frontend and backend PRs would share files such as CI config and docs indexes and conflict more often.
- **No shared repository:** templates and CI would be copied into each repository and drift apart.
