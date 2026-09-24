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
| [0023](0023-feature-tiers-and-audit-schedule.md) | Feature tiers and security audit schedule | Accepted |
| [0024](0024-authorization-model.md) | Authorization model: permissions, ranked roles, and escalation rules | Accepted |
| [0025](0025-sensitive-actions-and-security-settings.md) | Safeguards for sensitive actions and "stricter only" company security settings | Accepted |
| [0026](0026-api-conventions.md) | API conventions | Accepted (`/api/v1` tentative) |
| [0027](0027-authentication-and-sessions.md) | Authentication, sessions, and onboarding | Accepted (session timeouts pending) |
| [0028](0028-backup-and-recovery.md) | Backup and recovery | Accepted (mirror location pending) |
| [0029](0029-request-approval-routing.md) | Request approval routing | Accepted (denial rule pending) |
| [0030](0030-security-study-method.md) | Security study method | Accepted |
| [0031](0031-demo-environment-and-data.md) | Demo environment, demo data, and logging | Accepted (phone connection pending) |
