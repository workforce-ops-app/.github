"""Run the operations listed in a repository's ci.toml and record the results.

The same script runs in GitHub Actions and locally, so a contributor sees the
same checks before pushing that the pull request will see.

    python ../.github/scripts/ci_runner.py              # from a repo root
    python ../.github/scripts/ci_runner.py --only lint  # a single operation

ci.toml format:

    [[setup]]                       # run first, not reported unless they fail
    run = "npm ci"
    requires = ["package-lock.json"]
    local = false                   # locally you manage your own environment

    [[operation]]
    name = "lint"                   # also the bypass label suffix: bypass:lint
    run = "ruff check ."            # {repo} expands to the repository root
    requires = ["pyproject.toml"]   # skipped with a reason if any path is missing
    pass_summary = "0 problems"     # optional; otherwise the last output line
    local = true                    # false = CI only
    timeout_minutes = 15
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import tomllib
from pathlib import Path

NON_BYPASSABLE = {"pr-policy", "secret-scan"}
IN_CI = os.environ.get("GITHUB_ACTIONS") == "true"
MAX_SUMMARY = 90


def _summary_from_output(output: str) -> str:
    for line in reversed(output.splitlines()):
        line = line.strip().strip("=").strip()
        if line:
            return line[:MAX_SUMMARY]
    return ""


def _run(command: str, repo: Path, timeout_minutes: int) -> tuple[int, str, float]:
    command = command.replace("{repo}", str(repo))
    start = time.monotonic()
    if IN_CI:
        print(f"::group::{command}", flush=True)
    try:
        # Commands come from the repository's own ci.toml, reviewed like any other code.
        proc = subprocess.run(  # noqa: S602
            command,
            shell=True,
            cwd=repo,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_minutes * 60,
        )
        code, output = proc.returncode, (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        code, output = 124, f"timed out after {timeout_minutes} minutes"
    print(output, flush=True)
    if IN_CI:
        print("::endgroup::", flush=True)
    return code, output, time.monotonic() - start


def _missing(requires: list[str], repo: Path) -> str | None:
    for path in requires:
        if not (repo / path).exists():
            return path
    return None


def run(config_path: Path, labels: set[str], only: str | None) -> list[dict]:
    repo = config_path.parent.resolve()
    config = tomllib.loads(config_path.read_text(encoding="utf-8"))
    results: list[dict] = []

    for step in config.get("setup", []):
        if _missing(step.get("requires", []), repo) or (not IN_CI and not step.get("local", True)):
            continue
        code, output, elapsed = _run(step["run"], repo, step.get("timeout_minutes", 15))
        if code != 0:
            results.append(
                {
                    "name": "setup",
                    "status": "fail",
                    "time": elapsed,
                    "summary": f"`{step['run']}` failed: {_summary_from_output(output)}",
                }
            )
            return results

    for op in config.get("operation", []):
        name = op["name"]
        if only and name != only:
            continue
        entry = {"name": name, "status": "skip", "summary": "", "time": None}
        missing = _missing(op.get("requires", []), repo)
        if missing:
            entry["summary"] = f"no {missing}"
        elif not IN_CI and not op.get("local", True):
            entry["summary"] = "runs in CI only"
        else:
            code, output, elapsed = _run(op["run"], repo, op.get("timeout_minutes", 15))
            entry["time"] = elapsed
            bypassed = f"bypass:{name}" in labels and name not in NON_BYPASSABLE
            if code == 0:
                entry["status"] = "pass"
                entry["summary"] = op.get("pass_summary") or _summary_from_output(output)
                if bypassed:
                    entry["summary"] += " (bypass label not needed)"
            elif bypassed:
                entry["status"] = "bypassed"
                entry["summary"] = f"failed, bypassed via label: {_summary_from_output(output)}"
            else:
                entry["status"] = "fail"
                entry["summary"] = _summary_from_output(output) or f"exit code {code}"
        results.append(entry)
    return results


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--config", default="ci.toml", type=Path)
    parser.add_argument("--out", default="ci-results/checks.json", type=Path)
    parser.add_argument("--only", help="run a single operation by name")
    args = parser.parse_args()

    labels = set(json.loads(os.environ.get("PR_LABELS") or "[]") or [])
    results = run(args.config, labels, args.only)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    icons = {"pass": "PASS", "fail": "FAIL", "skip": "SKIP", "bypassed": "BYPASS"}
    print("\nOperation            Status  Summary")
    for r in results:
        print(f"{r['name']:<20} {icons[r['status']]:<7} {r['summary']}")
    return 1 if any(r["status"] == "fail" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
