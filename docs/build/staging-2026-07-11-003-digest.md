# Curation digest — staging/2026-07-11-003 (H6 #3: Ducat evidence + voice, Benowitz books)

**What this PR is:** step 3, tranche 3 — the Ducat evidence and voice memory
that tranche 2 couldn't build ("nothing Ducat-authored found on this
machine"), now built from the owner-delivered back catalog: the athlete-
education caption set, two curriculum handoffs, the Beyond the Season Book 1
package, the NIL workshop deck (referenced), the typography spec, plus the
three Benowitz FRS Blueprint book manuscripts. Per D-079 every record below is
a proposal until you merge.

**Scope correction (before anything else):** the delivered caption set is
**36 posts across Weeks 1–20**, not the 24-post/12-week set described at
intake. The export matches `Ducat_.md` §3 ("2 posts/week across Weeks 1–20 —
up to 40 posts"); 4 of the 40 post folders shipped images but no caption file
(W06-B Fee-Only-Fee-Based-Commission, W08-B Family-Friends-Money-Boundaries,
W12-A Money-Skills-Outlast-the-Season, W18-B Four-Year-Career-Forty-Year-Plan).
All 36 existing captions were read in full and vendored.

**Verification performed (D-062):** four live fetches, four OK, zero failures —
Fla. Stat. §1006.74 from leg.state.fl.us (NIL commercial-use right, workshop
mandate, and the no-solicitation clause quoted from live text; history line
confirms four amendments since 2020), the IRS estimated-taxes page
(pay-as-you-go sentence, $1,000 trigger, four payment periods, penalty and
safe harbors verbatim), the IRS Roth IRA page (no-deduction + tax-free
qualified distributions verbatim), and the IRS IRA contribution-limits page
(the "taxable compensation for the year" cap — fetched because the Roth
overview page alone does not state the earned-income rule). Fact statements
originate in the fact-checked caption set; every rule-based statement was
checked against the live source before its record was written.

## Sections

1. **S-DUC-0001…0010** — ten Ducat source records: six firm-owned tier-3
   (caption set, both curriculum handoffs recorded for what each IS —
   Weeks-1-20 edition vs 24-post edition, BTS Book 1 manuscript, BTS
   compliance memo, NIL deck referenced-not-vendored) and four live-verified
   tier-1 (FL NIL statute; IRS estimated-taxes, Roth IRA, and IRA
   contribution-limits pages).
2. **S-BEN-0005…0007** — the three FRS Retirement Blueprint manuscripts
   (firm-owned back catalog; facts NOT extracted at seeding, by design).
3. **F-DUC-0001…0007** — seven structural facts, mechanisms over volatile
   numerics (the caption set's own discipline): NIL = business income for
   commercial use of identity; rules vary by state/school/level +
   compliance-office-first; pay-as-you-go quarterly estimated taxes; 1099
   no-withholding; Roth IRA requires taxable compensation; separate
   business/personal accounts (mechanism, practitioner-only source,
   confidence medium); the FL statutory NIL right + workshop mandate. Every
   fact carries `review_by` (≤ 12 months), usage notes with the compliance
   framing (DUC-C5 tax riders, no-dollar-figures routing), and honest scope
   notes where the live source covered only part of a caption's claim.
4. **VX-DUC-0001…0010** — ten voice exemplars against the ratified-but-⚑
   voice profile, each `why` naming the move it models: naming the
   unglamorous specific (W01-B), fewer-words-more-weight closers (W02-A),
   never-perform-enthusiasm (W03-A), the composed debunk (W05-A),
   directness-5 without salesmanship (W06-A), weight-per-word aphorisms on a
   fear topic (W08-A), role-boundary teaching (W10-A), seen-rather-than-sold
   (W15-B), composed-on-sudden-money (W18-A), systems-over-suspicion +
   the maxim register (W20-B).
5. **Assets + manifests** — 46 files vendored: 36 captions, 3 BTS book files,
   2 curriculum handoffs, the typography spec (DUC), 4 FRS book files (BEN).
   New DUC manifest (8 entries) + BEN manifest extended (AST-BEN-BOOKS-FRB).
   Referenced-not-vendored inventory below.

## Review flags (⚑ — decide before or at merge)

- **⚑ Disclosure drift (found, not resolved — flagging only per instruction).**
  The caption set's disclosure block differs from `disclosures.md` on six
  axes:
  1. **"fee-only" appears in every one of the 36 caption disclosures**
     ("a Florida-registered investment adviser (fee-only)") while DUC-C6 holds
     "fee-only" firm-wide per DEC-BEN-0001 ("use fiduciary"). Worse, the firm
     is internally inconsistent three ways: captions + both curriculum
     handoffs say **fee-only**; the BTS books/launch kits say **fee-based**;
     and the BWM_FRB compliance memo §1(5) itself flags this exact
     fee-only(BEN)/fee-based(DUC) conflict as its "highest priority" pre-print
     action item (resolve via Form ADV, then conform all materials).
  2. Base wording: captions "Educational and informational only — not
     individualized investment, financial, tax, legal, or accounting advice,
     and not a recommendation of any investment, strategy, or product…
     public-facing brand of Joy Financial Group LLC" vs DISC-DUC-01
     "Educational content only. Not individualized investment, tax, or legal
     advice… a brand of Joy Financial Group LLC."
  3. Registration phrase: captions "Florida-registered" vs DISC-DUC-01
     "Florida state-registered."
  4. Non-affiliation list: captions "any university, athletic department,
     league, or government agency" vs DISC-DUC-01 "any professional league,
     team, players' association, university, athletic conference, or NIL
     collective" — the caption list **omits NIL collective, players'
     association, team, and conference** (DUC-C1's motivating cases) and adds
     government agency / athletic department. The BTS book uses a third,
     longer list.
  5. Tax rider: captions prepend "NIL and athlete income is generally
     taxable." and say "about your specific situation" vs DISC-DUC-TAX-01's
     "regarding your specific situation."
  6. The captions deploy rider families with no `disclosures.md` counterpart
     at all: NIL (rules-vary/verify), INV (investing risk / past performance),
     PRV (private-investment risk), CON (not legal advice / attorney review),
     GIV (charitable/tax-planning), BRD (trademark/right-of-publicity).
     Either disclosures.md grows ratified verbatim records for these or
     future DUC pieces can't reproduce the back catalog's stack.
- **⚑ DUC voice sliders are still PROPOSED** (brand-voice.md header) — these
  ten exemplars are your calibration set. Two deliberate tensions to rule on:
  the set says **"financial team" / "team" constantly** (W06-A, W10-A, W12-B,
  W20-B) while brand-voice.md reserves "team" for the sport; and several
  captions use **training-discipline analogies** ("percentages and reps,"
  W02-B; "reps before highlights," W11-B) that sit near the
  no-sports-metaphors-for-money line while feeling native to the voice.
  Exemplars were chosen to minimize (but W10-A/W20-B can't fully avoid) the
  "team" usage; VX-DUC-0007's `why` carries the flag inline.
- **⚑ Not live-verified:** BrokerCheck/IAPD claims (W08-A/W10-B), the
  SE-tax-covers-both-halves detail (F-DUC-0004 usage_notes route it to the
  IRS SE-tax page before reuse), USPTO/trademark mechanics (W13-A/B), and the
  accredited-investor criteria (W15-A) — no fact records were written for
  these; they stay caption-only until a run needs them.
- `approved_by: wes / approved_on: 2026-07-11` is written into the records on
  the D-079 theory that **your merge is the approval**; git history is the
  truth if you merge later.
- `verified_by: seed-verification` (not FACT): first live run re-verifies
  anything it cites per the freshness contract.
- F-DUC-0006 (separate accounts) is the one fact resting solely on the firm's
  own back catalog — mechanism claim, confidence `medium`, no external rule
  exists to check it against. Drop it if you want tranche 3 to be 100%
  externally anchored.
- The BTS and FRS book series are both **"drafts pending CCO review"** per
  their own memos — the manuscripts are vendored as provenance, not as
  approved content.

## Referenced, not vendored (origin paths recorded in manifests)

- 25 Ducat feed JPEGs (extracted) + square/story zips (25 each) —
  `C:/Users/Mrder/OneDrive/Desktop/Benowitz and Ducat Post/Ducat/{Feed,Square,Story}/`
- 100 Ducat ad creatives (25 × 4 formats) —
  `C:/Users/Mrder/OneDrive/Desktop/Benowitz and Ducat ads/benowitz-ducat-ads/Ducat/`
- `Ducat_NIL_Workshop_01_Football.pptx` (~1.9 MB) — Downloads (S-DUC-0006)
- Beyond the Season cover-directions zip — Downloads
- Per-post JPGs of the caption set (2 per post) — remain in the Downloads
  export tree

## What merging does

DUC stops being the evidence-empty project: NIL/tax/Roth content can cite
F-ids instead of `[UNVERIFIED]`, and SK-B9/RUB-VOICE-1 finally has a Ducat
exemplar set — which doubles as the calibration evidence for ratifying the
PROPOSED sliders. BEN gains its three-book back catalog as provenance for
future fact extraction. Post-merge: indexes regenerate on main; the 26
non-exemplar captions stay in assets as future candidates.

## Still missing (tranche 4+, needs you)

Ducat Books 2–3 manuscripts (launch kit references them; not on this
machine); the disclosure-drift ruling above (which wording is canon);
BrokerCheck/IAPD + accredited-investor fact records if athlete
advisor-vetting content is planned; TRD and FDR remain seeded-empty.
