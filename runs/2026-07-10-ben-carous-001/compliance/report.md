# Compliance review — run 2026-07-10-ben-carous-001 (Instagram carousel + caption, DROP exit)

- **Reviewer:** COMPL (SK-B14 co-compliance-review + SK-B15 co-disclosure-management)
- **Date:** 2026-07-10
- **Deliverables reviewed (final-form, post-fact-check + voice):**
  - `voice/drop-carousel-v2.md` (8 slides, on-image text)
  - `voice/caption-v2.md`
- **Ledger:** `factcheck/ledger.yaml` v1 (full pass, blocking summary CLEAR, `high_risk_non_verified: 0`); FACT findings at `factcheck/findings.md`
- **Profile applied:** `projects/benowitz-wealth/compliance.md@1.0.0` (+ `projects/_shared/ria-compliance-envelope.md` via its include), `projects/benowitz-wealth/disclosures.md@1.0.0`
- **Voice-pass integrity input:** `voice/claim-diff.yaml` — 0 semantic-delta hits on both file pairs (tool-sight controls run); zero slide-text edits; all 27 literal claim texts byte-present; CL-28's carrier structure (slide order, fork framing, "still tax-deferred") unchanged.

**Rule-ID citation scheme used below:** `ENV-HL1..HL4` = the envelope's four hard lines; `ENV-SR-*` = envelope standing rules (FEEONLY, FIGURES, TAXLINE, COMPARE, SOFTER); `BEN-C1..C6` = brand rules; `SK-B15` = disclosure selection/placement rules.

## Verdict

**PASS** — no blocked or major findings; 3 minor flags (fix optional, one with a recommended costless fix); named publish-gate conditions attach and must be on the producer checklist at H2; one profile-gap proposal candidate queued below. The human gate (H2) follows; nothing in this report substitutes for it.

## Deterministic tier (the floor, not the review)

| Check | Command | Result |
|---|---|---|
| Compliance lint (carousel) | `python validators/compliance_lint.py runs/2026-07-10-ben-carous-001/voice/drop-carousel-v2.md --project benowitz-wealth` | 0 findings, exit 0 |
| Compliance lint (caption) | `python validators/compliance_lint.py runs/2026-07-10-ben-carous-001/voice/caption-v2.md --project benowitz-wealth` | 0 findings, exit 0 |
| Disclosure check (short-format, tax) | `python .claude/skills/co-disclosure-management/scripts/disclosure_check.py runs/2026-07-10-ben-carous-001/voice/drop-carousel-v2.md --project benowitz-wealth --short-format --tax` | PASS: 0 violations, exit 0 |

## Flags

### FLAG-1 — minor — SHORT-01 record used where the caption could carry the full record (SK-B15 selection; BEN-C1 mapping rows 1/3 boundary)

- **What:** Slide 8 and the caption both close on DISC-BEN-SHORT-01 + DISC-BEN-TAX-01 + "Full disclosures in profile." Nowhere in the deliverable does DISC-BEN-FRS-01 appear in full; it is delegated to the profile.
- **Rationale:** The SHORT fallback is scoped to "genuinely space-constrained formats," with "(Story frame, Reel cover)" as the profile's enumerated examples — a carousel is not enumerated. The **on-image** constraint is real (FRS-01 is ~65 words; the slide legibility budget is ~25 words/slide — it will not fit a final slide legibly, and the disclosure never shrinks, so SHORT-01 on-image is the correct SK-B15 outcome there). The **caption**, however, is not space-constrained: Instagram allows ~2,200 characters and the caption as drafted has ample room for FRS-01 verbatim. All three short-format conditions are met as drafted (SHORT-01 verbatim; full text designated to live in the profile; the deliverable says so explicitly, twice), and the approved parent asset (drop-001 reel, human-approved) carries the same SHORT-01 + profile posture — so this is not adjudicated a violation. It is flagged because the stronger posture is free.
- **Minimal suggested fix (D4 — optional; any text change re-enters at fact_check per D5):** append DISC-BEN-FRS-01 verbatim (with DISC-BEN-TAX-01 already present) at the end of `caption-v2.md`. This removes the piece's dependency on profile state for the full record; publish-gate condition 3 below then shrinks accordingly.
- **Severity basis:** minor — non-affiliation (ENV-HL4) is stated on the piece itself via SHORT-01, on-image and in-caption; the gap is record depth and a runtime dependency, not absence.

### FLAG-2 — minor — termination rule carried by caption only, not on-image (misleading-by-omission check; FACT F5 handoff)

- **What:** The slides alone present the payout fork (Slides 1-7) without the precondition "You must leave FRS-covered work for that balance to pay out." The caption carries it (CL-19, verified, high risk, F-BEN-0003).
- **Adjudication — slides-alone acceptable as drafted, with a named residual:** On-platform, an Instagram carousel never renders without its caption; the unit Wes approves at H2 and the unit the audience receives in feed is slides + caption, and the caption states the rule in its second line (above the fold region). No slide asserts or implies the contrary (nothing on-image suggests the payout coexists with continued FRS employment — Slide 1 opens after the payout event); each slide claim was verified standalone, so the omission subtracts context without creating a false implication. ENV-HL1/BEN-C3 are not triggered by the omission. **Residual risk:** slides travel captionless when screenshotted or re-shared — in that frame the piece teaches the fork without its hard precondition.
- **Minimal suggested fix (optional):** if slide budget allows, add the rule as a kicker line to Slide 3 or 4 (e.g. Slide 4 gains "First, the rule: you must leave FRS-covered work for it to pay out." — 13 words, within the 25-word slide budget). Since Slides 3-4 are byte-inherited claim text, this is an addition, not an edit, but it still re-enters at fact_check (D5) — H2 may prefer to accept the residual instead.

### FLAG-3 — minor — Slide 1 "Most members never hear it called a decision." (BEN-C3 adjacency; ENV-SR-SOFTER; D8)

- **What:** unverified behavioral texture (CL-03, low risk) sitting near the frame the parent run rejected as misleading ("Here's the part nobody mentions" — drop-001 CL-19 adjudication).
- **Adjudication — acceptable:** the sentence describes member experience without an omitting actor; it does not imply FRS (or anyone) conceals anything, so BEN-C3 is not violated and the parent's secrecy-frame adjudication is distinguished, not contradicted. Hedged ("Most"), categorical `unverified` (D8), and byte-identical to text carried in the approved parent asset (drop-001/CL-17). Flagged so H2 inherits the distinction explicitly rather than silently.
- **Fix:** none required.

## Judgment-layer adjudications (no flag)

1. **On-image implications, slide by slide (a sequence can imply what no slide says):**
   - Slides 1-2 (check + decision + "half of that is right"): verified fork setup; no outcome language.
   - Slides 3-4 (pension automatic / lump sum elective): verified pair; symmetric, descriptive.
   - Slide 5 (ordinary income + 20% withholding): verified; the stacking-clause trim makes it strictly narrower than its source (FACT F4), and the caption carries the full clause — no distortion.
   - Slide 6 ("still tax-deferred"): keeps deferred-not-tax-free framing; no "save thousands" outcome language (ENV-HL1 clean; F-BEN-0007 usage-note hard line respected).
   - Slide 7 fork close: "Choose cash… / Choose the rollover…" presents the two routes as considerations, not results; neither route is recommended (ENV-HL3 clean).
   - **Slides 5-7 as a sequence (CL-28, FOUND, verified):** the implied comparative claim — cash taxed in the payout year vs rollover deferred — is exactly what F-BEN-0010 states, comparative in the evidence itself. The comparison does not tip into a performance claim: no dollar figure, no "better," no outcome the firm delivers. Adjudicated compliant.
   - Slide 8: single CTA, free-webinar claim is a publish-gate item, disclosure line present.
2. **ENV-HL2 (testimonials): clean** — no client voices, stories, or endorsements anywhere.
3. **BEN-C2 (solvency fear) / false urgency: clean** — no deadline pressure, no fear framing on either surface.
4. **BEN-C4: clean** — nothing suggests Benowitz can improve the pension itself.
5. **ENV-SR-FEEONLY (DEC-BEN-0001 hold): clean** — "fee-only" appears nowhere. **ENV-SR-FIGURES:** no named public figures. **ENV-SR-COMPARE:** no comparative claims about other advisors.
6. **Qualification carriage: verified intact.** Both adaptations of the qualified parent claim (Slide 7 CL-13; caption CL-23, from drop-001/CL-11 "the timing becomes yours" — deferral-until-withdrawal, NOT unconditional control) carry the qualification as verified-with-qualification, and the voice pass preserved the placement condition both times: each clause sits immediately after its deferral mechanics (the caption beat break was deliberately placed before the couplet, keeping CL-23 adjacent to its mechanics). Placement honors the qualification; it does not discharge it — correctly kept auditable.
7. **On-image vs caption consistency: no contradictions** (FACT F5 concurred) — the caption is a strict superset (adds CL-19 termination rule and CL-22 stacking clause).
8. **Injection scan (D6): clean.** No embedded directives in either deliverable; the provenance/metadata header lines are marker lines, not instruction payloads.

## Required-language table (SK-B15; checked beyond the lint — placement, format, legibility)

| Required record | Where required (carousel rule: final slide + caption; short-format conditions apply) | Present? | Placement as drafted | Verbatim? |
|---|---|---|---|---|
| DISC-BEN-SHORT-01 (short-format minimum) | Final slide + caption | Present, both | Slide 8 closing line; caption closing line | Byte-verbatim vs disclosures.md@1.0.0, both (re-checked this review) |
| DISC-BEN-TAX-01 (tax referral — BEN-C5 / ENV-SR-TAXLINE; TAX CONTENT run) | Rides the disclosure on tax content | Present, both surfaces | Slide 8 line (4th sentence); caption dedicated line | Byte-verbatim, both |
| Explicit statement of where the full disclosure lives (short-format condition) | On the deliverable | Present, both | "Full disclosures in profile." — Slide 8 line and caption closing line | n/a (statement) |
| DISC-BEN-FRS-01 (standard, full) + TAX-01 rider | Profile at publish (short-format relocation) | **Not in the deliverable — delegated to profile** | Profile bio/link at publish time | Publish-gate condition 3; see FLAG-1 for the recommended in-caption carriage |
| Non-affiliation (ENV-HL4) | Every piece | Present | "Not affiliated with FRS." on-image (Slide 8) and in-caption; full BEN-C1 text via profile at publish | Yes (SHORT form on the piece) |

Legibility note for VDIR/production: the Slide 8 disclosure line is 5 sentences (~30 words) sharing the closing slide with the CTA — render it as the persistent bottom block at readable contrast, in safe area; it is on_screen ledger text (CL-16) and must ship exactly as written.

## Publish-gate conditions (hard — producer checklist at H2; none verifiable from the drafts)

1. **Webinar confirmed live and free** before publish (CL-14/CL-24, `unverified` — "free" is an on-image factual claim).
2. **Registration link actually present in the profile** at publish (CL-15/CL-25 — "Register at the link in our profile." is false until it is).
3. **DISC-BEN-FRS-01 with the DISC-BEN-TAX-01 rider actually placed in the profile** at publish and for the life of the post (CL-16/CL-27 qualifications). "Full disclosures in profile." is false — and the short-format disclosure posture broken (SK-B15 / BEN-C1) — until this is done. Adopting FLAG-1's fix moves the full record into the caption and reduces this condition to the profile being merely consistent.
4. Slide and caption text are locked (D5): any wording change at production or publish — including re-typesetting that alters the disclosure line — re-enters at fact_check.

## Proposal candidates (profile gap — routed to proposals, not flagged from vibes)

- **PG-1:** `compliance.md`'s disclosure-mapping row for space-constrained formats enumerates "(Story frame, Reel cover)" only; carousels are covered by SK-B15's placement table ("final slide + caption") but no rule states which *record* a carousel carries — SHORT-01 (on-image constraint is real) or FRS-01-in-caption (caption is not constrained). This run resolved it by precedent (approved drop-001 posture) + judgment. Proposal: add an explicit carousel row (suggested: SHORT-01 on final slide + FRS-01 verbatim in caption; profile pointer then optional).

---

automated and model review only — not regulatory clearance.
