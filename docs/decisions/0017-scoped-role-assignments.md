# 0017. Attach scope to each role assignment

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
When someone is given a role, the assignment also says *where* it applies: the whole company, one department, one team, or one employee. A person can hold different roles in different places, for example manager of one department and scheduler for a team elsewhere.

## Context
The proposal separates *what* a user may do (permissions, via roles) from *whom or what* it applies to (scope), and requires manager relationships to be stored explicitly rather than inferred from job titles.

## Decision
```
role_assignments(id, company_id, user_id, role_id,
                 scope_type  ENUM('company','department','team','employee'),
                 department_id NULL, team_id NULL, employee_id NULL)
CHECK: exactly the column matching scope_type is set; all three are NULL for 'company'
```
- All references are company-aware foreign keys ([0016](0016-tenant-isolation.md)).
- **Structure:** each team belongs to one department. Each employee belongs to **one department** and may be on **several teams** within the company.
- **Nesting:** a department scope covers the department's teams and all its members; a team scope covers the team's members; an employee scope covers that employee. Resolution is done in code, one level deep.
- **Self-service** actions (viewing one's own schedule, requesting time off) use separate `*_own` permissions and need no scope row.
- `authorize(user, permission, target)` passes when at least one of the user's role assignments grants the permission **and** its scope covers the target.

## Consequences
- Answers "can a user hold different roles in different departments?": yes.
- Modules register a *scope resolver* for their resources (see [0012](0012-extensibility-patterns.md)), which maps a shift, request, or task to the employee/team/department it belongs to.
- Deeper hierarchies (sub-departments) would need a new decision.

## Alternatives considered
- **Scope stored per user:** simpler, but cannot express different scopes for different roles.
- **A generic `scope_id` column:** fewer columns, but the database could not enforce the references.
