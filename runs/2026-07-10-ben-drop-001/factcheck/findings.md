# FACT findings — run 2026-07-10-ben-drop-001 (full pass)

Deliverable: `drafts/drop-reel-v1.md` · Ledger: `factcheck/ledger.yaml` (v1)
· Packet: RP-2026-0710-01 · Pass: full, FACT, 2026-07-10T18:04:49-04:00
· ledger_validate: VALID (0 violations)

## Blocking summary (E1)

**high_risk_non_verified = 1. The run does not clear fact_check as drafted.**

- **CL-01 (HOOK, high, unverified):** "Your DROP payout may be the biggest
  check of your career." No evidence anywhere in RP-2026-0710-01 supports a
  magnitude claim — the packet's uncertainty section *deliberately* excludes
  member-specific figures. WRITE declared it `[UNVERIFIED]` honestly; the
  block is structural. Three exits: (1) RSRCH sources a supportable magnitude
  fact into a refreshed packet; (2) WRITE reframes the hook without the
  factual shadow — e.g. "Your DROP payout arrives as a single check — and it
  comes with a decision attached."; (3) the flag rides to human review and
  Wes adjudicates. FACT does not rewrite; option 2's wording is a suggestion,
  not an edit.

All other high-risk claims (CL-04, CL-07, CL-08, CL-10, CL-12, CL-15, CL-16)
are `verified` or `verified-with-qualification`. Every verification was made
against opened evidence: the packet claims AND their underlying F-records
(F-BEN-0003/0004/0006/0007/0010), plus F-BEN-0001/0002/0005 and
`disclosures.md` for the FOUND and on-screen claims.

## FOUND claims (undeclared by WRITE)

Independent extraction (`extract_claims.py`, 5 candidates — all already
declared) plus manual sweep surfaced four material claims WRITE missed:

- **CL-16 (STAKES, high, verified-with-qualification):** the audience address
  "Teachers, deputies, firefighters, state staff" implies DROP applies to
  these occupational groups. F-BEN-0005 (opened): DROP is available **only to
  FRS Pension Plan members; Investment Plan members are not eligible.** The
  packet excluded eligibility facts as out of brief scope, but the draft's
  address walks into eligibility territory anyway. Mitigation: the reel's
  frame ("Your DROP payout") self-selects members already in DROP, who are
  Pension Plan members by definition. Flag rides to COMPL: is the unqualified
  occupational address acceptable for this format?
- **CL-17 (HOOK, low, unverified):** "Most members never hear it called a
  decision." Texture with a factual shadow; no evidence. Legitimate final
  state at low risk.
- **CL-18 (BEAT ONE, low, unverified):** "Most members picture a payday."
  Same class as CL-17.
- **CL-19 (BEAT TWO, low, misleading):** "Here's the part nobody mentions:"
  — frames rules that are publicly documented on the packet's own tier-1 IRS
  source (S-BEN-0002) as hidden knowledge. Low risk, non-blocking; suggested
  softening below.

## Qualifications (required wording)

- **CL-10 (BEAT THREE, high):** "…into an IRA or another plan…" — evidence
  (F-BEN-0007) says "an IRA or another **qualified** plan." True as
  qualified; unqualified, "another plan" overreaches: not every plan is an
  eligible rollover destination.
- **CL-11 (BEAT THREE, medium):** "The timing becomes yours." — evidence
  supports *deferral until later withdrawal*, not unconditional control of
  timing; distribution rules still govern retirement accounts and the packet
  contains nothing on those limits.
- **CL-12 (TURN, high):** "Your termination date decides which tax year that
  money lands in" — true for the **cash** route as a planning teaching: the
  tax code keys on the year of *distribution* (F-BEN-0010), and termination
  at DROP end is what makes the balance payable (F-BEN-0003/0004). Limits:
  the distribution date, not the termination date, is the technical trigger;
  and on the rollover route the money does not "land" in any tax year until
  later withdrawal.
- **CL-15 (on-screen, high):** first three sentences match DISC-BEN-SHORT-01
  verbatim, and "Full disclosures in profile." satisfies the short-format
  explicit-pointer condition. True **only if** DISC-BEN-FRS-01 actually
  appears in the profile or first comment at publish — hard publish-gate
  condition.
- **CL-16:** see FOUND above — Pension-Plan-only boundary (F-BEN-0005).

## Suggested minimal corrections (FACT does not edit the draft)

1. **CL-10:** "into an IRA or another plan" → "into an IRA or another
   qualified plan" (one word restores the evidence boundary).
2. **CL-19:** "Here's the part nobody mentions:" → e.g. "Here's the part
   that rarely comes up:" (removes the secrecy frame).
3. **CL-01:** reframe or source (see Blocking summary) — this one is the
   blocker.

## Verified-clean notes

- CL-04 states the termination rule as the hard requirement F-BEN-0003's
  usage note demands (work-order-REQUIRED framing honored).
- CL-07 respects F-BEN-0010's prohibition on quantifying the tax cost for a
  stranger; CL-08 matches the IRS 20%-withholding text essentially verbatim.
- DISC-BEN-TAX-01 ("Consult a qualified tax professional regarding your
  specific situation.") appears verbatim in the CTA — required companion for
  the tax content (F-BEN-0006/0007/0010 usage notes). Not a factual claim,
  so not ledgered; noted here as satisfied.
- Packet freshness: all cited facts `status: active`, `review_by` 2027-07-01
  / 2027-07-10 — within window as of 2026-07-10. No outdated statuses.

## Publish-gate conditions (for QA / producer checklist, non-blocking here)

- DISC-BEN-FRS-01 full text must be placed in the profile or first comment
  (CL-15 condition; disclosures.md short-format rule).
- Confirm the DROP Exit webinar is live, free, and the profile link resolves
  (CL-14, "Register at the link in our profile").

---

# Re-check (cycle 2) — drop-reel-v2.md

Ledger: `factcheck/ledger.yaml` v2 · Pass: full, FACT,
2026-07-10T18:13:25-04:00, trigger "revision cycle 1"
· ledger_validate: VALID (0 violations) against `drafts/drop-reel-v2.md`

## Verdict: CLEAR — high_risk_non_verified = 0

Independent extraction on v2 (`extract_claims.py`, 5 candidates) mapped
entirely to declared ids (CL-04, CL-07, CL-08, CL-10, CL-12); manual sweep
found no new undeclared material claims. WRITE's revision-change-log claims
were checked against the actual v2 text and evidence, not taken on trust.

Touched-claim dispositions:

- **CL-01 (v1 blocker) → verified.** Reframed structurally: "Your DROP
  payout arrives as a single check." asserts payout FORM only — a direct
  restatement of F-BEN-0004's "becomes payable as a one-time lump sum."
  Magnitude superlative gone. Resolved by reframe, not re-sourcing.
- **CL-10 → verified (qualification discharged).** "another qualified plan"
  restored — now an exact scope match to F-BEN-0007.
- **CL-12 → verified (qualification discharged).** "Choose cash, and it's
  taxed in the year it pays out." keys the tax year to the distribution
  event and is explicitly scoped to the cash route — both v1 limits
  respected; matches F-BEN-0010 directly.
- **CL-16 → verified (qualification discharged).** The conditional address
  ("if you're in DROP") scopes STAKES to members already in DROP — Pension
  Plan members by definition — so no eligibility implication remains for
  Investment Plan members (F-BEN-0005 boundary respected). The v1 COMPL flag
  on this point is withdrawn as resolved.
- **CL-19 → unverified (was misleading).** Secrecy frame removed per the
  suggested softening; what remains is low-risk texture, legitimate final
  state. Noted: WRITE's intervention note says the v1 wording is a listed
  brand-voice transition — if VOICE reverts it, that is a semantic delta and
  re-enters fact_check in delta mode.
- **CL-03, CL-08, CL-13 (changed text, not in my v1 finding set):**
  re-checked anyway — CL-03's conditional narrows a supported claim
  (verified stands); CL-08's dropped "And" is cosmetic (verified stands);
  CL-13's "You can see that year coming." carries the same foreseeability
  teaching via the F-BEN-0002/0003/0004 chain (verified).

Standing items (unchanged, non-blocking): CL-11 and CL-15 keep their
verified-with-qualification statuses and wording; CL-14/CL-17/CL-18 remain
low-risk unverified. Publish-gate conditions still ride: DISC-BEN-FRS-01
full text in profile or first comment (CL-15); webinar live, free, link
resolves (CL-14).

Status counts (v2): verified 13 · verified-with-qualification 2 ·
unverified 4 · misleading 0 · outdated/incorrect/requires-professional-review 0.
