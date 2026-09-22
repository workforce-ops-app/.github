# Documentation

**In short:** documentation is part of the change, not an afterthought. Every pull request updates the documents its change affects, in the same PR. Each repository documents its own code; this repository holds what is shared.

## The document categories

| Category | Answers | Backend | Frontend |
|---|---|---|---|
| **Project Architecture** | How is it built and why? | `docs/architecture/`: layers, modules, data model (schema diagrams), auth/authz, tenancy, audit, jobs | `docs/architecture/`: page structure, `js/api/` layer, components, security measures (CSP, safe rendering) |
| **Contributor Documentation** | How do I work on it? | `docs/contributing/`: setup, commands, conventions for this repo | same, for the frontend |
| **User Documentation** | How do I use it? | `docs/user/`: API usage for frontend developers and integrators | `docs/user/`: guides per role (employee, manager, administrator, owner) |
| **Project Features** | What can it do? | `docs/features/<feature>.md`: rules, permissions, states, endpoints, data, audit events | `docs/features/<feature>.md`: screens, flows, which endpoints each uses |

Additional documents:

| Document | Where | Purpose |
|---|---|---|
| Decision records | `.github/docs/decisions/` | What was decided, why, and what else was considered |
| API reference | backend `docs/api/` | Generated from the OpenAPI spec; PRs note contract changes |
| Security | backend `docs/security/` | Threat model, list of controls, findings log |
| Operations | backend `docs/operations/` | Backup and restore, recovery, later deployment |
| Glossary | backend `docs/architecture/glossary.md` | Shared vocabulary: tenant, scope, stewardship, candidate… |
| Shared contributor guide | `.github/docs/contributing/` | This guide |
| Release notes | GitHub Releases | Generated from PR titles; there is no hand-edited changelog |

## Rules

1. **Same PR.** Update the docs in the PR that changes the behavior. The PR template has a checklist, and CI warns when code changes without any docs change. Use the `docs:not-needed` label when a change really needs none, such as an internal refactor.
2. **Plain language first.** Every document starts with a short **In short:** paragraph a non-developer can follow, then the details.
3. **One file per feature, decision, and guide page.** Small files keep documentation PRs from conflicting.
4. **Diagrams as code.** Use Mermaid in Markdown (GitHub renders it) so diagrams are reviewed and versioned like code.
5. **Describe what exists.** Planned work belongs in issues, not in the docs. A feature doc may have a *Status* line (planned / in progress / done).
6. **Security findings stay private until fixed.** Add them to the findings log only after the fix merges.
7. **New decisions get a record.** When a PR makes a decision that others would ask "why?" about, add a decision record in the same PR (or a linked `.github` PR).

## Templates

Start from the files in [`docs/templates/`](../templates/):

- `feature.md`: a feature document
- `decision.md`: a decision record
- `user-guide.md`: a user guide page
- `runbook.md`: an operations procedure
