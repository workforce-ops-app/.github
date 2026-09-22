# Review branches

**In short:** `review/integration` always contains `main` plus every open, ready-for-review pull request merged together, so the team can test everything at once and find out early when two PRs clash. It is rebuilt automatically and must never become a pull request.

## review/integration

- **Rebuilt automatically** whenever `main` changes or a pull request into `main` is opened, updated, reopened, closed, or marked ready for review.
- **Rebuilt from scratch** each time: reset to `main`, then each ready PR merged in PR-number order. Merged or closed PRs never linger.
- **Draft PRs are left out.**
- **Conflicts:** a PR that does not merge cleanly is left out, and it gets a comment saying what it conflicts with (`main` or specific PRs). The comment updates once the conflict is gone. Resolving it early avoids a painful merge later.
- **CI runs on the combined result**, which catches PRs that pass alone but break together. See the Actions tab for `ci` runs on `review/integration`.
- The rebuild summary (included and left-out PRs) is shown on each `review-integration` run.

## Using it

```
git fetch origin
git switch review/integration                    # first time
git reset --hard origin/review/integration       # every time after
```

Use `reset --hard`, not `pull`: the branch is force-pushed on every rebuild.

**Never commit to it or open a PR from it.** Commits would be erased by the next rebuild, and `pr-policy` fails any PR whose head is a `review/*` branch.

## Other review branches

To test a specific combination that `review/integration` does not cover, such as a branch without a PR or a draft, create a separate branch **only when that is explicitly requested**:

```
git switch -c review/<purpose> origin/main
git merge --no-ff origin/feat/14-time-off-requests
git merge --no-ff origin/feat/15-shift-tasks
git push -u origin review/<purpose>
```

These branches can be pushed and CI runs on them. They are never turned into pull requests and are not cleaned up automatically. Delete them when finished (`git push origin --delete review/<purpose>`).
