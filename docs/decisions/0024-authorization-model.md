# 0024. Authorization model: permissions, reporting lines, and escalation rules

- **Status:** Accepted
- **Date:** 2026-09-23 (revised 2026-09-28 at sign-off)

## In short
Every action is a named permission, and roles bundle permissions. Reporting lines record who reports to whom: being above someone in that chain decides whose roles, requests, and account you may act on, and your permissions decide what you may do. Every check is deny-by-default, and nobody can change their own access.

## Context
The proposal requires role-based access with scopes ([0017](0017-scoped-role-assignments.md)) and protection against privilege escalation, one of the security proposal's goals. In review, the team rejected letting administrators manage other administrators just because they share a role, but wanted an organization to be able to put one administrator (or manager) over others, set up from above. Real workplaces also have people who report to several managers.

## Decision
- **Permission names:** `resource.action`, lowercase, with a `_self` suffix for self-service (`schedule.view_self`, `time_off.cancel_self`). Each module declares its own.
- **Starting roles:** Owner (locked; a company always has at least one), Administrator, Manager, Employee. All but Owner are editable, and companies may add roles.
- **Reporting lines:** a `reporting_lines` table records that one person reports to another. A person can report to several managers, and a manager can have many reports. Authority passes down the **whole chain**: if C reports to B and B reports to A, A is above C. The Owner counts as above everyone.
- **The chain decides who, permissions decide what.** Being above someone grants nothing by itself. Acting on a person needs both a position above them in the chain and the matching permission:
  - changing their role assignments (`role.assign`);
  - reviewing their requests (see [0029](0029-request-approval-routing.md));
  - account actions such as setup and reset links, deactivation, and signing them out (`user.manage`).
- **Changing reporting lines:** you must be above **both** people and hold `reporting_line.manage`. It is a sensitive action (password re-entry, [0025](0025-sensitive-actions-and-security-settings.md)) and is audited.
- **Escalation rules:**
  - nobody changes their own role assignments or reporting lines;
  - nobody grants a permission they don't hold, whether by editing a role or assigning one;
  - reporting lines can't form a loop (A above B above A), and nobody reports to themselves;
  - the last owner can't be removed or demoted, and owner changes happen only through ownership transfer;
  - every role, permission, assignment, and reporting line change is written to the audit log.
- **Check:** `authorize(user, permission, target)`, deny by default. For records (shifts, tasks, announcements), it passes when an assignment grants the permission and its scope covers the target. For actions on a person, the user must also be above that person in the chain. `_self` permissions pass only for the user's own records. Modules register resolvers, and lists use a scope filter that becomes a database condition.
- **Data:** a `reporting_lines` table (manager, employee, end date); roles have no rank.
- **Delegation limits** (who may edit a role, approval for same-level grants, and owner changes) are in [0032](0032-delegation-limits.md).

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Escalation rules become concrete security tests, for example "an administrator cannot reset another administrator's password without being above them", "nobody can add a reporting line that puts themselves above a peer", and "a loop in reporting lines is rejected".
- Checks on people walk the chain with a recursive query, written with SQLAlchemy ([0022](0022-sqlalchemy-and-alembic.md)).
- Companies must keep reporting lines up to date; a person with no line above them can only be managed by the Owner.

## Alternatives considered
- **Ranked roles, "at or below your rank":** any administrator could manage every other administrator, which the team rejected.
- **Ranked roles, "strictly below", with extra tiers such as Lead Administrator:** works, but a rank describes a job level rather than who actually manages whom, and changing one role's rank affects everyone holding it.
- **Nested teams:** mixes the org chart with authority, and would put recursive checks into every scope check and list.
- **A single "reports to" column on users:** allows only one manager per person.
