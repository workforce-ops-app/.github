# Design review 6: Feature details

**In short:** how each feature works where the proposal left details open: schedules, time off, shift coverage and swaps, who approves requests, notifications, shift tasks, and announcements.

## Schedules

| # | Question | Answer | Status |
|---|---|---|---|
| 6.1 | What does a shift show? | Date and times, details, notes, and optional **event information** (an event name and description for special occasions, e.g. "Inventory night"). Event information was proposed by Corbin. | answered |
| 6.2 | Can employees see their department's schedule? | **Yes, by default**: the Employee role includes department schedule viewing; administrators can remove it. | answered |
| 6.3 | Draft and publish? | **Yes**, next tier: managers prepare changes and publish them. Details (who publishes, what employees see before publishing) are designed with the feature. | answered |
| 6.4 | Can a shift have nobody assigned? | **Yes**: an **open shift**, flagged on the schedule until someone takes it (needed for approved time off, below). | answered |

## Time off

| # | Question | Answer | Status |
|---|---|---|---|
| 6.5 | How does a request work? | A **flat request** ("I want these days off"), not a swap. The form shows the employee's shifts on those days, so both sides see the impact. | answered |
| 6.6 | What happens to the affected shifts? | The manager can arrange coverage **before or after** approving: **assign** someone directly (eligibility checks and the over-hours warning apply) or **offer** the shift to eligible coworkers (the coverage workflow, started by the manager). On approval, any uncovered shift becomes an **open shift**. | answered |
| 6.7 | Company rules (advance notice, response deadlines, reminders, automatic expiry or denial)? | The basic request-and-approve flow is **core**; these rules arrive in **next** with the other configurable rules. States: pending, approved, denied, cancelled, expired. Automatic actions are audited. | answered |

## Shift coverage and swaps (next tier)

The workflow follows the web proposal: request before the cutoff → coworkers **accept**, **decline**, or **offer a swap** → the requester accepts, declines, or counters a swap → agreed options become **candidates** → the requester sends candidates to the manager (or the system forwards them at a deadline) → the manager approves one or rejects all → the schedule updates and everyone involved is notified. **The original schedule doesn't change until final approval.**

| # | Question | Answer | Status |
|---|---|---|---|
| 6.8 | Who is an eligible coworker? | Someone in the **same department** as the shift; with an **active account** (not deactivated) and not on approved time off that day; with **no overlapping shift**, including a company-set rest gap (e.g. 8 hours). | answered |
| 6.9 | What about weekly hours limits? | **Flag, don't block.** Candidates who would exceed the company's limit are shown with a clear warning; the manager may still choose them; the audit entry records the approval went over the limit. | answered |
| 6.10 | Shift qualifications (e.g. certifications)? | Kept on the list as a future feature (stretch). | answered |
| 6.11 | Who receives a coverage request? | The requester chooses **everyone eligible** or **specific eligible coworkers**. | answered |
| 6.12 | Requests inside the cutoff? | Each company chooses **block** or **require special manager approval**; default: special approval, 24-hour cutoff. | answered |
| 6.13 | How long can swap negotiation go on? | Up to **3 rounds** of counter-offers, and only **before the cutoff**. | answered |
| 6.14 | What happens at the cutoff mid-negotiation? | Unfinished offers expire (both notified); already-agreed candidates are sent to the manager automatically; with none, the request follows the company's late-request rule. | answered |
| 6.15 | What if things change before approval? | Eligibility is **re-checked at approval**, with warnings shown again; the request is cancelled automatically if the original shift changed or was cancelled. | answered |
| 6.16 | Are swaps two-way? | **Yes**: the requester must also be eligible for the coworker's shift. | answered |

## Who approves requests

| # | Question | Answer | Status |
|---|---|---|---|
| 6.17 | Several managers cover one employee: who approves? | A company setting, **required approvals**, per request type (time off, coverage); **default 1**. Every other manager whose scope covers the employee is notified of each review and decision. | answered |
| 6.18 | What if one manager denies? | Proposed: **any denial ends the request**, the cautious choice. | **for Michael and Corbin to discuss** |
| 6.19 | What if more approvals are required than managers exist? | Applies when more than one manager covers the employee: administrators and higher are **notified of the misconfiguration**, and the requirement drops to **all available managers** (e.g. 4 required, 3 managers → 3). If no eligible reviewer exists at all, the request goes to administrators. | answered |
| 6.20 | Can someone review their own request? | **No.** A manager's own time off goes to their managers or administrators. | answered |

## Notifications (next tier)

| # | Question | Answer | Status |
|---|---|---|---|
| 6.21 | Channels? | **In-app**: a bell with an unread count and a list; the page checks every 60 seconds; kept 90 days. Email is stretch. | answered |
| 6.22 | Who gets notified of what? | Administrators choose per event type, starting from sensible defaults. | answered |

## Shift tasks (next tier)

| # | Question | Answer | Status |
|---|---|---|---|
| 6.23 | What is a task? | Title, instructions, department or team, and two switches: **needs verification** and **notes allowed**. | answered; Corbin to review |
| 6.24 | How are tasks assigned? | Three kinds: **to shifts matching a pattern** (e.g. every closing shift); **to a person on a date**; **to whoever is on duty** (the first to complete it closes it). | answered; Corbin to review |
| 6.25 | How do tasks repeat? | One-time, daily, chosen weekdays, weekly, or a monthly date. Upcoming copies are created **7 days ahead**. Managers can add tasks any time, including same-day (**no minimum lead time**). Changing a pattern updates only upcoming unfinished copies. | answered |
| 6.26 | Completing and verifying? | The employee marks it done with an optional note and can undo until it's verified. Verification by any manager whose scope covers it; **nobody verifies their own**. Unfinished at the end of the shift = **missed**, visible to managers. | answered |

Permissions: `task.view_own`, `task.complete`, `task.note`, `task.manage`, `task.assign`, `task.verify`.

## Announcements (next tier)

| # | Question | Answer | Status |
|---|---|---|---|
| 6.27 | Who can see an announcement? | The whole company, or chosen departments or teams, **limited to the author's scope**. | answered |
| 6.28 | Formatting? | **Plain text plus bold only**, no links (links in announcements are a phishing risk); cleaned on display. | answered |
| 6.29 | Read tracking and acknowledgement? | Read tracking for authors and managers. **The author chooses per announcement whether acknowledgement is required** (off by default), with a list of who hasn't acknowledged. | answered |
| 6.30 | Editing and removal? | Author or `announcement.manage` can edit or **archive**; nothing is deleted; edits are audited. Options: important, pinned, optional end date. | answered |

Permissions: `announcement.view`, `announcement.create`, `announcement.manage` (archive replaces the proposal's `announcement.delete`).

## Resulting documents (after approval)

Backend feature pages for schedules, time off, coverage and swaps, tasks, and announcements, and data model changes: `shifts.employee_id` becomes optional with an `open` status, and shifts gain details, notes, and event fields.

Recorded as decision [0029](../../decisions/0029-request-approval-routing.md).
