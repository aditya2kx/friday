"""DX-event telemetry (R17). One emit() for every surface.

Events go to BigQuery ($FRIDAY_BQ_PROJECT.friday_dev.dx_events). If BQ is
unreachable (offline laptop), events buffer to ~/.friday/dx_events_buffer.jsonl
and flush() pushes them later. Schema: docs/specs/dx-events.md.
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib

PROJECT = os.environ.get("FRIDAY_BQ_PROJECT", "friday-prod-7401")
DATASET = os.environ.get("FRIDAY_BQ_DATASET", "friday_dev")
TABLE = "dx_events"
BUFFER = pathlib.Path.home() / ".friday" / "dx_events_buffer.jsonl"

VALID_SOURCES = {"intake", "triage", "fleet", "ritual", "console", "voice", "spec", "test"}
VALID_TYPES = {"repeat_signal", "manual_touch", "preference_gap", "component_health",
               "spec_gap", "stop", "test"}


def _row(event_type, source, payload, actor, component, run_ref, repeat_score):
    assert source in VALID_SOURCES, f"bad source {source}"
    assert event_type in VALID_TYPES, f"bad event_type {event_type}"
    return {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "source": source, "event_type": event_type, "actor": actor,
        "component": component, "run_ref": run_ref, "repeat_score": repeat_score,
        "payload": json.dumps(payload or {}),
    }


def emit(event_type: str, source: str, payload: dict | None = None, *,
         actor: str = "system", component: str | None = None,
         run_ref: str | None = None, repeat_score: float | None = None) -> bool:
    """Returns True if written to BQ, False if buffered locally."""
    row = _row(event_type, source, payload, actor, component, run_ref, repeat_score)
    try:
        from google.cloud import bigquery
        errors = bigquery.Client(project=PROJECT).insert_rows_json(
            f"{PROJECT}.{DATASET}.{TABLE}", [row])
        if errors:
            raise RuntimeError(errors)
        return True
    except Exception:
        BUFFER.parent.mkdir(parents=True, exist_ok=True)
        with BUFFER.open("a") as f:
            f.write(json.dumps(row) + "\n")
        return False


def flush() -> int:
    """Push buffered events to BQ. Returns count flushed."""
    if not BUFFER.exists():
        return 0
    from google.cloud import bigquery
    rows = [json.loads(l) for l in BUFFER.read_text().splitlines() if l.strip()]
    if not rows:
        return 0
    errors = bigquery.Client(project=PROJECT).insert_rows_json(
        f"{PROJECT}.{DATASET}.{TABLE}", rows)
    if errors:
        raise RuntimeError(f"flush failed: {errors}")
    BUFFER.unlink()
    return len(rows)
