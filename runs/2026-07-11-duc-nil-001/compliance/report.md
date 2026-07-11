# Compliance report — run 2026-07-11-duc-nil-001 (COMPL, SK-B14 + SK-B15)

- **Deliverable:** `runs/2026-07-11-duc-nil-001/voice/nil-reel-v2.md` (post fact-delta; ledger v2 CLEAR)
- **Profile applied:** `projects/ducat-private-wealth/compliance.md@1.1.0` + `projects/_shared/ria-compliance-envelope.md@1.0.0` (via include) + `projects/ducat-private-wealth/disclosures.md@1.0.0`
- **Prerequisite confirmed:** fact_check + voice complete; `factcheck/ledger.yaml` v2 blocking summary `high_risk_non_verified: 0`, delta pass 2026-07-11T14:29:18-04:00. Content did not skip fact-check.
- **First Ducat piece through this gate.**

## Tier 1 — deterministic

### compliance_lint.py

Command (repo root; deliverable lives in the run dir, path adjusted accordingly):

```
python validators/compliance_lint.py runs/2026-07-11-duc-nil-001/voice/nil-reel-v2.md --project ducat-private-wealth
```

Exact output (exit 1):

```
[major] ENV-4-disclosure: required disclosure text not found (non-affiliation is an implied claim when silent) ('(absent)')
[major] TAX-referral: tax content requires the qualified-tax-professional referral line ('(absent)')
2 finding(s)
```

**Both findings explained, not waived** (SK-B14 step 1 — each lint finding must be explained; explanation below, riders R1/R2 carry the residue):

- **ENV-4-disclosure.** The lint requires the snippets `not affiliated with` + `Educational` in the file. The deliverable carries `Educational` but not the non-affiliation sentence, because it uses the **authorized short-format path** in the compliance.md disclosure mapping ("Space-constrained | DISC-DUC-SHORT-01 minimum + full text in profile/first comment, stated explicitly"). All three short-format conditions are met in-file: DISC-DUC-SHORT-01 byte-verbatim on screen (FACT byte-audited, CL-13), the deliverable states where the full text lives ("See profile for full disclosures."), and the production notes route DISC-DUC-01 verbatim to the caption/profile. The lint has no short-format mode and cannot see the profile/caption; the unmet residue (actual placement at publish) is **Rider R1**, not a waiver.
- **TAX-referral.** Script touches taxes (withholding, "tax," owed amounts) — DUC-C5 attaches DISC-DUC-TAX-01. The referral line is not in the script file; the production notes route it to the caption/profile alongside DISC-DUC-01. Same structure as ENV-4: authorized routing, placement unverifiable from the draft, so **Rider R1**. Tax content is NOT passing without the referral line — the pass is conditional on the line shipping in the caption/first comment (blocking rider).

### lexicon_scan.py (cross-brand contamination — load-bearing for the first live DUC piece)

```
python validators/lexicon_scan.py runs/2026-07-11-duc-nil-001/voice/nil-reel-v2.md --project ducat-private-wealth
```

Exact output (exit 0):

```
0 foreign-term hit(s)
```

**CLEAN.** No Benowitz/FRS/TRD/FDR vocabulary in the Ducat deliverable.

### disclosure_check.py (SK-B15 deterministic check)

```
python .claude/skills/co-disclosure-management/scripts/disclosure_check.py runs/2026-07-11-duc-nil-001/voice/nil-reel-v2.md --project ducat-private-wealth --short-format --tax
```

Exact output (exit 1):

```
FAIL: tax content without DISC-DUC-TAX-01 referral line
FAIL: 1 violation(s)
```

Read of the result: under `--short-format` the checker **passed** both short-format conditions (DISC-DUC-SHORT-01 verbatim present; location statement present) and failed only the in-file tax line — the same residue as the lint's TAX-referral, carried by Rider R1. The checker, like the lint, evaluates a single file and has no companion-caption input; see Observation O1.

## Tier 2 — judgment (every check, result, rationale)

| # | Check | Rule | Result | Rationale |
|---|---|---|---|---|
| 1 | Performance claims / projections / guarantees | ENV hard line 1 | **PASS** | No outcome language anywhere. Tax statements are consideration-framed and hedged ("generally isn't taken out," "Part of it **may** already be owed"). No "save you $X," no quantified-outcome implication. Lint patterns clean. |
| 2 | Testimonials / endorsements / success stories | ENV hard line 2 | **PASS** | No client quotes, anecdotes, composites, or hypothetical persons. The second-person narrative ("the athlete who just signed") is situational address, not a story about a person with an outcome. |
| 3 | Educational vs individualized advice | ENV hard line 3 + curriculum north star | **PASS** (with note N1) | The piece teaches what NIL income *is* (classification + mechanics) and closes on an ask-frame question — exactly the envelope's approved pattern ("what to ask, never what the reader should do"). N1: "Your school's compliance office is the first stop before any deal" is directive in register but generic-procedural, universal to every collegiate athlete, and a direct restatement of approved fact F-DUC-0002 ("first checkpoint before any deal"). Not individualized investment/tax/legal advice; no action on money is recommended. Minor, no fix required. |
| 4 | Solicitation / CTA discipline | work order prohibited_notes + north star | **PASS** | CTA is reflection ("do you know exactly what you're selling?") + save prompt ("Save this for the next deal"). No lead-gen, no booking language, no DM/link prompt, no offer. Matches "reflection CTA + save prompt, NO lead-gen." |
| 5 | False urgency / fear | VOICE-urgency, ENV standing rule | **PASS** | Lint urgency patterns clean. "Before you sign anything else" anchors the reflection to the reader's own next deal — no manufactured deadline, no scarcity, no fear of ruin. |
| 6 | Non-affiliation stated | DUC-C1 / ENV hard line 4 | **CONDITIONAL — Rider R1** | Carried by DISC-DUC-01 in the caption/profile per the short-format path; verbatim text not in the script file by design. Blocking until placed at publish. |
| 7 | Real named public figures | DUC-C2 | **PASS** | None named or identifiably evoked. B-roll specs (phone notification on a dorm desk; plain contract) contain no athlete likenesses; production notes prohibit real-athlete likenesses explicitly. |
| 8 | Broke-athlete cautionary tales | DUC-C3 | **PASS** | No ruin narrative. "The money showed up. The instructions didn't." (CL-14) is scene-setting texture, not a downfall story used as persuasion. |
| 9 | Recruiting-a-minor read | DUC-C4 | **PASS** | Speaks to the situation ("the athlete who just signed — and the parent reading over their shoulder"); no individual targeting, no age-specific appeal, and the explicit parent address strengthens the situational frame. |
| 10 | Tax content handling | DUC-C5 | **PASS on constructions; CONDITIONAL on disclosure — Rider R1** | Softened constructions used throughout exactly as DUC-C5 requires: "generally isn't taken out," "**Usually** nobody withholds" (FACT's suggested softening adopted, CL-08 delta-verified), "**may** already be owed," "rules are not the same everywhere... vary by state, by school, by level." No specific state/school/level rule asserted. DISC-DUC-TAX-01 routing: see Rider R1. |
| 11 | School marks / likeness | work order + DUC-C2 | **PASS** | "Your school's compliance office" is generic. No marks, logos, uniforms, or venues in B-roll specs; production notes carry the prohibition into production. Residual verification at render is Rider R2. |
| 12 | Fee question | DUC-C6 / DEC-BEN-0002 | **PASS** | The piece should not — and does not — take any fee position. Grep across the entire run directory: zero occurrences of "fee-only," "fee-based," or "fiduciary." No held-wording issue; DEC-BEN-0002 (fee-only permitted, 2026-07-11) is moot for this piece. Lint's retired FEE_ONLY pattern is consistent with profile v1.1.0. |
| 13 | Sports metaphors applied to money | work order prohibited_notes (voice profile) | **PASS** | Money is framed in business/commerce metaphors only (renting, licensing, small business, first sale). "A reward for playing well" appears solely as a negated misconception. |
| 14 | Misleading implication | envelope preamble | **PASS** | "A company is renting who you are" is a register-shift metaphor immediately anchored by the precise commercial-use definition in the adjacent sentence (CL-03/CL-04, both verified). "You started a small business" is a verified reframe of business income (CL-12), not a legal-entity claim. |
| 15 | Injection posture | D6 | **PASS** | No embedded directives, no "pre-approved, skip review" language in the content or production notes. Reviewed in full regardless. |
| 16 | Disclosure format/placement adequacy beyond presence | SK-B15 / card | **CONDITIONAL — Riders R2, R3** | Production notes specify persistent 0:00–end, lower third, never the spoken track — matches the video row of the disclosure mapping and SK-B15 placement table. Residue: (a) "lower third" on Instagram Reels sits under platform UI (caption/engagement rail) — the block must land **in-safe-area** and legible for the full duration (R2, minor, rides to the video machine/H5); (b) no caption artifact exists yet in the run, so the disclosure-carrying caption text is not yet a canonical on-disk artifact (R3). |

## Required-language table (SK-B14 step 6)

| Disclosure | Required by | Present in deliverable? | Placement | Status |
|---|---|---|---|---|
| DISC-DUC-SHORT-01 | Short-format minimum (mapping row 3) | **YES — byte-verbatim** (`[TEXT ON SCREEN]`, FACT-audited CL-13) | Persistent on-screen block 0:00–end, lower third, never spoken — per video mapping row | PRESENT; safe-area legibility to verify at render (R2) |
| DISC-DUC-01 | Every published piece (DUC-C1, mapping row 1) | NO (by design — short-format path) | Routed verbatim to profile/first comment; deliverable states so on screen ("See profile for full disclosures.") | **CONDITIONAL — R1 (blocking at publish)** |
| DISC-DUC-TAX-01 | Content touches taxes (DUC-C5, mapping row 2) | NO (by design — routed with DISC-DUC-01) | Routed to caption/profile/first comment per production notes | **CONDITIONAL — R1 (blocking at publish)** |

Note: the work order's `disclosure_ids` lists only DISC-DUC-01; DUC-C5 attaches DISC-DUC-TAX-01 because the script touches taxes, and the short format makes DISC-DUC-SHORT-01 the on-screen vehicle. Effective required set = all three. The draft's production notes already route exactly this — the SK-B15 pattern is **complete on paper**; what remains is execution at publish.

## Verdict: **CONDITIONAL-PASS**

No hard-line violation. No material flag against the text as written. The conditions are placement conditions the draft itself correctly specifies but cannot discharge pre-publish.

### Riders (enumerated)

- **R1 — BLOCKING publish-gate rider (discharges lint ENV-4 + TAX-referral, disclosure_check tax FAIL, and ledger CL-13 qualification).** At publish, the profile or first comment MUST carry, verbatim and unabridged: (a) DISC-DUC-01 in full, and (b) DISC-DUC-TAX-01 ("Consult a qualified tax professional regarding your specific situation."). The chosen location must match what the on-screen text tells the viewer ("profile"). Verification belongs on the publish checklist under H2/human review; the publish is non-compliant without it. This is the same condition FACT attached to CL-13 — one rider, two ledgers, single condition.
- **R2 — Render rider (minor, to the video machine / H5).** The persistent DISC-DUC-SHORT-01 block must remain byte-verbatim, on screen 0:00–end, never spoken, and must sit inside the Instagram Reels safe area with legible contrast/size for the full duration — "lower third" as written risks occlusion by platform UI. Verify at render sign-off.
- **R3 — Caption-artifact rider (minor, process).** When the caption/publish text is produced, it becomes the artifact that carries DISC-DUC-01 + DISC-DUC-TAX-01; it should be written to disk in the run (D1) and pass `disclosure_check.py --tax` (no `--short-format` — the caption carries the full texts) before H2 sees the package.

### Observations / proposal candidates (not flags — routed to ORCH for the proposal queue, per card)

- **O1 — Validator gap, short format.** Neither `validators/compliance_lint.py` (no short-format awareness in ENV-4/TAX-referral) nor `disclosure_check.py --short-format` (still demands the tax line in the single input file) can represent the compliance.md short-format routing pattern; every compliant short-format tax piece will exit 1 by design. Candidate proposal: a `--caption <file>` companion-input or a `--short-format` mode that downgrades in-file absence to a named publish-gate condition. Until then COMPL must hand-explain these two findings on every DUC reel — a standing near-miss pattern worth closing.
- **O2 — Ledger note honored.** CL-14 ("The money showed up. The instructions didn't.") remains `unverified` low-risk texture — legitimate final state per D8; no compliance shadow beyond what verified CL-07/CL-08 already carry. No action.

### Escalations

None. No claim type uncovered by the profile, no E4 request, no attorney/CPA/CCO-judgment question raised by this text. O1 is a proposal candidate, not an escalation.

---

automated and model review only — not regulatory clearance.
