"""Entry points for the pre-commit hooks declared in .pre-commit-hooks.yaml."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from . import rules


def _current_branch() -> str:
    out = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=False
    )
    return out.stdout.strip()


def _report(result: rules.Result) -> int:
    for warning in result.warnings:
        print(f"warning: {warning}")
    for error in result.errors:
        print(f"error: {error}", file=sys.stderr)
    return 0 if result.ok else 1


def commit_message() -> int:
    """commit-msg stage: validate format and add 'Refs #N' from the branch name if missing."""
    if len(sys.argv) < 2:
        print("error: expected the commit message file path", file=sys.stderr)
        return 1
    path = Path(sys.argv[1])
    message = path.read_text(encoding="utf-8")
    result = rules.check_commit_message(message)
    if result.ok and not rules.has_issue_reference(message):
        issue = rules.issue_number_from_branch(_current_branch())
        if issue:
            path.write_text(message.rstrip("\n") + f"\n\nRefs #{issue}\n", encoding="utf-8")
            print(f"Added 'Refs #{issue}' from the branch name.")
    return _report(result)


def branch_name() -> int:
    """pre-push stage: validate the branch being pushed and block direct pushes to protected branches."""
    local = os.environ.get("PRE_COMMIT_LOCAL_BRANCH", "").removeprefix("refs/heads/") or _current_branch()
    remote = os.environ.get("PRE_COMMIT_REMOTE_BRANCH", "").removeprefix("refs/heads/") or local
    result = rules.Result()
    if remote in rules.PROTECTED_BRANCHES:
        result.errors.append(f"Direct pushes to '{remote}' are not allowed; open a pull request instead.")
    else:
        result = rules.check_branch(local)
    return _report(result)
