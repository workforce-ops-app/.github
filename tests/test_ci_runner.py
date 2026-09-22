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


if __name__ == "__main__":
    unittest.main()
