# 0005. Multi-page frontend with plain ES modules and no build step

- **Status:** Accepted
- **Date:** 2026-09-22

## In short
The user interface is a set of ordinary web pages written in HTML, CSS, and plain JavaScript, with no framework. Each page has its own files, and all communication with the server goes through one small layer.

## Context
The proposal specifies HTML/CSS/JavaScript. The team wants modular files, a strong defense against cross-site scripting, and the option to adopt a framework later if the interface outgrows plain JavaScript.

## Decision
```
pages/                 one HTML file per page
css/{base,components,pages}/
js/
├── api/               client.js (credentials, CSRF, errors) + one file per backend module
├── core/              session state, permission-aware UI helpers, safe DOM helpers
├── components/        reusable UI pieces
└── pages/             one entry module per page
```
- No inline `<script>` or `on*=` attributes, so a strict Content Security Policy can be enforced.
- Never assign user data to `innerHTML`; use `textContent` or the helpers in `core/`. Lint rules enforce this.
- Node.js is used only for development tooling (formatting, linting, tests), not in production.

## Consequences
- No bundler to configure or keep updated.
- A very interactive interface may eventually outgrow plain JavaScript. Because every server call goes through `js/api/`, pages could be rebuilt with a framework without touching the backend.

## Alternatives considered
- **A single-page-app framework (React, Vue):** more capability, but adds a build pipeline and moves away from the proposal's stated stack.
