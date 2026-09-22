<!--
Title: <type>(<area>): <summary>   e.g. feat(time-off): add request submission endpoint
Types: feat, fix, security, refactor, test, docs, chore
The three top-level sections below are checked by CI and must be filled in.
-->

## Summary
<!-- Plain language: what this PR does and why. -->

## What changed
<!-- Plain-language bullets a non-developer could follow. -->
-

---
## Details

### Technical changes
<!-- Modules, files, design choices a reviewer should know about. -->

### Database / migrations
<!-- "None", or the migration name and what it changes. One migration per PR. -->
None

### API contract changes
<!-- "None", or endpoints added/changed and the frontend impact. -->
None

### Security checklist
- [ ] Every new or changed endpoint calls `authorize()` with a permission and scope
- [ ] Queries are tenant-scoped (company) and parameterized
- [ ] User content is rendered safely (no `innerHTML` with data)
- [ ] Sensitive actions write to the audit log
- [ ] Tests added, including a cross-tenant or privilege-escalation case where relevant
<!-- Tick what applies; strike through (~~text~~) anything that does not apply to this PR. -->

### Documentation
- [ ] Project Architecture
- [ ] Contributor Documentation
- [ ] User Documentation
- [ ] Project Features
- [ ] Not needed (add the `docs:not-needed` label)

### How to test
<!-- Steps a reviewer can follow. -->
1.

### Merge notes
<!-- Depends on other PRs? Conflict risk? Must merge before/after something? "None" is fine. -->
None

### Bypass justification
<!-- Only if a bypass:<check> label is applied: which check, why, and the teammate's agreement. Otherwise leave "None". -->
None

### Related issues
<!-- Closes #N or Refs #N (other repo: Refs workforce-ops-app/<repo>#N) -->
Closes #
