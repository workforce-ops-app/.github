import unittest

from workforce_ops_hooks import rules


class TitleTests(unittest.TestCase):
    def test_valid_titles(self):
        for title in (
            "feat(time-off): add request submission endpoint",
            "fix(auth): reject expired sessions",
            "chore(deps): bump ruff from 0.16.7 to 0.16.8",
            "security(authz)!: require scope on shift edits",
        ):
            self.assertTrue(rules.check_title(title).ok, title)

    def test_invalid_titles(self):
        for title in (
            "Add time off",
            "feat: missing area",
            "feature(time-off): unknown type",
            "feat(Time Off): bad area",
            "feat(time-off):no space",
        ):
            self.assertFalse(rules.check_title(title).ok, title)


class BranchTests(unittest.TestCase):
    def test_valid_with_issue(self):
        result = rules.check_branch("feat/14-time-off-requests")
        self.assertTrue(result.ok)
        self.assertEqual(result.warnings, [])

    def test_valid_without_issue_warns(self):
        result = rules.check_branch("docs/contributor-guide")
        self.assertTrue(result.ok)
        self.assertEqual(len(result.warnings), 1)

    def test_invalid(self):
        for branch in ("my-branch", "feature/14-x", "feat/14_Time", "feat/"):
            self.assertFalse(rules.check_branch(branch).ok, branch)

    def test_special_branches(self):
        for branch in ("main", "production", "review/integration", "dependabot/pip/ruff-0.16.8"):
            self.assertTrue(rules.check_branch(branch).ok, branch)
        self.assertFalse(rules.check_branch("review/Bad Name").ok)

    def test_issue_number(self):
        self.assertEqual(rules.issue_number_from_branch("fix/7-login"), "7")
        self.assertIsNone(rules.issue_number_from_branch("fix/login"))


class CommitMessageTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(rules.check_commit_message("feat(tasks): add task list\n\nRefs #3\n").ok)

    def test_merge_commit_allowed(self):
        self.assertTrue(rules.check_commit_message("Merge branch 'main' into feat/3-tasks").ok)

    def test_missing_blank_line(self):
        self.assertFalse(rules.check_commit_message("feat(tasks): add\nbody right away").ok)

    def test_coauthor_trailer_rejected(self):
        message = "feat(tasks): add list\n\nCo-authored-by: Someone <someone@example.com>\n"
        self.assertFalse(rules.check_commit_message(message).ok)

    def test_comment_lines_ignored(self):
        self.assertTrue(rules.check_commit_message("# comment\nfix(ui): align table\n").ok)


class IssueReferenceTests(unittest.TestCase):
    def test_references(self):
        self.assertTrue(rules.has_issue_reference("Closes #12"))
        self.assertTrue(rules.has_issue_reference("refs workforce-ops-app/workforce-ops-backend#4"))
        self.assertFalse(rules.has_issue_reference("see issue 12"))


if __name__ == "__main__":
    unittest.main()
