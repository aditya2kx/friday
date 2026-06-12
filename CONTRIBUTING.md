# Contributing to FRIDAY

## 1. Branch → PR → gates → operator approval → squash merge

Every change lands via a pull request. Never push directly to `main` (Constitution art. 1).
Agents never merge (Constitution art. 2). Branch naming: `<topic>-<short-description>`.

## 2. The decision document is the review

Fill every field in `.github/pull_request_template.md`. Evidence, not promises.
Missing or empty fields fail CI (`scripts/check_decision_doc.py`). The 9-field
decision document is the mechanism — it captures risk, intent, evidence, and blast radius
so the operator can approve or redirect in one read.

## 3. Cost tracking

Install the pre-commit hook once per clone:

```bash
bash scripts/install-git-hooks.sh
```

Seed the cost ledger after creating a PR:

```bash
python scripts/pr_cost_ledger.py set-meta --pr <N> --branch <branch>
```

Cost ledger lives in BigQuery (`$FRIDAY_PROJECT.friday_dev`). Zero build cost is a hard failure.

## 4. Executor protocol

When executing a milestone spec, follow the executor protocol in `docs/milestones/M0.md` §0.
STOP on ambiguity; log a `spec_gap` event. The spec is the source of truth.
