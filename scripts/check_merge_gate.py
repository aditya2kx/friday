#!/usr/bin/env python3
"""Tier-aware merge gate — Constitution art. 2 + R6.

Tier 0: green CI alone may merge (operator approval not required).
Tier 1/2 (or unparseable tier): operator must have submitted an APPROVED review.

Usage (CI):
  python3 scripts/check_merge_gate.py --body "$PR_BODY" --pr "$PR" --operator aditya2kx

Exit 0 = merge allowed. Exit 1 = blocked.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

TIER_SECTION = re.compile(r"^##\s*1\.\s*Risk tier\s*$", re.IGNORECASE | re.MULTILINE)
TIER_VALUE = re.compile(r"\btier\s*([012])\b", re.IGNORECASE)
OPERATOR = "aditya2kx"


def section_text(body: str, header: re.Pattern[str]) -> str:
    m = header.search(body)
    if not m:
        return ""
    rest = body[m.end() :]
    nxt = re.search(r"^##\s*\d+\.", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def parse_tier(body: str) -> int:
    """Return 0/1/2. Unparseable → 1 (fail closed)."""
    text = section_text(body, TIER_SECTION)
    if not text.strip():
        return 1
    m = TIER_VALUE.search(text)
    if not m:
        return 1
    return int(m.group(1))


def operator_approved(pr: int, operator: str, repo: str) -> bool:
    out = subprocess.run(
        ["gh", "pr", "view", str(pr), "--repo", repo, "--json", "reviews"],
        capture_output=True,
        text=True,
        check=True,
    )
    reviews = json.loads(out.stdout).get("reviews") or []
    return any(
        r.get("author", {}).get("login") == operator and r.get("state") == "APPROVED"
        for r in reviews
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--body", required=True)
    p.add_argument("--pr", type=int, required=True)
    p.add_argument("--operator", default=OPERATOR)
    p.add_argument("--repo", default=None)
    args = p.parse_args()
    repo = args.repo or subprocess.run(
        ["gh", "repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    tier = parse_tier(args.body)
    print(f"merge-gate: tier={tier}")

    if tier == 0:
        print("merge-gate: Tier 0 — operator approval not required")
        return 0

    if operator_approved(args.pr, args.operator, repo):
        print(f"merge-gate: Tier {tier} — operator {args.operator} approved")
        return 0

    print(
        f"merge-gate: BLOCKED — Tier {tier} requires approval from {args.operator}. "
        "Approve the PR to unlock merge.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
