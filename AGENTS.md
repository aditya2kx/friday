# FRIDAY — Start Here

FRIDAY is the autonomous dev platform (operator persona: "Jarvis"). It builds and operates
the domain agents (BHAGA, CHITRA, AKSHAYA, CHANAKYA) and itself, via a 24/7 fleet.

**Read order for any task:** 1) `.cursor/rules/constitution.md` (always loaded), 2) the
relevant `docs/specs/*`, 3) the active milestone spec in `docs/milestones/`.

| You want to… | Read |
|---|---|
| Understand the requirements | `docs/REQUIREMENTS.md` (R1–R17) |
| See the master plan | `docs/milestones/` (one spec per milestone) |
| Add an agent | `docs/specs/agent-manifest.md` |
| Add a skill | `docs/specs/skill-manifest.md` |
| Emit/inspect DX telemetry | `docs/specs/dx-events.md` |
| Open a PR | `CONTRIBUTING.md` + PR template (decision document) |

Migration context: the legacy system lives at `aditya2kx`'s `jarvis` repo and keeps running
production (BHAGA) untouched until M11 cutover. Never modify the legacy repo from here.
