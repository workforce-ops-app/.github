"""Minimal GitHub REST helpers shared by the automation scripts (standard library only)."""

from __future__ import annotations

import json
import os
import urllib.request

MARKER_PREFIX = "<!-- "


def request(method: str, path: str, payload: dict | None = None) -> dict | list | None:
    url = f"{os.environ.get('GITHUB_API_URL', 'https://api.github.com')}{path}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)  # noqa: S310 - fixed https API host
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as response:  # noqa: S310
        body = response.read()
        return json.loads(body) if body else None


def paged(path: str) -> list:
    items: list = []
    page = 1
    sep = "&" if "?" in path else "?"
    while True:
        batch = request("GET", f"{path}{sep}per_page=100&page={page}") or []
        items.extend(batch)
        if len(batch) < 100:
            return items
        page += 1


def upsert_comment(repo: str, number: int, marker: str, body: str) -> None:
    """Create or update the single comment on an issue/PR that carries `marker`."""
    for comment in paged(f"/repos/{repo}/issues/{number}/comments"):
        if marker in (comment.get("body") or ""):
            request("PATCH", f"/repos/{repo}/issues/comments/{comment['id']}", {"body": body})
            return
    request("POST", f"/repos/{repo}/issues/{number}/comments", {"body": body})


def find_comment(repo: str, number: int, marker: str) -> dict | None:
    for comment in paged(f"/repos/{repo}/issues/{number}/comments"):
        if marker in (comment.get("body") or ""):
            return comment
    return None
