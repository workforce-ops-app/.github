import json
import tempfile
import unittest
from pathlib import Path

import ci_report


class ReportTests(unittest.TestCase):
    def build(self, files):
        with tempfile.TemporaryDirectory() as tmp:
            for name, data in files.items():
                Path(tmp, name).write_text(json.dumps(data), encoding="utf-8")
            return ci_report.build(Path(tmp), "workforce-ops-backend", "1e39397abc", "python", "")

    def test_policy_first_and_overall_pass(self):
        report, failed = self.build(
            {
                "checks.json": [
                    {"name": "lint", "status": "pass", "summary": "0 problems", "time": 8.5},
                    {"name": "typecheck", "status": "skip", "summary": "no app", "time": None},
                ],
                "policy.json": {
                    "results": [{"name": "pr-policy", "status": "pass", "summary": "ok", "time": 0.4}],
                    "warnings": ["No linked issue"],
                },
            }
        )
        self.assertFalse(failed)
        self.assertLess(report.index("pr-policy"), report.index("lint"))
        self.assertIn("2 passed · 0 failed · 1 skipped", report)
        self.assertIn("No linked issue", report)
        self.assertTrue(report.startswith(ci_report.MARKER))

    def test_failure_and_bypass(self):
        report, failed = self.build(
            {
                "checks.json": [
                    {"name": "lint", "status": "fail", "summary": "3 | errors", "time": 1.0},
                    {"name": "typecheck", "status": "bypassed", "summary": "failed", "time": 61.0},
                ]
            }
        )
        self.assertTrue(failed)
        self.assertIn("3 \\| errors", report)
        self.assertIn("1 bypassed", report)
        self.assertIn("1m 1s", report)

    def test_no_results_fails(self):
        _, failed = self.build({})
        self.assertTrue(failed)


if __name__ == "__main__":
    unittest.main()
