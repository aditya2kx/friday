"""Tests for core.telemetry (R17 DX-event instrumentation)."""
import json
import pytest
import core.telemetry as T


def test_row_rejects_bad_source():
    with pytest.raises(AssertionError):
        T._row("test", "bad_source", {}, "actor", None, None, None)


def test_row_rejects_bad_type():
    with pytest.raises(AssertionError):
        T._row("bad_type", "test", {}, "actor", None, None, None)


def test_emit_buffers_when_bq_unreachable(tmp_path, monkeypatch):
    buf = tmp_path / "dx_events_buffer.jsonl"
    monkeypatch.setattr(T, "PROJECT", "no-such-proj-xyz")
    monkeypatch.setattr(T, "BUFFER", buf)
    result = T.emit("test", "test", {"m": "hello"}, actor="test")
    assert result is False
    assert buf.exists()
    lines = buf.read_text().splitlines()
    assert len(lines) == 1


def test_buffered_line_roundtrip(tmp_path, monkeypatch):
    buf = tmp_path / "dx_events_buffer.jsonl"
    monkeypatch.setattr(T, "PROJECT", "no-such-proj-xyz")
    monkeypatch.setattr(T, "BUFFER", buf)
    T.emit("test", "test", {"k": "v"}, actor="x", component="y", run_ref="z", repeat_score=1.0)
    row = json.loads(buf.read_text().splitlines()[0])
    for key in ("ts", "source", "event_type", "actor", "component", "run_ref", "repeat_score", "payload"):
        assert key in row
