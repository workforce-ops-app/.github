# Project overview

**In short:** the Workforce Operations Application is a two-person semester project that counts for two courses. One course grades the working web application through two live demos; the other grades a research report on how the application was secured and tested. This page lists what each course expects, who does what, and how work is tracked.

## Team

| Member | GitHub |
|---|---|
| Corbin Hay | `c-hayCodes` |
| Michael Trosper | `Trosper3` |

## Courses and deliverables

### CS 3311: Secure Client Server Web Development

| Deliverable | When | What |
|---|---|---|
| Midterm presentation | midterm week (date to be announced) | live demo of the application's progress to the instructor and class |
| Final presentation | final week (date to be announced) | live demo of the finished application |
| Quizzes | during the semester | individual, on web technologies and concepts |

### CS 4416/5516: Foundations in Cybersecurity and Resilience

| Deliverable | When | What |
|---|---|---|
| Project proposal | submitted | *Workforce Operations Manager* security proposal |
| Final project report | end of semester (date to be announced) | IEEE conference format, **at most 10 pages**; see the [report plan](report-plan.md) |
| Datasets and artifacts | with the report | every dataset and script used, submitted or linked by public URL |
| Peer evaluations | about every two weeks | team members evaluate each other |

Each team member submits their own copy of joint deliverables. Late work loses 10% per day and is not accepted after three days.

## Scope by stage

The features planned for each demo are recorded in decisions [0023](../decisions/0023-feature-tiers-and-audit-schedule.md) and [0036](../decisions/0036-midterm-scope-schedules.md).

| Stage | Target |
|---|---|
| **Midterm** | schedules, on the security pieces it needs (sign-in, company isolation, roles with scopes, audit log), plus a practised presentation (0036) |
| **Core** | the rest of the core tier, after the midterm and before the next tier |
| **Next** | working by the final demo |
| **Stretch** | if time allows |

## How we work

- **Split by feature, not by layer.** Each teammate owns features end to end (backend, frontend, docs, tests), working closely together, and reviews the other's pull requests. There is no expectation of an even split.
- **Every change goes through a pull request** approved by the other teammate ([workflow](../contributing/workflow.md)).
- **Work is tracked on one project board per repository** ([backend](https://github.com/orgs/workforce-ops-app/projects/1), [frontend](https://github.com/orgs/workforce-ops-app/projects/2), [.github](https://github.com/orgs/workforce-ops-app/projects/3)), with the columns Backlog, Ready, In progress, In review, and Done ([workflow](../contributing/workflow.md#project-board)).
- **The plan is the pinned [Roadmap](https://github.com/workforce-ops-app/.github/issues/24) issue:** the phases from design to the final demo, what each phase must prove before the next starts, and a tracker issue for each phase and larger feature ([slices and trackers](../contributing/issues-and-prs.md#slices-and-tracker-issues)).

## Repositories

| Repository | Purpose |
|---|---|
| [.github](https://github.com/workforce-ops-app/.github) | shared templates, CI, contributor guide, decisions, this project documentation |
| [workforce-ops-backend](https://github.com/workforce-ops-app/workforce-ops-backend) | FastAPI and MySQL backend |
| [workforce-ops-frontend](https://github.com/workforce-ops-app/workforce-ops-frontend) | HTML, CSS, and JavaScript frontend |
| `workforce-ops-research` (planned) | datasets, analysis scripts, and results for the report: the replication package |

## Design decisions

**New to the design? Start with the [design overview](design-overview.md)**: the whole system in a few minutes and a reading order. The project's design decisions and their reasons are in the [decision records](../decisions/README.md). The discussion that led to them is kept in the [design review sign-off](https://github.com/workforce-ops-app/.github/issues/17) issue.
