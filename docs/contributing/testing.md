# Testing

**In short:** every change comes with tests that check what the code must do and what it must never do. A test is only as good as its assertions: running code proves nothing, checking the result does. Coverage shows how much of the code the tests ran, and therefore what has not been checked at all; it is not a measure of security. Security confidence comes from tests written the way an attacker would try things, together with static analysis, dependency audits, review, and active testing.

## Kinds of tests

| Kind | Checks | Backend | Frontend |
|---|---|---|---|
| **Unit** | one piece of code on its own, fast | `tests/unit/` (pytest) | `tests/unit/` (Vitest) |
| **Security** | what an attacker would try: other companies' data, raising your own access, injection, leaks | `tests/security/` (from Phase 2) | header and Content Security Policy checks |
| **Integration** | the parts working together: the API with MySQL, the pages through nginx | `tests/integration/` | Playwright |

All of them run in CI on every pull request ([CI](ci.md)), and locally with `python ../.github/scripts/ci_runner.py`.

## What makes a test worth having

- **It asserts the outcome, not just that the code ran.** This test runs every line of the error handler and proves nothing:
  ```python
  def test_crash(client):
      client.get("/api/test/crash")  # no assertions: passes even if the response leaks a password
  ```
  This one proves what matters:
  ```python
  response = client.get("/api/test/crash")
  assert response.status_code == 500
  assert secret not in response.text  # the real error never reaches the browser
  assert "Traceback" not in response.text
  ```
- **It checks what must not happen, not only what should.** For every rule, ask what an attacker would try, and test that it fails: another company's ID answers 404, a peer cannot change your roles, submitted text is never echoed back.
- **It names the threat it covers.** Security tests refer to the threat model's IDs (for example `I4`, `T5`, `E3`) or the rule IDs on the design pages (`AZ1`, `AU3`), so the [threat model](https://github.com/workforce-ops-app/workforce-ops-backend/blob/main/docs/security/threat-model.md) and the tests can be checked against each other.
- **It does not depend on the machine.** Settings, the current folder, and outside services are replaced for the test (pytest's `monkeypatch` and `tmp_path`), so a developer's own `.env` cannot change the result.

## Coverage: a map, not a score

The backend measures **line and branch coverage**: which lines of `app/` the tests ran, and whether both sides of every `if` ran. The CI report shows it in the unit-test row (for example `16 passed · coverage 100%`), and locally:

```
python -m pytest --cov --cov-report=term    # missing line numbers listed per file
```

How to read it:
- **Uncovered code is unchecked by tests.** Each missing line is either a behavior worth a test or code that may not be needed. Start reviews there.
- **Covered code is not proven correct.** A line counts as covered as soon as any test runs it, with or without assertions (see above).
- **No minimum is enforced yet.** Security-relevant code (sign-in, permissions, company separation, the audit log, error handling) should be fully covered by tests that assert the attacker's view. A threshold may be added once there is more code.

The frontend turns coverage on with its first unit tests.

## How the project looks for vulnerabilities

Testing is one layer. Each layer finds things the others miss:

| Layer | Finds | Where |
|---|---|---|
| **Abuse-case tests** | what an attacker could do, checked on every change | `tests/security/`, named after threat IDs |
| **Coverage** | code no test has touched yet | the CI report and `--cov-report=term` |
| **Static analysis** | dangerous patterns without running the code (SQL built from strings, `innerHTML` with data, hardcoded secrets) | ruff's security rules, ESLint's `no-unsanitized`, CodeQL |
| **Dependency audit** | known vulnerabilities in libraries | pip-audit and npm audit in CI; Dependabot |
| **Review** | logic flaws tools cannot see, such as a check in the wrong place | every pull request ([workflow](workflow.md)) |
| **Active testing** | what an attacker can do against the running application | the audits with OWASP ZAP, sqlmap, and Burp Suite ([decision 0030](../decisions/0030-security-study-method.md)) |

Findings from any layer follow the security policy: fixed first, then a regression test, then an entry in the findings log.
