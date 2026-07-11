# FACT findings — run 2026-07-11-duc-nil-001 — nil-reel-v1.md (full pass, v1)

Adjudicated 2026-07-11T14:19:20-04:00 against the approved-fact evidence base
(F-DUC-0001, F-DUC-0002, F-DUC-0004 — all opened) and their cited sources
(S-DUC-0001 incl. W01-A caption file opened, S-DUC-0007, S-DUC-0008 — all
opened), plus projects/ducat-private-wealth/disclosures.md and compliance.md.
No web access; live verification of these records occurred at seeding
(2026-07-11). Findings only — no rewrites (D4).

## Verdict input (T7)

**High-risk non-verified claims: 0. Ledger complete and validated. → voice_edit.**

- `schema_validate.py`: `OK runs/2026-07-11-duc-nil-001/factcheck/ledger.yaml [claim-ledger]`
- `ledger_validate.py --deliverable`: `VALID: ledger.yaml (0 violation(s))` —
  on-screen byte-presence, evidence-ref, and blocking-summary recomputation all pass.

## Extraction and reconciliation

- Independent extraction: **14 material claims** (stated, implied, on-screen).
- WRITE declared **13**; all 13 located in the draft at the declared anchors —
  **zero declared-but-absent**.
- **1 FOUND** (undeclared): CL-14.
- `extract_claims.py` ran clean but returned only 1 candidate ("Part of it may
  already be owed.") — its tax-claim filter deliberately suppresses hedged
  constructions, and this script is hedged by design (DUC-C5). The manual
  adversarial sweep is the extraction of record; the script is a floor, not
  the boundary (SK-B2). Not a script failure — no escalation.

## Status tally (14 claims)

| Status | Count | Claims |
|---|---|---|
| verified | 11 | CL-01..07, CL-09..12 |
| verified-with-qualification | 2 | CL-08, CL-13 |
| unverified | 1 | CL-14 (low risk) |

High-risk claims after FACT's CL-01 reclassification: 9 (CL-01, CL-03, CL-05,
CL-07, CL-08, CL-09, CL-10, CL-11, CL-13). All are verified or
verified-with-qualification. Record-anchored throughout: every verified
status cites an opened fact record and its opened source; no vibe matches
accepted on tax/legal/eligibility claims.

## Findings

### F-1 · CL-14 · FOUND (undeclared claim) · non-blocking
- **Claim:** "The money showed up. The instructions didn't." (STAKES)
- **Status:** unverified (low risk).
- **Evidence:** none in the approved-fact set on what guidance accompanies NIL
  payments. The withholding shadow inside it is separately ledgered and
  verified (CL-07/CL-08).
- **What would fix it:** nothing required — low-risk texture; unverified is
  its legitimate final state. WRITE should declare it from v2 onward if the
  line survives voice edit (declaration-coverage hygiene, mirrors the BEN
  precedent).

### F-2 · CL-01 · risk reclassification · non-blocking
- **Claim:** "Your first NIL check is not a paycheck." (HOOK)
- **Finding:** WRITE risked it medium (definition); FACT reclassifies **high**
  — the paycheck negation trades on tax/withholding character
  (risk-classification.md: tax treatment is high regardless of framing).
- **Status:** verified either way (F-DUC-0001 not-a-salary negation;
  F-DUC-0004 W-2 withholding contrast), so no blocking effect.
- **What would fix it:** ledger already carries the corrected risk; no text
  change needed.

### F-3 · CL-08 · verified-with-qualification · non-blocking, flagged forward
- **Claim:** "Nobody withholds for you. The full amount lands in your
  account." (BEAT THREE)
- **Finding:** F-DUC-0004 scopes no-withholding to 1099 independent-contractor
  income, "the form behind **most** NIL payments." The unconditional "Nobody
  withholds" stretches most -> all; a W-2-structured NIL arrangement would
  withhold, and the evidence is silent on prevalence. Context mitigates: the
  "generally" hedge (CL-07) is spoken ~20 seconds earlier, and sentence two
  ("full amount lands") matches the fact verbatim.
- **What would fix it:** one softening word, e.g. "Usually nobody withholds
  for you." — WRITE/VOICE's call, not FACT's edit (D4). If VOICE touches it,
  the change re-enters as a fact_delta on CL-08 only.

### F-4 · CL-13 · disclosure byte-match · PASS, with publish-gate rider
- **On-screen text vs DISC-DUC-SHORT-01:** **byte-exact match** —
  "Educational only. Not advice. See profile for full disclosures."
  (disclosures.md@1.0.0). `ledger_validate.py` independently confirms
  byte-presence in the deliverable (D-016).
- **Short-format conditions:** the deliverable explicitly states where full
  disclosures live ("See profile…"), and the production notes correctly route
  DISC-DUC-01 verbatim **plus** DISC-DUC-TAX-01 (script touches taxes —
  DUC-C5) to caption/profile, persistent on-screen placement 0:00–end, never
  the spoken track (disclosure-mapping video row).
- **Rider:** the claim is only true if that placement actually happens at
  publish — hard publish-gate condition for COMPL/QA, not verifiable from the
  draft.

### F-5 · Usage-note compliance checks · PASS (recorded, no action)
- F-DUC-0001 "always pair with the vary-by-state caveat": paired — CL-10 in
  BEAT THREE. PASS.
- F-DUC-0004 scope firewall (both-halves SE-tax mechanism not independently
  fetched at seeding): the draft does **not** restate it. PASS.
- F-DUC-0002 "never state what any particular state/school/level permits":
  the draft states no volatile specifics. PASS.
- Caption-vs-visual consistency: B-roll directions (banking notification,
  plain unsigned contract) assert nothing beyond CL-06/CL-07; no school
  marks, no real-athlete likenesses in the directions (DUC-C2 / work order).
  PASS at script level; render-time check belongs to the video machine.

## Escalations

None. No requires-professional-review statuses, no source conflicts, no
packet inadequacy — the approved-facts-only evidence base covered every
material claim the script makes.
