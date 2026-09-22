"""Naming and message rules shared by the local git hooks and the CI PR policy.

Keeping every rule in this one module means a rule change lands in one place
and both enforcement points pick it up.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

TYPES = ("feat", "fix", "security", "refactor", "test", "docs", "chore")

PROTECTED_BRANCHES = ("main", "production")
REVIEW_PREFIX = "review/"
DEPENDABOT_PREFIX = "dependabot/"

_TYPE_GROUP = "|".join(TYPES)

# <type>(<area>): <summary>   e.g. feat(time-off): add request submission endpoint
TITLE_RE = re.compile(rf"^(?P<type>{_TYPE_GROUP})\((?P<area>[a-z0-9][a-z0-9-]*)\)!?: (?P<summary>\S.*)$")

# <type>/<issue#>-<slug>  (issue number encouraged)   or   <type>/<slug>
BRANCH_RE = re.compile(rf"^(?P<type>{_TYPE_GROUP})/(?:(?P<issue>\d+)-)?(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")

REVIEW_BRANCH_RE = re.compile(r"^review/[a-z0-9]+(?:-[a-z0-9]+)*$")

# Refs #12, Closes #12, Fixes org/repo#12, Resolves #12
ISSUE_REF_RE = re.compile(
    r"\b(?:refs|closes|close|closed|fixes|fix|fixed|resolves|resolve|resolved)\s+(?:[\w.-]+/[\w.-]+)?#\d+",
    re.IGNORECASE,
)

COAUTHOR_TRAILER_RE = re.compile(r"^co-authored-by:", re.IGNORECASE | re.MULTILINE)


@dataclass
class Result:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def check_title(title: str) -> Result:
    """Validate an issue, PR, or commit subject line."""
    result = Result()
    if not TITLE_RE.match(title.strip()):
        result.errors.append(
            f"Title '{title.strip()}' must match '<type>(<area>): <summary>' "
            f"where type is one of: {', '.join(TYPES)}."
        )
    return result


def check_branch(branch: str) -> Result:
    """Validate a branch name that work is pushed from."""
    result = Result()
    if branch in PROTECTED_BRANCHES or branch.startswith(DEPENDABOT_PREFIX):
        return result
    if branch.startswith(REVIEW_PREFIX):
        if not REVIEW_BRANCH_RE.match(branch):
            result.errors.append(f"Review branch '{branch}' must look like 'review/<lowercase-slug>'.")
        return result
    match = BRANCH_RE.match(branch)
    if not match:
        result.errors.append(
            f"Branch '{branch}' must match '<type>/<issue#>-<slug>' "
            f"(e.g. feat/14-time-off-requests) where type is one of: {', '.join(TYPES)}."
        )
    elif match.group("issue") is None:
        result.warnings.append(
            f"Branch '{branch}' has no issue number. Basing work on a logged issue is encouraged."
        )
    return result


def issue_number_from_branch(branch: str) -> str | None:
    match = BRANCH_RE.match(branch)
    return match.group("issue") if match else None


def check_commit_message(message: str) -> Result:
    """Validate a full commit message (subject, optional body, trailers)."""
    result = Result()
    lines = [line for line in message.splitlines() if not line.startswith("#")]
    subject = lines[0].strip() if lines else ""
    if not subject:
        result.errors.append("Commit message is empty.")
        return result
    # Merge commits created by git itself are allowed through untouched.
    if subject.startswith("Merge "):
        return result
    result.errors.extend(check_title(subject).errors)
    if len(lines) > 1 and lines[1].strip():
        result.errors.append("Leave a blank line between the subject and the body.")
    if COAUTHOR_TRAILER_RE.search("\n".join(lines)):
        result.errors.append("Co-authored-by trailers are not used in this project; remove the trailer.")
    return result


def has_issue_reference(text: str) -> bool:
    return bool(ISSUE_REF_RE.search(text or ""))
