# Design review 3: Authorization

**In short:** every action is a named permission. Roles bundle permissions, and each role has a rank. A person can only manage roles at or below their own rank, never their own. Every check asks two things: does the person's role allow this, and does their scope cover this record? Risky actions need extra steps, such as re-entering the password, a waiting period, or a second approval.

| # | Question | Answer | Status |
|---|---|---|---|
| 3.1 | How are permissions named? | `resource.action`, lowercase, with an `_own` suffix for acting on your own records. | answered |
| 3.2 | Which roles does a new company start with, and are they editable? | Owner, Administrator, Manager, Employee, with ranks; Owner locked, the rest editable; companies may add roles. | answered |
| 3.3 | Can administrators manage other administrators? | **Yes**, as happens in real organizations, but never themselves and never above their own rank. | answered |
| 3.4 | How is privilege escalation prevented? | Rank rules plus escalation rules (below). | answered |
| 3.5 | How does the permission check work? | `authorize(user, permission, target)`, deny by default, with scope resolvers and a scope filter for lists. | answered |
| 3.6 | Which actions are sensitive, and what do they require? | See the table below; waiting period **48 hours**, bulk threshold **10+ shifts**. | answered |
| 3.7 | Can companies change security settings? | **Yes, but only stricter** than the platform's defaults (table below). | answered |
| 3.8 | Is platform support access in the first build? | **No**: stretch. | answered |

## Permissions (core)

Later features add their own, declared in their module.

| Area | Permissions |
|---|---|
| Schedules | `schedule.view_own`, `schedule.view`, `schedule.edit` |
| Time off | `time_off.request`, `time_off.cancel_own`, `time_off.view`, `time_off.review` |
| People and structure | `user.view`, `user.manage`, `org.manage` |
| Roles | `role.view`, `role.manage` (define roles), `role.assign` (give roles to people) |
| Company | `settings.manage`, `audit.view`, `audit.verify` |
| Owner-only | `company.transfer_ownership` |

Next-tier features add, among others: `task.view_own`, `task.complete`, `task.note`, `task.manage`, `task.assign`, `task.verify`, `announcement.view`, `announcement.create`, `announcement.manage`, and coverage permissions.

## Starting roles and ranks

| Role | Rank | Gets | Editable |
|---|---|---|---|
| Owner | 100 | everything | **no**; a company always has at least one owner |
| Administrator | 80 | everything except owner-only permissions | yes |
| Manager | 50 | view, edit, and review schedules, time off, and people within their scope | yes |
| Employee | 10 | own schedule and the department's schedule; request and cancel own time off | yes |

Custom roles get a rank **at or below** the rank of the person creating them.

## Rank and escalation rules

- A person can give, change, or remove roles **at or below their own highest rank**, never above.
- Nobody can change **their own** role assignments.
- Nobody can grant a permission **they don't hold themselves**, whether by editing a role or assigning one.
- The **last owner** can't be removed or demoted; owner changes happen only through ownership transfer.
- Every role, permission, and assignment change is written to the audit log.

| Person | Can manage |
|---|---|
| Owner | Administrators, Managers, Employees (owners via ownership transfer only) |
| Administrator | other Administrators (not themselves), Managers, Employees |
| Manager | Employees in their scope, only if granted `role.assign` |

## How a check works

- One function: `authorize(user, permission, target)`. **Deny by default.**
- Allowed only if one of the user's role assignments grants the permission **and** its scope covers the target:
  - company scope covers everything in the company;
  - department scope covers that department;
  - team scope covers that team's members;
  - employee scope covers that one person.
- `_own` permissions pass only when the target belongs to the user.
- Each feature registers a **resolver** that says which employee, team, and department a record belongs to, so new features work without changing the check.
- **Lists** use a companion **scope filter** that turns the user's scopes into a database condition, so a list can never include a row the user may not see.

## Sensitive actions

| Action | Core | Next |
|---|---|---|
| Transfer ownership | re-enter password | **48-hour** waiting period (can be cancelled); all owners and admins notified |
| Remove an administrator, or change admin-level permissions | re-enter password | second approval by another owner or admin; affected person notified |
| Change which permissions a role grants | re-enter password | owners notified |
| Large schedule change (**10+ shifts** at once) | confirmation showing the count | second approval above a company-set limit |
| Change security settings | re-enter password | owners notified |
| Enable support access (stretch) | | re-enter password; time-limited; admins notified |

## Company security settings: "stricter only"

Each setting has a platform default and a platform limit. Owners can only move a setting in the stricter direction; each change requires re-entering the password and notifies all owners.

| Setting | Platform default | Companies may set |
|---|---|---|
| Idle sign-out | per the [session decision](04-api-and-authentication.md#sessions) | shorter, not below 5 min |
| Maximum session | per the session decision | shorter, not below 1 h |
| Failed attempts before lock | 5 | fewer, not below 3 |
| Lock duration | 15 min → 30 min → 1 h | longer first steps, never over the 1 h maximum |
| Minimum password length | 15 | longer, up to 64 |
| Setup/reset link validity | 48 h | shorter, not below 1 h |
| Ownership transfer wait | 48 h | longer, up to 7 days |
| Second approval for bulk schedule changes | 10+ shifts | a lower number, not below 2 |
| Actions requiring password re-entry | platform list | add actions, never remove |

Recorded as decisions [0024](../../decisions/0024-authorization-model.md) and [0025](../../decisions/0025-sensitive-actions-and-security-settings.md).
