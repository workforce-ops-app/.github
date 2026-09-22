# 0010. Python 3.13, MySQL 8.4 LTS, Node.js 22 LTS

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
The project uses current, long-supported versions of its main tools, and only moves to newer ones on purpose.

## Context
The team needs stable versions that will be supported for the life of the project, and the same versions locally and in CI.

## Decision
| Component | Version | Role |
|---|---|---|
| Python | 3.13 | backend, CI scripts, git hooks |
| MySQL | 8.4 LTS | database |
| Node.js | 22 LTS | frontend development tooling only |

CI installs these exact major/minor versions. Dependabot is configured not to move Python or MySQL past them, and applies patch releases only.

## Consequences
- Upgrading one of these needs a new decision record and one PR that updates Docker images, CI, `dependabot.yml`, and the local setup guide together.

## Alternatives considered
- **Always latest:** more frequent breakage for no feature the project needs.
