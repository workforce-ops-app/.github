import unittest

import ci_runner


class SummaryTests(unittest.TestCase):
    def test_last_non_empty_line(self):
        self.assertEqual(ci_runner._summary_from_output("a\n\n=== 3 passed ===\n\n"), "3 passed")

    def test_color_codes_removed(self):
        output = "\x1b[90m10:26PM\x1b[0m \x1b[33mWRN\x1b[0m \x1b[1mleaks found: 2\x1b[0m\n"
        self.assertEqual(ci_runner._summary_from_output(output), "10:26PM WRN leaks found: 2")

    def test_truncated(self):
        self.assertEqual(len(ci_runner._summary_from_output("x" * 500)), ci_runner.MAX_SUMMARY)


class PatternSummaryTests(unittest.TestCase):
    PYTEST = (
        "......  [100%]\n"
        "Name            Stmts   Miss  Cover\n"
        "TOTAL              86      5    94%\n"
        "6 passed in 0.31s\n"
    )
    PATTERNS = [r"(\d+) passed", r"TOTAL.* (\d+%)"]

    def test_fills_format_with_first_groups(self):
        summary = ci_runner._summary_from_patterns(self.PYTEST, self.PATTERNS, "{0} passed · coverage {1}")
        self.assertEqual(summary, "6 passed · coverage 94%")

    def test_missing_pattern_returns_none(self):
        self.assertIsNone(ci_runner._summary_from_patterns("6 passed\n", self.PATTERNS, "{0} {1}"))

    def test_pattern_without_group_uses_whole_match(self):
        self.assertEqual(ci_runner._summary_from_patterns("ok: 3 files", [r"\d+ files"], "{0}"), "3 files")

    def test_color_codes_ignored(self):
        output = "\x1b[32m6 passed\x1b[0m in 0.3s"
        self.assertEqual(ci_runner._summary_from_patterns(output, [r"(\d+) passed"], "{0}"), "6")


if __name__ == "__main__":
    unittest.main()
