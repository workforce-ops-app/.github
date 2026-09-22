# Decision records

**In short:** a short record of each significant decision: what we chose, why, and what we gave up. When someone asks "why is it done this way?", the answer should be here.

New records start from [`../templates/decision.md`](../templates/decision.md) and take the next number. Records are never deleted; a decision that changes gets a new record, and the old one is marked *Superseded by NNNN*.

| # | Decision | Status |
|---|---|---|
| [0001](0001-record-decisions.md) | Record decisions as numbered files | Accepted |
| [0002](0002-repository-layout.md) | Separate backend and frontend repositories plus a shared `.github` repository | Accepted |
| [0003](0003-same-origin-deployment.md) | Serve frontend and API from one origin behind a reverse proxy | Accepted |
| [0004](0004-backend-feature-modules.md) | Organize the backend by feature module | Accepted |
| [0005](0005-frontend-multi-page-vanilla-js.md) | Multi-page frontend with plain ES modules and no build step | Accepted |
| [0006](0006-branching-and-promotion.md) | `main` → `production` with squash merges into `main` | Accepted |
| [0007](0007-review-integration-branch.md) | Automatically rebuilt `review/integration` branch | Accepted |
| [0008](0008-ci-pipeline-and-report.md) | Shared CI pipeline with a single PR report comment | Accepted |
| [0009](0009-ci-bypass-policy.md) | Bypasses allowed but discouraged, justified, and followed up | Accepted |
| [0010](0010-runtime-versions.md) | Python 3.13, MySQL 8.4 LTS, Node.js 22 LTS | Accepted |
| [0011](0011-dependency-updates-and-pinning.md) | Dependabot updates and SHA-pinned actions | Accepted |
| [0012](0012-extensibility-patterns.md) | Extension points for features not yet planned | Accepted |
| [0013](0013-documentation-structure.md) | Four documentation categories, docs in the same PR | Accepted |
| [0014](0014-markdown-issue-templates.md) | Markdown issue templates instead of issue forms | Accepted |
| [0015](0015-public-repositories.md) | Public repositories with private vulnerability reporting | Accepted |
| [0016](0016-tenant-isolation.md) | Keep companies separate in one shared database | Accepted |
| [0017](0017-scoped-role-assignments.md) | Attach scope to each role assignment | Accepted |
| [0018](0018-audit-log-chains.md) | Per-company audit chains sealed with HMAC-SHA256 | Accepted |
| [0019](0019-uuidv7-ids.md) | UUIDv7 primary keys | Accepted |
| [0020](0020-status-over-deletion.md) | Change status instead of deleting records | Accepted |
| [0021](0021-time-handling.md) | Store moments in UTC, schedule in the workplace's time zone | Accepted |
| [0022](0022-sqlalchemy-and-alembic.md) | SQLAlchemy 2.0 and Alembic for database access | Accepted |
