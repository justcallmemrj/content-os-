# Build Plan — Multi-Agent Content OS

Governing documents: `claude-code-master-prompt.md` (operating rules), `claude-code-slice-prompt.md` (milestone 1 scope, steps 0–6), `phase-8-implementation-package.md` §4 (build sequence). This file tracks: the step we are on, its exit criteria, and what comes next. Updated every session.

## MILESTONE 1 COMPLETE — slice ACCEPTED and signed 2026-07-10 (tag v1.0-slice)

All ten §5 criteria met with evidence (`docs/build/slice-acceptance.md`).
H2 exercised live (approved verbatim, edit distance 0 → the north-star
baseline). BUILD-MODE deleted at signature: the main session now runs under
full protected-path enforcement; every merge to main is Wes's.

## Current: step 8 — Video, HyperFrames binding [WES: H5] — BUILT, AT H5

Machinery on branch `build/2026-07-10-step8-video` (PR pending): video machine
V1–V11 (Phase 5 §5 verbatim; child-run chaining at trunk T15 — ASSUMPTION: a
done script run's video production enters as a child run with `parent_run`,
D-047 pattern), storyboard + render-manifest schemas, SK-C1 FULL (upstream
vendored at pin 6152437d/v0.7.49, byte-verified; 8 framework skills in, 13
workflow routers excluded ⚑), SK-B16/B17/C3, RUB-VIDEO-1 + RUB-VIDEO-BUILD-1 ⚑.

**Live run 2026-07-10-ben-dropvid-001: V1→V9 walked, state `human_signoff` —
STOPPED AT H5 (Wes).** Text byte-match 100% (exit criterion met); QA 8.3/10
required 7/7; local render at pin; 9 transitions, 7 envelopes, 1 escalation
(adjudicated). Delivery package: `runs/2026-07-10-ben-dropvid-001/final-package.md`
(8 enumerated H5 flags: placeholder slates, silent, derived tokens ⚑
P-2026-0710-005, font fallbacks, no wordmark, caption L-cut, disclosure
placement, polish notes).

**Exit needs from Wes:** H5 decision on the render · merge the step-8 PR
(ratifies flagged items) · then tag `build-step-8`. V10/V11 (publish →
performance_review) are Wes-side post-H5.

## Previous: step 7 — Social profile + adaptation + calendar [WES] — COMPLETE, PR #11 OPEN

Both social runs H2-approved and locked; RUB-SOCIAL-1 authored. **PR #11 still
awaits Wes's merge click** (verified OPEN this session; the build's delegated
merge was blocked by the permission layer — the click must be Wes's own).
Tag `build-step-7` immediately after it lands. Also open: tranche-3 seeding
(Ducat materials + the three books, from Wes) · MEMC batch for the now-5
queued proposals → H6 · quarterly review cadences begin.

## Previous: step 6 — Slice run & acceptance [WES]

**Status:** READY TO START. Step 5 CLOSED: 13 definitions in .claude/agents/
(D-071 pins exact), adherence fixtures for all 8 slice agents with
deterministic shadows verified, `python scripts/test_agents.py` ALL GREEN
(tag `build-step-5`).

**Step-6 scope (slice prompt):** author remaining fixtures (contamination,
injected-failure, missing-source, minimal compliance seeds) → execute the
LIVE DROP-reel run through every trunk gate to H2 (Wes decides) → the
ten-criterion acceptance battery (package §5) with evidence →
`docs/build/slice-acceptance.md` → Wes signs → tag v1.0-slice. The acceptance
commit also: deletes state/BUILD-MODE (DEC-BUILD-005 sunset), files the
benowitz-ducat-social retirement record, ratifies DEC-BUILD-006.
**Wes must be present for H2 and the sign-off.**

## Previous: step 3 — Memory seeding (D-079)

**Status:** TRANCHE 1 STAGED — **PR #1 open, awaiting Wes's H6 merge**:
https://github.com/justcallmemrj/content-os-/pull/1 (D-038 decomposition:
envelope + four project scaffolds + BEN/DUC full sets + DEC-BEN-0001; digest is
the PR body). Step 2 PASSED (tag `build-step-2`; DEC-BUILD-005 ratified).

**Remaining for step-3 exit (package §4):** Wes merges the staging PRs (H6);
indexes regenerate post-merge; `benowitz-ducat-social` retirement record at
cutover (after step 4). Tranche 2 BUILT (PR #3): BEN facts/sources/exemplars
from the back catalog, sources live-verified. D-068 hosted enforcement LIVE
(ruleset active; direct push rejected in test); DEC-BUILD-006 defines PR
classes (staging = Wes-only, build = self-merge until acceptance).

## Open blockers (require Wes)

1. **Merge PR #1** (scaffolds/envelope; DUC sliders flagged) and **PR #3**
   (BEN evidence + exemplars; review flags in the digest).
2. Tranche-3 inputs: Ducat evidence/exemplars (20-week curriculum, NIL decks),
   the three Benowitz books — none found on this machine.
3. Ratify DEC-BUILD-006 at the next gate.

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
