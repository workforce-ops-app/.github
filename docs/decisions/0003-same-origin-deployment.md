# 0003. Serve frontend and API from one origin behind a reverse proxy

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
Even though the frontend and backend are separate projects, users reach both through one web address: pages at `/`, the API at `/api`. This keeps login cookies and cross-site protections simple and strict.

## Context
Separate origins (for example `app.example.com` and `api.example.com`, or different ports) require CORS and cross-site cookies. That weakens session protection (`SameSite` must be relaxed) and makes CSRF defenses harder. It would also be an easy finding in our own security audit.

## Decision
- An nginx reverse proxy (in the frontend image) serves the static frontend and forwards `/api/*` to the FastAPI service.
- Session cookies are `HttpOnly; Secure; SameSite=Strict`.
- No CORS is enabled in production. Local development may run the two on different ports, with the frontend dev setup proxying `/api`.

## Consequences
- Cookies never need to be sent cross-site; CSRF protection remains as defense in depth.
- The frontend's nginx configuration is part of the security surface and is reviewed as such (headers, CSP).
- Deployment must route both through the same host once a hosting target is chosen.

## Alternatives considered
- **Separate origins with CORS:** more moving parts and weaker cookie settings.
- **FastAPI serving the static files:** couples the repositories' deployments together.
