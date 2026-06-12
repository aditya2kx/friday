# Skill Manifest Spec (`SKILL.md` frontmatter)

Every skill is declared by a `SKILL.md` file at `skills/<name>/SKILL.md`.
The file starts with YAML frontmatter (between `---` delimiters), followed by
the skill body (≤ 50 lines of prose; heavy logic lives in code).

## Frontmatter Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Lowercase identifier (matches directory name) |
| `description` | string | yes | What the skill does + when to use it (one paragraph) |
| `entrypoints` | object | yes | `{python: "skills.x.y:func", cli: "python -m skills.x"}` |
| `credentials` | list | no | Registry names of credentials this skill reads |
| `consumers` | list | no | Agents that use this skill, or `[all]` |

## Body

Prose explanation: context, caveats, usage examples. Keep ≤ 50 lines.
All heavy implementation logic goes in the Python module(s), not the SKILL.md body.

## Example — secrets_sync

```markdown
---
name: secrets_sync
description: Push a secret from macOS Keychain (acquisition) to GCP Secret Manager (canonical). Use when onboarding any new credential so cloud workers can read it.
entrypoints:
  python: "skills.secrets_sync.sync:push"
  cli: "python -m skills.secrets_sync.sync <keychain-service> <sm-secret-name>"
credentials: []
consumers: [all]
---
# secrets_sync
Keychain is acquisition-only; Secret Manager is canonical (Constitution art. 6, 10).
Acquire via operator login + `security add-generic-password`, then push here.
```
