import unittest
from pathlib import Path

import pr_policy

GOOD_BODY = """## Summary
Adds time-off requests.

## What changed
- Employees can request days off.

---
## Details
### Technical changes
New module.

### Bypass justification
None

Closes #14
"""


def make_pr(**overrides):
    pr = {
        "title": "feat(time-off): add request submission",
        "body": GOOD_BODY,
        "head": {"ref": "feat/14-time-off-requests"},
        "base": {"ref": "main"},
        "user": {"login": "someone"},
        "labels": [],
    }
    pr.update(overrides)
    return pr


def commit(message, sha="abcdef1234"):
    return {"sha": sha, "commit": {"message": message}}


class PolicyTests(unittest.TestCase):
    def test_good_pr_passes(self):
        commits = [commit("feat(time-off): add model")]
        result = pr_policy.evaluate(make_pr(), commits, ["docs/features/time-off.md"])
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.warnings, [])

    def test_review_branch_rejected(self):
        result = pr_policy.evaluate(make_pr(head={"ref": "review/integration"}), [], [])
        self.assertFalse(result.ok)

    def test_production_only_from_main(self):
        result = pr_policy.evaluate(make_pr(base={"ref": "production"}), [], [])
        self.assertFalse(result.ok)

    def test_promotion_allowed(self):
        pr = make_pr(
            title="chore(release): promote main to production",
            head={"ref": "main"},
            base={"ref": "production"},
            body="## Summary\nShips #14 and #15.",
        )
        self.assertTrue(pr_policy.evaluate(pr, [], ["app/x.py"]).ok)

    def test_missing_sections(self):
        result = pr_policy.evaluate(make_pr(body="just a description"), [], [])
        self.assertEqual(len([e for e in result.errors if "section" in e]), 3)

    def test_template_comments_do_not_count_as_content(self):
        body = GOOD_BODY.replace("Adds time-off requests.", "<!-- plain language -->")
        self.assertFalse(pr_policy.evaluate(make_pr(body=body), [], []).ok)

    def test_unfilled_template_fails(self):
        template = Path(__file__).resolve().parent.parent / ".github" / "PULL_REQUEST_TEMPLATE.md"
        body = template.read_text(encoding="utf-8")
        errors = pr_policy.evaluate(make_pr(body=body), [], []).errors
        self.assertTrue(any("Summary" in e for e in errors))
        self.assertTrue(any("What changed" in e for e in errors))

    def test_bypass_needs_justification(self):
        pr = make_pr(labels=[{"name": "bypass:typecheck"}])
        self.assertFalse(pr_policy.evaluate(pr, [], []).ok)
        pr["body"] = GOOD_BODY.replace(
            "### Bypass justification\nNone", "### Bypass justification\nmypy bug #9"
        )
        self.assertTrue(pr_policy.evaluate(pr, [], ["docs/a.md"]).ok)

    def test_coauthor_commit_rejected(self):
        commits = [commit("feat(x): y\n\nCo-authored-by: A <a@example.com>")]
        self.assertFalse(pr_policy.evaluate(make_pr(), commits, []).ok)

    def test_warnings(self):
        body = GOOD_BODY.replace("Closes #14", "")
        result = pr_policy.evaluate(make_pr(body=body, head={"ref": "feat/no-issue"}), [], ["app/main.py"])
        self.assertTrue(result.ok)
        self.assertEqual(len(result.warnings), 3)  # branch without issue, no linked issue, docs

    def test_docs_not_needed_label(self):
        pr = make_pr(labels=[{"name": "docs:not-needed"}])
        self.assertEqual(pr_policy.evaluate(pr, [], ["app/main.py"]).warnings, [])

    def test_dependabot_relaxed(self):
        pr = make_pr(
            title="chore(deps): bump ruff from 0.16.7 to 0.16.8",
            head={"ref": "dependabot/pip/ruff-0.16.8"},
            body="Bumps ruff.",
            user={"login": "dependabot[bot]"},
        )
        result = pr_policy.evaluate(pr, [], ["pyproject.toml"])
        self.assertTrue(result.ok, result.errors)
        self.assertEqual(result.warnings, [])


if __name__ == "__main__":
    unittest.main()
