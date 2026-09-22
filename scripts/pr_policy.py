"""Check a pull request against the project's workflow rules.

Runs in CI on pull_request events. Reads the event payload and the GitHub API,
then writes ci-results/policy.json for ci_report.py. Errors fail the check;
warnings appear in the report without failing it. pr-policy cannot be bypassed.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))

from github_api import paged  # noqa: E402
from workforce_ops_hooks import rules  # noqa: E402

REQUIRED_SECTIONS = ("## Summary", "## What changed", "## Details")
PROMOTION_SECTIONS = ("## Summary",)
DOC_PATHS = ("docs/", "README.md")
BOT_AUTHORS = {"dependabot[bot]"}


def _section(body: str, heading: str) -> str:
    """Text under a markdown heading, up to the next heading of the same or higher level."""
    level = heading.split(" ")[0]
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower() == heading.lower():
            collected = []
            for nxt in lines[i + 1 :]:
                marker = nxt.split(" ")[0]
                if marker.startswith("#") and len(marker) <= len(level) and set(marker) == {"#"}:
                    break
                collected.append(nxt)
            text = "\n".join(collected)
            # Ignore template guidance comments.
            while "<!--" in text and "-->" in text:
                start = text.index("<!--")
                text = text[:start] + text[text.index("-->", start) + 3 :]
            return text.strip()
    return ""


def _filled(text: str) -> bool:
    """True when a section has real content, not just empty list markers from the template."""
    for line in text.splitlines():
        stripped = line.strip().removeprefix("- [ ]").removeprefix("- [x]").lstrip("-*0123456789. ")
        if any(ch.isalnum() for ch in stripped):
            return True
    return False


def evaluate(pr: dict, commits: list[dict], files: list[str]) -> rules.Result:
    result = rules.Result()
    title = pr["title"]
    body = pr.get("body") or ""
    head = pr["head"]["ref"]
    base = pr["base"]["ref"]
    author = pr["user"]["login"]
    labels = {label["name"] for label in pr.get("labels", [])}
    is_bot = author in BOT_AUTHORS
    is_promotion = head == "main" and base == "production"

    # Branch flow
    if head.startswith(rules.REVIEW_PREFIX):
        result.errors.append(
            f"'{head}' is a review branch. Review branches are for combined testing only and "
            "can never be merged; open PRs from the individual topic branches instead."
        )
    if base == "production" and not is_promotion:
        result.errors.append("Only 'main' may be merged into 'production'.")
    if base not in ("main", "production"):
        result.errors.append(f"PRs must target 'main' (or 'production' for promotions), not '{base}'.")

    # Title and branch name
    result.errors.extend(rules.check_title(title).errors)
    if not is_bot and not is_promotion:
        branch = rules.check_branch(head)
        result.errors.extend(branch.errors)
        result.warnings.extend(branch.warnings)

    # Description structure
    if not is_bot:
        for heading in PROMOTION_SECTIONS if is_promotion else REQUIRED_SECTIONS:
            if not _filled(_section(body, heading)):
                result.errors.append(f"The description needs a filled-in '{heading}' section.")
        if not is_promotion and not rules.has_issue_reference(body):
            result.warnings.append(
                "No linked issue (`Closes #N` or `Refs #N`). Basing work on a logged issue is encouraged."
            )

    # Bypass labels need a written justification.
    bypass_labels = sorted(label for label in labels if label.startswith("bypass:"))
    if bypass_labels:
        justification = "\n".join(
            line
            for line in _section(body, "### Bypass justification").splitlines()
            if line.strip() and not rules.ISSUE_REF_RE.fullmatch(line.strip())
        ).strip()
        if justification.lower() in ("", "none", "n/a", "-"):
            result.errors.append(
                f"Bypass label(s) {', '.join(bypass_labels)} are applied, so the "
                "'### Bypass justification' section must explain why."
            )

    # Commit trailers
    for commit in commits:
        message = commit["commit"]["message"]
        if rules.COAUTHOR_TRAILER_RE.search(message):
            result.errors.append(
                f"Commit {commit['sha'][:7]} has a Co-authored-by trailer, which this project does not use."
            )

    # Documentation
    if not is_bot and not is_promotion and "docs:not-needed" not in labels:
        code_changed = any(not f.startswith(DOC_PATHS) and not f.startswith(".github/") for f in files)
        docs_changed = any(f.startswith(DOC_PATHS) for f in files)
        if code_changed and not docs_changed:
            result.warnings.append(
                "Code changed but no documentation did. Update docs/ or add the `docs:not-needed` label."
            )
    return result


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    start = time.monotonic()
    pr = event["pull_request"]
    repo = os.environ["GITHUB_REPOSITORY"]
    number = pr["number"]
    commits = paged(f"/repos/{repo}/pulls/{number}/commits")
    files = [f["filename"] for f in paged(f"/repos/{repo}/pulls/{number}/files")]

    result = evaluate(pr, commits, files)
    for warning in result.warnings:
        print(f"warning: {warning}")
    for error in result.errors:
        print(f"error: {error}")

    if result.ok:
        summary = "title, branch, description and commits follow the rules"
    else:
        summary = f"{len(result.errors)} problem(s): " + " ".join(result.errors)
    out = Path("ci-results/policy.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "results": [
                    {
                        "name": "pr-policy",
                        "status": "pass" if result.ok else "fail",
                        "summary": summary,
                        "time": time.monotonic() - start,
                    }
                ],
                "warnings": result.warnings,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
