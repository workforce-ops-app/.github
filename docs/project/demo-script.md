# Run the midterm demo

- **When to use:** the midterm presentation, and every practice run before it.
- **Who can run it:** either of us, on a laptop with Docker Desktop and both repositories.
- **Last tested:** not yet (draft; the first full run happens once the midterm slices have merged).

## In short
The midterm demo shows one complete feature, schedules, on the security foundation underneath it ([decision 0036](../decisions/0036-midterm-scope-schedules.md)). A manager plans the week and an employee sees their shifts. Then we try three attacks live and show that each fails: reading another company's shift, an employee changing a shift by calling the API directly, and a forged request without the anti-forgery token. Finally we show that every change was written to the audit log. The demo takes about 8 minutes.

**Draft:** steps marked *(fill in when … merges)* depend on slices that are not built yet. The overall order and what each step proves are settled; the exact clicks and names are filled in as the slices land, and checked in the practice runs ([presentation plan](midterm-presentation.md)).

## Before you start

**The day before**
- Pull `main` in both repositories and start from a fresh database (below), so the demo runs on exactly the merged code.
- Do one full practice run with this script.
- Record that practice run as a screen video. It is the fallback if the live demo fails in class.

**Setup (about 5 minutes, before class)**
1. Start Docker Desktop and wait until it says it is running.
2. Backend, from `workforce-ops-backend`:
   ```
   docker compose down --volumes           # start from an empty database
   docker compose up -d --build
   docker compose run --rm api alembic upgrade head
   python -m scripts.seed_demo             # the two demo companies (fill in when O2 merges)
   ```
3. Frontend, from `workforce-ops-frontend`: `docker compose up -d --build` (fill in when F3 merges).
4. Open http://localhost:8080 in the browser. Close every other tab and notification, and zoom the page so the back of the room can read it.
5. Open the browser's developer tools once (F12), on the **Console** tab, and close them again; they are used for the attacks.
6. Have a terminal open in `workforce-ops-backend` for the audit log step.

**Accounts** (fill in when O2 and Z1 merge: names, emails, and the department each belongs to)

| Who | Company | Role | Used for |
|---|---|---|---|
| a manager | Northwind Cafe | Manager, scoped to one department | planning the week; the cross-company attempt |
| an employee in that department | Northwind Cafe | Employee | viewing shifts; the direct API attempt |
| any shift | Summit Outfitters | | its ID is the target of the cross-company attempt |

The demo password comes from the `DEMO_PASSWORD` environment variable (the seed script reads it); it is never written in this script or the repository. Write the Summit shift's ID on your notes before class (fill in the command that prints it when SD1 merges).

**What could go wrong:** Docker not running; a port already in use (8000, 8080, or 3307); an old database volume with different passwords (fixed by `docker compose down --volumes`); the classroom network (everything runs on the laptop, so no network is needed).

## Steps

| # | Do | Say (what it proves) |
|---|---|---|
| 1 | Show the sign-in page at http://localhost:8080 | One address serves the pages and the API through nginx, with strict security headers ([0003](../decisions/0003-same-origin-deployment.md)). |
| 2 | Sign in as the Northwind **manager** | Passwords are hashed with Argon2id; the session is a random token in an `HttpOnly`, `SameSite=Strict` cookie, stored on the server only as a hash. |
| 3 | Open **My shifts**, then the **department week** | The page talks to the API through one client; times show in the workplace's time zone. |
| 4 | In edit mode, add a shift, assign it to the employee, and make another one open | Every change is checked on the server against the manager's permission and scope. |
| 5 | Select 10 or more shifts and reassign or cancel them; show the "This will change N shifts" confirmation | Large changes need the exact count confirmed, so a slip cannot change a whole schedule ([0025](../decisions/0025-sensitive-actions-and-security-settings.md)). |
| 6 | Sign out; sign in as the **employee**. Show My shifts and the week, with no edit buttons | Employees see their own shifts and their department's week, nothing more. |
| 7 | **Attack 1, direct API call.** In the Console, as the employee, try to change a shift through the API (command below). Show the **403** | Hiding the buttons is only a convenience; the server checks every request (rule AZ11). |
| 8 | **Attack 2, forged request.** Send the same kind of change without the anti-forgery token (command below). Show the refusal | Another website cannot make the browser change data on someone's behalf (CSRF, threat S4). |
| 9 | Sign out; sign in as the **manager** again. **Attack 3, another company's data.** Request the Summit shift by its ID (command below). Show the **404** | Company A cannot see company B's data, even with the exact ID, and the answer is the same as for an ID that does not exist, so it reveals nothing ([0016](../decisions/0016-tenant-isolation.md)). |
| 10 | In the terminal, list the newest audit log entries (command below) | Every change from steps 4 and 5 is recorded with who, what, and when, in a signed chain that shows any later tampering ([0018](../decisions/0018-audit-log-chains.md)). |
| 11 | Close: what comes next (time off, administration, coverage and swaps) | The foundation is in place; the next features build on it. |

**Commands for the attacks** (paste into the Console; fill in the final paths and IDs when SC1 and UI1 merge):

```js
// Step 7, as the employee: the app's own API client, so the request is a normal one.
const { api } = await import("/js/api/client.js");
await api.patch("/api/shifts/<employee's department shift ID>", { notes: "changed" });
// Expected: ApiError with status 403 (Forbidden).

// Step 8: the same change sent by hand, without the X-CSRF-Token header.
await fetch("/api/shifts/<shift ID>", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ notes: "forged" }),
}).then((r) => r.status);
// Expected: refused before the permission check (the exact status is set by S3; fill in).

// Step 9, as the Northwind manager: Summit's shift by its exact ID.
await api.get("/api/shifts/<Summit shift ID>");
// Expected: ApiError with status 404 (Not Found), the same as for an ID that does not exist.
```

**Command for the audit log** (from `workforce-ops-backend`; fill in when L1 merges):

```
docker compose exec db mysql -u workforce_app -p workforce_ops -e "SELECT seq, action, target_type, occurred_at FROM audit_events ORDER BY occurred_at DESC LIMIT 10"
```

It asks for the app password from your `.env`; type it, do not show it on screen.

## Verify
- Each step's result matches the "Say" column: shifts appear, the confirmation shows the right count, the attacks answer 403, refused, and 404, and the audit log lists the changes.
- Nothing on screen shows a password, a token, or a stack trace.

## Roll back
- If a step fails live: say what should have happened, switch to the recorded practice video for that step, and continue.
- After the demo, or before the next practice run: `docker compose down --volumes` in both repositories, then repeat the setup.

## Record
After each practice run, note anything that failed or confused as an issue (one per problem), and update this script. Fill in **Last tested** after the full run on a fresh setup.
