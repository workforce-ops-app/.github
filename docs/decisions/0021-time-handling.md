# 0021. Store moments in UTC, schedule in the workplace's time zone

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Exact moments are stored in universal time (UTC). Shifts are scheduled in the time zone of the workplace, and each shift remembers that zone, so daylight-saving changes never move a shift by an hour. Whole days, like a day off, are stored as plain dates.

## Context
Shifts happen at a physical workplace. Companies may have departments in different time zones, and clocks change twice a year. Deadlines such as "at least 24 hours before the shift" must be exact.

## Decision
- **Moments** (created/updated times, shift start and end, deadlines, expirations) are stored in UTC as `DATETIME(6)`. MySQL's `TIMESTAMP` type is avoided because it ends in 2038.
- **Workplace zone:**
  - `companies.timezone`: an IANA zone name such as `America/Chicago` (required)
  - `departments.timezone`: optional override for departments elsewhere
  - `shifts.timezone`: the zone the shift was scheduled in, copied when it is created
- **Calendar dates** (time-off days, holidays) are stored as `DATE` and interpreted in the company's zone (or the department's, if it has one).
- **Deadlines and time gates** are computed and compared in UTC.
- The API sends and receives moments as ISO 8601 with an explicit offset (`2026-09-22T14:00:00Z`) and dates as `YYYY-MM-DD`. The frontend shows shift times in the shift's zone.
- Showing times in each person's own zone is a possible later addition.

## Consequences
- Conversions must happen consistently at the API boundary; the API conventions will spell this out.
- The server and database run in UTC; nothing relies on their local time.

## Alternatives considered
- **Store local times only:** breaks deadline math and daylight-saving transitions.
- **One zone per company only:** does not handle departments in other zones.
