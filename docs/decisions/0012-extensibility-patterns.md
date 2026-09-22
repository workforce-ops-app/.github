# 0012. Extension points for features not yet planned

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
The shared parts of the application offer "plug-in points", so a feature nobody has planned yet can be added by writing new code rather than rewriting existing code.

## Context
The proposals describe the initial features, but the application should be able to grow (for example payroll or inventory) without destabilizing what already works or creating merge conflicts.

## Decision
| Extension point | How a new feature uses it |
|---|---|
| **Module discovery** | Adding `app/modules/<feature>/router.py` registers its endpoints |
| **Permission registry** | The module's `permissions.py` declares its permissions |
| **Scope resolvers** | The module registers how to find which company, department, team, or employee a resource belongs to, so `authorize(user, permission, target)` works without changes to `authz/` |
| **Internal events** | Modules publish events (for example `time_off.approved`); notifications, audit, and detection subscribe instead of being called directly |
| **Module settings** | Company-configurable policies are declared per module with types and defaults and stored in one generic table |
| **API versioning** | All endpoints live under `/api/v1`; breaking changes ship as `/api/v2` alongside |
| **Permission-driven navigation** | The frontend menu is generated from the pages a user may access |
| **`js/api/` layer** | Frontend pages never call `fetch` directly |

## Consequences
- The shared layers take slightly more design up front.
- **Known limit, background jobs:** jobs run inside the API process, which is correct for a single server. If the API ever runs on several servers, jobs will need a database lock or a separate worker process.
- **Known limit, frontend:** see [0005](0005-frontend-multi-page-vanilla-js.md).
- Sessions are stored in the database, so running several API servers is otherwise possible.

## Alternatives considered
- **Adding extension points when first needed:** cheaper now, but retrofitting them touches every existing module.
