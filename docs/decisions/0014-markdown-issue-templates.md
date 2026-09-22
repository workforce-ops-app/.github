# 0014. Markdown issue templates instead of issue forms

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Issue templates are plain Markdown files, so an issue looks the same whether it was written on the website or from the command line, and matches the pull request structure.

## Context
GitHub offers issue *forms* (YAML) with required fields, and Markdown templates. Forms render every field as a `###` heading and cannot express the "plain language first, then *Details*" layout used by pull requests. Forms are also not used when issues are created from the GitHub CLI or the API.

## Decision
Use Markdown templates in `.github/ISSUE_TEMPLATE/` with `## Summary`, `## Why it matters`, a divider, and `## Details` subsections, the same shape as the PR template. Blank issues are disabled.

## Consequences
- The structure is identical everywhere issues are created.
- Required fields are not enforced for issues; reviewers and the templates' guidance comments carry that. PR structure *is* enforced by `pr-policy`.

## Alternatives considered
- **Issue forms:** enforce required fields, but give inconsistent output and do not apply to CLI-created issues.
