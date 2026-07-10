# Curation digest — staging/2026-07-10-002 (H6 #2: facts, sources, exemplars)

**What this PR is:** step 3, tranche 2 — the first evidence and voice memory,
drawn from your own back catalog per "let's do it": the five webinar scripts
(`Webinar Scripts 2.zip`) and the 30-post published carousel package
(`Benowitz-Carousels.zip`). Benowitz only; Ducat evidence/exemplars still need
source material (nothing Ducat-authored found on this machine).

**Verification performed (D-062):** three of four sources fetched LIVE today —
Florida Statute §121.091 (96-month cap and termination requirement quoted from
the live text), the IRS rollover page (20% mandatory withholding + direct-
rollover deferral quoted verbatim), and the SSA Fairness Act page (confirmed
live). MyFRS.com confirmed as the official member resource. Fact statements
originate in your fact-checked webinar scripts and published posts; where the
statement is statutory, the statute was checked directly.

## Sections

1. **S-BEN-0001…0004** — four tier-1 source records (statute, IRS, SSA, MyFRS),
   each noting what was verified live at seeding.
2. **F-BEN-0001…0010** — ten facts, structural-first (the webinar's own
   discipline): DROP definition, 96-month cap, termination requirement, exit
   mechanics, Pension-Plan-only eligibility, 20% withholding, direct-rollover
   deferral, WEP/GPO repeal (with the most-FRS-work-was-covered nuance baked
   into the statement), post-2011 COLA rule, lump-sum tax treatment. Every fact
   carries `review_by` (≤12 months), usage notes with the compliance framing,
   and `claim_key`s that extend the spec's own example vocabulary.
3. **VX-BEN-0001…0005** — five voice exemplars with the *why* recorded: the
   plain-English definition pattern (Post 03), send-them-to-their-paperwork
   (Post 10), accuracy-as-voice on policy news (Post 12), the spoken teaching
   register, and compliance-shaped product talk (webinar Slide 8).
4. **Assets + manifest** — the five webinar scripts and all 30 caption files
   vendored under `assets/` (rights: firm-owned; slide JPGs deliberately NOT
   vendored — they stay in Downloads; manifest records the pointer).
   `.gitattributes` gains text-exception rules so these stay diffable instead
   of disappearing into LFS.

## Review flags (things you might drop or edit before merging)

- `approved_by: wes / approved_on: 2026-07-10` is written into the records on
  the D-079 theory that **your merge is the approval** — if you merge on a
  different day, the git history is the truth and the field is cosmetic.
- `verified_by: seed-verification` (not FACT): FACT doesn't exist until step 5;
  first live run re-verifies anything it cites per the freshness contract.
- F-BEN-0009's COLA formula matches your published Post 10; its statutory bases
  (§121.101) was NOT independently fetched today — statement rests on your
  fact-checked post plus MyFRS routing.

## What merging does

BEN gains a citable evidence base (the DROP reel slice run can cite F-ids
instead of flagging everything `[UNVERIFIED]`) and a real exemplar set for
SK-B9/RUB-VOICE-1. Post-merge: indexes regenerate on main; remaining 25 posts
stay in assets as future exemplar candidates.

## Still missing (tranche 3, needs you)

Ducat evidence + exemplars (the 20-week curriculum / NIL decks — not on this
machine); the three Benowitz books; any additional approved pieces you want in
the voice set.
