"""Keep the combined project board in step with the issues, branches, and pull requests (issue #103).

Runs on a schedule from this repository with the organization secret ADD_TO_PROJECT_TOKEN.
Each run:

1. Reads every card on the board and the issue behind it.
2. Works out the Status each card should have (rules in `desired_status` and `tracker_status`).
3. Fills a missing Tier from the issue's milestone.
4. Assigns a pull request's author to the issue that pull request closes.
5. Comments on open pull requests that close no issue, and removes the comment once they do.

The script is split into reading (`fetch_*`), deciding (`plan`), and writing (`apply`), so the
deciding part can be unit-tested without the GitHub API. Set DRY_RUN=true to print the plan only.
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

# The branch-name rule lives with the git hooks, so the board reads branches the same way they are checked.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hooks"))

from github_api import find_comment, graphql, paged, request, upsert_comment  # noqa: E402
from workforce_ops_hooks import rules  # noqa: E402

ORG = "workforce-ops-app"
PROJECT_NUMBER = 4
REPOS = (".github", "workforce-ops-backend", "workforce-ops-frontend", "workforce-ops-research")

# Status column names, exactly as they appear on the board.
BACKLOG, READY, IN_PROGRESS, IN_REVIEW, DONE = "Backlog", "Ready", "In progress", "In review", "Done"
STRETCH = "Stretch"
# Milestones that map straight onto a Tier option of the same name.
TIER_MILESTONES = ("Final demo", "Stretch")

# Hidden marker that lets later runs find (and update or remove) the comment they posted.
UNLINKED_MARKER = "<!-- project-sync:unlinked-pr -->"
# Pieces are joined without line breaks because GitHub comments show every line break.
UNLINKED_BODY = (
    f"{UNLINKED_MARKER}\n"
    "This pull request does not close an issue, so the "
    f"[project board](https://github.com/orgs/{ORG}/projects/{PROJECT_NUMBER}) cannot show it.\n\n"
    f"If it finishes an issue, add a line such as `Closes #N` (or `Closes {ORG}/<repository>#N`) "
    "to the description; this comment disappears on the next board sync. "
    "If it only relates to an issue without finishing it (`Refs #N`), you can ignore this.\n"
)


# ---------------------------------------------------------------------------
# Data read from GitHub, reduced to what the rules need
# ---------------------------------------------------------------------------


@dataclass
class LinkedPR:
    """An open pull request whose description closes the issue (`Closes #N`)."""

    number: int
    repo: str
    author: str
    author_is_bot: bool


@dataclass
class Card:
    """One board card that holds an issue (draft notes and pull request cards are ignored)."""

    item_id: str  # the card's id on the board
    issue_id: str  # the issue's GraphQL id, used to find sub-issues
    repo: str
    number: int
    title: str
    closed: bool
    status: str | None  # current Status column, None if unset
    tier: str | None  # current Tier field, None if unset
    milestone: str | None
    assignees: set[str]
    open_blockers: int  # issues blocking this one that are still open
    sub_issue_ids: list[str]  # GraphQL ids of sub-issues; non-empty means this is a tracker
    closed_sub_issues: int
    linked_prs: list[LinkedPR] = field(default_factory=list)

    @property
    def ref(self) -> str:
        """Short name for logs, for example workforce-ops-backend#53."""
        return f"{self.repo}#{self.number}"


@dataclass
class OpenPR:
    """An open pull request, checked for a missing `Closes` link."""

    repo: str
    number: int
    head: str
    base: str
    author_is_bot: bool
    closes_issues: int


@dataclass
class Plan:
    """Everything one run would change. `apply` carries it out; tests inspect it."""

    status: list[tuple[Card, str]] = field(default_factory=list)  # (card, new Status)
    tier: list[tuple[Card, str]] = field(default_factory=list)  # (card, new Tier)
    assign: list[tuple[Card, str]] = field(default_factory=list)  # (card, login to add)
    comment: list[OpenPR] = field(default_factory=list)  # PRs that need the unlinked comment
    uncomment: list[OpenPR] = field(default_factory=list)  # PRs whose comment can go


# ---------------------------------------------------------------------------
# Deciding: pure functions, no API calls
# ---------------------------------------------------------------------------


def tier_from_milestone(milestone: str | None) -> str | None:
    """The Tier a milestone implies: the milestones and the Tier options share names."""
    return milestone if milestone in TIER_MILESTONES else None


def desired_status(card: Card, has_branch: bool) -> str:
    """Status for an issue that is not a tracker. The first matching rule wins."""
    if card.closed:
        return DONE  # merged (or closed by hand)
    if card.linked_prs:
        return IN_REVIEW  # a pull request that closes it is open
    if has_branch:
        return IN_PROGRESS  # someone pushed a branch named <type>/<number>-<slug>
    if card.status == IN_PROGRESS:
        return IN_PROGRESS  # moved there by a person; only a pull request or closing moves it on
    tier = card.tier or tier_from_milestone(card.milestone)
    if tier == STRETCH or card.open_blockers:
        return BACKLOG  # not for the final demo, or waiting on other work
    return READY


def tracker_status(card: Card, statuses: dict[str, str]) -> str:
    """Status for a tracker: it moves with its sub-issues, since nobody works on a tracker directly.

    `statuses` maps issue ids to the Status already decided for them (sub-issues not on the
    board are missing from it, and then only their closed count matters).
    """
    if card.closed:
        return DONE
    underway = card.closed_sub_issues > 0 or any(
        statuses.get(sub) in (IN_PROGRESS, IN_REVIEW, DONE) for sub in card.sub_issue_ids
    )
    return IN_PROGRESS if underway else BACKLOG


def plan(cards: list[Card], branch_issues: dict[str, set[int]], open_prs: list[OpenPR]) -> Plan:
    """Decide every change for one run.

    `branch_issues` maps a repository to the issue numbers that have a branch there.
    """
    result = Plan()
    statuses: dict[str, str] = {}

    # Ordinary issues first, so trackers can look at their sub-issues' new Status.
    for card in cards:
        if not card.sub_issue_ids:
            statuses[card.issue_id] = desired_status(card, card.number in branch_issues.get(card.repo, set()))

    # Trackers can contain trackers (the Roadmap holds the phase trackers), so repeat until nothing
    # changes. Each pass settles at least one more level, and the nesting is shallow.
    trackers = [card for card in cards if card.sub_issue_ids]
    for _ in range(len(trackers) + 1):
        changed = False
        for card in trackers:
            new = tracker_status(card, statuses)
            if statuses.get(card.issue_id) != new:
                statuses[card.issue_id] = new
                changed = True
        if not changed:
            break

    for card in cards:
        if statuses[card.issue_id] != card.status:
            result.status.append((card, statuses[card.issue_id]))
        tier = tier_from_milestone(card.milestone)
        if card.tier is None and tier:
            result.tier.append((card, tier))
        # Record who did the work: the author of each open pull request that closes the issue.
        if not card.closed:
            for pr in card.linked_prs:
                if not pr.author_is_bot and pr.author not in card.assignees:
                    result.assign.append((card, pr.author))
                    card.assignees.add(pr.author)  # two PRs by one author: assign once

    for pr in open_prs:
        if not needs_link_check(pr):
            continue
        if pr.closes_issues == 0:
            result.comment.append(pr)
        else:
            result.uncomment.append(pr)
    return result


def needs_link_check(pr: OpenPR) -> bool:
    """Bots, promotions to production, and review branches never close issues, so leave them alone."""
    return not (
        pr.author_is_bot
        or pr.base == "production"
        or pr.head.startswith((rules.REVIEW_PREFIX, rules.DEPENDABOT_PREFIX))
    )


def branch_issue_numbers(branches: list[str]) -> set[int]:
    """Issue numbers named by branches like feat/14-time-off-requests; branches without one are skipped."""
    numbers = set()
    for name in branches:
        match = rules.BRANCH_RE.match(name)
        if match and match["issue"]:
            numbers.add(int(match["issue"]))
    return numbers


# ---------------------------------------------------------------------------
# Reading from GitHub
# ---------------------------------------------------------------------------

ITEMS_QUERY = """
query($org: String!, $number: Int!, $cursor: String) {
  organization(login: $org) {
    projectV2(number: $number) {
      items(first: 50, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          status: fieldValueByName(name: "Status") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
          tier: fieldValueByName(name: "Tier") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
          content {
            ... on Issue {
              id number title state
              repository { name }
              milestone { title }
              assignees(first: 10) { nodes { login } }
              blockedBy(first: 30) { nodes { state } }
              subIssuesSummary { completed }
              subIssues(first: 50) { nodes { id } }
              closedByPullRequestsReferences(first: 10, includeClosedPrs: false) {
                nodes { number state repository { name } author { __typename login } }
              }
            }
          }
        }
      }
    }
  }
}
"""

FIELDS_QUERY = """
query($org: String!, $number: Int!) {
  organization(login: $org) {
    projectV2(number: $number) {
      id
      fields(first: 50) { nodes { ... on ProjectV2SingleSelectField { id name options { id name } } } }
    }
  }
}
"""

PRS_QUERY = """
query($org: String!, $repo: String!, $cursor: String) {
  repository(owner: $org, name: $repo) {
    pullRequests(states: OPEN, first: 100, after: $cursor) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number headRefName baseRefName
        author { __typename login }
        closingIssuesReferences(first: 1) { totalCount }
      }
    }
  }
}
"""


def _is_bot(author: dict | None) -> bool:
    """Deleted accounts come back as null; treat them like bots (nobody to assign)."""
    return not author or author.get("__typename") == "Bot" or author.get("login", "").endswith("[bot]")


def fetch_cards() -> list[Card]:
    """Every issue card on the board, following the pages."""
    cards, cursor = [], None
    while True:
        page = graphql(ITEMS_QUERY, org=ORG, number=PROJECT_NUMBER, cursor=cursor)
        items = page["organization"]["projectV2"]["items"]
        for node in items["nodes"]:
            issue = node.get("content") or {}
            if "number" not in issue:
                continue  # a draft note or a pull request card
            cards.append(
                Card(
                    item_id=node["id"],
                    issue_id=issue["id"],
                    repo=issue["repository"]["name"],
                    number=issue["number"],
                    title=issue["title"],
                    closed=issue["state"] == "CLOSED",
                    status=(node.get("status") or {}).get("name"),
                    tier=(node.get("tier") or {}).get("name"),
                    milestone=(issue.get("milestone") or {}).get("title"),
                    assignees={a["login"] for a in issue["assignees"]["nodes"]},
                    open_blockers=sum(1 for b in issue["blockedBy"]["nodes"] if b["state"] == "OPEN"),
                    sub_issue_ids=[s["id"] for s in issue["subIssues"]["nodes"]],
                    closed_sub_issues=issue["subIssuesSummary"]["completed"],
                    linked_prs=[
                        LinkedPR(
                            p["number"],
                            p["repository"]["name"],
                            (p["author"] or {}).get("login", ""),
                            _is_bot(p["author"]),
                        )
                        for p in issue["closedByPullRequestsReferences"]["nodes"]
                        if p["state"] == "OPEN"
                    ],
                )
            )
        if not items["pageInfo"]["hasNextPage"]:
            return cards
        cursor = items["pageInfo"]["endCursor"]


def fetch_fields() -> tuple[str, dict[str, dict]]:
    """The board's id, and each single-select field by name with its options' ids by name."""
    project = graphql(FIELDS_QUERY, org=ORG, number=PROJECT_NUMBER)["organization"]["projectV2"]
    fields = {
        f["name"]: {"id": f["id"], "options": {o["name"]: o["id"] for o in f["options"]}}
        for f in project["fields"]["nodes"]
        if f  # fields that are not single-select come back empty
    }
    return project["id"], fields


def fetch_branch_issues() -> dict[str, set[int]]:
    """Issue numbers that have a branch, per repository."""
    return {
        repo: branch_issue_numbers([b["name"] for b in paged(f"/repos/{ORG}/{repo}/branches")])
        for repo in REPOS
    }


def fetch_open_prs() -> list[OpenPR]:
    prs = []
    for repo in REPOS:
        cursor = None
        while True:
            page = graphql(PRS_QUERY, org=ORG, repo=repo, cursor=cursor)["repository"]["pullRequests"]
            prs += [
                OpenPR(
                    repo,
                    p["number"],
                    p["headRefName"],
                    p["baseRefName"],
                    _is_bot(p["author"]),
                    p["closingIssuesReferences"]["totalCount"],
                )
                for p in page["nodes"]
            ]
            if not page["pageInfo"]["hasNextPage"]:
                break
            cursor = page["pageInfo"]["endCursor"]
    return prs


# ---------------------------------------------------------------------------
# Writing to GitHub
# ---------------------------------------------------------------------------

SET_FIELD = """
mutation($project: ID!, $item: ID!, $field: ID!, $option: String!) {
  updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field,
                                        value: {singleSelectOptionId: $option}}) { projectV2Item { id } }
}
"""


def apply(changes: Plan, project_id: str, fields: dict[str, dict], dry_run: bool) -> list[str]:
    """Carry out the plan. Returns the log lines; a failed step is logged and the rest still run."""
    log, failures = [], 0

    def step(text: str, action) -> None:
        nonlocal failures
        if dry_run:
            log.append(f"would {text}")
            return
        try:
            action()
            log.append(text)
        except Exception as error:  # noqa: BLE001 - keep going so one bad card does not stop the sync
            failures += 1
            log.append(f"FAILED to {text}: {error}")

    def set_field(card: Card, name: str, value: str) -> None:
        graphql(
            SET_FIELD,
            project=project_id,
            item=card.item_id,
            field=fields[name]["id"],
            option=fields[name]["options"][value],
        )

    for card, value in changes.status:
        step(
            f"move {card.ref} from {card.status or 'no status'} to {value}",
            lambda c=card, v=value: set_field(c, "Status", v),
        )
    for card, value in changes.tier:
        step(f"set {card.ref} Tier to {value}", lambda c=card, v=value: set_field(c, "Tier", v))
    for card, login in changes.assign:
        step(
            f"assign {login} to {card.ref}",
            lambda c=card, u=login: request(
                "POST", f"/repos/{ORG}/{c.repo}/issues/{c.number}/assignees", {"assignees": [u]}
            ),
        )
    for pr in changes.comment:
        step(
            f"comment on {pr.repo}#{pr.number} (closes no issue)",
            lambda p=pr: upsert_comment(f"{ORG}/{p.repo}", p.number, UNLINKED_MARKER, UNLINKED_BODY),
        )
    for pr in changes.uncomment:
        # Only a PR that once had the comment needs a write; looking it up costs one read.
        existing = find_comment(f"{ORG}/{pr.repo}", pr.number, UNLINKED_MARKER)
        if existing:
            step(
                f"remove the unlinked comment from {pr.repo}#{pr.number}",
                lambda c=existing, p=pr: request(
                    "DELETE", f"/repos/{ORG}/{p.repo}/issues/comments/{c['id']}"
                ),
            )

    if failures:
        log.append(f"{failures} change(s) failed")
    return log


def main() -> int:
    dry_run = os.environ.get("DRY_RUN", "").lower() == "true" or "--dry-run" in sys.argv
    project_id, fields = fetch_fields()
    changes = plan(fetch_cards(), fetch_branch_issues(), fetch_open_prs())
    log = apply(changes, project_id, fields, dry_run) or ["board already up to date"]
    print("\n".join(log))

    # Show the same lines on the run's summary page in GitHub Actions.
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as out:
            out.write("### Project board sync" + (" (dry run)" if dry_run else "") + "\n\n")
            out.write("\n".join(f"- {line}" for line in log) + "\n")
    return 1 if any(line.startswith("FAILED") for line in log) else 0


if __name__ == "__main__":
    sys.exit(main())
