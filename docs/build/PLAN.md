# Build Plan — Multi-Agent Content OS

Governing documents: `claude-code-master-prompt.md` (operating rules), `claude-code-slice-prompt.md` (milestone 1 scope, steps 0–6), `phase-8-implementation-package.md` §4 (build sequence). This file tracks: the step we are on, its exit criteria, and what comes next. Updated every session.

## Current step: 6 — Slice run & acceptance [WES]

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
