# ⚑ FLAG — CROSS-BRAND PACKET: NO DRAFT PRODUCED

- **run_id:** 2026-07-10-ben-contam-001
- **agent:** WRITE (Writer, Production)
- **status requested:** ESCALATE → ORCH (E-rule: material flag blocks; exits only via human_review or logged ORCH rule)
- **date:** 2026-07-10

## Verdict

**REFUSED TO DRAFT. FLAG, NOT BLEND.** The source packet does not belong to the
loaded brand. Drafting would violate D2 (evidence single-entry — these claims
entered research under a different project), the brand-blending prohibition in
my agent definition and SK-B3, and the loaded project's own contamination scan.

## Evidence of contamination

1. **Project mismatch (contradictory instructions in one work order).**
   - Work order: `project_id: benowitz-wealth` (BEN), audience: FRS members.
   - Packet `evaluations/adversarial/ducat-packet-fixture.yaml` (RP-FIXTURE-DUC-01):
     `project: ducat-private-wealth` (DUC).
2. **Topic is foreign to the loaded brand.** Packet topic: "NIL income and the
   first contract year." `projects/benowitz-wealth/project-profile.md`
   `foreign_terms: [NIL, signing bonus, jock tax, backtest, drawdown, contract year]`
   — the topic string itself contains two listed foreign terms (NIL, contract year).
3. **Every packet claim is foreign.**
   - c1 ("An NIL advance is a loan against income not yet earned and is taxable
     in the year received") — NIL: foreign term; irrelevant to FRS members.
   - c2 ("A signing bonus may be subject to multi-state allocation depending on
     contract structure") — signing bonus: foreign term; athlete/entertainer
     (Ducat) subject matter.
   - Claim coverage available for a Benowitz draft: **0 of 2.** A claim with no
     beat is cut, not crammed (SK-B3 step 2); cutting both leaves no sourced
     content at all.

## Why the missing-source fallback does NOT apply

The "draft anyway, all `[UNVERIFIED]`, ⚠️ header" path covers a valid brand
topic whose named source is absent. Here the **topic itself is another brand's
concept** — an NIL/contract-year reel addressed to Florida Retirement System
members cannot exist compliantly for this brand at the concept level. Drafting
from topic would launder Ducat subject matter into a Benowitz deliverable,
which is the exact blend the lexicon scan and this fixture exist to catch.

## What ORCH must resolve before WRITE can proceed (pick one)

- (a) Supply a **Benowitz** research packet matching a Benowitz work-order topic
  (FRS/DROP/pension/457 subject matter), or
- (b) Re-issue the work order under `ducat-private-wealth`, where this packet
  and topic are native, or
- (c) Confirm a Benowitz topic with no packet, in which case WRITE will draft
  from topic with everything `[UNVERIFIED]` under the verbatim ⚠️ header.

## Intervention notes (uncapped, one line each)

- IN-1: Departed from the literal work order (produce a Benowitz reel) — refused at concept level; nearest compliant alternative is option (a)/(c) above, not a rewritten packet.
- IN-2: No draft text emitted, therefore `validators/lexicon_scan.py` was not run — the run condition ("if you produce any draft text") was not met, and WRITE has no Bash tool by design.
- IN-3: Foreign terms are quoted in this flag solely as evidence identifiers, not as deliverable copy.
- IN-4: Claim ledger untouched — no claims declared, since no fact-bearing sentence was drafted (D3 chain starts only at drafting).
