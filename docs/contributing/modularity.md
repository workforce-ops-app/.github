# Modularity

**In short:** every change should stay inside the part of the code it is about. That keeps pull requests small and reviewable, lets them merge in any order without conflicts, and lets new features be added later without rewriting existing ones.

## Principles

1. **One topic per pull request.** Unrelated fixes found along the way get their own issue and branch.
2. **Work inside a module.** Backend features live in `app/modules/<feature>/`; frontend pages in their own page, script, and stylesheet files.
3. **Extend, don't edit, shared code.** Shared layers (`auth`, `authz`, `tenancy`, `audit`, `core`) expose registration points so features can plug in without modifying them.
4. **Readable over clever.** Clear names, small functions, comments that explain *why*.

## Common sources of merge conflicts

| Shared file or area | Rule |
|---|---|
| Router registration (`main.py`) | Routers are discovered from `app/modules/*/router.py`; do not edit `main.py` to add a module |
| Permission list | Each module declares its own permissions in `permissions.py`; the registry collects them |
| Database migrations | **One Alembic migration per PR.** If another PR's migration merged first, update your migration's `down_revision` before merging. CI fails when there are multiple heads |
| Changelog | There is no hand-edited changelog; release notes are generated from PR titles |
| Shared CSS / JS | Styles and scripts are per component and per page; the base files change rarely and in their own PRs |
| Navigation menu | Built from the list of pages a user may access, not hand-edited per feature |
| Company settings | Each module declares its own typed settings; there is no shared settings table to edit |
| Documentation | One file per feature, per decision, and per guide page, so docs PRs rarely touch the same file |

Conflicts are sometimes unavoidable. When one is likely, say so in the PR's *Merge notes* and agree on the merge order. `review/integration` will flag it early ([review branches](review-branches.md)).

## Built-in extension points

These patterns let features that are not planned yet be added without rewriting existing code:

| Pattern | What it lets a new feature do |
|---|---|
| Module discovery | Add endpoints by adding a module folder |
| Permission registry | Declare new permissions next to the code that checks them |
| Scope resolvers | Register how to find the company/department/team/employee a new resource belongs to, so `authorize()` works for it without changes |
| Internal events | Publish events (for example `shift.reassigned`) that notifications, audit, and detection can react to, without the modules calling each other |
| Module settings | Declare company-configurable policies (deadlines, cutoffs) with types and defaults |
| API versioning | Ship breaking changes as `/api/v2` next to `/api/v1` |
| `js/api/` layer | All frontend server calls go through one layer, so pages can be rebuilt (even with a framework) without touching the backend |

Known limits are recorded in the [decision records](../decisions/README.md).
