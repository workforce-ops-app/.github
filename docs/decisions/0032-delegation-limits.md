# 0032. Delegation limits: role editing, same-level grants, owner changes, and account changes

- **Status:** Accepted
- **Date:** 2026-09-30

## In short
Access is handed down from the owner, one layer at a time. Each person can pass on at most what they hold, and only to people below them. Giving someone a role at your own level needs approval from someone above you. A role can only be changed by someone who is above everyone holding it. Owners are added or removed only by owners, and with several owners, all the others must agree. Changing your own name or email also needs approval from above.

## Context
[0024](0024-authorization-model.md) stops anyone from granting a permission they do not hold, and requires a position above a person to act on them. Reviewing the threat model showed two gaps:
- Editing a role changes it for **everyone** who holds it. An administrator with `role.manage` could weaken or reshape the Administrator role held by a peer, without being above that peer.
- Anyone could give a person below them a role **equal** to their own, so the number of people at a level could grow without anyone above knowing.

The owner is the only person who holds every permission; everyone else holds a part of it, given from above.

## Decision
- **Editing roles:** creating a role, changing what it grants, renaming it, or archiving it is allowed only when **every current holder** of the role is below the editor in the reporting chain. The Owner may edit any role except Owner, which is locked. A new role has no holders yet, so creating one only needs `role.manage` (and still grants nothing the creator lacks).
- **Same-level grants need approval from above:** assigning a role whose permissions include **all** of the granter's own permissions for that scope creates an approval request. The assignment grants nothing until it is approved. Reviewers are found the same way as for requests in [0029](0029-request-approval-routing.md): the granter's direct managers who hold `role.assign`, then further up the chain, ending at the Owner. Grants strictly smaller than the granter's own take effect at once (with password re-entry where [0025](0025-sensitive-actions-and-security-settings.md) requires it).
- **Owners:** a company may have several owners, for true co-owners. Only owners add or remove owners, always with password re-entry.
  - One owner: acts alone.
  - Several owners: **adding** an owner needs every current owner to approve; **removing** one needs every owner **except the one being removed**, so no owner can block their own removal and no owner can remove another alone.
  - The last owner cannot be removed. Leaders who are not co-owners (for example a board of directors) get their own role below the owner, not the Owner role.
- **Changes to your own account:** anyone may ask to change their own display name (core) or email address (next tier). The change takes effect only when approved by the nearest person above them who holds `user.manage`, walking up the chain as for same-level grants and ending at the Owner.
  - An email change also needs the password re-entered when it is requested, is checked for uniqueness when requested and again when approved, and ends the person's other sessions when it takes effect.
  - Owners: with several owners, another owner approves. A sole owner's request goes to **platform staff** to verify; until platform staff screens exist, the platform operators decide with a command-line tool, recorded in the platform audit chain.
  - Administrators with `user.manage` who are above the person can still change the name or email directly.
- **Approval requests** use one shared record for role grants, owner changes, account changes, and time off (0029). A role grant, owner change, or account change nobody decides within **7 days** is **declined as not reviewed**: it counts as declined, and the audit log records that nobody reviewed it. The requester can send it again. Other kinds of request set their own deadline on their feature page, with the same outcome (a time-off request, for example, is declined as not reviewed if still undecided when its first day begins).
- **Tier:** core ([0023](0023-feature-tiers-and-audit-schedule.md)), except email changes, which are next tier (a confirmation link to the new address can be added once email delivery exists).

## Consequences
- New escalation rules AZ13 to AZ15 and their security tests (backend authorization page).
- Admins-over-admins set up their teams one approval at a time; the audit log shows who asked and who approved.
- Part of 0025's "second approvals" (for equal grants and owner changes) moves from stretch to core. Second approvals for removing an administrator and for bulk schedule changes stay in stretch.
- The shared approval record is built with authorization (Phase 2), before time off uses it. It must also record platform staff as approvers.
- A stolen session alone cannot change a person's sign-in email: it needs the password and approval from above.

## Alternatives considered
- **Only the Owner edits roles:** simplest and strict, but the Owner would do all role setup, even for large companies.
- **Only strictly smaller grants:** power always shrinks going down, but the Owner would have to personally create every administrator.
- **Truly unanimous owner removal (including the owner being removed):** nobody could be removed against their will, but a rogue owner could never be removed.
- **Keeping the gaps and relying on the audit log:** changes would be recorded, but only noticed after the damage.
