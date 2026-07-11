# QA notes — run 2026-07-10-ben-dropli-001 — voice/drop-linkedin-v2.md vs RUB-SOCIAL-1

- **Evaluator:** QA (D4-bound; findings, not rewrites)
- **Rubric:** evaluations/rubrics/RUB-SOCIAL-1.md (written anchors only)
- **Inputs read:** factcheck/ledger.yaml v2 · compliance/report.md (trusted, not
  re-litigated) · drafts/first-comment.md · voice/change-log.md ·
  voice/claim-diff.yaml · projects/benowitz-wealth/brand-voice.md@1.0.0 ·
  audience.md#linkedin-referrers · disclosures.md@1.0.0 · voice/exemplars
  VX-BEN-0001..0005 · parent run context (2026-07-10-ben-drop-001,
  parent_artifact_hash per workorder)
- **Date:** 2026-07-10
- **Verdict:** pass · composite 9.4/10 · no required failures · no
  low-confidence scores (all seven dimensions count)

## Required criteria (validators run by QA; chain outputs read, not re-derived)

| # | Result | Evidence |
|---|---|---|
| R1 facts | pass | `ledger_validate.py runs/.../factcheck/ledger.yaml --deliverable runs/.../voice/drop-linkedin-v2.md` → VALID, 0 violations; recomputed `high_risk_non_verified: 0`. All 9 high-risk claims verified or verified-with-qualification (CL-04/07/08/10/12 inherited; CL-24/25/26/27 fresh). Inherited statuses ride on FACT's parent-hash verification (blocking_summary: parent_artifact_hash matches the approved parent artifact byte-for-byte) — read, not re-derived. Non-blocking unverified: CL-20/21 (low texture), CL-22 (medium behavioral), CL-14 (low operational, caught by publish-gate condition 3). |
| R2 visual-copy | pass (n/a) | Pure-text LinkedIn post — no on-image or on-slide surface exists, so the visual-copy validator has nothing to map. Judged pass with note: the format's only "on-screen" text is the post body itself, and the two `on_screen: true` ledger entries (CL-25 disclosure block, CL-26 placement sentence) are byte-presence-enforced in v2 under R1's validator run. No compatibility surface, no compatibility risk. |
| R3 compliance | pass | COMPL verdict **PASS** (0 blocked/major; 2 minor fix-optional flags). `compliance_lint.py --project benowitz-wealth` re-run by QA on v2 → 0 findings, and on drafts/first-comment.md → 0 findings. Trusting COMPL's adjudications per D4 (ENV-HL1..HL4 clean; FLAG-1/FLAG-2 minor). |
| R4 disclosure | pass | LinkedIn placement per SK-B15/BEN-C1: full disclosure in first comment, stated in-post. Both halves verified: (a) `disclosure_check.py drafts/first-comment.md --project benowitz-wealth` (standard mode) → PASS — DISC-BEN-FRS-01 + DISC-BEN-TAX-01 present verbatim; (b) `disclosure_check.py voice/drop-linkedin-v2.md --short-format --tax` → PASS — DISC-BEN-SHORT-01 verbatim in-post, location statement present ("...in the first comment."), TAX-01 rides the post's final line. The un-verifiable half — the comment actually being posted first with the live URL — is COMPL publish-gate condition 1/2 at H2, by design outside draft-QA scope. |
| R5 format | pass | `social_format_check.py --format linkedin` on v2 → PASS, 0 findings (279 words in the 150–300 work-order band; first-comment statement present; no naked link in post). |
| R6 contamination | pass | `lexicon_scan.py --project benowitz-wealth` → 0 foreign-term hits on v2 AND on first-comment.md. No Ducat/TRD/FDR lexicon bleed. |

## Scored dimensions — anchor rationale

**Audience relevance — 5.** The 5-anchor is "names the specific person and the
moment they're in; they can check it against their own life." The post is
addressed to audience.md#linkedin-referrers exactly: the district benefits
coordinator (named, with her moment — the spring knock, the lowered voice, the
door closing), union reps (parking lot), sheriff's office HR (exit paperwork),
CPAs (March, a tax year too late). Each of the four named referrer roles gets a
checkable moment. "The first person an FRS member asks... It's you." turns the
whole piece to face the reader. This is the anchor's text made flesh.

**Originality — 4.** Interpolated. The frame — writing the DROP-exit fork to
the professional beside the member rather than to the member, with "you are the
first person asked" as the thesis — is the 5-anchor's unglamorous specific;
nobody else's feed says "CPAs get it in March, sometimes a tax year too late."
But this is a D-047 adaptation: the middle ~60% (the fork, 20% withholding,
trustee-to-trustee mechanics, deadline-vs-runway) is inherited parent teaching
that is, in isolation, solid-but-familiar rollover education (the 3-anchor).
Fresh frame at 5, inherited core at 3 → 4. This is the adaptation profile's
expected price, not a defect.

**Clarity — 5.** Fold test: LinkedIn truncates around the first two to three
lines. Line one places the reader (coordinator, spring, the knock); line two
hands over the exact question the post answers ("the pension part I understand,
but what happens with the check?"). The idea — members bring YOU this question;
here is the answer to hand them — is fully armed above the fold. The body then
answers in order (rule → pension arm → lump-sum arm → cash cost → rollover
route → foreseeability) with no unexplained jargon for this audience
(DROP/FRS are the readers' own vocabulary per brand-voice; "trustee to
trustee" grounded immediately in "into an IRA or another qualified plan").

**Brand fit — 5.** Deterministic half clean: VOICE's voice_fingerprint PASS
(median 9w / p90 18w / grade 7.0, inside all bands; 0 banned openings, 0
avoided phrases — lexicon_scan corroborates). Preferred moves all present:
specific over general throughout; fragments for emphasis ("The lump sum
doesn't. It waits for your instruction." / "It's you."); says the uncomfortable
part ("The rule is hard: you must leave FRS-covered work"); second person
aimed per the LinkedIn platform_override at the professional beside the
client. Vocabulary compliant: "teachers, deputies, firefighters" — never
"first responders" or "public servant." Reads like the exemplars: register
sits on VX-BEN-0001's LinkedIn variant (same facts, professional register,
closes on the decision) and VX-BEN-0003's accuracy-as-voice posture; the
"Here's the decision, stated plainly" opener is the brand's contracted
"Here's" move (VX-BEN-0002/0003). The parent-adjudicated misleading transition
("nobody mentions") correctly not introduced. Fingerprint-clean AND
exemplar-resemblant — the 5-anchor's conjunction holds.

**Platform fit — 5.** The 5-anchor names this exact case: "LinkedIn to the
professional-beside-the-client." Also native in form: prose paragraphs with a
scan-cadence break at the fork (VOICE's whitespace edit), registration link
kept out of the post body and in the first comment (LinkedIn reach-native),
279 words, no staccato-one-liner habits, no wrong-platform artifacts
(no hashtag stack, no link-in-bio idiom).

**Engagement potential — 5.** The forward has a reason that serves the
*reader*: it is the answer to the question they keep being asked, scoped to
"members close to their DROP date" — forwarding it makes the coordinator
better at the moment the post itself describes. The weigh-in question ("what's
the part of this decision members most often learn last?") asks for the
reader's professional observation, not applause. Zero borrowed urgency — the
piece explicitly de-escalates ("That's the difference between a deadline and
runway"), consistent with the brand's urgency slider pinned at 1. No
engagement-bait patterns.

**CTA quality — 4.** Honest tension, documented: the closing paragraph carries
forward + weigh-in. That dual is brand-voice.md's ratified LinkedIn
cta_pattern **verbatim** ("forward this / weigh in — never book-a-call") and
COMPL adjudicated it compliant; the forward verb is exactly the anchor's
right-verb-for-platform, natural (it closes the loop the hook opened — you're
the one asked; here's what to hand them), and there is no book-a-call and no
pressure framing anywhere. But the rubric's 5-anchor says "one ask," and QA
scores against written anchors, not against the voice profile. Two asks that
are one ratified pattern and zero pressure is above the 3-anchor
("clear but bolted-on" — this is neither) and short of the letter of 5 →
4. The rubric/profile mismatch is filed as a MEMC observation; if the rubric
is clarified to treat a ratified platform pattern as "one ask," this score
would read 5 on the same text.

**Composite:** (5+4+5+5+5+5+4)/7 = 4.71 × 2 = **9.4** (equal weights v1,
normalized to /10).

## Golden comparison

None possible: no goldens exist for the social profile (the rubric itself
records "goldens: none yet for social — the first approved social run becomes
golden-candidate #2"). This is golden-candidate territory — if this run clears
H2, QA proposes it through proposals/queue/ (D-079). Until a social golden and
at least one rejected negative exist, regression detection for this profile
has no baseline; worth noting at manager_review.

## Observations (MEMC-tagged; separate from the verdict)

1. **[MEMC/publish-checklist — HARD riders]** COMPL conditions 1–4 bind at H2:
   (1) the drafted first comment posted as the FIRST comment immediately at
   publish — the in-post sentence "The registration link and our full
   disclosures are in the first comment." is false, and the disclosure posture
   broken, until it is (CL-25/CL-26 qualifications); (2) the
   `[WEBINAR-REGISTRATION-LINK]` placeholder replaced with the live URL before
   posting; (3) webinar confirmed live and free (inherited CL-14, legitimately
   unverified); (4) text locked — any publish-time wording change re-enters at
   fact_check (D5).
2. **[MEMC/rubric-gap]** RUB-SOCIAL-1's CTA 5-anchor ("one ask") cannot be
   satisfied by brand-voice.md's own ratified LinkedIn cta_pattern ("forward
   this / weigh in"), which is dual by design. Every rubric-conformant LinkedIn
   piece for this brand will cap at CTA 4 as written. Candidate rubric
   clarification: define "one ask" as one ratified pattern / one direction of
   action. Flagged, not escalated — the score is stable and verdict-neutral;
   if it starts flipping verdicts, that's the E-path rubric-ambiguity trigger.
3. **[MEMC/adaptation-pattern]** The D-047 child-run economics held: 10
   inherited byte-identical sentences kept FACT to a delta pass (7 fresh + 1
   found claim adjudicated) and VOICE to two cosmetic edits. The measurable
   price appears exactly where expected — originality 4 (inherited familiar
   core) — while the fresh referrer frame does the differentiating work.
4. **[MEMC/pattern — tool-sight control]** VOICE proved the claim_diff zero
   with a planted-change control (twenty→thirty percent → exactly 1 hit)
   instead of assuming the differ saw the file — the drop-001 tool-blindness
   lesson applied unprompted. Keep this pattern.
5. **[verdict-neutral]** COMPL FLAG-1 (CL-22 "almost never" — unverified
   frequency assertion; softer wording suggested) and FLAG-2 (unlabeled
   illustrative hook scene; adjudicated not-a-testimonial) remain open as
   optional items for H2. Adoption of either suggested change re-enters at
   fact_check as a delta (D5). Not QA flags — trusting COMPL's minor/optional
   classification (D4).
