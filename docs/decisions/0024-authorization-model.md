# 0024. Authorization model: permissions, ranked roles, and escalation rules

- **Status:** Accepted
- **Date:** 2026-09-23

## In short
Every action is a named permission, roles bundle permissions and carry a rank, and people can only manage roles at or below their own rank. Every check is deny-by-default and needs both the permission and a scope that covers the record.

## Context
The proposal requires role-based access with scopes ([0017](0017-scoped-role-assignments.md)), administrators managing administrators as in real organizations, and protection against privilege escalation, one of the security proposal's goals.

## Decision
- **Permission names:** `resource.action`, lowercase, `_own` suffix for self-service. Each module declares its own.
- **Starting roles:** Owner (rank 100, locked), Administrator (80), Manager (50), Employee (10). All but Owner are editable, and companies may add roles ranked at or below their creator.
- **Rank rule:** manage roles at or below your highest rank; administrators may manage other administrators.
- **Escalation rules:** nobody changes their own assignments; nobody grants a permission they don't hold; the last owner can't be removed or demoted; owner changes only through ownership transfer; every change is audited.
- **Check:** `authorize(user, permission, target)`, deny by default; passes when an assignment grants the permission and its scope covers the target; `_own` only for the user's own records; modules register resolvers; lists use a scope filter that becomes a database condition.
- **Data:** `roles` gains a `rank` column.

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Escalation rules become concrete security tests (e.g. "an administrator cannot add a permission they lack to a role").
- Custom roles need a rank chosen at creation.

## Alternatives considered
- **Strictly lower rank only:** safer, but administrators could not manage each other, which is unrealistic.
- **Flat roles without ranks:** cannot express "can't manage someone above you".
