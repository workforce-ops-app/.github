"""Open a follow-up issue when a PR merged with a bypass label or without an approval.

Emergency merges stay possible, but they always leave a visible record for the
teammate to review afterwards.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from github_api import paged, request


def main() -> int:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    pr = event["pull_request"]
    if not pr.get("merged"):
        return 0
    repo = os.environ["GITHUB_REPOSITORY"]
    number = pr["number"]
    author = pr["user"]["login"]

    bypass = sorted(label["name"] for label in pr.get("labels", []) if label["name"].startswith("bypass:"))
    latest: dict[str, str] = {}
    for review in paged(f"/repos/{repo}/pulls/{number}/reviews"):
        user = (review.get("user") or {}).get("login")
        if user and user != author and review["state"] in ("APPROVED", "CHANGES_REQUESTED", "DISMISSED"):
            latest[user] = review["state"]
    approved = any(state == "APPROVED" for state in latest.values())

    reasons = []
    if bypass:
        reasons.append(f"CI check(s) were bypassed: {', '.join(f'`{b}`' for b in bypass)}")
    if not approved:
        reasons.append("it was merged without an approving review from a teammate")
    if not reasons:
        print(f"PR #{number} merged normally; no follow-up needed.")
        return 0

    team = os.environ.get("REVIEW_TEAM", "")
    mention = f"@{team} " if team else ""
    body = "\n".join(
        [
            "## Summary",
            f"PR #{number} was merged into `{pr['base']['ref']}` outside the normal review process. "
            "A teammate should look over the change now that it is merged.",
            "",
            "## Why it matters",
            "Emergency merges are allowed, but every one gets a follow-up review so nothing slips through.",
            "",
            "---",
            "## Details",
            "### What happened",
            *[f"- {r}" for r in reasons],
            "",
            "### Acceptance criteria",
            f"- [ ] {mention}reviewed the merged changes in #{number}",
            "- [ ] Any problems found have their own issues",
            "",
            f"Refs #{number}",
        ]
    )
    issue = request(
        "POST",
        f"/repos/{repo}/issues",
        {
            "title": f"chore(review): post-merge review of #{number}",
            "body": body,
            "labels": ["post-merge-review", "type:chore", "priority:high"],
        },
    )
    print(f"Opened follow-up issue #{issue['number']} for PR #{number}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
