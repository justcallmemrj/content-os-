# QA notes — run 2026-07-10-ben-drop-001 — voice/drop-reel-v3.md vs RUB-SCRIPT-1

- **Evaluator:** QA (D4-bound; findings, not rewrites)
- **Rubric:** evaluations/rubrics/RUB-SCRIPT-1.md (anchors, not intuition)
- **Inputs read:** factcheck/ledger.yaml v2 · compliance/report.md (trusted, not
  re-litigated) · projects/benowitz-wealth/brand-voice.md@1.0.0 ·
  voice/exemplars/VX-BEN-0001..0005 · projects/benowitz-wealth/audience.md ·
  drafts/hooks.md · research/RP-2026-0710-01.yaml (source tiers/windows)
- **Date:** 2026-07-10
- **Verdict:** pass · composite 9.6/10 · no required failures · no
  low-confidence scores (all nine dimensions count)

## Required criteria (validators run by QA; chain outputs read, not re-derived)

| # | Result | Evidence |
|---|---|---|
| R1 facts | pass | `ledger_validate.py ... --deliverable voice/drop-reel-v3.md` → VALID, 0 violations. Ledger v2 nominally targets drafts/drop-reel-v2.md; the validator run against v3 confirms coverage holds (v2→v3 punctuation-only per handoff 07 / voice/claim-diff.yaml, per COMPL §7). blocking_summary CLEAR: high_risk_non_verified 0; all 8 high-risk claims verified or verified-with-qualification; CL-15 on_screen byte-presence intact in v3. |
| R2 compliance | pass | COMPL verdict CONDITIONAL PASS — the text passes as written; both flags minor/fix-optional; no revision cycle triggered. `compliance_lint.py` re-run by QA → 0 findings. The conditions are publish-gate riders (see observations), not text failures — trusting the chain per D4. |
| R3 duration | pass | `duration_check.py` → PASS, 197 spoken words in band 170–200 (reel-90s), ~93s est. Top of band — noted as a constraint on any future spoken additions. |
| R4 disclosure | pass | `disclosure_check.py --short-format` → PASS, 0 violations. DISC-BEN-SHORT-01 byte-matched on-screen + required location statement. Persistence/safe-area is an H5 render check (COMPL condition 3), out of script-QA scope by design. |
| R5 structure | pass | `structure_check.py` → PASS, 0 findings. Beats present (HOOK/STAKES/BEAT×3/TURN/CTA), markers on every block, single CTA. |
| R6 contamination | pass | `lexicon_scan.py --project benowitz-wealth` → 0 foreign-term hits. |

## Scored dimensions — anchor rationale

**Hook — 4.** Above the 3-anchor ("clear topic entry, but generic"): second
person, names the specific stake (your DROP payout; a decision attached), quiet
mechanism, no borrowed urgency, no question, no banned opening. Short of the
5-anchor because the fact-check reframe (CL-01: magnitude superlative removed,
form-only claim kept) leaves sentence one stating something the member already
knows ("arrives as a single check"); the actual grab is deferred to sentence
three ("never hear it called a decision"). The hook now takes three sentences
to arm rather than earning the next five seconds on its first. Compare
drafts/hooks.md #1 (the v1 parent, killed on evidence) — the tradeoff was
correct, and it cost exactly this point.

**Clarity — 5.** A distracted first-time viewer can restate the lesson in one
sentence: "the DROP lump sum doesn't move itself — cash is taxed that year
with 20% withheld, a rollover stays tax-deferred, and you pick." The fork is
stated twice (beats two/three, then the turn). No unexplained jargon for this
audience (DROP/FRS are their words per brand-voice vocabulary); "trustee to
trustee" is immediately grounded ("into an IRA or another qualified plan").

**Logical flow — 5.** Each beat necessitates the next: decision exists (HOOK)
→ forced, foreseeable timing (STAKES) → automatic arm vs. waiting arm (BEAT
ONE) → cash arm cost (BEAT TWO) → rollover arm mechanics (BEAT THREE) → the
turn genuinely reframes: deadline-anxiety inverted into "runway"
(foreseeability as an asset). Beats cannot shuffle without damage — the fork
requires the split, the split requires the stakes. The TURN's first sentence
briefly restates CL-12, but as setup for the reframe, not as the reframe.

**Educational value — 5.** Teaches what the reader actually doesn't know
(audience.md topic bank: "rollover-vs-check, the year the money lands"), with
checkable specifics throughout: mandatory 20% federal withholding on direct
payouts (CL-08), ordinary-income stacking in the distribution year (CL-07),
trustee-to-trustee mechanics (CL-10), foreseeable tax year (CL-13). No
platitudes; honors the packet's uncertainty boundary (no member-specific
figures, no quantified tax cost).

**Personal voice — 5.** Zero avoided-phrase hits (checked against
brand-voice.md list; lexicon scan corroborates 0). Zero banned openings. All
five preferred moves present: specific over general; fragments for emphasis
("The lump sum doesn't." / "That's runway."); one CTA; says the uncomfortable
part ("The rule is hard. You must leave FRS-covered work"); second person
throughout. Vocabulary compliant: "teachers, deputies, firefighters" — never
"first responders" or "public servant"; members are *in DROP*. Signature
transition "But that's not the real question." used verbatim at the TURN.
Register matches VX-BEN-0004's spoken-teaching target (plain-English
translation + one concrete picture — the envelope, "turns on by itself,"
"waits for your instruction") and VX-BEN-0005's consideration-not-steer
posture on the two routes. Resemblance ≥4 comfortably. One noted dilution:
the second signature transition appears as the compliance-softened "Here's the
part that rarely comes up" (CL-19 fix) rather than the ratified "nobody
mentions" wording — deliberate, documented, and not AI-warm homogenization;
does not drop the score.

**Spoken cadence — 4.** Mostly natural breaths — short sentences and fragments
place pauses after claims, and the v2→v3 pass (colons→periods on CL-04/05/07)
was itself a cadence repair. Two spots still need a breath the text doesn't
mark: the CL-10 run ("The money moves trustee to trustee ... nothing withheld,
still tax-deferred" — ~19 words with two trailing fragments) and the STAKES
occupational list + conditional. That is squarely the 3-anchor's "two or three
spots" territory but with the rest of the script above the 5-anchor →
interpolate to 4. Producer note: direct the pauses at the commas; no text
change required (and none proposed — D4).

**Platform fit — 5.** Reel consumption pattern honored: hook lands inside
0:00–0:05 with timestamps on every block; ~20s beats; B-roll direction where
attention dips (BEAT ONE); CTA form matches brand cta_patterns for reels
("single ask, spoken" — "Register at the link in our profile"); persistent
on-screen text block for disclosure rather than spoken-track substitution;
197 words/~93s inside the reel-90s canon band. No essay pacing, no
wrong-format habits.

**CTA quality — 5.** One ask (register). Natural exit from the turn: "runway"
→ the webinar as how you use it, and "walks through the whole decision" closes
the loop opened by the hook's "decision attached." Zero pressure or urgency
language (the TURN explicitly de-escalates: "That's not a deadline."). The
trailing tax-referral sentence is required work-order copy, not a second ask
(COMPL §3 accounting honored — it is script copy, not the disclosure).

**Source quality — 5.** Every material (high-risk) claim traces through the
ledger to RP-2026-0710-01 c1–c5, all tier 1: Florida Statutes §121.091
(S-BEN-0001) and IRS rollovers publication (S-BEN-0002), basis: direct,
confidence: high. Time-sensitive facts all inside review windows (review_by
2027-07-01/2027-07-10 vs. access 2026-07-10). The only unverified claims
(CL-14/17/18/19) are low-risk texture or operational items whose legitimate
final state is unverified — none material, and CL-14 is caught by publish-gate
condition 2.

**Composite:** (4+5+5+5+5+4+5+5+5)/9 = 4.78 × 2 = **9.6** (equal weights v1).

## Golden comparison

No goldens exist for the script profile — `evaluations/goldens/` contains only
scaffold. No nearest-golden citation or delta narrative is possible. **This
run is golden-candidate #1**: if it clears H2, QA proposes it as the first
script-profile golden through proposals/queue/ (D-079 path). Until a golden
and at least one rejected negative exist, regression detection for this
profile has no baseline — worth noting at manager_review.

## Observations (MEMC-tagged; separate from the verdict)

1. **[MEMC/publish-checklist — HARD riders]** COMPL conditions 1–3 bind at
   their gates: (1) profile/first comment = verbatim DISC-BEN-FRS-01 **with
   DISC-BEN-TAX-01 appended** (FRS-01 alone fails BEN-C5 for tax content);
   (2) webinar live + free + link resolves (CL-14); (3) on-screen block
   persistent full-runtime, verified at H5. Condition 4 (accounting): the
   spoken TAX-01 sentence is script copy, never logged as the tax-disclosure
   placement.
2. **[MEMC/validator-gap]** compliance_lint's TAX-referral rule is
   placement-blind — a clean lint says nothing about *where* the disclosure
   lives. COMPL adjudicated placement manually this run. Candidate lesson: add
   a placement-aware check (written-channel presence) to the lint.
3. **[MEMC/pattern]** V1's sole E1 blocker (CL-01) was cleared by *reframe*
   (magnitude → form) rather than re-sourcing. Cheap, effective, and its
   price is measurable here: hook 4, not 5. Reusable fix pattern with a known
   cost.
4. **[MEMC/voice]** The ratified transition "Here's the part nobody mentions:"
   is unusable under BEN-C3 adjacency in FRS content (CL-19). If the softened
   "rarely comes up" variant recurs, propose ratifying a compliant variant in
   brand-voice.md transitions rather than improvising per-run.
5. **[MEMC/observation]** Duration sits at 197/200 words — the band's ceiling.
   Any future spoken addition needs an offsetting cut. COMPL's optional
   on-screen TAX-01 append (report §3.4) is written-channel only and
   duration-safe if adopted.
6. **[verdict-neutral]** COMPL-2 (residual "never hear it called a decision"
   adjacency) remains open as an optional fix; adoption re-enters at
   fact_check as a delta (D5). Not a QA flag — trusting COMPL's minor/optional
   classification.
