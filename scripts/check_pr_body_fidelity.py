#!/usr/bin/env python3
"""check_pr_body_fidelity.py — §3 must mention every file changed in the PR.

The decision document is not just a template fill — §3 What changed must
account for each path in the diff so the operator can approve from the
description alone (Constitution art. 3, R5).

Usage (CI):
  python3 scripts/check_pr_body_fidelity.py --body "$PR_BODY" --base "$BASE_SHA"

Exit 0 = every changed file is referenced in §3.
Exit 1 = one or more changed files are missing from §3.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import textwrap

WHAT_CHANGED = re.compile(r"^##\s*3\.\s*What changed", re.IGNORECASE | re.MULTILINE)
NEXT_SECTION = re.compile(r"^##\s*4\.\s*", re.IGNORECASE | re.MULTILINE)
MIN_BASENAME_LEN = 4


def _section_three(body: str) -> str:
    m = WHAT_CHANGED.search(body)
    if not m:
        return ""
    rest = body[m.end() :]
    m2 = NEXT_SECTION.search(rest)
    return rest[: m2.start()] if m2 else rest


def _changed_files(base: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [ln.strip() for ln in out.stdout.splitlines() if ln.strip()]


def _mention_candidates(path: str) -> list[str]:
    parts = path.split("/")
    cands = [path]
    if len(parts) >= 2:
        cands.append("/".join(parts[-2:]))
    cands.append(parts[-1])
    # de-dupe, longest first so we prefer specific matches
    seen: set[str] = set()
    ordered: list[str] = []
    for c in sorted(cands, key=len, reverse=True):
        if c not in seen:
            seen.add(c)
            ordered.append(c)
    return ordered


def _mentioned(path: str, section: str) -> bool:
    hay = section.lower()
    for cand in _mention_candidates(path):
        if len(cand) < MIN_BASENAME_LEN and cand != path:
            continue
        if cand.lower() in hay:
            return True
    return False


def check(body: str, base: str) -> list[str]:
    section = _section_three(body).strip()
    if not section:
        return ["§3 What changed: section heading not found in PR description"]

    files = _changed_files(base)
    if not files:
        return []

    missing = [f for f in files if not _mentioned(f, section)]
    return missing


def main() -> int:
    p = argparse.ArgumentParser(description="Verify §3 mentions every file in the PR diff")
    p.add_argument("--body", required=True)
    p.add_argument("--base", required=True, help="Base ref SHA (PR base commit)")
    args = p.parse_args()

    missing = check(args.body, args.base)
    if missing:
        print("PR body fidelity check FAILED — §3 What changed does not mention:\n")
        for path in missing:
            print(f"  ✗ {path}")
        print(
            textwrap.dedent(f"""
            The PR description must list every changed path in §3 What changed.
            This PR touches {len(missing)} file(s) not referenced in the description.

            Quick fix: gh pr edit <n> --body-file <updated.md>
            Include each path (or an unambiguous basename like merge-gate.yml).
            """).strip()
        )
        return 1

    n = len(_changed_files(args.base))
    print(f"PR body fidelity check PASSED — §3 mentions all {n} changed file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
