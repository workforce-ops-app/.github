"""Post or update the CI report comment on a pull request.

Runs from a workflow_run-triggered job so it has write access even when the CI
run itself did not (for example on Dependabot PRs). The report artifact was
produced by code from the PR branch, so the PR number inside it is verified
against the commit that CI actually ran on before anything is posted.

Expects ci-report/report.md and ci-report/pr.json in the working directory.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from github_api import request, upsert_comment

MARKER = "<!-- ci-report -->"


def main() -> int:
    report_dir = Path(os.environ.get("REPORT_DIR", "ci-report"))
    pr_file = report_dir / "pr.json"
    if not pr_file.exists():
        print("No pull request associated with this run; nothing to post.")
        return 0

    number = int(json.loads(pr_file.read_text(encoding="utf-8"))["number"])
    repo = os.environ["GITHUB_REPOSITORY"]
    head_sha = os.environ["HEAD_SHA"]

    pr = request("GET", f"/repos/{repo}/pulls/{number}")
    if not isinstance(pr, dict) or pr["head"]["sha"] != head_sha:
        print(f"PR #{number} does not match the commit CI ran on ({head_sha[:7]}); not posting.")
        return 0

    body = (report_dir / "report.md").read_text(encoding="utf-8")
    if MARKER not in body:
        body = f"{MARKER}\n{body}"
    upsert_comment(repo, number, MARKER, body[:65000])
    print(f"Updated the CI report on PR #{number}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
