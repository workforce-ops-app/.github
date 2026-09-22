"""Combine CI result files into the markdown report posted on pull requests.

    python ci_report.py --results ci-results --out ci-report/report.md

Exits non-zero when any operation failed, which makes 'ci / overall' the one
status check that branch rules need to require.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

MARKER = "<!-- ci-report -->"
ICONS = {"pass": "✅", "fail": "❌", "skip": "⏭️", "bypassed": "⚠️"}
# pr-policy first, then checks, then anything else in file-name order.
ORDER = {"policy.json": 0, "checks.json": 1}


def _time(seconds: float | None) -> str:
    if seconds is None:
        return "—"
    return f"{seconds:.1f}s" if seconds < 60 else f"{int(seconds // 60)}m {int(seconds % 60)}s"


def _cell(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ")


def build(results_dir: Path, repo: str, sha: str, stack: str, run_url: str) -> tuple[str, bool]:
    files = sorted(results_dir.glob("*.json"), key=lambda p: (ORDER.get(p.name, 9), p.name))
    rows: list[dict] = []
    warnings: list[str] = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            rows.extend(data.get("results", []))
            warnings.extend(data.get("warnings", []))
        else:
            rows.extend(data)

    counts = {status: sum(1 for r in rows if r["status"] == status) for status in ICONS}
    failed = counts["fail"] > 0 or not rows

    lines = [
        MARKER,
        f"### {repo} — CI Report",
        f"`{stack}` · commit `{sha[:7]}`" + (f" · [run log]({run_url})" if run_url else ""),
        "",
        "| Operation | Status | Summary | Time |",
        "|---|:---:|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['name']} | {ICONS[r['status']]} | {_cell(r['summary'])} | {_time(r.get('time'))} |"
        )

    overall = "❌" if failed else "✅"
    tally = f"{counts['pass']} passed · {counts['fail']} failed · {counts['skip']} skipped"
    if counts["bypassed"]:
        tally += f" · {counts['bypassed']} bypassed"
    lines += ["", f"**Overall: {overall} {tally}**"]
    if not rows:
        lines.append("\nNo results were produced; check the run log.")

    if warnings:
        lines += ["", "<details open><summary>⚠️ Warnings</summary>", ""]
        lines += [f"- {w}" for w in warnings]
        lines += ["", "</details>"]
    if counts["bypassed"]:
        lines += [
            "",
            "> A check was bypassed. Bypasses need the teammate's approval and a filled-in "
            "*Bypass justification* in the PR description.",
        ]
    return "\n".join(lines) + "\n", failed


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", default="ci-results", type=Path)
    parser.add_argument("--out", default="ci-report/report.md", type=Path)
    parser.add_argument("--stack", default=os.environ.get("CI_STACK", ""))
    args = parser.parse_args()

    repo = os.environ.get("GITHUB_REPOSITORY", "local").split("/")[-1]
    sha = os.environ.get("REPORT_SHA") or os.environ.get("GITHUB_SHA", "0000000")
    run_url = ""
    if os.environ.get("GITHUB_RUN_ID"):
        run_url = (
            f"{os.environ['GITHUB_SERVER_URL']}/{os.environ['GITHUB_REPOSITORY']}"
            f"/actions/runs/{os.environ['GITHUB_RUN_ID']}"
        )

    report, failed = build(args.results, repo, sha, args.stack, run_url)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(report, encoding="utf-8")

    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(report)
    print(report)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
