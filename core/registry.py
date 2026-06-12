#!/usr/bin/env python3
"""Registry: enumerate agents (agents/*/agent.yaml) and skills (skills/*/SKILL.md).

CLI:  python -m core.registry --list
"""
import argparse
import json
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


def _frontmatter(fp: pathlib.Path) -> dict:
    text = fp.read_text()
    if not text.startswith("---"):
        return {}
    try:
        return yaml.safe_load(text.split("---", 2)[1]) or {}
    except (ValueError, yaml.YAMLError):
        return {}


def agents() -> list[dict]:
    out = []
    for fp in sorted(ROOT.glob("agents/*/agent.yaml")):
        data = yaml.safe_load(fp.read_text()) or {}
        data["_path"] = str(fp.relative_to(ROOT))
        out.append(data)
    return out


def skills() -> list[dict]:
    out = []
    for fp in sorted(ROOT.glob("skills/*/SKILL.md")):
        fm = _frontmatter(fp)
        fm["_path"] = str(fp.relative_to(ROOT))
        out.append(fm)
    return out


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--list", action="store_true")
    args = p.parse_args()
    catalog = {"agents": agents(), "skills": skills()}
    if args.list:
        for a in catalog["agents"]:
            print(f"agent  {a.get('name','?'):12} {a.get('status','')} {a.get('description','')}")
        for s in catalog["skills"]:
            print(f"skill  {s.get('name','?'):12} {s.get('description','')}")
    else:
        print(json.dumps(catalog, indent=2))


if __name__ == "__main__":
    main()
