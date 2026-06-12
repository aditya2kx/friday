#!/usr/bin/env python3
"""
check_decision_doc.py — CI gate that fails if the PR description doesn't
satisfy the 9-field decision document in .github/pull_request_template.md.

Usage:
  # In CI (GitHub Actions):
  python3 scripts/check_decision_doc.py --body "$PR_BODY"

  # Locally against a PR:
  python3 scripts/check_decision_doc.py --pr 19

Exit 0 = description is complete.
Exit 1 = one or more required sections are missing or unfilled.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import textwrap

# ---------------------------------------------------------------------------
# Required sections — (section_id, header_regex, min_content_chars, label)
# Content is measured after stripping HTML comments and whitespace.
# ---------------------------------------------------------------------------
REQUIRED_SECTIONS = [
    (
        "risk_tier",
        re.compile(r"^##\s*1\.\s*Risk tier", re.IGNORECASE | re.MULTILINE),
        10,
        "§1 Risk tier",
    ),
    (
        "intent",
        re.compile(r"^##\s*2\.\s*Intent", re.IGNORECASE | re.MULTILINE),
        40,
        "§2 Intent",
    ),
    (
        "what_changed",
        re.compile(r"^##\s*3\.\s*What changed", re.IGNORECASE | re.MULTILINE),
        60,
        "§3 What changed",
    ),
    (
        "test_evidence",
        re.compile(r"^##\s*4\.\s*Test evidence", re.IGNORECASE | re.MULTILINE),
        60,
        "§4 Test evidence",
    ),
    (
        "verification",
        re.compile(r"^##\s*5\.\s*60.second verification", re.IGNORECASE | re.MULTILINE),
        30,
        "§5 Verification recipe",
    ),
    (
        "blast_radius",
        re.compile(r"^##\s*6\.\s*Blast radius", re.IGNORECASE | re.MULTILINE),
        20,
        "§6 Blast radius",
    ),
    (
        "rollout",
        re.compile(r"^##\s*7\.\s*Rollout", re.IGNORECASE | re.MULTILINE),
        20,
        "§7 Rollout & rollback",
    ),
    (
        "cost",
        re.compile(r"^##\s*8\.\s*Cost", re.IGNORECASE | re.MULTILINE),
        10,
        "§8 Cost",
    ),
    (
        "not_verified",
        re.compile(r"^##\s*9\.\s*NOT verified", re.IGNORECASE | re.MULTILINE),
        10,
        "§9 NOT verified",
    ),
]

# Placeholder phrases that count as "not filled in"
PLACEHOLDER_PATTERNS = [
    re.compile(r"<paste real commands \+ real output here>", re.IGNORECASE),
    re.compile(r"<paste commands \+ output here>", re.IGNORECASE),
    re.compile(r"^\s*#\s*TODO", re.IGNORECASE | re.MULTILINE),
    re.compile(r"\[to be filled\]", re.IGNORECASE),
    re.compile(r"\[fill in\]", re.IGNORECASE),
    re.compile(r"^\s*TBD\s*$", re.IGNORECASE | re.MULTILINE),
]


def _strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def _section_content(body: str, header_re: re.Pattern, next_header_re: re.Pattern | None) -> str:
    """Return the text between this section header and the next (or end of body)."""
    m = header_re.search(body)
    if m is None:
        return ""
    start = m.end()
    if next_header_re:
        m2 = next_header_re.search(body, start)
        end = m2.start() if m2 else len(body)
    else:
        end = len(body)
    return body[start:end]


def _check_body(body: str) -> list[str]:
    """Return list of human-readable error strings; empty list means OK."""
    errors: list[str] = []

    for i, (sid, header_re, min_chars, label) in enumerate(REQUIRED_SECTIONS):
        next_re = REQUIRED_SECTIONS[i + 1][1] if i + 1 < len(REQUIRED_SECTIONS) else None

        raw_content = _section_content(body, header_re, next_re)
        if not raw_content:
            errors.append(f"  ✗ {label}: section heading not found in PR description")
            continue

        content = _strip_html_comments(raw_content).strip()

        if len(content) < min_chars:
            errors.append(
                f"  ✗ {label}: section appears empty or too short "
                f"({len(content)} chars, need ≥ {min_chars})"
            )
            continue

        for pat in PLACEHOLDER_PATTERNS:
            if pat.search(content):
                errors.append(f"  ✗ {label}: contains unfilled placeholder text")
                break

    return errors


def _fetch_pr_body(pr_number: int) -> str:
    import json as _json
    result = subprocess.run(
        ["gh", "pr", "view", str(pr_number), "--json", "body"],
        capture_output=True,
        text=True,
        check=True,
    )
    return _json.loads(result.stdout).get("body", "").strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate PR description against the 9-field decision document")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body", help="PR body text (pass ${{ github.event.pull_request.body }} in CI)")
    group.add_argument("--pr", type=int, help="PR number to fetch via gh CLI")
    args = parser.parse_args()

    body = args.body if args.body else _fetch_pr_body(args.pr)

    if not body or not body.strip():
        print("ERROR: PR description is empty.\n", file=sys.stderr)
        _print_reminder()
        return 1

    errors = _check_body(body)
    if errors:
        print("Decision document check FAILED — the following sections are missing or incomplete:\n")
        for e in errors:
            print(e)
        print()
        _print_reminder()
        return 1

    print("Decision document check PASSED — all 9 sections are present and filled.")
    return 0


def _print_reminder():
    print(textwrap.dedent("""
        The PR description must follow the 9-field decision document template in
        .github/pull_request_template.md. The operator reads it to decide
        whether to approve — it must answer, without follow-up questions:

          §1  Risk tier              — Tier 0/1/2 + one line why
          §2  Intent                 — problem, why now, originating issue
          §3  What changed           — grouped by area, every non-obvious decision
          §4  Test evidence          — commands run + actual output (not a plan)
          §5  60-second verification — the one post-merge check that proves it works
          §6  Blast radius           — consumers, breaking changes, schema changes
          §7  Rollout & rollback     — revert-safe? ordering? what to watch
          §8  Cost                   — build cost (ledger) + runtime cost delta
          §9  NOT verified           — the honesty section (write "none" only if true)

        Quick fix: edit the PR description on GitHub to use the template sections,
        or run: gh pr edit <n>  and add all 9 sections.
    """).strip())


if __name__ == "__main__":
    sys.exit(main())
