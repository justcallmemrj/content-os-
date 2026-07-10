# Build Plan — Multi-Agent Content OS

Governing documents: `claude-code-master-prompt.md` (operating rules), `claude-code-slice-prompt.md` (milestone 1 scope, steps 0–6), `phase-8-implementation-package.md` §4 (build sequence). This file tracks: the step we are on, its exit criteria, and what comes next. Updated every session.

## Current step: 3 — Memory seeding (D-079)

**Status:** TRANCHE 1 STAGED — **PR #1 open, awaiting Wes's H6 merge**:
https://github.com/justcallmemrj/content-os-/pull/1 (D-038 decomposition:
envelope + four project scaffolds + BEN/DUC full sets + DEC-BEN-0001; digest is
the PR body). Step 2 PASSED (tag `build-step-2`; DEC-BUILD-005 ratified).

**Remaining for step-3 exit (package §4):** Wes merges ≥1 staging PR (H6);
facts/disclosures/exemplars from the back catalog filed as proposals (tranche 2
— BLOCKED on Wes's source materials); indexes regenerate post-merge;
`benowitz-ducat-social` retirement record at cutover (after step 4).

## Open blockers (require Wes)

1. Merge (or annotate) PR #1 — flag: DUC voice sliders are derived, not ratified.
2. Provide tranche-2 inputs: DROP/FRS source material + 10–20 approved pieces
   per brand (on-machine candidates listed in LOG session 6).
3. GitHub Pro still not visible to the API (403 on rulesets) — check billing;
   ruleset retry queued.
4. Real `git config user.name` value.

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
