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
