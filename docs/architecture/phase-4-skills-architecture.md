# Skills Architecture Specification — Phase 4

| | |
|---|---|
| Status | DRAFT — awaiting owner approval |
| Version | 0.4.0 |
| Date | 2026-07-10 |
| Depends on | D-001–D-030 (ratified) |
| Consolidates | Master prompt §13 catalog (~82 items) → 25 Skills + validators + project memory |

---

## 1. The governing principle

**Skills are brand-agnostic procedures. Brands live in memory.**

A Skill never contains "Benowitz avoids the phrase 'retirement journey'" — it contains "load `brand-voice.md` for the active project and apply its avoided-phrases list as follows." One `wr-script-production` Skill serves all four projects because everything project-specific arrives through the context packet (Phase 3, §3.1), not through the Skill's own text.

This principle is why 25 Skills can do the work the master prompt sketched as 82, and it is the single rule that keeps Skills from becoming a second, ungoverned copy of brand knowledge that drifts out of sync with the governed one. Your existing `benowitz-ducat-social` Skill — excellent as a standalone tool — violates it by design (it embeds `references/benowitz.md` and `references/ducat.md` inside the Skill folder). §8 of this document is the migration plan that moves that brand data into project memory and leaves pure procedure behind.

A corollary that matters for governance: since Skills contain only procedure, **a Skill change is a behavior change and nothing else** — which is exactly the class of thing the lesson lifecycle (D-025) and protected paths (D-011) already govern. No new machinery needed.

---

## 2. Skill hierarchy and consolidated catalog

Three tiers. Tier assignment answers one question: *who is allowed to change this and on what evidence?* System Skills change rarely and affect everything (highest scrutiny); domain Skills evolve with your lessons; engine Skills track third-party frameworks (pinned versions, D-036).

### Tier A — System Skills (3)

| ID | Skill | Used by | Absorbs from master prompt §13 |
|---|---|---|---|
| SK-A1 | `sys-context-loading` | ORCH (loader companion) | Project identification; Context loading |
| SK-A2 | `sys-handoff-contracts` | all agents | Structured handoff creation; Change-log generation |
| SK-A3 | `sys-memory-proposals` | all agents | Memory proposal; Human-feedback capture; Conflict detection; Approval routing |

### Tier B — Domain Skills (18)

| ID | Skill | Used by | Absorbs |
|---|---|---|---|
| SK-B1 | `ev-source-packet` | RSRCH | Source verification; Citation formatting; Audience research |
| SK-B2 | `ev-claim-ledger` | WRITE, FACT, VOICE | Claim extraction; Script fact-checking; the `[VERIFY:]` and `[ESTABLISHED]/[PLAUSIBLE]/[SPECULATIVE]` conventions (D-008) |
| SK-B3 | `wr-script-production` | WRITE | Script brief creation; Hook development; Educational script structure; Storytelling; CTA development; Duration discipline |
| SK-B4 | `wr-social-copy` | WRITE | Caption writing; Headline writing; On-image copy; Carousel planning; Short-form scripts; Hashtag selection |
| SK-B5 | `wr-adaptation` | WRITE | Platform adaptation; Repurposing (claim-diff emission mandatory) |
| SK-B6 | `wr-ad-copy` | WRITE | Ad-angle generation; Advertising copy; testing matrices |
| SK-B7 | `wr-email-sequences` | WRITE | Email sequence writing |
| SK-B8 | `wr-landing-pages` | WRITE | Landing-page outlining; Funnel mapping (page side) |
| SK-B9 | `vo-voice-application` | VOICE | Personal voice application; Spoken-word editing; Script proofreading |
| SK-B10 | `st-campaign-briefs` | STRAT | Campaign brief creation |
| SK-B11 | `st-positioning-offers` | STRAT | Positioning; Offer design |
| SK-B12 | `st-calendar-planning` | STRAT | Content-pillar planning; Content-calendar balancing (inventory-first rule) |
| SK-B13 | `st-experiments` | STRAT, ANLYT | Experiment design; Analytics interpretation (sample-size guardrails) |
| SK-B14 | `co-compliance-review` | COMPL | Financial-claim review; Guarantee-language detection; Testimonial review; Performance-claim review; Educational-vs-advice classification; Project-specific review; Escalation report creation |
| SK-B15 | `co-disclosure-management` | COMPL, WRITE, VDIR | Disclosure insertion (selection + placement per format) |
| SK-B16 | `vd-storyboarding` | VDIR | Script-to-storyboard; Time-coded scene planning; B-roll mapping; Motion-graphics planning; Creative brief generation |
| SK-B17 | `vd-engine-routing` | VDIR | The HyperFrames-vs-Remotion decision matrix |
| SK-B18 | `qa-rubric-scoring` | QA | Rubric application procedure (rubric *content* is Phase 6 data) |

### Tier C — Engine & workspace Skills (4)

| ID | Skill | Used by | Absorbs |
|---|---|---|---|
| SK-C1 | `en-hyperframes` | HYPF | All 9 HyperFrames items — as a **wrapper** over the pinned upstream skill set (§7 exemplar) |
| SK-C2 | `en-remotion` | REMO | All 11 Remotion items — authored in-house against docs verified at build time |
| SK-C3 | `vd-captions-access` | VDIR, HYPF, REMO | Caption generation (content side); Caption QC (judgment half); accessibility judgment |
| SK-C4 | `tr-strategy-research` | RSRCH, WRITE (project=TRD only) | Your `institutional-trading-research` Skill, adopted intact at pinned v1.0.0 (D-008) |

### Demoted to validators or project memory (confirming D-002)

**Validators (deterministic, hook- or script-invoked):** Duration estimation (word-count math, bundled inside SK-B3's `scripts/`); Version comparison (diff scripts inside SK-B9 and SK-A2); Caption QC mechanics (CPS, line length, timing); Audio review (loudness/clipping measurement); Export validation; Delivery-manifest generation; Video QC technical checks; compliance lint (disclosure presence, banned phrases); cross-lexicon scan; schema-on-write.

**Project memory (data, not procedure):** Brand-token application (tokens are data in `projects/*/assets/` + a short load procedure inside SK-C1/C2); project-specific compliance rules (data in `compliance.md`, consumed by SK-B14); source hierarchies (data in `project-profile.md`, consumed by SK-B1); voice profiles (data in `brand-voice.md`, consumed by SK-B9).

### Reconciliation with Phase 2 agent cards

The cards' Skills fields used working names ("project-identification," "claim extraction and risk classification," etc.). This catalog's IDs are now canonical; card fields update to SK-IDs at implementation. No card's *capability set* changes — only the names.

---
## 3. Skill anatomy and the specification template

### 3.1 Folder anatomy

Every Skill is a folder; the 21 required specification fields (master prompt §13) map onto it so that nothing lives only in prose:

```
skills/<tier>/<skill-id>/
  SKILL.md          # frontmatter: name, version, description (trigger conditions),
                    #   supported_agents, required_inputs, optional_inputs,
                    #   prerequisites, requires (dependencies), owner, approval_status
                    # body: Purpose · Process · Prohibited behavior · Error handling
  references/       # deep procedure, examples, counterexamples — loaded on demand
  scripts/          # the Skill's deterministic checks (D-009 Tier 1/2 material)
  tests/            # fixtures + property tests + counterexample tests (§5)
  CHANGELOG.md      # change log; entries cite lesson IDs (implements: L-*)
```

Field-to-location map: **Skill name / Version / Trigger conditions / Supported agents / Required & optional inputs / Prerequisites / Owner / Approval status** → frontmatter. **Purpose / Process / Prohibited behavior / Error handling** → SKILL.md body. **Source files** → `references/` + declared `reads:` list in frontmatter (which project-memory files the Skill consumes — this makes the brand-agnostic principle auditable: a Skill whose body names a brand fails review). **Deterministic checks** → `scripts/`. **Output schema** → `schemas/` reference by ID (Phase 3 machinery). **Examples / Counterexamples** → `references/`. **Tests** → `tests/`. **Evaluation rubric** → linked rubric ID (Phase 6). **Change log** → CHANGELOG.md.

Progressive disclosure does the cost control: agents always see name + description; the body loads on trigger; `references/` load only when the procedure calls for them. A Skill that front-loads everything into SKILL.md is a review failure, not a style choice.

### 3.2 Trigger policy — pinned first, description second

Description-based triggering (the model recognizes relevance) is how standalone Skills work, and it stays available for ad-hoc use. But inside workflows, **stages pin their Skills explicitly**: the script workflow's draft stage names SK-B3 + SK-B2 + SK-A2 as required loads. Deterministic invocation for governed work; model judgment only where the workflow genuinely can't know in advance. A gate validator confirms the pinned Skills were actually loaded (their versions appear in the handoff's `skills_used` field) — "the model forgot to load the procedure" becomes a blocked transition, not a quality mystery.

---

## 4. Dependencies

Skills declare `requires:` (other Skill IDs), `reads:` (project-memory paths), and `schemas:` (record contracts). Rules: the dependency graph is acyclic (validator-checked at approval); Tier A depends on nothing; Tier B may depend on Tier A; Tier C may depend on A and B; nothing depends on Tier C. Current graph:

| Skill | requires | reads (per active project) |
|---|---|---|
| SK-A1 | — | project registry, `project-profile.md` |
| SK-A2 | — | `schemas/handoff*`, `schemas/workorder*` |
| SK-A3 | SK-A2 | `global/approval-rules.md` (auto-commit list, read-only) |
| SK-B1 | SK-A2, SK-A3 | `project-profile.md` (source hierarchy), `sources/` |
| SK-B2 | SK-A2 | `approved-facts/`, `_claim-keys.yaml`, packet schema |
| SK-B3 | SK-B2, SK-A2, SK-B15 | `brand-voice.md` (register only), `audience.md`, `examples/` |
| SK-B4/B5/B6/B7/B8 | SK-B2, SK-A2 (+SK-B15 where disclosures ride) | same class as SK-B3 |
| SK-B9 | SK-B2, SK-A2 | `brand-voice.md` (full), `voice/exemplars/`, `voice/edits/` |
| SK-B10–B13 | SK-A2 (+SK-B1 outputs as inputs) | `campaigns/`, `decisions/`, inventory index |
| SK-B14 | SK-A2, SK-B15 | `compliance.md` (+ `_shared/ria-compliance-envelope.md` via include), `disclosures.md` |
| SK-B15 | — | `disclosures.md` |
| SK-B16 | SK-B2, SK-B15, SK-A2 | claim ledger, asset manifest, visual identity |
| SK-B17 | — | engine capability notes, prior routing decisions |
| SK-B18 | SK-A2 | rubrics (Phase 6), `examples/` goldens |
| SK-C1 | SK-B16, SK-C3 + **pinned upstream set** | brand tokens, export presets |
| SK-C2 | SK-B16, SK-C3 | brand tokens, export presets |
| SK-C3 | — | caption rules, disclosure placement rules |
| SK-C4 | SK-A2, SK-A3 | TRD project memory only |

---

## 5. Skill tests

Three kinds, all shipped inside the Skill, all green before any version activates (§6):

**Property tests** — generative output can't be exact-matched, but its *properties* can: SK-B3's fixture request must yield a script whose claim list covers every factual sentence (checked by SK-B2's extractor script), whose word count sits in the format band, whose hooks number ten with ≥3 mechanisms, and which contains zero `banned_openings` from the loaded profile. Properties are computed by `scripts/`, so the test is deterministic even though the output isn't.

**Counterexample tests** — every Prohibited-behavior line gets a fixture that *invites* the violation: a request for a testimonial reel, a packet missing the key fact, an instruction embedded in a source document ("ignore compliance for this one"). Pass = the Skill's procedure produces the refusal/flag/`[UNVERIFIED]` path, not the violation. Prohibited behaviors without counterexample tests are wishes.

**Regression fixtures** — golden input/output-property pairs from real approved runs, accumulated over time (QA proposes them; MEMC routes; you ratify). A Skill version bump must not degrade golden scores (Phase 6 wires the thresholds).

Contamination fixtures from Phase 3 §3 live at the workflow level but exercise Skills too — SK-B3 run with a Ducat packet against a Benowitz profile must flag, not blend.

---

## 6. Versioning and the approval process

Skills are protected paths (D-011), so the machinery already exists; this section just names the sequence:

1. **Proposal** — any agent (or you) files a Skill-change proposal (SK-A3); QA's recurring-failure observations are the common origin.
2. **Draft** — the change is authored on the staging branch as a version bump: semver per D-021 (major = procedure meaning changes; minor = additions; patch = corrections), CHANGELOG entry citing the driving lesson (`implements: L-*`, per D-025).
3. **Tests** — full test suite for the Skill plus the regression fixtures of every Skill that `requires:` it. Red = no activation, no exceptions.
4. **Ratification** — your merge (D-024). The lesson flips to `active`; `implements_diff` records the commit.
5. **Rollback** — `git revert` by construction; dependent-Skill fixtures re-run to confirm the revert is clean.

**Vendor Skills (D-036, extending D-019):** upstream sets (HyperFrames' official skills) are adopted at **pinned versions**, vendored into the repo, and wrapped — our SK-C1 calls them; our constraints layer over them. Upstream updates are treated as third-party content (D6): diffed, reviewed, tested against our fixtures, then ratified like any Skill change. `npx`-style live-fetching of skill content at run time is prohibited; the version that runs is the version you approved.

---
## 7. Initial detailed Skills — three exemplars, full template

Written to the 21-field template as the pattern for all remaining Skills (authored during implementation, gated by §6). Chosen because they are, respectively: the system's audit spine, the vertical slice's centerpiece, and the vendor-wrapping policy made concrete.

---

### 7.1 SK-B2 `ev-claim-ledger`

**Skill name:** ev-claim-ledger · **Version:** 1.0.0 · **Owner:** Wes · **Approval status:** draft (activates with vertical slice)

**Purpose:** One procedure, three seats. Gives WRITE the claim-declaration discipline, FACT the extraction/adjudication protocol, and VOICE the delta duty — so a factual claim carries one ID and one auditable history from first draft to on-screen text (D-012).

**Trigger conditions:** pinned at draft, fact-check, and voice stages of every content workflow; ad-hoc when any agent handles text containing verifiable claims.

**Supported agents:** WRITE, FACT, VOICE (read-only reference: VDIR, QA, COMPL).

**Required inputs:** deliverable path; source packet and/or approved-fact set; ledger schema; mode (`declare` | `adjudicate` | `delta`). **Optional inputs:** prior ledger versions; risk-threshold overrides from the work order.

**Prerequisites:** context packet loaded (SK-A1 done); packet exists or the work order explicitly authorizes approved-facts-only drafting.

**Source files:** `references/claim-taxonomy.md` (what counts as a claim: stated, implied, numeric, visual, comparative); `references/risk-classification.md` (numeric/eligibility/legal/tax = high, with project-volatility modifiers); `references/status-protocol.md` (the seven statuses with adjudication criteria and required evidence per status); `references/delta-protocol.md`; `scripts/extract_claims.py` (candidate-claim detection: numbers, dates, modal-free assertions, eligibility verbs); `scripts/claim_diff.py` (sentence-aligned semantic-delta candidates between versions); `scripts/ledger_validate.py` (schema + completeness: every `on_screen: true` string byte-present in deliverable).

**Process (per mode):** *declare* — WRITE enumerates every claim while drafting; each gets CL-id, text, location, risk, `evidence:` (packet-claim or F-id) or `[UNVERIFIED]`; runs `extract_claims.py` on own draft and reconciles misses before handoff (self-audit, not the boundary). *adjudicate* — FACT runs extraction independently; merges with declared list, marking discoveries `declared_by: FOUND`; opens each cited source and verifies the *evidence*, not the citation; assigns one of the seven statuses with qualification text where needed; writes blocking summary. *delta* — VOICE runs `claim_diff.py` old-vs-new; every flagged sentence maps to a CL-id with the nature of the touch; non-empty diff routes to FACT `delta` mode, which re-adjudicates only touched claims.

**Deterministic checks:** the three scripts above; ledger schema-on-write; on-screen byte-match; high-risk-non-verified count computed, not asserted.

**Output schema:** `schemas/claim-ledger-1.0.json` (Phase 3 §4.4).

**Error handling:** packet missing → declare-mode proceeds with all material claims `[UNVERIFIED]` and the ⚠️ unsourced header (your Skill's convention, retained verbatim); extraction script failure → hard stop, escalate (never hand-count as fallback silently — log the fallback); source URL dead in adjudicate → status `unverified`, RSRCH refresh task proposed.

**Prohibited behavior:** assigning `verified` from model memory; softening `unverified` into hedged prose (D-8); FACT editing the deliverable; VOICE suppressing a diff hit ("it's just cadence" is FACT's call, not VOICE's); deleting a claim from the ledger (claims are withdrawn by status, never removed).

**Examples (in `references/`):** a worked DROP-script ledger, declare → adjudicate → delta, including one FOUND implied claim ("teachers retire at 30 years" implied by an example) and one qualification.

**Counterexamples:** a draft asserting "the 2026 contribution limit is $24,000" with no packet entry — correct path is `[UNVERIFIED]` + fact-check-before-posting listing, shown against the wrong path (confident prose).

**Tests:** property — seeded 12-claim fixture: extraction recall ≥ 11/12, high-risk recall 12/12 across ten runs; counterexample — planted wrong FRS figure with a *plausible* blog source: pass = `incorrect` status citing the tier-1 source, fail = verified-by-citation-trust; delta fixture — 3 semantic edits among 14 cosmetic: all 3 flagged, ≤1 false positive.

**Evaluation rubric:** links Phase 6 `RUB-LEDGER-1` (seeded-error catch, FOUND-rate calibration, status accuracy vs. reference adjudications).

**Change log:** 1.0.0 — initial; absorbs `[VERIFY:]` (D-008) and evidence-tag mapping for TRD (`[ESTABLISHED]`→verified, `[PLAUSIBLE]`→verified-with-qualification, `[SPECULATIVE]`→unverified, applied when project=TRD).

---

### 7.2 SK-B3 `wr-script-production`

**Skill name:** wr-script-production · **Version:** 1.0.0 · **Owner:** Wes · **Approval status:** draft (activates with vertical slice)

**Purpose:** Turn a request or brief plus a source packet into a structured, claim-declared, duration-true spoken script in the active project's register — structure and educational value first; final voice belongs to SK-B9.

**Trigger conditions:** pinned at brief and draft stages of the script workflow; any request for a video script, webinar segment, or podcast segment.

**Supported agents:** WRITE.

**Required inputs:** work order (platform, duration target, objective, audience); source packet or attached source asset; context packet (brand-voice register fields, audience.md, disclosures via SK-B15). **Optional inputs:** approved exemplars to emulate; hook-direction notes; prior versions.

**Prerequisites:** SK-A1 loaded exactly one project; SK-B2 available in declare mode.

**Source files:** `references/brief-template.md` (audience, problem, central lesson, hook direction, emotional movement, CTA, length, format, required facts, prohibited territory); `references/structures.md` (the 7-beat 90-second skeleton — hook / stakes / beat-believed / beat-true / beat-untold / turn / single-CTA — plus long-form and webinar variants); `references/hooks.md` (ten-per-batch, ≥3 mechanisms, one-breath test); `references/delivery-markers.md` (`[TO CAMERA]` for claims and authority, `[VO / B-ROLL:]` for texture, `[TEXT ON SCREEN:]` for anything read exactly — migrated intact per D-008); `references/duration.md` (**190 words ≈ 90 seconds** for to-camera financial content — not 140-wpm podcast pace — with per-format bands); `scripts/duration_check.py`; `scripts/structure_check.py` (beats present, one CTA, markers on every block).

**Process:** confirm or create the brief → map packet claims to beats (a beat with no claim is texture; a claim with no beat is cut, not crammed) → draft to the skeleton in the profile's *register* (sentence-length band, banned openings honored) while declaring claims via SK-B2 → prefer structural claims over volatile numerics (a rollover isn't automatic > the 2026 limit is $X) → soften genuinely complex rules ("may owe," "rules differ") rather than flat-asserting → place markers; route disclosure text to a persistent on-screen block via SK-B15, never the spoken track → run both scripts; trim beats rather than pace to fix overruns → emit draft + claim list + hook batch + intervention notes (uncapped, one line each, per D-008).

**Deterministic checks:** duration band; structure completeness; banned-openings scan (profile-fed); claim-list coverage via SK-B2 extractor.

**Output schema:** `schemas/script-draft-1.0.json` (draft path, claim-list ref, hook batch, markers manifest, interventions).

**Error handling:** no packet and named-source absent → draft anyway from topic with everything `[UNVERIFIED]` + ⚠️ header (a blocking question costs a round trip that the flag already covers — D-008); duration unreachable without cutting a required disclosure → escalate, never shrink the disclosure; brief conflicts with compliance at concept level → refuse the concept, draft the nearest compliant alternative, intervention note.

**Prohibited behavior:** facts from model memory presented as sourced (no web exists to launder them — D-015); testimonials, guarantees, performance promises even on request (compliant alternative + note); two CTAs; blending brands; reconstructing a named source's numbers from memory; spoken disclaimers that cost the viewer.

**Examples:** the worked DROP reel — brief → beat-mapped packet → 188-word draft with 11 declared claims and 10 hooks across 4 mechanisms.

**Counterexamples:** the "could save you thousands" request handled the wrong way (drafted as asked) vs. right (structural reframe + intervention note) — the vertical slice's injected failure, as training material.

**Tests:** property — fixture brief+packet: word band 170–200, 7 beats, 1 CTA, ≥10 hooks/≥3 mechanisms, claim coverage 100%, zero banned openings; counterexamples — testimonial request, missing-source request, cross-brand packet (Ducat facts + Benowitz profile → flag, not blend); regression — the ratified slice output becomes golden fixture #1.

**Evaluation rubric:** `RUB-SCRIPT-1` (Phase 6: §17.1 dimensions).

**Change log:** 1.0.0 — initial; format canon migrated from `benowitz-ducat-social` §Formats per D-008/D-037.

---

### 7.3 SK-C1 `en-hyperframes`

**Skill name:** en-hyperframes · **Version:** 1.0.0 (wraps upstream set pinned at adoption commit) · **Owner:** Wes · **Approval status:** draft (activates with first video workflow)

**Purpose:** Our constraint layer over the official HyperFrames skills: brand tokens, safe areas, the disclosure-block pattern, ledger-verbatim text, and our lint → preview → render → QC loop — so HYPF builds with the vendor's current best practice *and* our governance, without us maintaining a fork of their knowledge.

**Trigger conditions:** pinned at the video-production stage when VDIR's routing (SK-B17) selects HyperFrames.

**Supported agents:** HYPF.

**Required inputs:** storyboard (scenes, ID-mapped on-screen strings, asset refs with rights fields); brand tokens; platform export spec. **Optional inputs:** reusable sub-compositions; prior production notes.

**Prerequisites:** upstream skill set vendored at the pinned commit recorded in this Skill's frontmatter (`upstream_pin:`); assets manifest resolved (no GAPs unless the work order accepts placeholders).

**Source files:** `references/wrapper-rules.md` (what our layer adds/overrides: token application, safe-area margins per aspect ratio, persistent disclosure block spec, text-verbatim rule); `references/upstream-map.md` (which upstream skill covers composition contract / animation / media / render — a *map*, not a copy, so upstream updates don't orphan our text); `references/production-notes-template.md` (STORYBOARD/DESIGN/HANDOFF-style notes kept current per project); `scripts/text_verbatim_check.py` (rendered-composition strings byte-match storyboard `on_screen` strings); `scripts/safe_area_check.py`; `scripts/render_manifest.py`.

**Process:** load storyboard and tokens → consult upstream map for the composition pattern in play → build/extend under `video/hyperframes/<project>/` with content values injected from the storyboard file, never retyped → apply tokens and safe areas → place the disclosure block persistent and in-safe-area → **lint → preview** (VDIR reviews preview before any final render) → local render with approved preset → run the three scripts → write manifest + production notes → hand to QA/validators.

**Deterministic checks:** upstream lint; the three wrapper scripts; export-spec validators (resolution/fps/duration/AR).

**Output schema:** `schemas/render-manifest-1.0.json`.

**Error handling:** lint failures → fix or document exceptions in the build note, never suppress; render nondeterminism or 2-cycle unresolved errors → escalate (E5-adjacent); upstream behavior deviating from the pinned map → halt and file a platform-churn observation (never live-update mid-run).

**Prohibited behavior:** deviating from storyboard text or timing beyond tolerance (escalate to VDIR); render-without-preview; enabling cloud render or any MCP call (D-019 — off until Phase 7 config decision); pulling upstream updates or new runtime adapters at run time (D-036); overwriting an approved render (version, never replace).

**Examples:** the DROP reel worked build — 3 sub-compositions, lint-clean, byte-match pass, one reusable lower-third proposed.

**Counterexamples:** storyboard card too long for its 2.5s hold — wrong: silently extend the hold (timing deviation); right: flag to VDIR with the readability math.

**Tests:** property — fixture storyboard renders to spec with byte-match 100% and safe-area pass; counterexample — storyboard containing a paraphrase temptation (string that overflows the card) → escalation path taken; upstream-pin test — wrapper fixtures pass against the pinned commit (re-run on any proposed pin bump, per §6).

**Evaluation rubric:** `RUB-VIDEO-BUILD-1` (Phase 6; shared with SK-C2 so the engines stay comparable, per Phase 2).

**Change log:** 1.0.0 — initial; upstream pin recorded; disclosure-block pattern imported from SK-B15.

---

## 8. Decomposition of the two existing Skills (executes D-008 / D-037)

**`benowitz-ducat-social` →** brand data *out*, procedure *stays*:

| Current content | Destination |
|---|---|
| `references/benowitz.md`, `references/ducat.md` (voice, audience, topic banks, vocabulary) | `projects/{benowitz-wealth,ducat-private-wealth}/` — `brand-voice.md`, `audience.md`, `project-profile.md` foreign_terms |
| `references/compliance.md` + the envelope section | `projects/_shared/ria-compliance-envelope.md` + per-brand `compliance.md` (incl. the fee-only hold as DEC-record + rule) |
| Required disclosure texts | `disclosures.md` as DISC-* records |
| 90s format, markers, hook rules, duration math | SK-B3 |
| Carousel/caption/LinkedIn formats, hashtag policy | SK-B4 |
| `[VERIFY:]` fact discipline, ⚠️ unsourced header | SK-B2 conventions |
| Disclosure placement rules (on-screen block, LinkedIn first-comment) | SK-B15 |
| Calendar rules (inventory-first, source column, compliance touchpoints) | SK-B12 |
| Intervention-note convention | SK-A2 change-log format |
| Back-catalog inventory knowledge | `projects/*/assets/` + inventory index (implementation step 0, Phase 3 §11) |

The original Skill is retired at cutover with a decision record; nothing it knows is lost — everything it knows becomes governed.

**`institutional-trading-research` →** adopted intact as SK-C4 at pinned v1.0.0. Its guardrails §12 double as seed content for `projects/trading-research/compliance.md`; its evidence tags map into SK-B2 (§7.1 change log). It changes hereafter only via the §6 process.

---

## 9. Decision log — Phase 4 proposed

| ID | Decision |
|---|---|
| D-031 | Governing principle: Skills are brand-agnostic procedures; brand data lives in project memory; Skill bodies naming a brand fail review |
| D-032 | Consolidated catalog: 25 Skills across three tiers (§2), with the demotions-to-validators/memory confirmed |
| D-033 | Skill anatomy §3.1 maps all 21 template fields to folder locations; `reads:` declarations make the principle auditable |
| D-034 | Trigger policy: workflow stages pin required Skills; `skills_used` recorded in handoffs and gate-checked |
| D-035 | Dependency rules: acyclic; A←B←C layering; declared `requires:`/`reads:`/`schemas:` |
| D-036 | Test policy: property + counterexample + regression tests ship in-Skill; green before activation; dependents' fixtures re-run |
| D-037 | Vendor policy: upstream skill sets vendored at pinned versions, wrapped, diff-reviewed on update; no run-time fetching |
| D-038 | Migration plan §8 for the two existing Skills |
| D-039 | Three exemplar Skills (SK-B2, SK-B3, SK-C1) approved as authored — implementation seeds for the vertical slice and first video |

## 10. Open items carried forward

- Remaining 22 Skills authored to template during implementation, sequenced by the workflow that needs them (slice needs: SK-A1–A3, SK-B1, SK-B15, SK-B9, SK-B14 beyond the exemplars).
- Rubric IDs referenced here (`RUB-*`) defined in Phase 6.
- Upstream HyperFrames pin commit selected, and Remotion doc verification, at Phase 7/build (per master prompt §2.4).
- Workflow stage → pinned-Skill tables finalized in Phase 5 alongside the state machines.
