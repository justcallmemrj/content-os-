# Controlled Learning & Evaluations Specification — Phase 6

| | |
|---|---|
| Status | DRAFT — awaiting owner approval |
| Version | 0.6.0 |
| Date | 2026-07-10 |
| Depends on | D-001–D-050 (ratified) |
| Closes open items | rubric content behind every G-R gate; RUB-* IDs from Phase 4; contamination suite requirement from Phase 3; voice-resemblance anchors from D-030 |

Orientation: Phases 3–5 built the learning *machinery* — lessons as records with a lifecycle (D-025), proposals as the only door (Phase 3 §4.8), staging-branch ratification (D-024), never-learn screening at the queue. What was missing is the *content*: how feedback actually gets captured without you filling out forms, what promotes a lesson between statuses, what the rubrics behind the QA gate actually say, which tests patrol which risks, and what happens the day an activated lesson turns out to be wrong. That's this document.

---

## 1. The feedback system — twelve sources, mechanically captured

Design rule: **feedback capture is structural, not clerical.** Eleven of the twelve §16.1 sources fall out of artifacts the system already produces; exactly one asks anything of you, and it's optional.

| Feedback source (§16.1) | Capture mechanism | Lands as |
|---|---|---|
| Your direct corrections / rewritten versions | **Auto-diff at H2/H5**: any edit you make is diffed against the presented version; VOICE analyzes diffs into edit-pair records | VE-* records + rule-candidate proposals |
| Your approvals / rejections | Gate results in the envelope; rejection reason captured free-text or via **optional one-tap tags** (voice-off, too-salesy, wrong-depth, factual-doubt, structural, other) | H2/H5 decision records; tag frequencies in telemetry |
| Compliance feedback | COMPL flags with rule IDs, aggregated by rule across runs | Flag telemetry; profile-gap proposals |
| Fact-check corrections | Ledger statuses + FOUND events + `incorrect`/`outdated` counts by topic | Ledger archive queries; fact-refresh proposals |
| Production errors / QC failures | Validator failure rows + build notes + V-loop counters | SQLite events; recurring-failure observations (QA) |
| Audience performance / campaign performance | ANLYT reports from manual exports (D-007), thresholds in §4 | AR-* reports; hypothesis log; `observed` lessons |
| Repeated workflow delays | Stage-duration telemetry vs. budgets (Phase 5 §8.4) | Timeout-tuning proposals |
| Repeated agent disagreements | `escalation` events + E3 memos, clustered by pair/topic | Disagreement telemetry; rule-gap or Skill-clarity proposals |

**The H2 decision capture, precisely:** when you approve as-is, that's one click and a golden-candidate signal. When you edit, the diff is the feedback — VOICE mines it later, asynchronously (D-046). When you reject, one optional tag or sentence multiplies the value of the rejection but is never required. The system is built to learn from what you were going to do anyway.

---

## 2. The candidate-lesson lifecycle, operationalized

Your §16.2 thirteen steps, mapped to owners and mechanisms, with the promotion criteria that were previously implicit:

| Status transition | Promoted by | Criteria |
|---|---|---|
| (event) → `observed` | any agent via SK-A3 | An observation with at least one concrete instance attached. Cheap by design — observing is free |
| `observed` → `candidate` | MEMC triage | **Either** ≥3 independent supporting instances **or** one explicit human correction (your edits count as explicit); contradiction search performed and recorded even when empty; scope assigned (project/agent/global); class assigned |
| `candidate` → `under-review` | MEMC batch | Never-learn screen passed (§3); risk tier assigned; eval plan attached where the tier requires one |
| `under-review` → `approved` | **you** (via staging digest) | Risk-tiered evidence bar met (below); for rule-class: eval run results attached and green |
| `approved` → `active` | **your merge** | The activation diff exists (D-025): a concrete change to a profile, Skill, or agent `lessons.md`, with `implements:` linkage; dependent fixtures green (D-036) |
| any → `rejected` / `superseded` / `archived` | MEMC (staged) or you | Reason recorded; rejected lessons are retained — they are the system's memory of what *didn't* work |

**Risk-tiered rigor** — the same bar for a phrase preference and a compliance-adjacent rule would either bureaucratize the small or under-protect the large:

| Tier | Examples | Bar to activate |
|---|---|---|
| Low | avoided-phrase addition, transition preference, timeout tuning | Your merge; no eval run required; regression fixtures still re-run |
| Medium | hook-mechanism guidance, structure variants, calendar-balance rules | Scoped eval on ≥5 goldens; no required-criterion change; composite non-regression |
| High | anything touching compliance profiles, disclosures, claim/status protocols, workflow gates, agent boundaries | Full affected-suite run + adversarial subset; explicit side-effects section; and where the change is compliance-substantive, the record notes it reflects **your** judgment or your professionals' — the system proposes wording, never regulatory positions |

**Class routing fix:** a "lesson" of class `fact` is not a lesson — it's a fact proposal and is re-routed to the Phase 3 fact path (source required, claim_key assigned). Lessons change *procedure and preference*; facts change *what's true*. Conflating them is how unsourced beliefs sneak into rules.

---

## 3. Never-learn enforcement — §16.3 item by item

| Never learn from | Enforcing mechanism |
|---|---|
| A single high/low-performing post | ANLYT thresholds (§4) cap performance findings at `observed` until replicated; MEMC promotion criteria require ≥3 instances |
| Temporary platform behavior | Performance lessons require persistence across ≥2 non-overlapping windows (§4); platform-anomaly flag in AR data-quality section blocks promotion |
| An unverified comment | Class routing: audience comments are `observed` color, never evidence; facts require sources (queue validator) |
| An unsupported correction | Corrections without a source become `[UNVERIFIED]`/unsourced-fact bounces, not rules — including yours: your factual corrections get a source request, not blind ingestion (D-8 applies to everyone) |
| A compliance exception | E4/H7 overrides file as DEC records scoped to the deliverable; a validator rejects lesson proposals citing an override DEC as evidence |
| A project preference applied globally | MEMC scope check; ambiguous scope fails toward narrower (Phase 3 fail-toward-review inverted for scope: fail toward *project*) |
| Accidental human wording | Single-instance human phrasing is `observed`; only repeated patterns or explicit "make this a rule" promote |
| A temporary campaign direction | Campaign-scoped guidance lives in the CB record, expires with `closed`; lesson proposals citing only an open campaign are held until close-out |
| A fact with no source | Queue validator auto-bounce (Phase 3 §4.8) |
| Sensitive personal information | S2/S3 screens at the queue (Phase 3 §9.1) |
| Third-party copyrighted content | Excerpt-limit validator at the queue; archiving policy D-029 |

---

## 4. Performance-learning controls (ANLYT thresholds)

Defaults, tunable by proposal with evidence: minimum **n ≥ 20 per comparison arm** for format/hook/topic claims; effect must **persist across ≥2 non-overlapping windows**; every comparison ships the **confound checklist** (topic mix, posting time, platform changes, audience shifts — each marked checked/uncontrolled); causal verbs are reserved for designed experiments (SK-B13) with pre-registered success criteria; anything under threshold is reported as *insufficient-data*, which is a complete answer, not a failure. Performance-sourced lessons enter at `observed` regardless of effect size — replication, not magnitude, promotes them.

---
## 5. Rubric architecture and registry

**Anatomy of a rubric** (`evaluations/rubrics/RUB-*.md`, protected): two sections with different powers. **Required criteria** are pass/fail and blocking — most are validator-fed, so failing one is a fact, not an opinion. **Scored dimensions** run 1–5 with written anchors at 1/3/5 (2 and 4 interpolate); the scorecard reports each dimension plus a weighted composite normalized to /10 for readability. QA may not average a required-criterion failure into a passing composite — that's the whole point of the split.

**Validator-fed vs. judgment:** every dimension declares its input. Duration accuracy, disclosure placement, banned-phrase counts, byte-match — deterministic inputs, QA reads the result. Hook strength, clarity, cadence — judgment against anchors and goldens. A rubric that pretends judgment is measurement fails review (the D-030 discipline, generalized).

**Registry:**

| ID | Gates | Covers (dimensions per master prompt §17) |
|---|---|---|
| RUB-SCRIPT-1 | trunk `qa`, script profile | §17.1 — written in full below |
| RUB-SOCIAL-1 | trunk `qa`, social profile | §17.2: audience relevance, originality, clarity, factual accuracy(R), brand fit, platform fit, visual-copy compatibility(R, validator), compliance(R), engagement potential, CTA quality |
| RUB-MKTG-1 | campaign `assembly_review` + child QA | §17.3: strategic alignment, audience insight, message consistency(R across children, validator-fed), offer clarity, claim support(R), funnel continuity, compliance(R), testability, measurement readiness(R), business relevance |
| RUB-VIDEO-1 | video V8 `judgment_qc` | §17.4: script alignment(R, byte-match), story clarity, pacing, visual quality, brand consistency, caption accuracy(R)+placement judgment, audio quality(R thresholds + judgment), motion quality, technical correctness(R), platform specs(R), rendering integrity(R), accessibility |
| RUB-VIDEO-BUILD-1 | V4–V7, both engines identically | build-note honesty, deviation handling, manifest completeness(R), reuse discipline |
| RUB-LEDGER-1 | FACT meta-eval | seeded-error catch, FOUND-rate calibration, status accuracy vs. reference adjudications |
| RUB-VOICE-1 | voice_edit output + VOICE meta-eval | required: deterministic fingerprint pass (lengths, phrases, readability band); scored: resemblance-to-exemplars, cadence-aloud, register fit; north star tracked: your post-edit distance |

## 6. RUB-SCRIPT-1 — written in full (the exemplar; pattern for the rest)

**Required criteria (pass/fail, blocking):**
R1 Factual accuracy — zero high-risk claims outside `verified`/`verified-with-qualification` (ledger-fed). R2 Compliance — COMPL verdict pass + lint clean. R3 Duration — validator band for the format (script profile canon). R4 Disclosure — required DISC-* present, persistent-placement spec met. R5 Structure — beats present, single CTA, markers on every block (validator). R6 Contamination — cross-lexicon scan clean.

**Scored dimensions (1–5; anchors at 1/3/5):**

**Hook strength** · 5: one breath; names a specific person or stake; earns the next five seconds without borrowed urgency or a question nobody asks themselves · 3: clear topic entry, but generic — works, doesn't grab · 1: banned-opening pattern, requires context to parse, or manufactures urgency.
**Clarity** · 5: a distracted first-time viewer could restate the central lesson in one sentence · 3: understandable with attention; one beat muddy · 1: assumes unexplained jargon or buries the lesson.
**Logical flow** · 5: each beat necessitates the next; the turn genuinely reframes · 3: ordered but additive — beats could shuffle without damage · 1: contradicts itself or the turn is a restatement.
**Educational value** · 5: teaches the thing the reader *actually* doesn't know; specific over general throughout · 3: accurate but available anywhere; partly generic · 1: platitudes; no checkable specifics.
**Personal voice** · 5: RUB-VOICE-1 resemblance ≥4 and zero avoided-phrase hits; reads as the exemplars do · 3: register correct, fingerprint neutral — "professionally fine" · 1: another brand's cadence or AI-warm homogenization (fingerprint fail is already R-blocked via VOICE's validator; this scores the judgment layer).
**Spoken cadence** · 5: reads aloud in natural breaths; pauses land after claims · 3: two or three spots need a breath the text doesn't give · 1: unreadable at pace without rewriting.
**Platform fit** · 5: hook timing, pacing, and CTA form match the platform's consumption pattern (reels ≠ webinar) · 3: platform-agnostic but serviceable · 1: wrong-format habits (essay pacing in a reel).
**CTA quality** · 5: one ask, natural exit from the turn, zero pressure language · 3: clear but bolted-on · 1: two asks, or pressure/urgency framing.
**Source quality** · 5: material claims trace to tier-1/2 sources; time-sensitive facts inside review windows (packet-fed) · 3: mixed tiers, all adequate · 1: any material claim resting on tier-4 alone.

Composite: equal weights v1; weight changes are medium-tier lessons. Golden comparison: scorecard cites nearest golden and the delta narrative.

## 7. Agent evaluations (§17.5) — telemetry and seeded tests, not vibes

| §17.5 dimension | Measured by |
|---|---|
| Task-routing accuracy | Seeded routing fixtures (quarterly) + intake audit sample vs. your corrections |
| Instruction adherence | Per-agent counterexample suites (the Tier-3 shadow, D-009) — every card's "must reject" list has a fixture |
| Appropriate tool use | Hook-denial log (attempts outside allowlist — should be ~zero) + tool-call patterns vs. card |
| Memory retrieval accuracy | Seeded fixtures: does WRITE cite the *right* F-id; does the loader assert namespaces |
| Memory-write quality | MEMC rejection rate by origin agent; staging acceptance rate |
| Hallucination rate | FOUND-rate (undeclared claims), verified-without-evidence audits, seeded-error catch inverse |
| Escalation accuracy | Precision/recall on seeded escalation fixtures + your overturn rate on real escalations |
| Handoff completeness | Envelope schema pass rate + downstream bounce rate |
| Cost efficiency / Latency | SQLite per-stage cost and duration vs. baselines (Phase 5 §8.4) |
| Human revision required | Your edit-distance per deliverable type — **the north-star metric across the whole system** |
| Regression frequency | Red counts per suite per agent-touched change |

## 8. The evaluation corpus and the named test types

```
evaluations/
  rubrics/            # RUB-*.md (protected)
  goldens/<proj>/<type>/     # approved outputs + expected-property files; QA proposes, you ratify (H6 path)
  negatives/          # rejected examples with the why — retained deliberately
  adversarial/        # injection payloads, testimonial bait, guarantee bait, urgency bait, cross-brand bait
  fixtures/           # seeded inputs for every named test type
  suites/             # composition files: which fixtures per trigger
```

Master prompt §17's named types, each mapped: **unit tests** → Skill `scripts/` + validators (Phase 4/7). **Workflow tests** → state-machine walks on fixtures (every transition exercised, including failure branches). **Golden examples** → as above; slice output is golden #1 (SK-B3 changelog). **Negative examples** → negatives/, cited by rubric anchors. **Adversarial tests** → adversarial/, run against WRITE/COMPL/MEMC/RSRCH counterexample paths. **Cross-project contamination** → Ducat-packet-against-Benowitz-profile class + lexicon seeds (Phase 3 §3 requirement, discharged here). **Outdated-fact tests** → fixture fact past `review_by` cited into a draft → must block at T6/T7. **Missing-source tests** → packet-less request → ⚠ header + `[UNVERIFIED]` path required. **Conflicting-memory tests** → claim_key collision fixture → MEMC memo required, no silent winner. **Compliance tests** → seeded-violation set, ≥1 per rule ID in each profile. **Render tests** → engine fixtures: byte-match, spec, safe-area, determinism re-render. **Regression suites** → compositions of the above per the trigger matrix (§9).

## 9. Regression triggers and thresholds

| Trigger | Suite scope |
|---|---|
| Skill version bump | That Skill's tests + every dependent's regression fixtures (D-036) |
| Profile / compliance / disclosure change | Exemplar re-lint (Phase 3 §7 case 7) + affected project's goldens + that profile's compliance seeds |
| Lesson activation | Scope-matched suite per risk tier (§2) |
| Staging-branch pre-merge | Hook-run: schema validation + affected fixtures — red staging never reaches your desk as green |
| Scheduled | Weekly: full golden pass + adversarial subset; monthly: full everything |

**Thresholds:** a required-criterion regression on any golden is **red, full stop** — no composite math can excuse it. Composite drop > 0.5/10 on any golden = red. Aggregate composite drift > 0.2 across a suite = yellow (investigate, not block). Reds block activation/merge mechanically; yellows file observations.

## 10. Rollback process — and the rehearsal

**The drill:** detection (red suite, your report, telemetry anomaly) → **freeze**: implicated lesson(s) identified via `implements:` linkage → **revert**: `git revert implements_diff` (guaranteed clean by D-025 construction) → dependent fixtures re-run to confirm → lesson status → `rejected` (reason: regression, evidence attached) or `superseded` if replaced → post-mortem note in the improvement report → if the regression escaped to published content, that's an H-level notification with the affected-artifact list (ledger + envelope hashes make "what did this touch" a query).

**The rehearsal (added to slice acceptance, extending D-006's injected-failure philosophy):** before the system carries real weight, one deliberate low-tier lesson is activated and then rolled back on purpose, end to end, with the drill timed. A rollback path that has never been walked is a diagram, not a capability.

## 11. Improvement reports (§16.4)

**Weekly digest** — script-assembled from SQLite, the queue, and git log; MEMC/QA annotate, nobody hand-writes it. Sections mirror §16.4 exactly: new observations · candidate lessons · approved/activated · rejected (with reasons) · prompt/Skill/agent/eval changes (from commit log) · performance changes (ANLYT deltas) · regressions and rollbacks · decisions awaiting you. **Monthly review** — ANLYT deep pass: hypothesis-log status, threshold-tuning proposals, cost/latency trends, calibration results (§12). The report is where "is the system actually getting better" stops being a feeling.

## 12. Calibrating the evaluators

QA's scores are only useful if they track yours. Mechanism: every ~10th H2-approved item, you blind-rate 2–3 scored dimensions (30 seconds, optional to skip any week); divergence > 1 point on a dimension across 3+ samples = QA calibration observation → anchor-clarification proposal. The evaluators get evaluated by the only ground truth this system has: you.

---

## 13. Decision log — Phase 6 proposed

| ID | Decision |
|---|---|
| D-051 | Feedback capture map §1; H2/H5 auto-diff + optional tags; no mandatory forms |
| D-052 | Lifecycle promotion criteria + risk-tiered rigor §2; fact-class re-routes to fact proposals |
| D-053 | Never-learn enforcement mapping §3 complete, incl. sourcing requirement applying to your corrections too |
| D-054 | ANLYT thresholds §4 (n≥20/arm, 2-window persistence, confound checklist, designed-experiments-only causality) |
| D-055 | Rubric architecture §5 (required vs. scored; validator-fed declared; 1–5 anchors; /10 composite) + registry |
| D-056 | RUB-SCRIPT-1 approved as authored (§6) — anchor pattern for the remaining rubrics |
| D-057 | Agent-eval measurement map §7; your edit-distance named the system north star |
| D-058 | Eval corpus structure + named-test-type mapping §8; golden governance via H6 |
| D-059 | Regression trigger matrix + thresholds §9 (required-criterion regressions are unconditional reds) |
| D-060 | Rollback drill + mandatory rehearsal in slice acceptance §10 |
| D-061 | Improvement report cadence + generated template §11; calibration sampling §12 |

## 14. Open items carried forward

- Report-generator and suite-runner scripts; SQLite queries backing §7 and §11 — Phase 7.
- Remaining rubrics authored to the §6 pattern during implementation, sequenced with their workflows.
- Fixture authoring (compliance seeds per rule ID, contamination set, adversarial set) — implementation step alongside memory seeding (Phase 3 §11).
- Dashboard information architecture consumes §7/§9/§11 outputs — Phase 7 per master prompt §20.
