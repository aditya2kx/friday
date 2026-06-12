#!/usr/bin/env python3
"""check_doc_freshness.py - flags code changes that land without their coupled doc.

Constitution art. 5: docs move in lock-step with code.
Couplings map code paths -> doc paths that must change in the same diff.
Per-directory rules: changing skills/<x>/*.py requires touching skills/<x>/SKILL.md;
changing agents/<x>/ requires touching that agent's charter.md or agent.yaml.

Usage: python3 scripts/check_doc_freshness.py --base <ref> [--strict]
Exit 0 = clean (or advisory mode), 1 = violations under --strict.
"""
import argparse
import subprocess
import sys

# (code path prefix, [doc paths - ANY one changing satisfies the coupling])
COUPLINGS = [
    ("core/telemetry.py", ["docs/specs/dx-events.md"]),
    ("core/ports/", ["docs/specs/"]),
    ("core/registry.py", ["docs/specs/agent-manifest.md", "docs/specs/skill-manifest.md"]),
    ("scripts/check_decision_doc.py", [".github/pull_request_template.md", "CONTRIBUTING.md"]),
    (".github/pull_request_template.md", ["scripts/check_decision_doc.py", "CONTRIBUTING.md"]),
]


def changed_files(base: str) -> list[str]:
    out = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        out = subprocess.run(["git", "diff", "--name-only", base],
                             capture_output=True, text=True, check=True)
    return [l.strip() for l in out.stdout.splitlines() if l.strip()]


def violations(changed: list[str]) -> list[str]:
    errs = []
    for prefix, docs in COUPLINGS:
        code_hits = [f for f in changed if f.startswith(prefix) and not f.startswith(tuple(docs))]
        doc_hit = any(f.startswith(d) for f in changed for d in docs)
        if code_hits and not doc_hit:
            errs.append(f"{prefix} changed ({code_hits[0]}…) without touching any of: {', '.join(docs)}")
    for kind, doc_names in (("skills", ["SKILL.md"]), ("agents", ["charter.md", "agent.yaml"])):
        dirs = {f.split("/")[1] for f in changed
                if f.startswith(f"{kind}/") and f.count("/") >= 2 and f.endswith(".py")}
        for d in dirs:
            if not any(f"{kind}/{d}/{doc}" in changed for doc in doc_names):
                errs.append(f"{kind}/{d}/ code changed without touching {' or '.join(doc_names)}")
    return errs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True)
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()
    errs = violations(changed_files(args.base))
    for e in errs:
        print(f"DOC-FRESHNESS: {e}")
    print("doc-freshness: clean" if not errs else f"doc-freshness: {len(errs)} coupling(s) unmet")
    return 1 if (errs and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
