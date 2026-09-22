# 0001. Record decisions as numbered files

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Important decisions are written down as short numbered documents so the reasoning survives after the conversation that produced it is forgotten.

## Context
The project combines a web application with a security study, and many choices (branching, CI, architecture) affect both. Reviewers, future contributors, and the project write-up all need to know *why* things are the way they are.

## Decision
Each decision gets its own file in `.github/docs/decisions/`, numbered in order, using the template in `docs/templates/decision.md`. Records are never deleted; a changed decision gets a new record that supersedes the old one.

## Consequences
- One file per decision means documentation PRs rarely conflict.
- A PR that makes a notable decision adds its record in the same change.

## Alternatives considered
- **A single design document:** it grows long, conflicts often, and loses the history of why things changed.
- **Wiki pages:** not reviewed through pull requests and not versioned with the code.
