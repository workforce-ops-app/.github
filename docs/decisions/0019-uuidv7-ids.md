# 0019. UUIDv7 primary keys

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Every record gets a long random-looking ID that also encodes when it was created. IDs cannot be guessed from one another, and new rows are still stored efficiently.

## Context
Sequential IDs (1, 2, 3…) in URLs let anyone guess other records' IDs and estimate how much data exists. Fully random IDs (UUIDv4) avoid that but make MySQL inserts slow, because new rows land all over the index.

## Decision
- Primary keys are **UUIDv7**, stored as `BINARY(16)` and exposed in the API as standard hyphenated UUID strings.
- UUIDv7 starts with a millisecond timestamp followed by random bits, so rows are inserted roughly in order.
- IDs are generated in the application with a small, maintained library (Python 3.13 has no built-in UUIDv7).
- Unguessable IDs are an extra layer only; every access is still authorized ([0016](0016-tenant-isolation.md), [0017](0017-scoped-role-assignments.md)).

## Consequences
- One ID per record, used everywhere.
- Raw database queries show binary IDs; `BIN_TO_UUID()` / `UUID_TO_BIN()` or small helpers make them readable.
- An ID reveals roughly when the record was created. That is acceptable for this application.

## Alternatives considered
- **Auto-increment integers:** simplest, but guessable and they reveal volumes.
- **Integer keys plus a separate public UUID:** hides internal IDs but means two IDs per record.
- **UUIDv4:** unguessable, but poor insert performance in InnoDB.
