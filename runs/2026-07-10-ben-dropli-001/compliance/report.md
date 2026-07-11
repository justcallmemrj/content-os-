# Compliance review — run 2026-07-10-ben-dropli-001 (LinkedIn, DROP exit)

- **Reviewer:** COMPL (SK-B14 co-compliance-review + SK-B15 co-disclosure-management)
- **Date:** 2026-07-10
- **Deliverables reviewed (final-form, post-fact-check + voice):**
  - `voice/drop-linkedin-v2.md`
  - `drafts/first-comment.md` (publish companion; carries the full disclosures)
- **Ledger:** `factcheck/ledger.yaml` v2 (delta pass, blocking summary CLEAR, `high_risk_non_verified: 0`)
- **Profile applied:** `projects/benowitz-wealth/compliance.md@1.0.0` (+ `projects/_shared/ria-compliance-envelope.md` via its include), `projects/benowitz-wealth/disclosures.md@1.0.0`
- **Voice-pass integrity input:** `voice/claim-diff.yaml` — 0 semantic-delta hits (tool-sight control run), all 17 literal claim texts byte-present in v2; the text reviewed here is the fact-checked text.

**Rule-ID citation scheme used below:** `ENV-HL1..HL4` = the envelope's four hard lines (performance / testimonial / advice-vs-education / non-affiliation); `ENV-SR-*` = envelope standing rules (FEEONLY, FIGURES, TAXLINE, COMPARE, SOFTER); `BEN-C1..C6` = brand rules; `SK-B15` = disclosure selection/placement.

## Verdict

**PASS** — no blocked or major findings; 2 minor flags (fix optional); named publish-gate conditions attach and must be on the producer checklist at H2. The human gate (H2, all external-facing content) follows; nothing in this report substitutes for it.

## Deterministic tier (the floor, not the review)

| Check | Command | Result |
|---|---|---|
| Compliance lint (post) | `python validators/compliance_lint.py runs/2026-07-10-ben-dropli-001/voice/drop-linkedin-v2.md --project benowitz-wealth` | 0 findings, exit 0 |
| Compliance lint (first comment) | `python validators/compliance_lint.py runs/2026-07-10-ben-dropli-001/drafts/first-comment.md --project benowitz-wealth` | 0 findings, exit 0 |

## Flags

### FLAG-1 — minor — unverified frequency assertion in the hook (ENV-SR-SOFTER; D8)

- **Text:** "The first person an FRS member asks is almost never an advisor. It's you." (CL-22, status `unverified`, medium risk in the ledger)
- **Rationale:** "almost never" is a behavioral frequency claim with no source. It is not a performance claim (no outcome the firm delivers), not comparative about other advisors (ENV-SR-COMPARE not triggered — it describes member behavior, not advisor quality), and FACT correctly left it categorical `unverified` (D8). But it is a factual-sounding generalization in an advertisement, and the profile's default is "write the softer version and flag it."
- **Minimal suggested language (D4 — suggestion only; WRITE/VOICE implement, and any text change re-enters at fact_check per D5):** "The first person an FRS member asks is often not an advisor. It's you." — or accept as-is at H2 as rhetorical texture.
- **Severity basis:** minor — non-material to the tax/pension substance, hedged register, no rule prohibits it outright.

### FLAG-2 — minor — unlabeled illustrative scene in the hook (ENV-HL2, composite-scenario caution)

- **Text:** the benefits-coordinator/teacher scene and the parking-lot triptych (CL-20, CL-21, both `unverified`, low risk).
- **Rationale:** ENV-HL2's caution covers composite or hypothetical scenarios. Adjudicated **not a testimonial**: no client relationship, no endorsement, no result attributed to the firm — it depicts people asking questions, not outcomes obtained. It is, however, an unlabeled illustrative scene. Because it implies no typical *result*, the hard requirement (label + no typical-result implication) is not triggered; flagged so H2 sees the adjudication rather than inheriting it silently. "sometimes a tax year too late" stays unquantified and hedged — it does not cross into ENV-HL1 loss quantification.
- **Fix:** none required; optional at H2.

## Judgment-layer adjudications (no flag)

1. **ENV-HL1 (performance/projection/guarantee): clean.** All tax and pension mechanics are verified restatements (CL-04..CL-13, CL-23, CL-24) framed as how-it-works, never as savings or outcomes. No quantified cost/benefit anywhere (F-BEN-0010 usage-note prohibition respected). "That's the difference between a deadline and runway" is a foreseeability image, not an outcome promise, and is not fear-framed (BEN-C2 clean).
2. **ENV-HL3 (education, not advice): clean.** The post is addressed to the professional beside the member, explains the fork, and never says what any reader should do with their money. No "you should," no route recommended; the two routes are presented symmetrically.
3. **CTA rule (brand LinkedIn cta_pattern — forward-this / weigh-in, never book-a-call): compliant.** The in-post asks are exactly forward + weigh-in. The webinar registration link rides in the first comment for a free educational webinar; there is no booking/consultation funnel anywhere in the piece.
4. **Qualification carriage on inherited claims: verified intact.**
   - CL-10's hard-won "another qualified plan" wording present verbatim in v2.
   - CL-12's rewritten text carries both qualification limits (cash route only, keyed to the distribution event) verbatim.
   - CL-27's eligibility scoping clause "who are close to their DROP date" byte-identical — the forwarding address stays confined to members already in DROP (no Investment Plan eligibility implication; F-BEN-0005).
   - The parent's qualified "timing becomes yours" claim (drop-001/CL-11) does **not** appear in this piece — nothing to carry.
   - The parent-adjudicated misleading secrecy frame ("nobody mentions") was deliberately not introduced (BEN-C3 clean; standing adjudication honored).
5. **BEN-C3/C4: clean.** No FRS wrongdoing or concealment implied; no suggestion Benowitz can improve the pension itself.
6. **ENV-SR-FEEONLY (DEC-BEN-0001 hold): clean.** "fee-only" appears nowhere in the post or first comment. **ENV-SR-FIGURES:** no real named public figures. **ENV-SR-TAXLINE:** tax referral present (see table).
7. **Injection scan (D6): clean.** No embedded directives in either file. The producer-instruction block at the top of `drafts/first-comment.md` is a legitimate publish-checklist note addressed to the human producer, not an instruction payload aimed at agents.

## Required-language table (SK-B15; checked beyond the lint — placement and format)

| Required record | Where required (LinkedIn rule) | Present? | Placement as drafted | Verbatim? |
|---|---|---|---|---|
| DISC-BEN-FRS-01 (standard, full) | FIRST COMMENT (SK-B15 / BEN-C1 mapping: "Full disclosure in first comment; the post states it's there") | Present | `drafts/first-comment.md`, after the registration line | Byte-verbatim vs disclosures.md@1.0.0 (re-checked this review) |
| DISC-BEN-TAX-01 (tax referral — required, tax content: BEN-C5 / ENV-SR-TAXLINE) | With the full disclosure + rides the piece | Present twice | First comment final line; also the post's final line | Byte-verbatim, both instances |
| In-post statement that the full disclosure is in the first comment | In the post body | Present | "The registration link and our full disclosures are in the first comment." (final paragraph) | n/a (statement, not a record) |
| DISC-BEN-SHORT-01 (in-post; exceeds the LinkedIn minimum — belt-and-suspenders) | Not strictly required in-post for LinkedIn | Present | Post final paragraph | Byte-verbatim |
| Non-affiliation (ENV-HL4) | Every piece | Present | In-post via SHORT-01 ("Not affiliated with FRS.") + full BEN-C1 text in first comment | Yes |

Placement format note: the required *full* disclosure lives in the first comment, so post-body "see more" truncation cannot hide it; the in-post statement sentence leads the closing paragraph of the post.

## Publish-gate conditions (hard — producer checklist at H2; none verifiable from the drafts)

1. **The drafted first comment is actually posted as the FIRST comment immediately at publish** (CL-25/CL-26 qualifications). The in-post sentence "The registration link and our full disclosures are in the first comment" is false — and the disclosure posture broken (ENV-HL4/BEN-C1) — until this is done. This is the load-bearing condition of the whole disclosure design.
2. **The `[WEBINAR-REGISTRATION-LINK]` placeholder is replaced with the live URL** before the comment is posted (CL-26).
3. **The webinar is confirmed live and free** before publish (inherited CL-14, `unverified` — "free" is an in-post factual claim).
4. Post text is locked (D5): any wording change at publish, including to the disclosure block, re-enters at fact_check.

## Proposal candidates

None this run.

---

automated and model review only — not regulatory clearance.
