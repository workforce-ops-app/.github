# Design review 8: Building and running

**In short:** the application uses demo data only. It must work on phones and computers, runs on a laptop for the demos, and keeps logs free of personal details. One catch: showing it on a real phone needs a secure (`https://`) connection to the laptop.

| # | Question | Answer | Status |
|---|---|---|---|
| 8.1 | Real users or demo data? | **Demo data only**, for demos and all testing. No real people's data, so the audit log and security pages can be shown live in class. | answered |
| 8.2 | Which devices? | **Phones and computers.** Employee features (schedule, time off, tasks, announcements, notifications) must work well on a phone; demos may use both. | answered |
| 8.3 | Accessibility and browsers? | WCAG 2.2 level AA (readable contrast, keyboard use, screen-reader labels); current Chrome, Edge, Firefox, and Safari. | answered |
| 8.4 | Look and feel? | Simple and clean; name and logo to be chosen. | open |
| 8.5 | Application logs? | Structured JSON lines with IDs, actions, and errors only, **never personal details or record contents**, so logs are safe for platform staff; kept **30 days**. The detection study reads the security-events table, not these logs. | answered |
| 8.6 | Where does the demo run? | On a **laptop** with Docker Compose; possibly also on a phone. | answered |
| 8.7 | How does a phone reach the laptop? | See below. | **to decide before the midterm** |

## Phone demos and HTTPS

The session cookie (`__Host-session`, [0027](../../decisions/0027-authentication-and-sessions.md)) only works over `https://`. A phone reaching the laptop over Wi-Fi uses plain `http://` by default, so signing in on the phone would fail. The options:

| Option | How | Trade-off |
|---|---|---|
| **Local HTTPS (preferred)** | a tool such as *mkcert* creates a certificate for the laptop; install it once on the phone | a little setup; nothing exposed to the internet |
| Temporary tunnel | e.g. Cloudflare Tunnel gives a public `https://` address during the demo | easy, but the app is briefly reachable from the internet |
| Browser phone view | the laptop browser's device mode | no setup; not a real phone |

Recorded as decision [0031](../../decisions/0031-demo-environment-and-data.md).
