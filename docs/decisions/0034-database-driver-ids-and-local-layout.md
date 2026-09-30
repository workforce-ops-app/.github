# 0034. Synchronous SQLAlchemy with PyMySQL, `uuid6` for IDs, and the local run layout

- **Status:** Accepted
- **Date:** 2026-09-30

## In short
The backend talks to MySQL through SQLAlchemy in the ordinary, synchronous way, using the PyMySQL driver. Record IDs are made with the small `uuid6` library. On one computer, the backend and the frontend each start with their own Docker Compose file, joined by a shared network so the browser still sees one address.

## Context
[0022](0022-sqlalchemy-and-alembic.md) chose SQLAlchemy and Alembic but left the MySQL driver, and synchronous versus asynchronous access, for when the backend is scaffolded. [0019](0019-uuidv7-ids.md) chose UUIDv7 IDs, which Python 3.13 cannot create on its own. And since nginx lives in the frontend repository and the API in the backend repository ([0002](0002-repository-layout.md), [0003](0003-same-origin-deployment.md)), the two need a way to run together on a developer's computer. The skeleton (Phase 1) needs all three answers.

## Decision
- **Synchronous SQLAlchemy 2.0 with PyMySQL.**
  - Endpoints and repositories are ordinary functions; FastAPI runs them in a thread pool, which serves this application's load comfortably.
  - PyMySQL is written in plain Python, so it installs the same way on Windows, macOS, and Linux, with nothing to compile.
- **`uuid6`** creates UUIDv7 IDs (`uuid6.uuid7()`), stored as `BINARY(16)` as in 0019.
- **Local run layout:**
  - The **backend's** `docker-compose.yml` runs the API (published on port 8000) and MySQL 8.4 (port 3307, next to XAMPP's 3306), and creates a Docker network named `workforce-ops`.
  - The **frontend's** `docker-compose.yml` runs nginx (published on port 8080), joins that network, and forwards `/api/*` to the backend's API service. The browser uses only `http://localhost:8080`, so pages and API share one address, as in production.
  - Each repository still starts on its own; the frontend's `/api` answers only while the backend is running. The frontend's CI smoke test decides in its own pull request whether it starts the backend image or a small stand-in.

## Consequences
- Beginner-friendly: database code reads top to bottom, with no `async`/`await`, and errors show ordinary stack traces in development.
- Many simultaneous slow requests would each hold a worker thread. If the application ever needs far more concurrency, moving to asynchronous sessions and an async driver is a contained change inside the repositories and the database layer.
- PyMySQL is slower than drivers written in C (such as mysqlclient); this application's queries are small, so the difference does not matter.
- `uuid6` becomes a dependency until Python's own `uuid` module can create version 7 IDs; switching then is a one-line change.
- Starting the whole application means two `docker compose up` commands, backend first; the contributor docs say so.

## Alternatives considered
- **Asynchronous SQLAlchemy with aiomysql or asyncmy:** better for very many simultaneous connections, but adds `async` everywhere, harder debugging, and more to learn, for load this application will not have.
- **mysqlclient:** faster, but needs a C compiler or prebuilt packages and is harder to install on Windows.
- **MySQL Connector/Python:** Oracle's official driver; heavier, and less commonly used with SQLAlchemy.
- **Other UUIDv7 libraries (`uuid-utils`, `uuid7`):** fine too; `uuid6` is pure Python, small, and widely used.
- **One combined Compose file in one repository:** one command to start everything, but ties the two repositories together and duplicates the other repository's service definitions.
