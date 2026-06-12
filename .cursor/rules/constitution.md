---
description: FRIDAY constitution - hard invariants, always loaded
alwaysApply: true
---
# The FRIDAY Constitution

Read this before planning anything. Each article is absolute; deep links carry detail.

## Process
1. Never push to `main`. Every change is a PR through the gates. No exceptions.
2. Agents never merge. Approval belongs to the operator or a ratified Tier-0 policy (docs/specs/autonomy-tiers.md, lands M5).
3. Every PR body is a complete decision document (.github/pull_request_template.md). Missing fields = failed CI, not a nitpick.
4. Specs are written so a weak model can execute them. STOP on ambiguity is success; log it as a spec_gap event.
5. Docs move in lock-step with code. A doc commit that lags the code is a bug.

## Safety
6. No secrets or PII in git, ever. Secret Manager is canonical; Keychain is acquisition-only.
7. Money math uses Decimal and is Tier-2 forever (human-reviewed, never auto-merged).
8. Never blind-retry an operation that may have fired a side effect. Checkpoint first, verify, then act.
9. Leave a breadcrumb on every failure (evidence + dx_event) before stopping.
10. Cloud reads cloud (Secret Manager, BQ, GCS) — never laptop files in any runtime path.

## Architecture
11. Business logic imports `core/ports/` only — never a vendor SDK directly. Adapters are swappable by config.
12. Judgment lives as high as necessary, capability as low as possible: skills hold zero judgment; sub-agents hold role judgment; agents hold domain judgment; Jarvis routes; the operator owns the irreversible.
13. Do the simplest thing that works. No speculative abstraction; promote to shared only on the second concrete use.
14. Small diffs. Verify, don't trust: claims require evidence (tests, output, screenshots).

## Memory
15. Write it down or it didn't happen: decisions, lessons, and preferences land in files (rules, checkers, tests) in the same cycle — never only in chat. Repetition of operator guidance is a platform bug (R17).
