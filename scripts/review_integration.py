"""Rebuild review/integration from main plus every open, ready-for-review PR.

The branch is rebuilt from scratch on every run, so merged or closed PRs never
linger in it. PRs are merged in PR-number order; a PR that conflicts is left out
and gets a comment naming what it conflicts with. Must run in a full-history
checkout with push access. Only this automation should write to the branch.
"""

from __future__ import annotations

import os
import subprocess
import sys

from github_api import find_comment, paged, request, upsert_comment

BRANCH = "review/integration"
MARKER = "<!-- review-integration -->"
BOT_NAME = "github-actions[bot]"
BOT_EMAIL = "41898282+github-actions[bot]@users.noreply.github.com"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=check)


def conflicts(a: str, b: str) -> bool:
    """True when merging two refs would conflict (does not touch the working tree)."""
    return git("merge-tree", "--write-tree", a, b, check=False).returncode != 0


def main() -> int:
    repo = os.environ["GITHUB_REPOSITORY"]
    git("config", "user.name", BOT_NAME)
    git("config", "user.email", BOT_EMAIL)

    pulls = [
        p
        for p in paged(f"/repos/{repo}/pulls?state=open&base=main&sort=created&direction=asc")
        if not p["draft"]
        and p["head"]["repo"] is not None
        and p["head"]["repo"]["full_name"] == repo
        and not p["head"]["ref"].startswith("review/")
    ]
    pulls.sort(key=lambda p: p["number"])

    git("fetch", "--no-tags", "origin", "main", *[p["head"]["ref"] for p in pulls])
    git("checkout", "-B", BRANCH, "origin/main")

    included: list[dict] = []
    skipped: list[tuple[dict, str]] = []
    for pr in pulls:
        ref = f"origin/{pr['head']['ref']}"
        merge = git(
            "merge",
            "--no-ff",
            "--no-edit",
            "-m",
            f"chore(review): merge #{pr['number']} ({pr['head']['ref']}) into {BRANCH}",
            ref,
            check=False,
        )
        if merge.returncode == 0:
            included.append(pr)
            continue
        git("merge", "--abort", check=False)
        if conflicts("origin/main", ref):
            reason = "`main` (rebase or merge `main` into the branch)"
        else:
            clashing = [f"#{o['number']}" for o in included if conflicts(f"origin/{o['head']['ref']}", ref)]
            reason = ", ".join(clashing) if clashing else "the combination of the PRs merged before it"
        skipped.append((pr, reason))

    git("push", "--force", "origin", f"{BRANCH}:{BRANCH}")
    sha = git("rev-parse", "HEAD").stdout.strip()

    # Pushes made with the workflow token do not start other workflows, but a
    # dispatch does, so CI runs on the combined branch as its own run.
    workflow = os.environ.get("CI_WORKFLOW", "ci.yml")
    request("POST", f"/repos/{repo}/actions/workflows/{workflow}/dispatches", {"ref": BRANCH})

    for pr, reason in skipped:
        upsert_comment(
            repo,
            pr["number"],
            MARKER,
            (
                f"{MARKER}\n⚠️ **Left out of `{BRANCH}`**: this PR conflicts with {reason}.\n\n"
                "Resolving it now avoids a merge conflict later. This comment updates automatically."
            ),
        )
    for pr in included:
        if find_comment(repo, pr["number"], MARKER):
            upsert_comment(
                repo, pr["number"], MARKER, (f"{MARKER}\n✅ This PR now merges cleanly into `{BRANCH}`.")
            )

    lines = [f"### `{BRANCH}` rebuilt at `{sha[:7]}`", "", "**Included (on top of `main`):**"]
    lines += [f"- #{p['number']} {p['title']}" for p in included] or ["- none"]
    if skipped:
        lines += ["", "**Left out (conflicts):**"]
        lines += [f"- #{p['number']} {p['title']} — conflicts with {r}" for p, r in skipped]
    summary = "\n".join(lines) + "\n"
    print(summary)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as fh:
            fh.write(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
