# QA notes — run 2026-07-11-duc-nil-001 — RUB-SCRIPT-1 applied by QA

Target: `voice/nil-reel-v2.md` (post fact-delta; ledger v2). **First Ducat
script through this gate** — these scores are the DUC lane's baseline; every
future DUC script comparison inherits them. Scored deliberately against the
DUC register (composed; fewer words, more weight), not the BEN one, and not
anchored to BEN's 9.6. Validator results read from the chain where recorded
(D1); deterministic checks re-run by QA where the rubric feeds on them
directly (HK3-scope scripts only). No content touched (D4).

## Required criteria (pass/fail, blocking)

- **R1 Factual accuracy — PASS (ledger-fed + re-validated).**
  `factcheck/ledger.yaml` v2 blocking summary: `high_risk_non_verified: 0`.
  All nine high-risk claims verified (8) or verified-with-qualification (1:
  CL-13, disclosure placement conditional at publish — inside the allowed
  status set). QA re-ran `ledger_validate.py --deliverable` against v2:
  `VALID: ledger.yaml (0 violation(s))` — on-screen byte-presence,
  evidence-refs, and blocking-summary recomputation all hold. CL-14
  (low-risk texture) is `unverified` — a legitimate final state per D8, not
  a high-risk violation.
- **R2 Compliance — PASS, conditional structure noted (COMPL-fed; not
  re-litigated).** COMPL verdict: **CONDITIONAL-PASS** — no hard-line
  violation, no material flag against the text as written; riders R1
  (BLOCKING at publish: DISC-DUC-01 + DISC-DUC-TAX-01 verbatim in
  profile/first comment), R2 (render safe-area, H5), R3 (caption artifact to
  disk). The rubric's literal "lint clean" is not met (compliance_lint exit
  1, 2 findings) — but COMPL adjudicated both findings as artifacts of the
  **authorized short-format disclosure path** the validators cannot
  represent (COMPL O1: every compliant short-format tax piece exits 1 by
  design), explained-not-waived, residue carried by blocking Rider R1.
  Mirrors the BEN precedent (conditional-pass with publish-gate conditions
  riding to H2/H5 scored R2 pass). QA reads the chain's verdict; the rubric
  wording gap is logged as an observation, not silently rounded over.
- **R3 Duration — PASS (validator, QA-run).** `duration_check.py`:
  `PASS: 191 spoken words (band 170-200 for reel-90s, ~90s est)`. Note:
  VOICE's change-log hand-count says 190 — a trivial tokenizer difference,
  in-band either way; the validator number is the number of record.
- **R4 Disclosure — PASS on the deliverable, rider-carried at publish.**
  DISC-DUC-SHORT-01 byte-verbatim on screen (FACT byte-audited at CL-13;
  ledger_validate independently confirms byte-presence); location statement
  present ("See profile for full disclosures."); persistent-placement spec
  (0:00–end, never spoken) matches the disclosure-mapping video row.
  `disclosure_check.py --short-format --tax` (COMPL-recorded) passed both
  short-format conditions and failed only the in-file tax referral line —
  the same single residue Rider R1 carries: DISC-DUC-TAX-01 rides to the
  caption/profile by design and cannot be discharged from the script file.
- **R5 Structure — PASS (validator, QA-run).** `structure_check.py
  --project ducat-private-wealth`: `PASS: 0 finding(s)` — beats present,
  single CTA, timecode + delivery markers on every block.
- **R6 Contamination — PASS (validator, QA-run — load-bearing for the first
  live DUC piece).** `python validators/lexicon_scan.py
  runs/2026-07-11-duc-nil-001/voice/nil-reel-v2.md --project
  ducat-private-wealth` → `0 foreign-term hit(s)`, exit 0. No
  Benowitz/FRS/TRD/FDR vocabulary in the Ducat deliverable. Matches COMPL's
  recorded run; QA's independent run is the R6 result of record.

No required failure exists, so no averaging question arises.

## Scored dimensions (1–5 against RUB-SCRIPT-1 anchors, DUC register)

**Hook — 5.** "Your first NIL check is not a paycheck. It only looks like
one." One breath for the load-bearing sentence; names a specific stake (the
viewer's own first NIL check, second person); a quiet contradiction of the
viewer's default category, which earns the next five seconds on genuine
tension rather than borrowed urgency. No banned opening, no manufactured
countdown, no question-nobody-asks. This is the anchor-5 pattern, and it is
the DUC register doing the grabbing — composure as the hook, kin to
VX-DUC-0001's "the part nobody posts about."

**Clarity — 5.** A distracted first-time viewer can restate the lesson in
one sentence — the TURN hands it to them: "You didn't receive free money.
You started a small business." No unexplained jargon anywhere (the script
teaches withholding mechanics without ever saying "1099" or "W-2" — the
mechanism is described, not name-dropped). Every beat is plain, single-idea
declaratives. No muddy beat found on three read-throughs.

**Logical flow — 4.** Beat-level chain is genuinely progressive:
misconception (BEAT ONE) → correct definition (BEAT TWO) → consequences
nobody stated (BEAT THREE) → reframe (TURN), and the TURN genuinely
reframes — "started a small business / first sale" recasts everything
prior, and the CTA question ("what you're selling") exits directly from it.
Held from 5 by one interior seam: BEAT THREE bundles two threads —
withholding mechanics, then rules-variance/compliance-office — joined by a
bare "And the rules are not the same everywhere." The second thread is
structurally mandated (F-DUC-0002 must pair with F-DUC-0001) but is
additive rather than necessitated at that point, and does not feed the
TURN. Above anchor-3 (the beats themselves could not shuffle without
damage); not seamless anchor-5.

**Educational value — 5.** Teaches exactly what the pre-money audience
does not know: the check's legal character (commercial use of NIL), its tax
mechanics (no withholding, part already owed), and the governing-rules
variance with a concrete first move (compliance office before any deal).
Specific over general throughout — "renting who you are," "the full amount
lands in your account," "vary by state, by school, by level." The
no-dollar-figures constraint (DUC-C5/structural-claims-only) does not cost
checkability: the definitional and mechanism claims are checkable against
statute and IRS treatment, and all are ledgered.

**Personal voice — 5.** Deterministic half (VOICE-recorded,
voice_fingerprint.py): median 7, p90 14 ≤ 18, grade 5.2, zero banned
openings, zero avoided phrases — PASS. Judgment half, scored by QA against
VX-DUC-0001..0010: the piece sits inside the exemplar register — flat
declaratives that end early ("There's a contract underneath it."), the
unglamorous specific named (compliance office, withholding, the contract
underneath), zero performed enthusiasm about a check the audience is
excited about (the brand's defining posture, VX-DUC-0009), zero sports
metaphors — money framed only in commerce terms (renting, licensing, small
business, first sale), with "a reward for playing well" appearing solely as
a negated misconception. "The money showed up. The instructions didn't."
is exemplar-ceiling compression, kin to VX-DUC-0002's "Same number on the
check. Different job to do after it arrives." Nearest kin overall:
VX-DUC-0002 (teaching the paycheck/1099 distinction by compression).
Resemblance ≥4 comfortably; no rejected DUC exemplars exist yet to
negative-check against (none exist for this project — noted, not skipped).
The STAKES parent-aside reads warmth ~3 against the PROPOSED slider 2 —
that is a slider-calibration question for Wes (VOICE's note 3), not a
fingerprint failure; sliders are ⚑ PROPOSED, and the prose profile
supports the line.

**Spoken cadence — 4.** Short declaratives make the piece speakable at
reel pace; pauses land after claims ("That makes it business income." /
"They change often."). Held from 5 by one flagged spot: "None of that is
what this is." (BEAT ONE) — the demonstrative stack is a delivery risk at
pace and needs the emphasis the text doesn't mark; VOICE's own
kept-with-delivery-note call confirms the text alone doesn't carry it.
One spot, not "two or three" — between anchors, resolves to 4.

**Platform fit — 5.** Reel-native throughout: hook inside the first two
seconds of spoken track, 10–20s beat lengths with timecodes, [TO CAMERA] /
[VO / B-ROLL] alternation for visual variety, ~191 words ≈ 88–91s against
the 90s format, persistent on-screen disclosure block (never spoken), and
a save-prompt close — the natively Instagram-shaped CTA mechanic for
education content the viewer returns to. No essay pacing, no
webinar-style enumeration.

**CTA quality — 4.** The exit is natural and pressure-free: "do you know
exactly what you're selling?" is the TURN's own question, and "before you
sign anything else" anchors to the reader's next deal rather than a
manufactured clock (COMPL check 5 concurs). Held from 5 on the rubric's
own letter: reflection question + "Save this for the next deal." is two
imperatives, and anchor-1 names "two asks" without a carve-out for a
mechanical save prompt. The pair is work-order-mandated (reflection CTA +
save prompt, curriculum north star) and the voice profile's reels pattern
("single ask, spoken") is satisfied by the single spoken question — so
this is nowhere near the anchor-1 failure the rubric is aiming at, but QA
scores the artifact against the rubric as written, not the mandate.
Scored 4; rubric-ambiguity observation filed (O-3 below) rather than
inflated to 5.

**Source quality — 5.** Every material claim traces to approved facts
resting on tier-1 sources: F-DUC-0001/F-DUC-0002 → S-DUC-0007 (Fla. Stat.
§1006.74, statute text + amendment history), F-DUC-0004 → S-DUC-0008
(IRS), with S-DUC-0001 (own approved caption set) as register precedent
only. Approved-facts-only evidence base, live-verified at seeding
2026-07-11 (same day — inside any review window). Time-sensitive exposure
is deliberately structural (no year-specific rules, no figures). The one
unverified claim (CL-14) is low-risk scene texture, not a material claim.

No low-confidence scores; all nine dimensions enter the composite.

**Composite: (5+5+4+5+5+4+5+4+5) = 42/45 → 9.3/10.**

## Golden comparison (the honest first-baseline answer)

The goldens registry holds exactly one golden — GOLDEN-BEN-SCRIPT-001
(benowitz-wealth, RUB-SCRIPT-1, composite 9.6, owner edit distance 0).
**No Ducat golden exists.** The BEN golden is a different brand register
(colleague-warm vs. composed) and is NOT a valid voice or register
comparator for a DUC piece — citing it as "nearest golden" would import
cross-brand drift into the DUC lane's first baseline. It serves here only
as structural/format precedent (same rubric, same reel-90s beat
architecture, both carried a conditional-pass disclosure rider to H2/H5).
Golden comparison for DUC: **none yet — this run is DUC golden candidate
#1 if approved at H2**, mirroring how BEN's first run handled the empty
registry. If H2 approves, QA proposes it via proposals/queue/.

## Regression notes (v1 → v2)

First DUC run — no prior run to regress against; delta is intra-run.
Two VOICE edits, both verifiably non-regressive:
1. CL-08 "Usually nobody withholds for you." — adopts FACT's suggested
   softening verbatim; delta-verified by FACT (v1 qualification
   discharged, now plain verified). Strict improvement on R1 posture.
2. TURN "So" opener cut — cadence gain, no ledger claim touched.
Duration 190→191-by-validator (net-zero by VOICE's count); band held.
All 13 untouched claim texts byte-audited intact by FACT; disclosure
block byte-identical v1→v2. No regression.

## Observations (tagged for MEMC — separated from the verdict)

- **O-1 (publish-checklist, HARD):** COMPL Rider R1 blocks publish — at
  publish the profile or first comment MUST carry DISC-DUC-01 verbatim AND
  DISC-DUC-TAX-01, matching the on-screen pointer ("profile"). Same
  condition as ledger CL-13's qualification — one condition, two ledgers.
  Rides to H2 with R2 (short-block in Reels safe area, legible 0:00–end —
  verify at H5) and R3 (caption text must become an on-disk run artifact
  and pass `disclosure_check.py --tax` before H2 sees the package).
- **O-2 (validator-gap, echoes COMPL O1 + BEN run's lint observation):**
  a fully compliant short-format tax piece exits 1 on both
  compliance_lint (ENV-4, TAX-referral) and disclosure_check
  --short-format (in-file tax line) **by design** — so RUB-SCRIPT-1's R2
  "lint clean" wording is literally unattainable for this whole class of
  deliverable. Two-part candidate lesson: (a) a `--caption <file>`
  companion input for the validators; (b) rubric wording that
  distinguishes "lint clean" from "lint findings adjudicated by COMPL as
  authorized-path residue." Until then this required criterion needs
  hand-explanation on every DUC reel — a standing instability risk for R2.
- **O-3 (rubric ambiguity, CTA):** the curriculum-locked CTA pattern
  (reflection question + save prompt) is two imperatives against
  anchor-1's "two asks" language; QA scored 4, not 5, and did not treat
  the mandate as a rubric override. If the pattern is the curriculum's
  permanent shape, the rubric (or a ratified DUC CTA pattern) should say
  whether a mechanical save prompt counts as an ask. Weight/anchor changes
  are medium-tier lessons.
- **O-4 (calibration, non-blocking):** VOICE's five slider-calibration
  notes for Wes stand (sliders ⚑ PROPOSED); QA's scoring assumed the
  prose profile over the unratified sliders where they diverge (warmth
  aside kept; median 7 under target 9 treated as exemplar-consistent).
  Also: change-log word count (190) vs duration_check (191) — trivial,
  but a canonical counting rule would keep future band-edge calls clean.

## Verdict

**PASS** → manager_review. All six required criteria pass (R2/R4 carry
COMPL's enumerated riders forward — placement conditions the draft
correctly specifies but cannot discharge pre-publish). Composite 9.3/10.
No escalations: no required criterion failed (let alone twice), no
unstable-score ambiguity beyond the O-2/O-3 wording notes, no
validator/judgment disagreement.
