# QA notes — run 2026-07-10-ben-carous-001 — voice/drop-carousel-v2.md + voice/caption-v2.md vs RUB-SOCIAL-1

- **Evaluator:** QA (D4-bound; findings, not rewrites)
- **Rubric:** evaluations/rubrics/RUB-SOCIAL-1.md (written anchors only)
- **Unit scored:** the published unit — 8-slide Instagram carousel (on-image
  text) + caption, together
- **Inputs read:** factcheck/ledger.yaml v1 + factcheck/findings.md ·
  compliance/report.md (trusted, not re-litigated) · voice/change-log.md ·
  voice/claim-diff.yaml · drafts/claim-list.yaml context via FACT F1 ·
  projects/benowitz-wealth/brand-voice.md@1.0.0 · audience.md#frs-50plus ·
  disclosures.md@1.0.0 · voice/exemplars VX-BEN-0001..0005 ·
  runs/2026-07-10-ben-cal-001/strategy/calendar.md#row-1 (the brief)
- **Date:** 2026-07-10
- **Verdict:** pass · composite 9.7/10 · no required failures · no
  low-confidence scores (all seven dimensions count)

## Required criteria (validators run by QA; chain outputs read, not re-derived)

| # | Result | Evidence |
|---|---|---|
| R1 facts | pass | `ledger_validate.py runs/.../factcheck/ledger.yaml --deliverable runs/.../voice/drop-carousel-v2.md` → VALID, 0 violations; recomputed `high_risk_non_verified: 0`. 13 high-risk claims all verified or verified-with-qualification. The 4 vwq entries (CL-13, CL-16, CL-23, CL-27) all carry qualification text — including both adaptations of the qualified parent claim drop-001/CL-11 ("the timing becomes yours" = deferral-until-withdrawal, not unconditional control), whose placement condition VOICE preserved (FACT F2, COMPL adjudication 6 — read, not re-derived). 6 unverified claims all low-risk texture/operational (CL-03/04/14/15/24/25). |
| R2 visual-copy | pass | Two halves. **(a) Validator half:** every on-image string is a ledger entry — CL-01..CL-16 are `on_screen: true` wall-to-wall (all 8 slides plus the disclosure line), and the R1 `ledger_validate --deliverable drop-carousel-v2.md` run enforces byte-exact presence of each in the final file (D-016): VALID. **(b) Judgment half, performed by QA on the FINAL files** (FACT F5 found superset on the drafts; VOICE made zero slide-text edits and one caption whitespace edit, but the check was redone here, not inherited): slide-by-slide against caption-v2 — Slide 1 = caption L1 (same fork setup); Slides 3–4 = caption L4–L5 (same automatic/elective pair); Slide 5 ⊂ caption L6 (caption adds the stacking clause — narrower on-image, per FACT F4, no distortion); Slide 6–7 consistent with caption L7 (same deferral + timing framing, qualification wording identical); Slide 8 = caption L9 (same CTA); disclosure lines consistent. Caption additions (L2 date-certain, L3 termination rule) contradict nothing on-image. **Zero contradictions in either direction; the caption is a strict superset.** CL-28's implied comparative (slides 5–7 sequence) rides an unchanged structure per claim-diff. |
| R3 compliance | pass | COMPL verdict **PASS** (0 blocked/major; 3 minor fix-optional flags; 1 profile-gap proposal candidate). `compliance_lint.py --project benowitz-wealth` re-run by QA: drop-carousel-v2.md → 0 findings; caption-v2.md → 0 findings. COMPL's adjudications (ENV-HL1–HL4 clean; CL-28 comparative compliant; FLAG-3 distinguished from the parent secrecy-frame rejection) trusted per D4. |
| R4 disclosure | pass | `disclosure_check.py --project benowitz-wealth --short-format --tax` re-run by QA on both surfaces: carousel-v2 → PASS 0 violations; caption-v2 → PASS 0 violations. DISC-BEN-SHORT-01 byte-verbatim on the final slide AND in the caption; DISC-BEN-TAX-01 byte-verbatim on both (TAX CONTENT run per the work order's prohibited_notes carry-over); the short-format say-where-it-lives condition met on both ("Full disclosures in profile."). The un-verifiable half — DISC-BEN-FRS-01 + TAX-01 rider actually in the profile at publish and for the life of the post — is COMPL publish-gate condition 3 at H2, by design outside draft-QA scope. |
| R5 format | pass | Both checks: `social_format_check.py --format carousel` on drop-carousel-v2.md → PASS, 0 findings (8 slides numbered; body slides one idea ≤25 words; final slide carries CTA + disclosure). `social_format_check.py --format caption` on caption-v2.md → PASS, 0 findings (hook line 16 words, under the 20-word fold rule; disclosure present). |
| R6 contamination | pass | `lexicon_scan.py --project benowitz-wealth` → 0 foreign-term hits on drop-carousel-v2.md AND caption-v2.md. No Ducat/TRD/FDR lexicon bleed. |

## Scored dimensions — anchor rationale

**Audience relevance — 5.** The 5-anchor: "names the specific person and the
moment they're in; they can check it against their own life." Addressed to
frs-50plus in second person at their exact moment: "Your DROP payout arrives
as a single check" — the topic-bank's named territory ("DROP exit…
rollover-vs-check, the year the money lands"). The caption's "If you're in
DROP, it ends on a date you already know" is the anchor's checkable-against-
their-own-life test in its purest form — the reader can literally look up that
date. Not a generic retirement moment; the specific irreversible one this
audience owns.

**Originality — 4.** Interpolated, same reasoning as the sibling run. The
unglamorous specifics are here and strong ("The lump sum doesn't. It waits
for your instruction." / twenty percent withheld / "Most members picture a
payday. Half of that is right.") — nobody else's feed teaches the DROP fork
slide by slide. But this is by design a same-week re-cut of the approved
drop-001 reel for the calendar (row 1: "rides the just-approved DROP reel
run"): the teaching core is inherited brand material, solid-but-familiar
within the brand's own output. Fresh-frame value is lower than the LinkedIn
sibling (no new address, same audience as the parent). 5-grade specifics on a
3-grade repackage premise → 4. The calendar intended exactly this trade.

**Clarity — 5.** Fold test passes on both surfaces: Slide 1 alone carries the
whole idea (check arrives + decision attached), and the caption's first line
(the hook, 16 words) restates it before the fold. One idea per slide
throughout (format-check corroborated); the fork is stated twice (slides 3–4,
then slide 7's choose/choose close) — a swiper who drops out mid-carousel
still leaves with the lesson. No unexplained jargon: DROP/FRS are the
audience's own vocabulary per brand-voice; "trustee to trustee" grounded in
"into an IRA or another qualified plan" on the same slide.

**Brand fit — 5.** Deterministic half: caption voice_fingerprint PASS (median
8w / p90 14w / grade 7.5, all bands; 0 banned openings, 0 avoided phrases —
lexicon corroborates); slide text is the approved parent's claim text at brand
cadence. Preferred moves present: specific over general; fragments for
emphasis ("The lump sum doesn't."); one CTA only; says the uncomfortable part
(the caption states the hard rule: "You must leave FRS-covered work for that
balance to pay out."); second person always. Exemplar resemblance: carousel
sits on VX-BEN-0001 (plain-English definition work, member's-own-words
register) and caption on VX-BEN-0002 (checkable fact → implication without
fear). Disclosure strings never smoothed. Fingerprint-clean AND
exemplar-resemblant — the conjunction holds.

**Platform fit — 5.** The 5-anchor names this exact case: "carousel
one-idea-per-slide" — format-check verified, ≤25 words per body slide, 8-slide
arc with a single-purpose closing slide. Caption is Instagram-native: hook
above the fold, whitespace beat break that Instagram preserves, link routed
via "link in our profile" (no dead in-caption URL), no hashtag spam (none
defined in profile — none used). The two surfaces do platform-correct
different jobs: slides carry the swipe lesson, caption carries the fuller
record.

**Engagement potential — 5.** The save that serves them: a slide-by-slide
reference card for a decision the reader knows the date of — the piece is
useful precisely at the moment they'll go looking for it, which is what makes
saving it rational rather than performative. "Most members picture a payday.
Half of that is right." earns the swipe with information, not withholding.
Zero borrowed urgency (urgency slider 1 honored; no deadline pressure, no
solvency fear — audience guardrails clean per COMPL). No engagement-bait
patterns anywhere.

**CTA quality — 5.** One ask, exactly: "Register at the link in our profile."
(single CTA canon kept — brand one-CTA preferred move; format-check confirms
the final slide carries CTA + disclosure only). Natural: slide 8's "walks
through the whole decision" closes the loop slide 1 opened ("a decision
attached"). Right verb for the platform: registration via profile link is the
Instagram-native route (no in-caption links exist), the ask matches the work
order objective (webinar-registration), the webinar is free and educational,
and there is no book-a-call and no pressure framing. The anchor's
save/forward parenthetical is exemplary, not exhaustive — its target is
pressure verbs and CTA pileup, and this piece has neither.

**Composite:** (5+4+5+5+5+5+5)/7 = 4.86 × 2 = **9.7** (equal weights v1,
normalized to /10).

## Golden comparison

None possible: no goldens for the social profile (rubric: "goldens: none yet
for social — the first approved social run becomes golden-candidate #2").
Golden-candidate territory: this run and 2026-07-10-ben-dropli-001 are both at
qa today; whichever clears H2 first is the natural first social golden, and QA
proposes it through proposals/queue/ (D-079). Note for manager_review: until a
social golden and at least one rejected negative exist, regression detection
for this profile has no baseline.

## Observations (MEMC-tagged; separate from the verdict)

1. **[MEMC/publish-checklist — HARD riders]** COMPL conditions 1–4 bind at H2:
   (1) webinar confirmed live and free (CL-14/CL-24 unverified; "free" is
   on-image text); (2) registration link actually present in the profile at
   publish — "Register at the link in our profile." is false until it is
   (CL-15/CL-25); (3) DISC-BEN-FRS-01 **with the DISC-BEN-TAX-01 rider**
   actually placed in the profile at publish and for the life of the post
   (CL-16/CL-27 qualifications) — "Full disclosures in profile." is false, and
   the short-format posture broken, until done; (4) slide and caption text
   locked (D5) — production re-typesetting that alters the Slide 8 disclosure
   line re-enters at fact_check. Production legibility rider (COMPL → VDIR):
   the Slide 8 disclosure line is on_screen ledger text (CL-16), persistent
   readable bottom block, exactly as written.
2. **[QA judgment on the F5/FLAG-2 handoff — answered as invited, verdict-
   neutral]** Should the carousel carry F-BEN-0003's termination rule
   on-image? As drafted: acceptable. The platform unit is slides + caption;
   the rule sits in the caption's second line (above the fold); no slide
   asserts or implies the contrary, and every slide claim verifies standalone
   — no required criterion is touched, and R2 confirms no contradiction. The
   residual is real: screenshotted or re-shared slides travel captionless and
   then teach the fork without its precondition. COMPL's optional Slide 4
   kicker ("First, the rule: you must leave FRS-covered work for it to pay
   out." — 13 words, inside the 25-word slide budget) is a cheap hardening H2
   may want; as an addition to locked-adjacent text it re-enters at fact_check
   (D5). QA does not block on it: the rubric has no criterion this fails, and
   blocking would be taste, not criteria.
3. **[MEMC/profile-gap — seconding COMPL PG-1]** No rule states which
   disclosure *record* a carousel carries; SHORT-01-everywhere was resolved by
   parent precedent + judgment this run. The on-image constraint is real
   (~65-word FRS-01 cannot render legibly on a slide) but the caption is not
   space-constrained — FLAG-1's fix (FRS-01 verbatim appended to the caption)
   is free and would shrink publish-gate condition 3 to mere profile
   consistency. Supports an explicit carousel row in the compliance mapping.
4. **[MEMC/pattern — tool-sight controls]** VOICE ran planted-change controls
   on BOTH file pairs (twenty→thirty percent; that year's→next year's — one
   hit each) and explicitly checked that "**Slide N:**" lines are inside the
   differ's parse. Two runs in a row now; the drop-001 blindness lesson has
   become standing practice. Keep it.
5. **[verdict-neutral]** COMPL FLAG-3: Slide 1's "Most members never hear it
   called a decision." (CL-03, low, unverified) is *distinguished* from the
   parent-rejected secrecy frame (no omitting actor, no concealment
   implication) — the distinction rides to H2 explicitly. CL-03/CL-04 stay
   categorical unverified (D8). FACT F1 (CC-/CP- declared ids vs the ledger's
   `^CL-\d{2,}$`) is a WRITE process note; ids were normalized with history
   preserved, no content impact.
