# Build Plan — Multi-Agent Content OS

Governing documents: `claude-code-master-prompt.md` (operating rules), `claude-code-slice-prompt.md` (milestone 1 scope, steps 0–6), `phase-8-implementation-package.md` §4 (build sequence). This file tracks: the step we are on, its exit criteria, and what comes next. Updated every session.

## Current step: 1 — Scaffold (tree, schemas, constitution, settings)

**Status:** BUILT — presented at the **[WES] gate** 2026-07-10. Step 0 is CLOSED
(specs verified 7/7 SHA-256, DEC-BUILD-001 resolution; tag `build-step-0`).

**Exit criteria (package §4):** tree matches spec (✓ Phase 7 §3.1 + Phase 3
§5.1); schemas lint (✓ 10 schemas, 46 fixture checks, 0 failures —
`python scripts/test_schemas.py`); constitution reviewed (**pending Wes** —
CLAUDE.md v1.0.0, 98 lines); auto-memory disabled and demonstrated (✓ headless
session produced no MEMORY.md).

## Open blockers (require Wes)

1. Constitution review = the step-1 gate itself.
2. Real GitHub URL + `user.name` (last message carried literal `<MY-USERNAME>`/`<MY NAME>` placeholders) → then `git remote add origin` + push + PR-based flow live.
3. Ratify DEC-BUILD-003 (jsonschema 4.26.0); confirm user-scope gh install is acceptable.
4. Confirm project-slug assumption (ducat-private-wealth / trading-research / founder-brand) and the state/workflow.sqlite commit-vs-ignore proposal (LOG.md session 2, open Qs 4–5).

## Build sequence (package §4)

| Step | Scope | Gate |
|---|---|---|
| 0 | Environment & re-verification — DONE (tag `build-step-0`) | passed 2026-07-10 |
| **1** | **Scaffold: tree, JSON Schemas, CLAUDE.md constitution, settings, auto-memory off — AT GATE** | **[WES]** |
| 2 | Enforcement layer: HK1–HK9, transition.py, schema_validate.py, SQLite DDL | [WES: denial demo] |
| 3 | Memory seeding (proposals-first, D-079); first H6 staging PR | [WES: inputs + merge] |
| 4 | Slice Skills: SK-B2/B3 full; SK-A1–A3, B1, B9, B14, B15 to template | tests green |
| 5 | 13 agent definitions + adherence fixtures | fixtures green |
| 6 | Slice run & acceptance battery (all ten §5 criteria); tag `v1.0-slice` | [WES: sign-off] |
| 7–11 | Out of slice scope (social, video engines, campaign, Ducat activation) | per package §4 |

## Next after this step

Step 2 (enforcement layer): HK1–HK9 hook scripts + deny/allow fixtures each;
`load_context.py`; `transition.py`; index generators; `schema_validate.py`;
SQLite DDL init (Phase 7 §4). Ends at [WES: watch the denial demo]. Starts only
after the constitution passes the step-1 gate.
