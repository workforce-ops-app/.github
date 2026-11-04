import unittest

import sync_project as sp


def card(number=1, **overrides):
    """A plain open, unblocked, Final demo issue on the board in Ready; override what a test needs."""
    values = {
        "item_id": f"item{number}",
        "issue_id": f"issue{number}",
        "repo": "workforce-ops-backend",
        "number": number,
        "title": "t",
        "closed": False,
        "status": sp.READY,
        "tier": "Final demo",
        "milestone": "Final demo",
        "assignees": set(),
        "open_blockers": 0,
        "sub_issue_ids": [],
        "closed_sub_issues": 0,
        "linked_prs": [],
    }
    values.update(overrides)
    return sp.Card(**values)


def pr(author="trosper", bot=False):
    return sp.LinkedPR(number=9, repo="workforce-ops-backend", author=author, author_is_bot=bot)


def open_pr(head="feat/1-x", base="main", bot=False, closes=0):
    return sp.OpenPR("workforce-ops-backend", 9, head, base, bot, closes)


class StatusRules(unittest.TestCase):
    def test_closed_is_done_even_with_a_branch(self):
        self.assertEqual(sp.desired_status(card(closed=True), has_branch=True), sp.DONE)

    def test_open_pr_is_in_review(self):
        self.assertEqual(sp.desired_status(card(linked_prs=[pr()]), has_branch=True), sp.IN_REVIEW)

    def test_branch_is_in_progress(self):
        self.assertEqual(sp.desired_status(card(open_blockers=2), has_branch=True), sp.IN_PROGRESS)

    def test_manual_in_progress_is_kept(self):
        self.assertEqual(sp.desired_status(card(status=sp.IN_PROGRESS), has_branch=False), sp.IN_PROGRESS)

    def test_pr_closed_without_merge_falls_back(self):
        # The card said In review, but its pull request is gone and nothing else applies.
        self.assertEqual(sp.desired_status(card(status=sp.IN_REVIEW), has_branch=False), sp.READY)

    def test_blocked_is_backlog(self):
        self.assertEqual(sp.desired_status(card(open_blockers=1), has_branch=False), sp.BACKLOG)

    def test_stretch_is_backlog_even_without_the_field(self):
        c = card(tier=None, milestone="Stretch")
        self.assertEqual(sp.desired_status(c, has_branch=False), sp.BACKLOG)

    def test_unblocked_is_ready(self):
        self.assertEqual(sp.desired_status(card(status=sp.BACKLOG), has_branch=False), sp.READY)


class TrackerRules(unittest.TestCase):
    def test_tracker_with_nothing_started_is_backlog(self):
        tracker = card(10, sub_issue_ids=["issue1"])
        self.assertEqual(sp.tracker_status(tracker, {"issue1": sp.READY}), sp.BACKLOG)

    def test_tracker_with_a_closed_sub_issue_is_in_progress(self):
        tracker = card(10, sub_issue_ids=["issue1"], closed_sub_issues=1)
        self.assertEqual(sp.tracker_status(tracker, {}), sp.IN_PROGRESS)

    def test_tracker_with_a_sub_issue_in_review_is_in_progress(self):
        tracker = card(10, sub_issue_ids=["issue1"])
        self.assertEqual(sp.tracker_status(tracker, {"issue1": sp.IN_REVIEW}), sp.IN_PROGRESS)

    def test_nested_trackers_settle(self):
        # Roadmap -> phase tracker -> slice with a branch: both trackers end up In progress.
        roadmap = card(24, status=sp.READY, sub_issue_ids=["issue54"])
        phase = card(54, status=sp.READY, sub_issue_ids=["issue1"])
        result = sp.plan([roadmap, phase, card(1)], {"workforce-ops-backend": {1}}, [])
        moved = {c.number: status for c, status in result.status}
        self.assertEqual(moved, {24: sp.IN_PROGRESS, 54: sp.IN_PROGRESS, 1: sp.IN_PROGRESS})

    def test_branch_in_another_repo_does_not_count(self):
        result = sp.plan([card(1)], {"workforce-ops-frontend": {1}}, [])
        self.assertEqual(result.status, [])


class PlanExtras(unittest.TestCase):
    def test_missing_tier_filled_from_milestone(self):
        result = sp.plan([card(tier=None, milestone="Final demo")], {}, [])
        self.assertEqual([t for _, t in result.tier], ["Final demo"])

    def test_unknown_milestone_leaves_tier_alone(self):
        result = sp.plan([card(tier=None, milestone="Midterm demo")], {}, [])
        self.assertEqual(result.tier, [])

    def test_pr_author_assigned_once(self):
        result = sp.plan([card(linked_prs=[pr("a"), pr("a")])], {}, [])
        self.assertEqual([login for _, login in result.assign], ["a"])

    def test_existing_assignee_and_bots_not_assigned(self):
        c = card(assignees={"a"}, linked_prs=[pr("a"), pr("dependabot[bot]", bot=True)])
        self.assertEqual(sp.plan([c], {}, []).assign, [])

    def test_unlinked_pr_gets_comment_linked_pr_loses_it(self):
        unlinked, linked = open_pr(closes=0), open_pr(closes=1)
        result = sp.plan([], {}, [unlinked, linked])
        self.assertEqual(result.comment, [unlinked])
        self.assertEqual(result.uncomment, [linked])

    def test_bots_promotions_and_review_branches_skipped(self):
        skipped = [
            open_pr(bot=True),
            open_pr(head="main", base="production"),
            open_pr(head="review/integration"),
            open_pr(head="dependabot/pip/ruff-1"),
        ]
        result = sp.plan([], {}, skipped)
        self.assertEqual((result.comment, result.uncomment), ([], []))


class BranchNames(unittest.TestCase):
    def test_only_numbered_branches_count(self):
        names = ["feat/14-time-off", "docs/no-number", "main", "review/integration", "fix/7-x"]
        self.assertEqual(sp.branch_issue_numbers(names), {14, 7})


if __name__ == "__main__":
    unittest.main()
