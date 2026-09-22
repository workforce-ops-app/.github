# 0018. Per-company audit chains sealed with HMAC-SHA256

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Every security-relevant action is written to an audit log that cannot be quietly edited. Each entry is linked to the previous one and signed with a secret key kept outside the database, so any change, deletion, or insertion breaks the chain and is detected.

## Context
"Maintain trustworthy audit records" is a goal of the security proposal. A plain hash chain detects accidental changes, but anyone with database write access could rewrite the rows and recompute every hash.

## Decision
- **One chain per company**, plus one **platform chain** for actions by platform personnel.
- **Entry fields:** sequence number, company, actor (user or `system`), action, target type and ID, timestamp (UTC), details (JSON), previous signature, signature.
- **Signature:** `HMAC-SHA256(key, canonical_json(fields) + previous_signature)`. Canonical JSON uses sorted keys and fixed formatting so the same entry always produces the same bytes. The key comes from the environment or a secret store, never the database, and has an ID so it can be rotated (old entries keep the ID of the key that signed them).
- **Ordering:** a per-chain head row (`audit_chain_heads`) is locked (`SELECT … FOR UPDATE`) while an entry is appended, so sequence numbers never collide or skip.
- **Verification:** a nightly job re-verifies every chain and records the result as an audit event; owners can run it on demand; the latest head signature is also written to the application log, outside the database.
- **Database permissions:** the application's database user has only `INSERT` and `SELECT` on audit tables (plus `UPDATE` on the chain head row). Migrations use a separate database user.
- Automatic actions (expirations, auto-forwarding) are logged with actor `system`.

## Consequences
- The signing key is a critical secret: losing it means old entries can no longer be verified, and leaking it weakens the protection back to a plain hash chain.
- Appends to one company's chain are serialized; different companies do not block each other.
- The design and its limits are good material for the security write-up.

## Alternatives considered
- **A single global chain:** simpler, but every write in every company contends for one lock, and one company's history cannot be verified on its own.
- **Plain SHA-256 chain:** detects tampering only by someone who cannot also recompute the chain.
- **An external append-only store:** strongest, but adds infrastructure the project does not have yet.
