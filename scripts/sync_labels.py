"""Create or update the shared labels in every repository of the organization.

    python scripts/sync_labels.py                      # all repos listed below
    python scripts/sync_labels.py workforce-ops-backend

Uses the GitHub CLI (`gh auth login` first). Existing labels are updated, extra
labels are left alone. labels.yml uses one flow mapping per line, so it is parsed
here without a YAML dependency.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ORG = "workforce-ops-app"
REPOS = [".github", "workforce-ops-backend", "workforce-ops-frontend"]
LINE_RE = re.compile(
    r'^- \{name: "(?P<name>[^"]+)", color: "(?P<color>[0-9a-f]{6})", description: "(?P<desc>[^"]*)"\}$'
)


def load_labels(path: Path) -> list[dict]:
    labels = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        match = LINE_RE.match(line)
        if not match:
            raise SystemExit(f"{path}:{number}: cannot parse label line: {line}")
        labels.append(match.groupdict())
    return labels


def main() -> int:
    labels = load_labels(Path(__file__).resolve().parent.parent / "labels.yml")
    for repo in sys.argv[1:] or REPOS:
        for label in labels:
            subprocess.run(
                [
                    "gh",
                    "label",
                    "create",
                    label["name"],
                    "--repo",
                    f"{ORG}/{repo}",
                    "--color",
                    label["color"],
                    "--description",
                    label["desc"],
                    "--force",
                ],
                check=True,
            )
        print(f"{repo}: {len(labels)} labels synced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
