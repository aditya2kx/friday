# Contributing to FRIDAY

## 1. Branch → PR → gates → operator approval → squash merge

Every change lands via a pull request. Never push directly to `main` (Constitution art. 1).
Agents never merge (Constitution art. 2). Branch naming: `<topic>-<short-description>`.

**PR authorship:** agents open PRs as `jarvis-agent-bot328` (bot PAT). The operator
(`aditya2kx`) reviews and approves — never author your own PR.

**Merge gate (tier-aware):** required CI check `merge-gate` enforces Constitution art. 2.
- **Tier 0** (docs/progress only): merge unlocks when CI is green — no approval required.
- **Tier 1/2**: merge stays blocked until the operator approves. Squash and merge is disabled server-side until `merge-gate` passes.

## 2. The decision document is the review

Fill every field in `.github/pull_request_template.md`. Evidence, not promises.
Missing or empty fields fail CI (`scripts/check_decision_doc.py`). The 9-field
decision document is the mechanism — it captures risk, intent, evidence, and blast radius
so the operator can approve or redirect in one read.

## 3. Cost tracking (M1 — not yet a CI gate)

Cost attribution scripts (`scripts/pr_cost_ledger.py`, `pr_cost_store.py`) and the
pre-commit hook are present for M1. **No cost workflow runs in CI until M1** — do not
add `pr-cost-advisory` or `pr-cost-finalize` checks before the ledger is seeded and
the gate is required.

When M1 lands, install the hook once per clone:

```bash
bash scripts/install-git-hooks.sh
```

## 4. Executor protocol

When executing a milestone spec, follow the executor protocol in `docs/milestones/M0.md` §0.
STOP on ambiguity; log a `spec_gap` event. The spec is the source of truth.
