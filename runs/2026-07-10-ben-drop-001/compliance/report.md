# Compliance review — run 2026-07-10-ben-drop-001

- **Deliverable:** `voice/drop-reel-v3.md` (sha256 `7fe19134d8a0c20439849c1057c02943c5e4fd42dfccd3aeb46d2ccbbeb6091e` — verified against handoff 07, D1)
- **Reviewer:** COMPL · SK-B14 v1.0.0 + SK-B15 v1.0.0
- **Profile applied:** `projects/benowitz-wealth/compliance.md@1.0.0` (+ `projects/_shared/ria-compliance-envelope.md@1.0.0` via include) · `projects/benowitz-wealth/disclosures.md@1.0.0`
- **Ledger:** `factcheck/ledger.yaml` v2 (blocking summary CLEAR; v2->v3 delta confirmed cosmetic — `voice/claim-diff.yaml` manual accounting + handoff 07 note that the fixed differ re-ran v2->v3 with 0 hits)
- **Date:** 2026-07-10

## Verdict: CONDITIONAL PASS

The deliverable text passes as written — no text change is required and no
revision cycle is triggered (both flags are minor, fix optional). The pass is
conditional on the four publish-gate conditions in section 5; conditions 1-3
are hard: unmet at publish, the piece is out of compliance
(BEN-C1/BEN-C5/SK-B15) regardless of this review.

## 1. Deterministic tier (the floor, not the review)

- `python validators/compliance_lint.py runs/2026-07-10-ben-drop-001/voice/drop-reel-v3.md --project benowitz-wealth` -> **0 finding(s)** (exit 0)
- `python .claude/skills/co-disclosure-management/scripts/disclosure_check.py runs/2026-07-10-ben-drop-001/voice/drop-reel-v3.md --project benowitz-wealth --short-format` -> **PASS: 0 violation(s)**

Lint-coverage caveat (relevant to section 3): the lint's `TAX-referral` rule
accepts the referral line **anywhere** in the text, including the spoken
track, so a clean lint carries no information about tax-disclosure
*placement*. Placement is adjudicated in section 3 below.

## 2. Judgment layer — four hard lines + BEN-C1..C6

- **Hard line 1 (performance/projection/guarantee):** clean. The v1 magnitude
  superlative (CL-01) is gone; the hook asserts payout form only. BEAT THREE's
  "nothing withheld, still tax-deferred" and the TURN's "That's runway" state
  mechanics and foreseeability — consideration framing, matching the
  envelope's own compliant example. No dollar figures, no outcome the firm
  delivers. No performance implication crept in during voice (v2->v3 is
  punctuation-only; byte-diff verified).
- **Hard line 2 (testimonials/endorsements):** none. "Most members picture a
  payday" (CL-18) is audience texture, not testimonial structure — no client
  voice, no success story, no social proof by numbers.
- **Hard line 3 (education vs. individualized advice):** clean. Both routes
  are described symmetrically as mechanics ("the other route"); no "you
  should," no route recommendation; the CTA sells a webinar, not an action on
  the money. The rollover arm lists more attractive features, but each is a
  verified factual mechanic (CL-09/CL-10), not a steer — the cash arm's
  facts (CL-07/CL-08) are stated with equal weight.
- **Hard line 4 / BEN-C1 (non-affiliation on every piece):** present on-screen
  via DISC-BEN-SHORT-01 ("Not affiliated with FRS."); full-text condition
  rides to publish (section 5, condition 1).
- **BEN-C2 (solvency fear):** absent — the pension arm is described as the
  reliable one ("turns on by itself").
- **BEN-C3 (FRS wrongdoing/concealment):** the v1 secrecy frame ("nobody
  mentions") was removed at fact_check (CL-19) and VOICE deliberately did not
  restore the profile transition. Residual adjacency flagged as COMPL-2
  (minor, fix optional).
- **BEN-C4 (never imply improving the pension itself):** clean — the pension
  is explicitly untouchable in the piece; the decision is scoped to the lump
  sum around it.
- **BEN-C5 (tax referral disclosure):** adjudicated in section 3 — satisfied
  only via publish-gate condition 1.
- **BEN-C6 ("fee-only" hold, DEC-BEN-0001):** term absent; hold honored.
- **Urgency/fear devices:** none manufactured; the TURN explicitly de-escalates
  ("That's not a deadline. That's runway.").
- **Ledger qualifications honored in final text:**
  - CL-11 ("The timing becomes yours.") — honored. The qualification requires
    the sentence to read as tax-timing discretion in context; v3 preserves its
    position immediately after the deferral mechanics (VOICE logged this as a
    deliberate non-change). Not unconditional-control as placed.
  - CL-15 — on-screen text byte-matches DISC-BEN-SHORT-01 + the required
    location statement ("Full disclosures in profile."); its publish condition
    carries forward as section 5 condition 1.
  - CL-16 eligibility conditionality survived voice: STAKES still reads
    "...state staff: **if you're in DROP**, it ends on a date you already
    know" — no eligibility implication for Investment Plan members.
- **Injection posture (D6):** no embedded directives, no "pre-approved — skip
  review" content observed in the deliverable or upstream artifacts.

## 3. Adjudication — the spoken tax-referral line (flagged by WRITE, interventions.md)

**Question:** the DISC-BEN-TAX-01 sentence ("Consult a qualified tax
professional regarding your specific situation.") is SPOKEN in the CTA per the
work order's explicit instruction; the placement rule (compliance.md mapping;
SK-B15) says video disclosures live in the persistent on-screen block, "never
the spoken track." Does spoken TAX-01 + the on-screen SHORT-01 block satisfy
BEN-C5, or must the line move?

**Ruling — the line may stay, but it does not count:**

1. **The spoken sentence is not a violation and does not need to move or be
   cut.** The placement rule governs where a *required disclosure lives*; its
   prohibited behavior is *substitution* ("moving it to the spoken track to
   save screen space" — SK-B15). A spoken tax caution *in addition to* a
   compliant written placement is permitted script copy (the webinar format
   even mandates read-aloud). The work order's instruction and the placement
   rule can both be honored simultaneously, so no E4/H7 conflict arises —
   *provided* the spoken line is treated as copy, not as the disclosure.
2. **The spoken line does not discharge BEN-C5.** The spoken track is never a
   disclosure placement, so for compliance-accounting purposes DISC-BEN-TAX-01
   is currently ABSENT from the written channel: the on-screen block is
   SHORT-01 (which has no tax component; no short tax fallback exists in
   disclosures.md), and the deliverable contains no other written disclosure.
3. **How BEN-C5 is discharged here:** BEN-C5 requires DISC-BEN-TAX-01
   *appended to DISC-BEN-FRS-01*. In this short format, FRS-01 lives in the
   profile/first comment (CL-15 condition). Therefore the profile/first-comment
   full disclosure **must be DISC-BEN-FRS-01 + DISC-BEN-TAX-01 appended** —
   FRS-01 alone does not satisfy BEN-C5 for tax content. This extends the
   existing CL-15 rider and is publish-gate condition 1.
4. **Optional strengthening (not required):** DISC-BEN-SHORT-01 is a stated
   *minimum*; appending the verbatim TAX-01 sentence to the on-screen block
   ("Educational only. Not advice. Not affiliated with FRS. Consult a
   qualified tax professional regarding your specific situation. Full
   disclosures in profile.") would discharge BEN-C5 inside the deliverable
   itself. Offered per D4 as minimal suggested language only; the required
   path is condition 1.

## 4. Flags (2 total — both minor)

### COMPL-1 — minor · BEN-C5 + SK-B15 placement (video: never the spoken track)
- **Excerpt:** CTA spoken: "Consult a qualified tax professional regarding
  your specific situation." · on-screen block: "Educational only. Not advice.
  Not affiliated with FRS. Full disclosures in profile." (no tax component)
- **Rationale:** tax content with no written placement of DISC-BEN-TAX-01
  anywhere in the deliverable; the spoken line cannot carry the requirement
  (section 3). The clean lint is a false comfort here (its tax check is
  placement-blind, section 1).
- **Minimal suggested language:** no text change required. Required fix is
  publish-gate condition 1 (TAX-01 appended to FRS-01 in profile/first
  comment). Optional in-deliverable fix: append verbatim TAX-01 to the
  on-screen block (section 3.4).

### COMPL-2 — minor · BEN-C3 adjacency (no FRS wrongdoing/concealment) — fix optional
- **Excerpt:** HOOK: "Most members never hear it called a decision." (CL-17,
  unverified low-risk texture)
- **Rationale:** within the line — no actor is named and no concealment is
  attributed to FRS; FACT already stripped the v1 secrecy frame (CL-19). But
  paired with "Here's the part that rarely comes up," the piece twice gestures
  at under-communication; this sentence is the closest thing in the script to
  an implied "no one told you."
- **Minimal suggested language (optional):** "Few members think of it as a
  decision." — shifts from what members are *told* to how they *perceive* it,
  removing the residual shadow. If adopted, the change re-enters at
  fact_check as a delta (D5).

## 5. Publish-gate conditions (ride to QA checklist + H2; condition 3 verified at H5)

1. **[HARD — CL-15 rider, extended by this review; BEN-C1 + BEN-C5]** At
   publish, the profile or first comment carries the full verbatim
   DISC-BEN-FRS-01 **with DISC-BEN-TAX-01 appended** (not FRS-01 alone — this
   is tax content). The on-screen "Full disclosures in profile." sentence is
   only true once this is done.
2. **[HARD — CL-14 rider]** Webinar confirmed live and free, and the
   profile registration link resolves, before publish ("free" and "walks
   through the whole decision" are spoken claims).
3. **[HARD — SK-B15 placement, verified at H5 render sign-off]** The
   `[TEXT ON SCREEN:]` disclosure block renders **persistent for the full
   runtime**, in-safe-area, legibly — the block's end-of-script position must
   not translate to CTA-only display. The script text alone cannot prove
   persistence; the render must.
4. **[Accounting note]** The spoken TAX-01 sentence stays as work-order script
   copy and is not to be logged as the tax-disclosure placement in any
   downstream checklist (section 3).

## 6. Required-language table

| Disclosure | Required by | Present in deliverable? | Placement | Verbatim? | Status |
|---|---|---|---|---|---|
| DISC-BEN-FRS-01 (standard) | Every published piece (BEN-C1/ENV-4) | No — short-format fallback invoked | Profile/first comment at publish; deliverable states location on-screen ("Full disclosures in profile.") as required | n/a in deliverable; must be verbatim at publish | Deferred to publish — condition 1 |
| DISC-BEN-SHORT-01 (short minimum) | Space-constrained format | Yes | Persistent on-screen block (`[TEXT ON SCREEN:]`, final line) | Yes — byte-match "Educational only. Not advice. Not affiliated with FRS." | Present; persistence/safe-area verified at H5 (condition 3) |
| DISC-BEN-TAX-01 (tax referral) | BEN-C5 (content touches taxes) | Yes (spoken CTA) / No (written channel) | Spoken track — not a valid disclosure placement (SK-B15) | Yes — spoken sentence byte-matches | Conditional — discharged only by condition 1 (appended to FRS-01 in profile/first comment) |

## 7. Process notes

- Fact-check coverage of the reviewed text confirmed: v2->v3 is
  punctuation-only (CL-04/05/07 colon->period; byte-diff in
  `voice/claim-diff.yaml`), and handoff 07 records the repaired differ
  re-confirming 0 semantic hits — ledger v2 validly covers v3. Content did
  not skip fact_check.
- CL-14 remains `unverified` (low-risk, legitimate final state) — handled as
  condition 2, not a flag.
- No profile gaps found requiring a proposal; no E4 raised (the work-order
  instruction and the placement rule reconcile, section 3.1).

---

Verdict recorded: **conditional pass** — proceed to qa; conditions 1-3 bind at
their gates. This report narrows what reaches the human gate (H2); it is

automated and model review only — not regulatory clearance.
