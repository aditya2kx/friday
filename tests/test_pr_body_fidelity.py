import importlib.util
import pathlib
import subprocess
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "check_pr_body_fidelity",
    _ROOT / "scripts" / "check_pr_body_fidelity.py",
)
_mod = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_mod)


def test_mentioned_by_basename():
    section = "- `merge-gate.yml` — tier-aware merge lock"
    assert _mod._mentioned(".github/workflows/merge-gate.yml", section)


def test_mentioned_by_full_path():
    section = "Updated `.github/workflows/auto-merge-on-approval.yml`"
    assert _mod._mentioned(".github/workflows/auto-merge-on-approval.yml", section)


def test_missing_file_detected():
    body = "## 3. What changed\n- only one file mentioned\n\n## 4. Test evidence\nx"
    # monkeypatch changed files via check() internals - test _mentioned directly
    assert not _mod._mentioned("scripts/check_merge_gate.py", _mod._section_three(body))


def test_check_passes_when_all_mentioned(tmp_path, monkeypatch):
    body = textwrap_body(
        [
            ".github/workflows/merge-gate.yml",
            "scripts/check_merge_gate.py",
            "CONTRIBUTING.md",
        ]
    )
    monkeypatch.setattr(_mod, "_changed_files", lambda _base: [
        ".github/workflows/merge-gate.yml",
        "scripts/check_merge_gate.py",
        "CONTRIBUTING.md",
    ])
    assert _mod.check(body, "base") == []


def test_check_fails_on_missing(monkeypatch):
    body = textwrap_body([".github/workflows/merge-gate.yml"])
    monkeypatch.setattr(_mod, "_changed_files", lambda _base: [
        ".github/workflows/merge-gate.yml",
        "scripts/check_merge_gate.py",
    ])
    missing = _mod.check(body, "base")
    assert missing == ["scripts/check_merge_gate.py"]


def textwrap_body(paths: list[str]) -> str:
    lines = ["## 3. What changed"]
    for p in paths:
        lines.append(f"- `{p}` — described")
    lines.extend(["", "## 4. Test evidence", "evidence " * 10])
    return "\n".join(lines)
