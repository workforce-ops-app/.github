# 0035. Logging unexpected errors

- **Status:** Accepted
- **Date:** 2026-10-01

## In short
When something unexpected breaks, the person using the application sees a generic message with a reference number, and the server log records that same number, the kind of error, and where in the code it happened. The log never records the error's own message, because it can contain passwords, database queries, or people's details. Only on a developer's own machine does the log keep the full message and stack trace, so problems can still be debugged.

## Context
[0031](0031-demo-environment-and-data.md) keeps logs to IDs, actions, and errors, with no personal details. But an error's message is written by whatever code failed, so it can carry anything: a database connection string, a SQL statement with submitted values, or an employee's name. The first version of the backend's error handler logged the full message and stack trace, and the web server (uvicorn) also logged them on its own, even when our handler did not. [0034](0034-database-driver-ids-and-local-layout.md) promises ordinary stack traces in development, so the rule needs a clear exception for that.

Found in the review of [workforce-ops-backend#36](https://github.com/workforce-ops-app/workforce-ops-backend/pull/36).

## Decision
- **Response:** an unexpected error answers 500 with the generic problem details from [0026](0026-api-conventions.md) and an `error_id` (a random UUID).
- **Log, outside development** (`APP_ENV` is `test` or `production`): one line with `action: request.failed`, the `error_id`, the error type (for example `RuntimeError`), and the file, line, and function of each step of the stack. Never the message and never the source lines, since a value can be written into either.
- **Log, in development only:** the same line plus the full message and stack trace.
- **Nothing escapes:** the backend catches unexpected errors in its own middleware and does not raise them again, so the web server has nothing to log in full.
- Tests check each of the three environments, and that the secret in a deliberately failing request never reaches the log outside development.

## Consequences
- A user's report can be matched to its log line through the `error_id`.
- Debugging a problem seen in test or production starts from the error type and location only; reproducing it in development gives the full details.
- `APP_ENV` must never be `development` on a shared or production server; the deployment docs say so when they are written.
- Errors that happen after a response has started cannot become a 500; they are still logged the same safe way.

## Alternatives considered
- **Log the full message everywhere, and trust nobody puts secrets in messages:** simplest, but we do not control third-party messages (database drivers include SQL and values), so it would break 0031.
- **Never log full details, even in development:** safest, but makes everyday debugging much harder and breaks the promise in 0034.
- **Scrub messages with patterns (passwords, emails):** easy to get wrong and impossible to make complete; logging only the type and location is reliable.
