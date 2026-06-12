# FRIDAY Requirements (ratified 2026-06-11)

## Capability requirements (testable)

- **R1 — Capture from anywhere:** any idea, in any registered forum (Slack first; ClickUp/email/voice later), becomes a triaged, specced work item in minutes. You never carry a mental backlog.
- **R2 — Clarify, don't spec:** the system asks you targeted questions in-thread; your intent is the spec. You never write tickets.
- **R3 — Fleet at a glance, from a phone:** one surface shows all ~20 in-flight runs — state, cost, what each is doing right now — web + mobile, globally available.
- **R4 — Mid-run steering:** you can read any run's transcript/diff and send it a correction *while it works*, from the phone. Not just observe.
- **R5 — Evidence-first approvals:** every approval request carries proof (tests, sandbox run, reconciliation diff, screenshots, cost) in the summary. Approve from the summary; drill in only when suspicious.
- **R6 — Risk-tiered autonomy:** docs/test/low-risk changes land on green CI alone; money-math/model/deploy changes wait for you. The trust dial is config you widen per area.
- **R7 — Same-day small changes:** idea → deployed for small changes without opening a laptop.
- **R8 — Say it once:** every correction becomes a rule, checker, or test in that same cycle. The same correction never returns; if it does, that's a platform bug.
- **R9 — Self-healing ops:** production failures self-file work items with evidence and usually self-fix; you see escalations and rollback confirmations only.
- **R10 — Interruptible autonomy:** you can grab any in-flight item into a Cursor session, steer it deeply, and hand it back to the fleet. Power-tool work remains a choice, never a requirement.
- **R11 — Spend control:** per-run and monthly token budgets with a hard breaker; cost visible per issue on the existing Grafana dev dashboard.
- **R12 — Voice-first input (Jarvis):** speech is the *primary* input from phone or desk — speak a requirement, a mid-run correction, an approval, a status query; the system answers back. Keyboard becomes optional, used by choice (deep work), never required for the daily loop.
- **R13 — Rich surfaces, not text walls:** progress and inputs render as rich UI — a live fleet board, approval cards with embedded evidence (diffs, screenshots, videos, cost), tappable/speakable decisions — rather than raw text threads.
- **R14 — The PR ritual, on-demand:** whenever you choose to come in, the review queue is ready — you review *descriptions only*, each PR description a complete decision document (contract below). Your comments in the ritual are harvested automatically and demonstrably improve future PRs (a comment that recurs becomes a rule/check; the same comment never needed twice).
- **R15 — Ambient room presence:** in the office, Jarvis is *in the room* — discreet far-field mics (wall/ceiling) with a local wake word ("Hey Jarvis") and room speakers for replies; no device in hand, no app to open. Barge-in supported; nothing streams to the cloud until the wake word fires.
- **R16 — Reachable from any phone, authenticated:** outside, Jarvis is a phone number — callable from *anyone's* phone (borrowed, hotel, car) — but the session itself must be authenticated before Jarvis discloses or does anything. Two factors at call start: something you know/have (spoken TOTP from an authenticator app, or a rotating passphrase) plus passive voice-ID; an unauthenticated caller hears a generic line and nothing else. Sensitive actions stay device-gated regardless.
- **R17 — Self-instrumenting DX (the friction flight recorder):** from day one, the system keeps tabs on its *own* developer experience — every repetition of yours, every manual touch, every "it didn't know my preference" moment is an event. It detects the friction pattern, attributes blame (missing rule? code gap? weak 3p component?), and **auto-files the improvement as a work item** — the platform treats your wasted minutes as production incidents.
