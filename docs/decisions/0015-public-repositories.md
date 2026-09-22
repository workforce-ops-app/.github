# 0015. Public repositories with private vulnerability reporting

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
All repositories are public for now, with no license. Anyone can read the code, but security problems are reported and fixed privately before they are made public.

## Context
Public repositories get organization rulesets, CodeQL code scanning, secret scanning with push protection, and shared `.github` defaults on GitHub's free plan. The project is also a security showcase, which makes public code a feature, as long as unfixed vulnerabilities are not published.

## Decision
- All three repositories are public. No license for now, so default copyright applies: the code can be read but not reused.
- Private vulnerability reporting is enabled; exploitable, unfixed findings are handled in private security advisories (see `SECURITY.md`).
- Secret scanning with push protection and CodeQL default setup are enabled; gitleaks also runs in CI and pre-commit.
- `.env` files are never committed; `.env.example` documents the variables.

## Consequences
- Every commit, issue, and PR is public; nothing sensitive may appear in them.
- Security-finding issues are filed only after the fix merges.

## Alternatives considered
- **Private repositories:** rulesets and some security features would need a paid plan (GitHub Team or an education upgrade).
