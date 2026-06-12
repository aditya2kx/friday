#!/usr/bin/env python3
"""rules_lint.py - CI gate for .cursor/rules/ hygiene.

Checks:
  1. Every rule file has valid YAML frontmatter with a description.
  2. At most ONE file has alwaysApply: true, and it is constitution.md.
  3. The always-on file is <= 80 lines of body.
Exit 0 = clean, 1 = violations (printed).
"""
import pathlib
import sys

import yaml

RULES = pathlib.Path(__file__).resolve().parents[1] / ".cursor" / "rules"
MAX_ALWAYS_ON_LINES = 80


def parse(fp: pathlib.Path):
    text = fp.read_text()
    if not text.startswith("---"):
        return None, text
    try:
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm), body
    except (ValueError, yaml.YAMLError):
        return None, text


def main() -> int:
    errs = []
    always_on = []
    for fp in sorted(RULES.glob("*.md")):
        fm, body = parse(fp)
        if fm is None:
            errs.append(f"{fp.name}: missing/invalid YAML frontmatter")
            continue
        if not fm.get("description"):
            errs.append(f"{fp.name}: frontmatter missing 'description'")
        if fm.get("alwaysApply") is True:
            always_on.append(fp.name)
            n = len([l for l in body.splitlines() if l.strip()])
            if n > MAX_ALWAYS_ON_LINES:
                errs.append(f"{fp.name}: always-on body is {n} lines (max {MAX_ALWAYS_ON_LINES})")
    if always_on and always_on != ["constitution.md"]:
        errs.append(f"alwaysApply files must be exactly [constitution.md], found {always_on}")
    for e in errs:
        print(f"RULES-LINT FAIL: {e}")
    print("rules-lint: clean" if not errs else f"rules-lint: {len(errs)} violation(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
