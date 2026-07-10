# Memory & Knowledge Architecture Specification — Phase 3

| | |
|---|---|
| Status | DRAFT — awaiting owner approval |
| Version | 0.3.0 |
| Date | 2026-07-10 |
| Depends on | D-001–D-019 (ratified) |
| Closes Phase 2 open items | full record schemas; proposal-queue and staging mechanics; retention policy |

Everything in this document obeys one sentence from Phase 1: *"the system remembers X" means "X is a versioned file the context loader injects," and "the system learned Y" means "you approved a commit that changed Y."* This spec defines those files field-by-field, the loader's isolation mechanics, the write path end-to-end, and what happens to every byte over time.

---

## 1. Layer model

Your master prompt §11 lists eight memory kinds. Four of them are **storage layers** (where records live, who loads them, how long they last) and four are **record types** (schemas that live inside layers). Separating the two removes a category error that would otherwise haunt the implementation — "evidence memory" isn't a place; it's a record type that lives in project memory.

### 1.1 The four storage layers

| Layer | Location | Loaded when | Written by | Lifespan |
|---|---|---|---|---|
| **L0 — Global owner memory** | `global/` | Every run, as the base overlay | Human commit only (approval-rules is protected; the rest via proposals) | Indefinite |
| **L1 — Project memory** | `projects/<id>/` | Exactly one project per run, overlaid on L0 | Proposal → MEMC → human commit (auto-commit classes excepted) | Indefinite; superseded, never deleted |
| **L2 — Agent procedural memory** | `agents/<ID>/lessons.md` | With the agent's definition at spawn | Generated at lesson *activation* (human commit — the file is a protected path) | Indefinite, versioned |
| **L3 — Task/run memory** | `runs/<run-id>/` + `state/workflow.sqlite` | Only by the run that owns it | The run's agents (each in its own subdir per §4.3 of Phase 2) | Active → archived → scratch purged (§8) |

L0 stays deliberately small: owner profile, general voice, workflow preferences, approval rules. The test for whether something belongs in L0: *would it be true and appropriate in every project simultaneously?* "Wes prefers complete drafts over partial drafts to approve" — yes, L0. "Avoid the phrase 'retirement journey'" — no; that's Benowitz voice memory even if it feels universal today.

L2 mechanics deserve one paragraph because they're subtle. Agents don't write their own procedural memory — that would be self-modification (D-011). Instead: an agent's improvement ideas become *lesson proposals*; a lesson that survives the lifecycle to `active` status gets compiled into that agent's `lessons.md` by the activation commit — which is yours. The agent experiences this as "my instructions now include an approved lessons section"; the system experiences it as an ordinary protected-path change with full provenance. Same machinery, no special case.

### 1.2 The record types (schemas in §4)

Evidence (facts + sources), voice (profile + exemplars + edit pairs + phrase lists), decisions, lessons — plus three types your §11 implies but doesn't name: **claim ledgers** (run-scoped, archived — the D-012 audit spine), **memory proposals** (the queue item everything rides in on), and **project profiles** (the identity record the loader reads first).

---

## 2. Data classifications

Two orthogonal axes. Every record carries both, and the axes drive different machinery: consequence drives the *write path*; sensitivity drives *handling and retention*.

### 2.1 Consequence class → write path

| Class | Definition | Write path |
|---|---|---|
| **Consequential** | Changes what the system believes, says, or does: facts, rules, voice, disclosures, lessons, decisions, profiles, schemas, workflows, agent definitions, Skills | Proposal → MEMC triage → staged diff → **your commit** |
| **Low-risk** | Bookkeeping that changes no behavior | MEMC auto-commit, logged |

The low-risk list is closed and enumerated: (1) run summaries, (2) superseded-flag annotations on records already superseded by an approved change, (3) example index regeneration, (4) changelog entries describing already-approved actions. **The list itself lives in `global/approval-rules.md` — a protected path** — so expanding what may auto-commit is itself a consequential change requiring your commit. The gate guards its own hinges.

### 2.2 Sensitivity class → handling

| Class | Contents | Rules |
|---|---|---|
| **S0 — Public** | Published/approved content, public sources | No restrictions beyond copyright policy (§9.2) |
| **S1 — Internal** | Strategy, campaigns, profiles, voice, lessons, decisions | Stays in the repo; never quoted into external-facing content |
| **S2 — Sensitive** | Client-related material in runs, raw performance exports, anything with personal data | Never enters L0–L2 memory; run-scoped only; flagged runs get shortened retention (§8.3); aggregated before analysis |
| **S3 — Secret** | Credentials, API keys, tokens | **Never in memory at any layer.** Environment/secret manager only (mechanics: Phase 7). A proposal containing an S3 pattern is auto-rejected by validator before MEMC even sees it |

---

## 3. Project-isolation rules

Isolation is mechanical, not behavioral — five mechanisms, layered:

**3.1 One-project loading.** The context loader (deterministic, D-002) reads `work_order.project_id`, assembles L0 + that project's L1 records into the context packet, and refuses to run on a missing or ambiguous ID — ambiguity escalates to you (ORCH card, confidence < 0.8 → ask). No agent has a tool that loads a second project; the capability doesn't exist (Tier 1). MEMC's cross-project *read* is the sole exception, and MEMC produces no content.

**3.2 Namespace assertion.** Every record ID embeds its project code (§4.1). The loader asserts every loaded record matches `project_id`; a stray ID is a hard failure, not a warning. This catches human filing errors, not just agent errors.

**3.3 Cross-lexicon validators.** Each project profile defines a `foreign_terms` list — vocabulary that signals another project's material. Benowitz output containing "NIL" or "signing bonus," Ducat output containing "DROP" or "Special Risk," either brand containing backtest/strategy vocabulary — flagged at the QA gate and again pre-final. Deterministic, tunable, and its false positives are cheap (a flag you dismiss) while its true positives are the Phase 1 top risk caught.

**3.4 Explicit cross-project authorization.** When a task legitimately spans brands, the work order carries a `cross_project` block: `{authorized_by, second_project, records_permitted[], reason}`. Only then may the loader include the *named records* — never a blanket second-project load. Outputs remain per-brand separate pieces (your existing Skill's "never blend" rule, now structural). Authorization is per-work-order; it never persists.

**3.5 Shared modules by explicit reference.** Benowitz and Ducat share one RIA compliance envelope (one firm, per your Skill). Modeling that as duplication invites drift; modeling it as leakage breaks isolation. So: `projects/_shared/ria-compliance-envelope.md` (protected), and each brand's `compliance.md` *explicitly includes it by path* plus brand-specific rules. Shared truth, single edit point, zero implicit access — an include is visible in the diff; leakage isn't.

A standing **contamination test suite** (Phase 6 builds it; Phase 3 makes it a requirement) exercises all five: golden tasks that fail if Ducat cadence appears in FRS content, if a trading claim survives into either brand, or if a loader accepts an ambiguous work order.

---
## 4. Record schemas

All records are Markdown files with YAML frontmatter (rationale in §5.2), one record per file, validated against JSON Schemas in `schemas/` on every write — a schema violation blocks the commit (hook). Frontmatter is shown per type; the Markdown body carries the human-readable elaboration.

### 4.1 ID registry

Namespaces are global governance — collisions and ad-hoc prefixes are how audit trails rot. This registry supersedes the draft conventions used in Phase 2 examples (e.g., the disclosure ID `D-BEN-FRS-01` becomes `DISC-BEN-FRS-01`).

| Prefix | Record type | Scope | Example |
|---|---|---|---|
| `D-` | System decision | Global | D-020 |
| `DEC-<PROJ>-` | Project decision | Project | DEC-BEN-0004 |
| `F-<PROJ>-` | Approved fact | Project | F-BEN-0012 |
| `S-<PROJ>-` | Source record | Project | S-BEN-0034 |
| `DISC-<PROJ>-` | Disclosure | Project | DISC-BEN-FRS-01 |
| `L-<PROJ>-` / `L-GLB-` | Lesson | Project / global | L-BEN-0003 |
| `VX-<PROJ>-` | Voice exemplar (approved or rejected) | Project | VX-DUC-0007 |
| `VE-<PROJ>-` | Voice edit pair | Project | VE-BEN-0021 |
| `P-<date>-` | Memory proposal | Queue | P-2026-0710-014 |
| `CL-` | Claim (within a run's ledger) | Run | CL-07 |
| `RP-` | Research packet | Run artifact | RP-2026-0710-03 |
| `CB-<PROJ>-` | Campaign brief | Project | CB-BEN-2026-Q3-01 |
| run IDs | `<date>-<proj>-<slug>-<seq>` | — | 2026-07-10-ben-drop-001 |

Project codes: `BEN`, `DUC`, `TRD`, `FDR`. Adding a project = adding a code here (consequential change).

### 4.2 Fact (evidence) record — `projects/<id>/approved-facts/F-*.md`

Your §11.5 fields, plus the machinery that makes conflict detection and freshness enforcement mechanical:

```yaml
id: F-BEN-0012
project: benowitz-wealth
claim_key: frs.pension.cola.post-2011-service   # normalized dotted key — see below
statement: >-
  FRS Pension Plan service earned on or after July 1, 2011 does not
  accrue a cost-of-living adjustment under current law.
topic: [frs, pension, cola]
source_ids: [S-BEN-0034]
source_type: primary-agency
jurisdiction: FL
published: 2025-07-01        # source publication date
effective: 2011-07-01        # when the rule itself took effect
accessed: 2026-07-08
last_verified: 2026-07-08
verified_by: FACT
confidence: high             # source-quality confidence (RSRCH card), not truth-probability
status: active               # draft | active | superseded | retired | flagged-outdated | quarantined
review_by: 2027-07-01        # freshness contract — validator blocks use past this date
supersedes: F-BEN-0007
superseded_by: null
excerpt: >-                  # minimal supporting excerpt, within quotation limits
  "...members with an effective retirement date on or after..."
usage_notes: State the service-date qualification whenever this fact appears.
approved_by: wes
approved_on: 2026-07-09
sensitivity: S0
```

**`claim_key` is the conflict-detection primitive.** It's a normalized dotted path naming *what the fact is about*, assigned by RSRCH on proposal and checked by MEMC: two `active` facts sharing a claim_key is a conflict, mechanically detected, no semantic guessing required. The key vocabulary grows in a maintained index (`approved-facts/_claim-keys.yaml`) so RSRCH reuses existing keys instead of coining near-duplicates.

**`review_by` is the freshness contract.** The expiry sweep (MEMC's script) flags approaching dates; a validator refuses to let an expired fact be cited into new content until re-verified — `flagged-outdated` is a working status, not a suggestion. Defaults by volatility: statutory rules 12 months; annually-adjusted figures (limits, premiums, COLA numbers) set to the next known adjustment date; volatile figures 90 days.

### 4.3 Source record — `projects/<id>/sources/S-*.md`

```yaml
id: S-BEN-0034
title: FRS Pension Plan Member Handbook
publisher: Florida Division of Retirement
url: https://...
type: agency-publication     # statute | regulation | agency-publication | regulator-guidance |
                             # peer-reviewed | practitioner | press | dataset | other
tier: 1                      # per this project's source hierarchy (RSRCH card)
published: 2025-07-01
effective: 2025-07-01
accessed: 2026-07-08
jurisdiction: FL
stability: annual            # static | annual | volatile — feeds review_by defaults
rights: us-fl-public-record  # drives archiving policy §9.2
archived_copy: sources/_archive/S-BEN-0034-2025-07.pdf   # or null — §9.2 rules
status: active
cited_by: [F-BEN-0012, F-BEN-0019]   # maintained by index generation — powers §7 case 6
```

`cited_by` is generated, not hand-maintained, and it's what makes source updates propagate: when a source is superseded, every fact citing it gets `flagged-outdated` in one sweep.

### 4.4 Claim ledger — `runs/<run-id>/factcheck/ledger.yaml` (archived with the run)

The D-012 audit spine, run-scoped:

```yaml
run: 2026-07-10-ben-drop-001
deliverable: drafts/drop-reel-script.md
version: 3
passes:
  - {type: full, by: FACT, at: 2026-07-10T14:22}
  - {type: delta, by: FACT, at: 2026-07-10T16:05, trigger: VOICE claim diff}
claims:
  - id: CL-07
    text: "Many Special Risk members can access their pension earlier than age 62."
    location: {file: drafts/drop-reel-script.md, anchor: beat-3}
    risk: high                # high | medium | low
    declared_by: WRITE        # or FOUND — undeclared claims FACT discovered (WRITE's eval metric)
    status: verified-with-qualification
    evidence: F-BEN-0019
    qualification: "Special Risk normal retirement differs; do not state a single age."
    on_screen: true           # D-016 — this string may appear as video text, verbatim
    history:
      - {at: ..., event: declared, by: WRITE}
      - {at: ..., event: verified, by: FACT, against: RP-2026-0710-03/c4}
      - {at: ..., event: edited, by: VOICE, diff: "you can → many Special Risk members can"}
      - {at: ..., event: delta-verified, by: FACT}
```

### 4.5 Voice memory — `projects/<id>/brand-voice.md` + `voice/`

Three record kinds plus one honest split. The **profile** (`brand-voice.md`, protected):

```yaml
version: 1.2.0
project: benowitz-wealth
tone:            # named 1–5 sliders — coarse on purpose; false precision invites gaming
  warmth: 4
  formality: 3
  directness: 4
  humor: 2
  urgency: 1     # deliberately low — no manufactured urgency, ever
sentence_length: {median_target: 11, p90_max: 22}   # words; measured, not vibes
readability_band: {grade_min: 6, grade_max: 9}
banned_openings: ["In today's world", "As a financial advisor", "Let's talk about"]
avoided_phrases: ["unlock", "leverage", "navigate the complexities", "peace of mind", "your financial journey"]
preferred_moves: ["specific over general", "fragment for emphasis", "one CTA only"]
transitions: ["Here's the part nobody mentions:", "But that's not the real question."]
cta_patterns: {reels: "single ask, spoken", linkedin: "forward this / weigh in — never book-a-call"}
platform_overrides: {linkedin: {audience_note: "write to the professional beside the client"}}
implements: [L-BEN-0003]     # lessons whose activation produced this version — provenance both directions
```

**Exemplars** (`voice/exemplars/VX-*.md`): the piece (or path to it), format, platform, `status: approved | rejected`, and *why* — rejected exemplars are retained as negatives; a model can't learn "not this" from a folder of only successes. **Edit pairs** (`voice/edits/VE-*.md`): before-ref, after-ref, edit summary, and `rule_candidates[]` that VOICE extracts and files as proposals — your actual edits are the highest-signal voice data the system will ever get, so capturing them is a standing job, not an occasional one.

The honest split (D-009 discipline applied to voice): the **fingerprint** is two things. *Deterministic measures* — sentence-length distribution, readability grade, banned/avoided-phrase count, opening-pattern check — computed by a validator, pass/fail against the profile. *Judgment resemblance* — "does this sound like Wes" — scored by VOICE/QA against exemplars, rubric-anchored in Phase 6. We never pretend the second is the first. The north-star metric stays what Phase 2 set: your post-edit distance shrinking over time.

### 4.6 Decision record — `projects/<id>/decisions/DEC-*.md` and `docs/decisions/D-*.md`

Your §11.7, verbatim in structure:

```yaml
id: DEC-BEN-0004
date: 2026-07-10
project: benowitz-wealth      # or "system" for D- records
decision: Hold "fee-only" out of all published copy pending Form ADV wording review.
reason: ADV consistency across both brands unconfirmed; "fiduciary" is separately supportable.
alternatives_considered:
  - {option: "Use fee-only now", rejected_because: "unverifiable against filed ADV"}
approver: wes
effective_version: compliance.md@1.1.0
related: [projects/_shared/ria-compliance-envelope.md]
supersedes: null
status: active                # active | superseded
```

Decisions are the *why* layer — the record you'll reach for in eight months when a rule looks arbitrary. E4 overrides, disagreement resolutions, and engine-routing overrides all file here automatically.

### 4.7 Lesson record — `projects/<id>/lessons/L-*.md`

Your §11.8 lifecycle, with activation made concrete:

```yaml
id: L-BEN-0003
scope: {project: benowitz-wealth, agents: [VOICE, WRITE]}
class: preference             # preference | fact | rule | hypothesis
statement: Prefer question-form hooks for DROP-topic reels.
status: candidate             # observed → candidate → under-review → approved → active
                              # terminal: rejected | superseded | archived
evidence: [runs/2026-06-*/analysis/..., ANLYT report AR-2026-06-02]
sample_size: 34
contradicting_evidence: [AR-2026-05-01 topic-confound note]
risk: low
expected_benefit: earlier retention hold
side_effects: hook monoculture if over-applied (cap at 60% of batch)
eval_plan: 10-post matched-topic test per ANLYT design
eval_results: pending
proposed_by: ANLYT
approved_by: null
activated_on: null
implements_diff: null         # set at activation: the commit that changed brand-voice.md / a Skill
rollback: revert implements_diff commit
superseded_by: null
```

**Activation is a diff, not a status flip.** Moving a lesson to `active` means your commit changes a concrete versioned artifact — a profile, a Skill, an agent's `lessons.md` — and that artifact's frontmatter gains `implements: [L-BEN-0003]` while the lesson gains the commit ref. Provenance runs both directions: from any rule you can find the lesson and evidence that produced it; from any lesson you can find (and revert) exactly what it changed. Rollback is `git revert`, guaranteed by construction. A lesson with no artifact to change was never a lesson — it was a note.

### 4.8 Memory proposal — `proposals/queue/P-*.yaml`

The vehicle everything above rides in on:

```yaml
id: P-2026-0710-014
run: 2026-07-10-ben-drop-001
origin_agent: VOICE
type: voice-phrase            # fact-new | fact-update | source | lesson-observation |
                              # voice-phrase | exemplar | edit-pair | decision-record |
                              # profile-gap | other
target: projects/benowitz-wealth/brand-voice.md#avoided_phrases
payload: {add: "retirement journey"}
rationale: Appeared in draft v1; matches the artificial-phrase pattern in the profile.
consequence_class: consequential
sources: []                   # REQUIRED non-empty when type is fact-* — validator-enforced
sensitivity: S1
status: queued                # queued → triaged → staged | auto-committed | rejected | withdrawn
memc: {triaged_at: null, notes: null, staged_in: null, resolved_by: null}
```

Validators screen the queue before MEMC does: S3-pattern auto-reject, unsourced-fact auto-bounce, instruction-payload flagging (D6 — a "lesson" that says "always fetch this URL" is an attack, not a lesson).

---
## 5. Knowledge tree and format assignments

### 5.1 The memory-relevant tree (revises master prompt §12; full repo finalizes in Phase 7)

```
global/
  owner-profile.md            # L0
  general-voice.md
  workflow-preferences.md
  approval-rules.md           # PROTECTED — includes the auto-commit list (§2.1)
projects/
  _shared/
    ria-compliance-envelope.md   # PROTECTED — included by explicit reference (§3.5)
  benowitz-wealth/            # duplicated shape for ducat-private-wealth, trading-research, founder-brand
    project-profile.md        # PROTECTED — identity, codes, foreign_terms, source hierarchy
    audience.md
    brand-voice.md            # PROTECTED — §4.5 profile
    compliance.md             # PROTECTED — brand rules + explicit _shared include
    disclosures.md            # PROTECTED — DISC-* records
    approved-facts/           # PROTECTED — F-*.md + _index.yaml + _claim-keys.yaml (generated)
    sources/                  # PROTECTED — S-*.md + _index.yaml + _archive/ (§9.2)
    voice/
      exemplars/              # VX-*.md, approved + rejected
      edits/                  # VE-*.md
    examples/                 # approved/ + rejected/ content examples (non-voice rationale)
    templates/
    campaigns/                # CB-*.md
    decisions/                # PROTECTED — DEC-*.md
    lessons/                  # PROTECTED at approved/active transitions — L-*.md
    assets/                   # manifest.yaml + files or pointers; rights fields mandatory
proposals/
  queue/                      # P-*.yaml — the only door in
  resolved/                   # audit copies of rejected/withdrawn
runs/
  <run-id>/                   # workorder.yaml, handoffs/, research/, drafts/, factcheck/,
                              # voice/, compliance/, qa/, storyboard/, logs/, summary.md
state/
  workflow.sqlite             # runs, states, transitions, eval scores, cost telemetry
schemas/                      # PROTECTED — JSON Schema per record type, versioned
docs/decisions/               # PROTECTED — system-level D-*.md
archive/                      # §8 destinations
```

Changes from your §12 draft, with reasons: `_shared/` added (§3.5 — shared truth without leakage); `proposals/` promoted to top level (the write path deserves architectural visibility); `state/` added for SQLite (telemetry isn't knowledge and shouldn't live among it); `voice/` split from `examples/` (voice exemplars answer "does this sound like me," content examples answer "is this good work" — different retrieval, different curators); generated indexes (`_index.yaml`, `_claim-keys.yaml`) made explicit so nobody hand-maintains what a script derives. `agents/`, `skills/`, `workflows/`, `tests/`, `evaluations/` are confirmed but specified in Phases 4–7.

### 5.2 Format assignments

| Content | Format | Why |
|---|---|---|
| Human-approved knowledge (facts, decisions, lessons, profiles, compliance) | Markdown + YAML frontmatter | Your approval surface is a git diff — it must read like a document, validate like data. Frontmatter is machine-checked; body is for humans |
| Machine-consumed records (proposals, ledgers, work orders, handoffs, manifests, indexes) | YAML (or JSON where a tool demands it) | Strict parsing; validators reject, not guess |
| Record contracts | JSON Schema in `schemas/` | Language-neutral validation; hooks enforce on write |
| Telemetry (states, transitions, evals, costs) | SQLite | Append-heavy, queryable, one file, zero server |
| Everything above | Git | Versioning, diffs, rollback, attribution — the audit log *is* the history (D-004) |
| Binary assets, renders | Files under `assets/` + `video/` with Git LFS | Text tooling stays fast; large media versions without bloating history |
| Postgres, document DB, vector DB, external PM software | **Not in v1** | D-004; revisit triggers logged: multi-user (Postgres), approved-facts corpus > ~500/project (vector), external collaborators (PM) |

---

## 6. Versioning and the ratification flow

**Substrate:** git, `main` = approved truth. Semantic versions in frontmatter for evolving documents (profiles, compliance, schemas, Skills): major = meaning changes, minor = additions, patch = corrections. Individual records (facts, decisions, lessons) don't version — they **supersede**: a changed fact is a *new* record with `supersedes:` set, and the old one flips to `superseded` with `superseded_by:` back-pointing. History is chained records plus git history; nothing is edited in place except status fields.

**The ratification flow, end to end:**

1. During a run, agents file proposals (§4.8) — the only door.
2. Validators pre-screen the queue (S3 patterns, unsourced facts, instruction payloads).
3. MEMC batch-triages (end of run + weekly): dedupe → conflict detection (claim_key + scope) → classify → never-learn checks (§16.3 of master prompt, mechanical) → route.
4. Low-risk class → auto-commit to `main`, changelog entry. Everything else → MEMC writes the proposed record files to a **staging branch** `staging/<date>-<seq>` and generates the **curation digest**: what changed, why, evidence, conflicts, one section per proposal, diffs attached.
5. You review the digest and diff; **your merge to `main` is the ratification.** Partial acceptance = you drop commits from the branch before merging; MEMC files the drops as rejections with your reason.
6. Post-merge hook regenerates indexes, re-runs the exemplar compliance lint if rules changed (§7 case 7), and updates the changelog.

Commit message convention (greppable audit): `approve(fact): F-BEN-0012 supersedes F-BEN-0007 [P-2026-0710-009]` · `activate(lesson): L-BEN-0003 → brand-voice.md@1.2.0` · `auto(summary): run 2026-07-10-ben-drop-001`.

---

## 7. Conflict resolution — the amended hierarchy, operationalized

Priority order (D-004): **1)** current human instruction — *except* against an approved compliance rule, which triggers E4 pause-and-confirm, never silent obedience; **2)** approved compliance rule; **3)** approved project rule; **4)** approved factual source (later `effective` date wins between two approved facts; loser auto-flags `superseded-pending`); **5)** approved workflow decision; **6)** global preference — with **scope specificity beats generality** as the standing tiebreak, so 3 > 6 without escalation; **7)** approved examples; **8)** candidate lessons; **9)** unapproved observations.

Your §11.9's seven cases, each with its mechanical procedure:

| Case | Detection | Procedure |
|---|---|---|
| 1–2. Two conflicting facts / old vs. new | claim_key collision among `active` facts | Later `effective` date wins; loser → `superseded-pending`; MEMC stages the supersede for your confirm |
| 3. Global vs. project preference | Loader overlay | Project wins mechanically at load time; no escalation, no log noise |
| 4. Human feedback vs. existing rule | E4 trigger | Pause, name the rule, confirm; outcome filed as DEC-*; standing change → lesson path |
| 5. Two agents, conflicting lessons | Same target/claim_key in queue | MEMC conflict memo: both positions verbatim + hierarchy analysis + recommendation → you |
| 6. A source has been updated | RSRCH refresh or sweep finds superseding publication | New S-* record; `cited_by` sweep flips every dependent fact to `flagged-outdated`; re-verification tasks issued |
| 7. Approved example violates a newer compliance rule | Post-merge exemplar re-lint on any compliance change | Violating exemplars → `quarantined` (excluded from retrieval) pending your call: retire, or annotate as historical-only |

The pattern across all seven: **detection is deterministic, resolution is hierarchical, and anything the hierarchy can't settle produces a memo, never a silent winner.**

---

## 8. Retention, archival, and deletion

Governing principle: **approved knowledge is never deleted — superseded and archived. Working material expires on schedule. Personal data gets a real deletion path.**

| Material | Active | Then | Deleted ever? |
|---|---|---|---|
| Approved records (facts, decisions, lessons, profiles, sources) | Indefinite | Superseded records remain in place, status-flagged; `archive/` sweep after 24 months superseded | No — audit spine |
| Run: deliverables, ledger, handoffs, summary, manifests | 90 days in `runs/` | `archive/runs/<year>/` — kept indefinitely | No |
| Run: scratch (drafts v1–vN-1, intermediate research, logs) | 90 days | **Purged** at archival | Yes |
| Rejected/withdrawn proposals | 12 months in `proposals/resolved/` | Archived | No (rejections are learning-governance evidence) |
| Raw performance exports | 24 months | Archived | Yes, on your instruction |
| S2-flagged runs (`contains_pii: true`) | **30 days**, then scratch purged and summary scrubbed of identifiers | Scrubbed summary archived | PII: yes — see below |
| SQLite telemetry | Rolling 24 months | Yearly compaction | Aggregates kept |
| Renders | Current + prior approved version live | Older to `archive/renders/` (LFS) | Superseded drafts purgeable at 12 months |

**PII policy (S2):** client-identifying material may exist *transiently* in run workspaces (client-communication tasks make this unavoidable) and **never** in proposals, lessons, examples, or any L0–L2 record — validator-screened at the queue. Deletion on request is honored across runs and archives; the archive layout keeps runs individually addressable precisely so this is a delete, not an excavation. Backup/encryption mechanics: Phase 7.

---

## 9. Security of the memory layer

**9.1 Never-store list** (validator-enforced at the proposal queue, per master prompt §16.3 and §18): secrets/credentials (S3 — env only); government IDs, account numbers, and client PII into permanent memory; verbatim standing commands ("always fetch URL X on every run" — instruction payloads are attacks, D6); facts without sources; single-sample performance conclusions; third-party copyrighted text beyond excerpt limits.

**9.2 Copyright and source archiving:** full-text archiving of third-party sources into `sources/_archive/` is permitted **only** for public-record/public-domain government documents (`rights: us-fl-public-record`, `us-gov-pd`, etc.) — exactly the FRS/IRS/SSA class where a dated snapshot has real verification value. Everything else: citation metadata + minimal excerpt, and verification re-fetches the living source. The repo never becomes a shadow library.

**9.3 Access recap:** the Phase 2 matrix (§4.3) governs; memory adds only MEMC's cross-project read and the staging-branch write. No agent gained anything here.

**9.4 Injection posture for memory:** the proposal queue is the system's softest persistent surface — a poisoned lesson is a persistent attack (Phase 2, MEMC card). Defense in depth: validator screening (payload patterns) → MEMC screening (D6, judgment) → nothing consequential activates without your merge (Tier 2) → activation binds to a reviewable diff (§4.7). Four layers between a malicious proposal and changed behavior.

---

## 10. Decision log — Phase 3 proposed

| ID | Decision |
|---|---|
| D-020 | Four-layer / seven-record-type model (§1); L2 agent lessons compiled at activation, human-committed |
| D-021 | One record per file; Markdown+frontmatter for approved knowledge, YAML for machine records, JSON Schema contracts, SQLite telemetry, Git LFS for media (§5.2) |
| D-022 | ID registry §4.1 (Phase 2 example conventions reconciled: disclosures → `DISC-`) |
| D-023 | `claim_key` conflict detection; `review_by` freshness contract with volatility defaults; `cited_by` source→fact propagation |
| D-024 | Ratification via staging branches + curation digest; merge-to-main = approval; auto-commit list lives inside protected `approval-rules.md` |
| D-025 | Lesson activation binds to a concrete artifact diff (`implements` / `implements_diff`); rollback = revert by construction |
| D-026 | Isolation mechanics §3.1–3.5, incl. per-work-order cross-project authorization and `_shared/` explicit-reference modules |
| D-027 | Sensitivity classes S0–S3; PII transient-in-runs-only, 30-day flagged retention, real deletion path |
| D-028 | Retention schedule §8 |
| D-029 | Copyright/archiving policy §9.2 (public-record snapshots only) |
| D-030 | Voice fingerprint split: deterministic measures (validator) vs. judgment resemblance (rubric); edit-pair capture as standing job |

## 11. Open items carried forward

- Handoff-contract full field schema — Phase 5 (ledger + work-order stubs here are forward-compatible).
- Rubric anchors for voice-resemblance and all §17 evaluations — Phase 6.
- Hook implementations (schema-on-write, protected-path block, queue screening), secret management, backup/encryption, Git LFS setup — Phase 7.
- First-population plan: seeding Benowitz/Ducat approved-facts and voice memory from the back catalog (books, webinar decks, the 60-post package) — proposed as Phase 8 implementation step 0, sized during Phase 7.
