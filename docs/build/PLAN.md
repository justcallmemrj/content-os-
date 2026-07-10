# Build Plan — Multi-Agent Content OS

Governing documents: `claude-code-master-prompt.md` (operating rules), `claude-code-slice-prompt.md` (milestone 1 scope, steps 0–6), `phase-8-implementation-package.md` §4 (build sequence). This file tracks: the step we are on, its exit criteria, and what comes next. Updated every session.

## Current step: 0 — Environment & re-verification (D-062)

**Status:** IN PROGRESS — environment inspected, doc surfaces re-verified, verification build-note drafted. **BLOCKED at the [WES] gate** on two items (see Open blockers).

**Exit criteria (package §4, verbatim):** Verification build-note filed as a decision record; deps installed **[WES: review note]**.

Slice-prompt refinements: HyperFrames pin *recorded but not built against*; Remotion license check deferred to step 9 and noted as such. Stop for acknowledgment.

## Open blockers (require Wes)

1. **BLOCKER — the seven phase specifications (Phases 1–7) are not on this machine.** The package "ships with" them (§header, §10.2) and every step from 1 onward cites them as the binding source (tree = Phase 7 §3.1, schemas = Phase 3 §4, hooks = Phase 7 §5, Skills = Phase 4 §7, agent cards = Phase 2 §6…). `agents.zip` contained only the package + two prompts. Searched: Downloads (all zips), Documents, home. Deviation memo filed in the step-0 build note. **Nothing past step 0 can be built faithfully without them.**
2. GitHub: private remote `content-os` + branch protection on `main` (package §10.1) — needs Wes's account. Also: `gh` CLI is not installed; proposal to install it is in the build note (needed for the H6 staging-PR flow).

## Build sequence (package §4)

| Step | Scope | Gate |
|---|---|---|
| **0** | **Environment & re-verification — CURRENT** | **[WES: review note]** |
| 1 | Scaffold: tree, JSON Schemas, CLAUDE.md constitution, settings, auto-memory off | [WES] |
| 2 | Enforcement layer: HK1–HK9, transition.py, schema_validate.py, SQLite DDL | [WES: denial demo] |
| 3 | Memory seeding (proposals-first, D-079); first H6 staging PR | [WES: inputs + merge] |
| 4 | Slice Skills: SK-B2/B3 full; SK-A1–A3, B1, B9, B14, B15 to template | tests green |
| 5 | 13 agent definitions + adherence fixtures | fixtures green |
| 6 | Slice run & acceptance battery (all ten §5 criteria); tag `v1.0-slice` | [WES: sign-off] |
| 7–11 | Out of slice scope (social, video engines, campaign, Ducat activation) | per package §4 |

## Next after this step

Step 1 (scaffold) — cannot start until (a) Wes acknowledges the step-0 note and (b) the Phase 1–7 specifications are provided and copied to `docs/architecture/` (then registered as protected paths, D-078).
