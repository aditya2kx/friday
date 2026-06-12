# DX Events Spec (`dx_events` table)

## Schema

Table: `$FRIDAY_BQ_PROJECT.friday_dev.dx_events` (partitioned by `DATE(ts)`)

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `ts` | TIMESTAMP | yes | UTC time of event |
| `source` | STRING | yes | Surface that emitted the event (see vocabulary below) |
| `event_type` | STRING | yes | Type of event (see vocabulary below) |
| `actor` | STRING | no | Who/what caused the event: `operator`, `executor`, or agent/sub-agent name |
| `component` | STRING | no | Port/adapter/agent/skill the event concerns |
| `run_ref` | STRING | no | Issue #, PR #, or run ID when applicable |
| `repeat_score` | FLOAT64 | no | 0–1 friction signal; higher = more repetition |
| `payload` | JSON | no | Arbitrary structured detail (serialized as JSON string) |

## Vocabulary

**VALID_SOURCES** (where the event originated):
- `intake` — Slack/voice/email intake connector
- `triage` — triage agent decisions
- `fleet` — dev worker fleet operations
- `ritual` — the daily PR ritual surface
- `console` — operator CLI/web console
- `voice` — voice session
- `spec` — spec execution (milestone executor)
- `test` — automated tests

**VALID_TYPES** (what happened):
- `repeat_signal` — operator repeated guidance already in the system (platform bug)
- `manual_touch` — human performed a step that should be automated
- `preference_gap` — system lacked a preference and used a default the operator corrected
- `component_health` — health check result for a port/adapter/agent
- `spec_gap` — executor encountered ambiguity not covered by the spec (STOP event)
- `stop` — executor halted per §0 protocol
- `test` — test/smoke event (acceptance checklists, CI verification)

## Buffer / Flush Behavior

If BigQuery is unreachable (laptop offline, auth not configured), events buffer to
`~/.friday/dx_events_buffer.jsonl`. Call `core.telemetry.flush()` to push buffered
events when connectivity is restored.

## Instrumentation Rule

**Every new surface (milestone deliverable) MUST list which events it emits in its
milestone spec's instrumentation section; `rules_lint` extends to enforce this in M7.**
