# Design review 5: Backup and recovery

**In short:** if someone inside or outside the company tries to destroy data, we want to lose at most 5 minutes of it and be running again within 4 hours. This works through three layers: stopping the damage where possible, keeping encrypted backups somewhere an attacker can't reach, and practising restores so we know they work.

| # | Question | Answer | Status |
|---|---|---|---|
| 5.1 | How do we limit damage in the first place? | The application's database login can't delete or alter tables; bulk destructive actions use sensitive-action safeguards; unusual mass changes alert administrators. | answered |
| 5.2 | How are backups taken and kept? | Nightly full backup plus the database change log copied off the server **every 5 minutes or streamed**; encrypted; write-once off-server storage; separate credentials; daily copies kept 30 days, weekly copies 3 months. | answered |
| 5.3 | Recovery targets? | Lose at most **5 minutes** of data (RPO); be running again within **4 hours** (RTO). Faster is welcome. | answered |
| 5.4 | How do we prove restores work? | A written restore procedure practised **monthly**, timed, with audit-chain verification after every restore; a timed "attacker destroyed the database" drill for the report and a demo. | answered |
| 5.5 | What about the code and GitHub data? | A periodic mirror of all three repositories **plus an export of issues, PRs, reviews, and the board** using the GitHub CLI. | answered |
| 5.6 | Where are the mirrors and exports stored? | Both teammates' machines, or a separate dedicated server or computer for extra redundancy. | **for Corbin to decide** |
| 5.7 | When is this built? | **Next** tier (may start early). Design, database permissions, scripts, and local drills with Docker can happen any time; the automatic schedule, off-server storage, and write-once protection wait until hosting is chosen. The repository mirror and export don't depend on hosting. | answered |

## Why the 4-hour target

The restore itself takes minutes for a database this size. The limiting factor is a person noticing and getting to a computer: a two-person student team cannot promise a faster response at any hour. Every drill records the actual time, so the report can state "target 4 hours, achieved *X* minutes".

## Threats covered

| Threat | Protection |
|---|---|
| Malicious or compromised user mass-cancelling or deactivating records | no deletions in the app ([0020](../../decisions/0020-status-over-deletion.md)), sensitive-action safeguards, mass-change alerts, point-in-time restore |
| Attacker with the application's database password | cannot drop or alter tables; audit log is append-only and signed ([0018](../../decisions/0018-audit-log-chains.md)) |
| Attacker in control of the server | backups are off-server, encrypted, write-once, with separate credentials |
| Database quietly rolled back to an older state | audit-chain heads are also recorded outside the database |
| Accidental or malicious repository deletion | repository mirror plus issue and PR export outside GitHub |
| Leaked secrets | rotation runbook for database passwords and the audit signing key |

## Resulting documents (after approval)

- Backup and restore runbooks in the backend's `docs/operations/`, from the runbook template
- A secret-rotation runbook
- A mirror and export script

Recorded as decision [0028](../../decisions/0028-backup-and-recovery.md).
