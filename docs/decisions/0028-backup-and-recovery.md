# 0028. Backup and recovery

- **Status:** Accepted (mirror storage location pending)
- **Date:** 2026-09-23

## In short
Backups are encrypted, kept off the server where an attacker can't delete them, and can restore the database to any minute. The goals are to lose at most 5 minutes of data and be running again within 4 hours. Restores are practised and timed, not just assumed to work.

## Context
"Maintain service availability and recoverability" is a security proposal goal, and both internal and external attackers may try to destroy data. Decisions 0018 and 0020 prevent quiet tampering and deletion through the application, but do not recover data.

## Decision
- **Damage limits:** the application's database user has no DROP, TRUNCATE, or ALTER; bulk destructive actions use sensitive-action safeguards ([0025](0025-sensitive-actions-and-security-settings.md)); mass-change alerts.
- **Backups:** nightly full backup plus binlog shipped off-server every 5 minutes or streamed; encrypted; write-once storage with separate credentials; retention 30 days daily, 3 months weekly.
- **Targets:** RPO 5 minutes; RTO 4 hours (measured in every drill).
- **Verification:** monthly timed restore drill; audit chains verified after every restore.
- **Repositories:** periodic mirror plus export of issues, PRs, reviews, and the board. **Storage location pending** (teammates' machines or a dedicated machine).
- **Timing:** next tier; hosting-dependent parts wait for a hosting decision.

Background: the team's [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17).

## Consequences
- Drill results feed the report's evaluation and give a strong demo.
- The RTO is a human-availability commitment as much as a technical one.

## Alternatives considered
- **Nightly backups only:** up to 24 hours of data lost.
- **Backups on the same server:** an attacker who controls the server deletes them too.
- **A 2-hour RTO:** technically possible, but not a promise two students can keep at any hour.
