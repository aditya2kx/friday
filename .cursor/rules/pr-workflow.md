---
description: PR lifecycle - load when creating or babysitting a PR
alwaysApply: false
---

# PR Workflow — Mandatory Babysitting

**After creating or pushing to any PR, immediately read and follow the `babysit` skill.**

Do NOT stop at "PR is up at https://…" and hand back to the user.
Do NOT ask whether to babysit — just do it.

## The full lifecycle every time

0. **Check for open PRs first** → `gh pr list --state open`. If a PR from this session is still open, push the new changes to **that** branch instead of opening a second PR. Never have two in-flight PRs from the same session.
1. **Install the cost hook (once per clone/worktree)** → `bash scripts/install-git-hooks.sh`. The `pre-commit` hook captures review cost into BigQuery on each commit. No `git add`, no staged files.
2. **Create PR as the bot** → `gh pr create …` (uses `GH_TOKEN` / bot PAT — **not** `env -u GH_TOKEN`). Operator approves; never author your own PR.
3. **Cost ledger (M1 only)** → deferred. No cost CI gate until M1. WIF + scripts are ready; do not seed or validate cost in M0.1.
4. **Babysit immediately** — read the `babysit` skill and follow it:
   - Resolve merge conflicts (take ours/theirs intelligently; never blindly prefer one side)
   - Wait for CI; fix any failures within this PR's scope
   - Triage review comments (Claude review bot + Adi's comments)
   - Loop until all checks are green and no open blocking comments remain
5. **Arm auto-merge** → Operator approval arms it via `auto-merge-on-approval.yml` (also re-arms when CI finishes or the PR base updates — no laptop `gh pr merge` needed). The agent itself never merges (Constitution art. 2).
6. **Confirm merged** → verify `state == MERGED` before ending the session
7. **Post-merge pull + verify** — after confirmed merged:
   - Pull the working copy to bring the squash commit in.
   - (M1) `pr-cost-finalize.yml` will write `merged_at` + final review cost to BQ.
   - (Grafana dashboard: ported in a later milestone)
   - Spot-check that expected artifacts landed: doc changes appear, nothing was omitted from the squash.
   - Report what SHA landed. Do NOT skip — the main working copy is what Adi reads; leaving it stale is a miss.

## What "babysitting" is NOT

- Changing CI workflow files just to suppress failures
- Making out-of-scope code changes to fix pre-existing issues
- Marking things done without actually verifying CI output

## Reminders

- Cost gate is **M1** — no cost CI in M0.1
- PRs must be authored by `jarvis-agent-bot328`; operator (`aditya2kx`) approves
- Always resolve `CHANGES_REQUESTED` reviews — reply if the concern is already addressed on the branch
