# Build Plan — Multi-Agent Content OS

Governing documents: `claude-code-master-prompt.md` (operating rules), `claude-code-slice-prompt.md` (milestone 1 scope, steps 0–6), `phase-8-implementation-package.md` §4 (build sequence). This file tracks: the step we are on, its exit criteria, and what comes next. Updated every session.

## Current step: 2 — Enforcement layer

**Status:** BUILT — presented at the **[WES: watch the denial demo] gate**
2026-07-10. Step 1 PASSED (constitution approved verbatim; tag `build-step-1`).
Slugs + SQLite decisions ratified (DEC-BUILD-004).

**Exit criteria (package §4):** every hook fixture green (✓ 32 cases 0 failures,
`python scripts/test_hooks.py`); scripted protected-path write demonstrably
denied (✓ live demo in `docs/build/step2-denial-demo.txt`: compliance.md edit
denied, spec edit denied every-mode, WRITE web fetch denied, direct state write
denied, loader refuses ambiguous project, transition.py sole state writer with
audit rows). **Pending Wes:** watch/acknowledge the demo; ratify DEC-BUILD-005
(build-mode phasing).

## Open blockers (require Wes)

1. Step-2 gate: acknowledge the denial demo; ratify DEC-BUILD-005.
2. GitHub push still queued: `gh auth login` did not stick (no hosts.yml on this
   machine — likely a stale-PATH terminal). Re-run in a NEW terminal; also
   confirm the trailing hyphen in `content-os-` and supply the real user.name.

## Build sequence (package §4)

| Step | Scope | Gate |
|---|---|---|
| 0 | Environment & re-verification — DONE (tag `build-step-0`) | passed 2026-07-10 |
| 1 | Scaffold — DONE (tag `build-step-1`; constitution approved) | passed 2026-07-10 |
| **2** | **Enforcement layer: HK1–HK9, transition.py, loader, schema_validate, DDL — AT GATE** | **[WES: denial demo]** |
| 3 | Memory seeding (proposals-first, D-079); first H6 staging PR | [WES: inputs + merge] |
| 4 | Slice Skills: SK-B2/B3 full; SK-A1–A3, B1, B9, B14, B15 to template | tests green |
| 5 | 13 agent definitions + adherence fixtures | fixtures green |
| 6 | Slice run & acceptance battery (all ten §5 criteria); tag `v1.0-slice` | [WES: sign-off] |
| 7–11 | Out of slice scope (social, video engines, campaign, Ducat activation) | per package §4 |

## Next after this step

Step 3 (memory seeding, D-079): four project profiles + `_shared/` envelope
scaffolded; `benowitz-ducat-social` decomposition per Phase 4 §8; back-catalog
facts/disclosures/exemplars filed as PROPOSALS; first staging PR; Wes merges
(H6). Requires from Wes at its start (slice prompt): the DROP/FRS source
material, 10–20 approved pieces per brand, ~1 hour for the PR review — and a
working GitHub push.
