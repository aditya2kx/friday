"""Tests for core.registry."""
from core.registry import agents, skills


def test_agents_includes_chanakya():
    names = [a.get("name") for a in agents()]
    assert "chanakya" in names


def test_skills_includes_secrets_sync():
    names = [s.get("name") for s in skills()]
    assert "secrets_sync" in names
