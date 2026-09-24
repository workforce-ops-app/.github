# Design review 1: Project and team

**In short:** the project serves two courses with different deliverables: two live demos for the web course, and a 10-page research report for the security course. The midterm demo is the first real deadline. Both teammates work across the whole stack by feature, and work is tracked on one project board.

| # | Question | Answer | Status |
|---|---|---|---|
| 1.1 | What are the deadlines and deliverables? | Web course (CS 3311): live demos in midterm week and final week, plus quizzes. Security course (CS 4416/5516): final report in IEEE format, at most 10 pages, with all datasets and artifacts submitted or linked. **Dates not announced yet.** | answered |
| 1.2 | What does the instructor expect? | The instructor looks at the repositories. No expectation of an even split. Report format per the course's project instructions. | answered |
| 1.3 | How is work divided? | Both teammates work across backend and frontend **by feature**, closely together, reviewing each other's PRs. | answered |
| 1.4 | Use a GitHub Project board? | **Yes**, one board for the organization collecting issues from all repositories. | answered |
| 1.5 | Demo setup? | The application runs on a laptop with Docker Compose; parts may be shown on a phone. See [building and running](08-building-and-running.md). | answered |
| 1.6 | Where do research datasets and scripts live? | A **separate public repository**, `workforce-ops-research`, as a replication package; optionally archived with a DOI at submission. | answered |

## Resulting design

- [Project overview](../README.md): courses, deliverables, team, repositories.
- [Research report plan](../report-plan.md): sections, evidence sources, course alignment, quality check.
- [Workflow](../../contributing/workflow.md#project-board): how the project board is used.
- A `workforce-ops-research` repository is created after this review is approved.
