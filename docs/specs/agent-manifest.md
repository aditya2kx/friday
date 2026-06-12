# Agent Manifest Spec (`agent.yaml`)

Every agent is declared by an `agent.yaml` file at `agents/<name>/agent.yaml`.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Lowercase identifier (matches directory name) |
| `description` | string | yes | One-sentence purpose |
| `status` | enum | yes | `chartered` \| `active` \| `migrating` \| `retired` |
| `entrypoint` | string or null | yes | Python module path (e.g. `agents.foo.pipeline`) or `null` if not yet implemented |
| `deploy` | object or null | no | `{target, schedule, project}` — Cloud Run target, cron schedule, GCP project |
| `secrets` | list | no | Secret Manager secret names this agent reads |
| `skills` | list | no | Skill names this agent invokes |
| `sub_agents` | list | no | Sub-agent names (if agent orchestrates sub-agents) |
| `notify` | object | no | `{channel}` — Slack channel ref for status updates |

## Status Values

- `chartered` — defined in plan, not yet implemented (sub-agents only have `charter.md`)
- `active` — running in production or fully implemented
- `migrating` — being migrated from legacy system
- `retired` — no longer active

## Example — CHANAKYA (chartered)

```yaml
name: chanakya
description: Product research, market analysis, strategy proposals
status: chartered
entrypoint: null
deploy: null
skills: []
sub_agents: []
```

## Directory Layout Convention

```
agents/<name>/
  agent.yaml       # this manifest
  charter.md       # purpose, skills, naming rationale
  pipeline.py      # entrypoint (when status = active)
  prompts/         # prompt templates
  sub_agents/      # sub-agent definitions
  tests/           # agent-specific tests
  eval/            # eval datasets and harnesses
```
