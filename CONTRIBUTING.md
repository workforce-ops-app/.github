# Contributing

**In short:** every change starts from an issue, happens on its own branch, and reaches `main` through a pull request that passes CI and is approved by a teammate. `main` is later promoted to `production`.

The full guide is in [`docs/contributing/`](https://github.com/workforce-ops-app/.github/tree/main/docs/contributing). The essentials:

1. **Start from an issue.** Use the issue templates. Titles look like `feat(time-off): add request submission`.
2. **Start clean.** Update `main` and delete local branches whose pull requests have merged ([workflow](https://github.com/workforce-ops-app/.github/blob/main/docs/contributing/workflow.md#1-start-clean)).
3. **Branch** as `<type>/<issue#>-<slug>`, e.g. `feat/14-time-off-requests`.
4. **Commit** with the same format as titles, referencing the issue: `Refs #14` or `Closes #14`.
5. **Keep changes modular.** One topic per pull request, and avoid touching shared files when you don't need to ([modularity](https://github.com/workforce-ops-app/.github/blob/main/docs/contributing/modularity.md)).
6. **Update the docs** that your change affects, in the same pull request.
7. **Open a pull request** using the template. CI posts a report comment; every check must pass.
8. **Get a teammate's approval**, then squash-merge.

Never open a pull request from a `review/*` branch; those exist only for combined testing.

Security problems that could be exploited must not go in public issues. See [SECURITY.md](SECURITY.md).
