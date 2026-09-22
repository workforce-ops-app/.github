---
name: Security finding
about: Record a security audit result that is fixed or not exploitable. Unfixed, exploitable findings go in a private advisory.
title: "security(<area>): <short summary>"
labels: ["type:security", "security-finding"]
---

<!--
These repositories are public. If this finding is exploitable and not yet fixed,
do NOT file it here. Open a private security advisory instead (see SECURITY.md)
and file this issue once the fix has merged.
-->

## Summary
<!-- Plain language: what the weakness was and what it could have allowed. -->

## Why it matters
<!-- Plain language: who or what data would have been at risk. -->

---
## Details

### Finding
- **Component:** <!-- module, endpoint, page -->
- **Category:** <!-- e.g. broken access control, injection, XSS, CSRF, auth/session, logging, misconfiguration -->
- **Severity:** <!-- low / medium / high / critical, with one line of reasoning -->
- **Threat source:** <!-- external attacker / malicious or compromised employee / platform -->
- **Found during:** <!-- backend audit / frontend audit / internal-user audit / external-user audit / CI / other -->

### How it was found
<!-- Tool, test, or manual review. -->

### Reproduction
<!-- Steps or request. Redact anything that would still work against a live system. -->

### Remediation
<!-- What fixed it and which PR. Add a regression test in tests/security where possible. -->

### Related
<!-- Advisory ID, PRs, other findings. -->
