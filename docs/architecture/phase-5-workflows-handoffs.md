# Workflows & Handoffs Specification — Phase 5

| | |
|---|---|
| Status | DRAFT — awaiting owner approval |
| Version | 0.5.0 |
| Date | 2026-07-10 |
| Depends on | D-001–D-039 (ratified) |
| Closes open items | full handoff schema (Phases 2–3); stage-pinned Skill tables (Phase 4) |

---

## 1. Workflow architecture — one trunk, not six machines

The master prompt asks for script, social, marketing, video, HyperFrames, and Remotion workflows. Building six bespoke state machines would repeat the mistake the agent and Skill consolidations already fixed: near-identical logic maintained in parallel until it drifts. The actual structure of the work is:

- **One content trunk** — the gated pipeline every text deliverable rides (intake → evidence → draft → verification chain → manager review → your approval). Script and social are **profiles** of this trunk: configuration (which stages are active, which Skills pin, which format validators run), not separate machines.
- **One video production machine** — chained from an approved, locked script (D-5). HyperFrames and Remotion are **engine bindings** inside it: the build stage runs SK-C1 or SK-C2, and everything else — gates, QC, sign-off — is deliberately identical so the engines stay comparable (Phase 2/4 requirement).
- **One campaign parent workflow** — marketing campaigns aren't a content pipeline; they're a *coordinator* that gets its strategy approved, then spawns child trunk runs (ads, emails, landing copy, scripts) and assembles them with cross-deliverable consistency checks.

Three machines, four profiles/bindings. Gates get defined once; a fix to the trunk fixes every content type; and "prevent agents from skipping states" (master prompt §14) is enforced in exactly one place — the transition table below, backed by hooks — instead of six.

**Where state lives:** the authoritative state is a row in `state/workflow.sqlite` plus the `state:` field in `runs/<id>/workorder.yaml`, both written by ORCH *after* each transition's checks pass. No agent's memory of "where we are" is ever load-bearing; a crashed session resumes by reading state, not by remembering it (§8).

---

## 2. The content trunk

### 2.1 States

| State | Owner | Purpose |
|---|---|---|
| `requested` | ORCH | Request received; task_id assigned |
| `intake` | ORCH | Classify deliverable; resolve project (confidence ≥ 0.8 or ask); one clarification round max |
| `context_loaded` | loader | Exactly one project's packet assembled; namespace assertions pass |
| `brief` | WRITE | Creative brief exists (skippable by profile when a ratified calendar row *is* the brief) |
| `research` | RSRCH | Source packet built (skippable when work order authorizes approved-facts-only or source asset attached) |
| `draft` | WRITE | Deliverable drafted; claims declared (SK-B2 declare) |
| `fact_check` | FACT | Ledger adjudicated; blocking summary computed |
| `revision` | WRITE/VOICE | Findings being addressed (the E1/E2 loop state; counter in SQLite) |
| `voice_edit` | VOICE | Voice + copyedit pass; change log + claim diff emitted |
| `fact_delta` | FACT | Conditional: only when claim diff non-empty (D-006) |
| `compliance` | COMPL | Profile applied; report written |
| `qa` | QA | Rubric + validators; verdict |
| `manager_review` | ORCH | Package assembled; request-match check; flags all resolved or escalated |
| `human_review` | **you** | Gate H2 — the D-005 gate; nothing external-facing passes without it |
| `approved` | system | Script/copy text **locks** (D-5); proposals filed; → `done` or → video machine |
| `done` / `archived` | system | Delivered; run archives per Phase 3 §8 |

`escalated` is a substate any state can enter (disagreement memo attached); it exits only through `human_review` early-entry or a logged ORCH rule application (E3).

### 2.2 Transition table

Gate types: **G-V** validator (deterministic, blocking) · **G-R** reviewer verdict · **G-M** manager check · **G-H** human. Every transition also fires the audit event (§8.3) and is initiated only by the listed party — hooks reject others (Tier 1/2).

| # | From → To | Initiator | Entry requires | Gate | On failure |
|---|---|---|---|---|---|
| T1 | requested → intake | ORCH | task_id; request text captured | — | — |
| T2 | intake → context_loaded | ORCH → loader | project resolved (≥0.8 conf or human answer); work order schema-valid | G-V | halt: ask human |
| T3 | context_loaded → brief \| draft | ORCH | packet assembled; namespace assertions pass; pinned Skills resolvable | G-V | halt: loader error |
| T4 | brief → research \| draft | ORCH | brief complete per SK-B3 template; concept-level compliance conflict absent | G-V + G-M | escalate (concept conflict → you) |
| T5 | research → draft | ORCH | packet schema-valid; uncertainty section present | G-V | RSRCH retry ×1 → escalate |
| T6 | draft → fact_check | ORCH | draft + claim list; duration/format validators pass; banned-openings scan clean | G-V | back to draft (validator report attached) |
| T7 | fact_check → voice_edit | ORCH | zero high-risk non-verified claims; ledger complete | G-R (FACT) | → revision |
| T8 | revision → fact_check | ORCH | findings addressed point-by-point in change log; cycle counter < 2 | G-V | counter = 2 → escalated (E2/E5) |
| T9 | voice_edit → fact_delta \| compliance | ORCH | clean version + change log + claim diff present (diff empty → skip delta) | G-V | back to voice_edit |
| T10 | fact_delta → compliance | ORCH | touched claims re-adjudicated; no new high-risk non-verified | G-R (FACT) | → revision |
| T11 | compliance → qa | ORCH | verdict = pass (conditional → revision with flags) | G-R (COMPL) | → revision \| blocked → escalated |
| T12 | qa → manager_review | ORCH | verdict = pass; required criteria all pass; contamination scan clean | G-R (QA) + G-V | → revision |
| T13 | manager_review → human_review | ORCH | package complete (deliverable, ledger, compliance report, scorecard, interventions, change history); request-match checklist pass | G-M | ORCH fixes package only (never content) |
| T14 | human_review → approved | **you** | your decision; edits you make re-enter at T6 (fact_check) — never patched in place | **G-H (H2)** | rejected → revision with your feedback \| killed → archived |
| T15 | approved → done \| video machine | ORCH | text locked (hash recorded); proposals filed to queue | G-V | — |

**Rollback rules:** any pre-approval state may roll back one state via ORCH with a logged reason (audit event `rollback`). `approved` never silently rolls back — post-approval changes are a **new version** entering at T6 with the prior approval superseded on record (D-5, D-048). Memory curation is *not* a trunk stage: proposals file at T15 and MEMC batches asynchronously (D-046) — learning never blocks delivery, and delivery never skips learning.

---
## 3. Trunk profiles

A profile is configuration over the trunk: active stages, format validators, pinned Skills, and payload types. Profiles live in `workflows/profiles/*.yaml` (protected).

### 3.1 `script` profile
All trunk stages active. This is the vertical slice (D-006), including the injected-failure acceptance test at T7 and the delta mechanism at T9–T10. Format validators: duration band (190w ≈ 90s canon, per-format bands), 7-beat structure, delivery markers present, single CTA, persistent-disclosure placement (SK-B15).

### 3.2 `social` profile
Trunk with: `brief` skipped when a ratified calendar row exists (`calendar_ref` on the work order — the row *is* the brief; a validator confirms the row's compliance-touchpoint flags carried over); `research` skipped for repurposing when the source asset is attached (its facts arrive pre-checked, but SK-B2 declare still runs — attached-source claims cite the asset, and anything beyond it is `[UNVERIFIED]`). Adds one post-approval stage for statics: `visual_brief` (VDIR, SK-B16-lite) producing the designer/Canva-ready spec whose on-image text is ledger-mapped (D-016 applies to statics too). Format validators: caption/carousel/LinkedIn structure, hashtag policy, on-image-text ↔ caption consistency.

### 3.3 `adaptation` profile (repurposing — D-047)
Adaptations and platform versions are **child runs** referencing an approved parent (`parent_run`, `parent_artifact_hash`). They enter the trunk at `draft` with SK-B5; fact-check runs in **delta scope**: unchanged claims inherit parent ledger statuses (hash-verified), changed/new claims adjudicate fresh. Voice, compliance, QA, and H2 all still run — a LinkedIn version is a new external-facing artifact, not a formality. This is how "one approved idea → eight assets" stays cheap without becoming unverified.

---

## 4. The campaign parent workflow

| State | Owner | Purpose / gate |
|---|---|---|
| `campaign_requested` → `strategy_brief` | ORCH → STRAT | SK-B10 brief: objective, audience, message, offer, conversion event, measurement plan, stop criteria |
| `strategy_review` | **you** | **G-H (H1)** — campaign strategy is a consequential class (master prompt §4.4); nothing spawns before this |
| `deliverable_planning` | STRAT + ORCH | Child-run manifest: every deliverable as a work-order stub with `parent_run` set |
| `children_active` | ORCH | Child trunk runs execute (parallel where independent); parent tracks their states |
| `assembly_review` | ORCH + G-V | Cross-deliverable consistency: ad claims ⊆ landing claims (ledger-ID comparison — the ad may not promise what the page doesn't support); offer language identical everywhere; disclosure coverage complete |
| `launch_ready` → `live` | **you** | **G-H (H4)** — launch checklist presented; *you* execute publication/spend (E6: the system has no tools for it) |
| `performance_review` | ANLYT | Scheduled per measurement plan; report → hypothesis log → candidate lessons |
| `closed` / `archived` | system | Decision record on outcome vs. stop criteria |

The assembly gate is the campaign's reason to exist as a workflow: individually compliant pieces can still disagree with each other, and ledger-ID set comparison catches that mechanically.

---

## 5. The video production machine (chained at trunk T15)

| # | From → To | Initiator | Entry requires | Gate | On failure |
|---|---|---|---|---|---|
| V1 | approved(script) → storyboard | ORCH | locked script hash; asset manifest generated (intake script) | G-V | manifest errors → halt |
| V2 | storyboard → engine_routing | ORCH | scenes sum to duration ± tol; 100% on-screen text ID-mapped; assets resolved or GAP; rights fields present | G-V | back to storyboard |
| V3 | engine_routing → build | ORCH | SK-B17 matrix scored + rationale logged; close call → **G-H (H3)** override gate | G-M (+H3 if flagged) | you choose |
| V4 | build → preview_review | HYPF \| REMO | lint clean (or exceptions documented); preview artifact exists | G-V | 2 diagnosis cycles → escalated (E5) |
| V5 | preview_review → render | VDIR | preview matches storyboard (scene-by-scene check); deviations zero or escalated | G-R (VDIR) | back to build with direction |
| V6 | render → technical_qc | engine | render manifest complete; output hashed | G-V | render error → V4 loop |
| V7 | technical_qc → judgment_qc | ORCH | validators: res/fps/duration/AR, text byte-match 100%, caption CPS/line/timing, loudness/clipping, safe areas, no blank frames | G-V | back to build (report attached) |
| V8 | judgment_qc → delivery_ready | QA (+VDIR input) | rubric pass: pacing, b-roll fit, caption placement judgment, brand consistency | G-R (QA) | revise → V4 \| storyboard flaw → V1 (rare; logged) |
| V9 | delivery_ready → human_signoff | ORCH | delivery package: render, manifest, QC reports, thumbnail/cover if requested | G-M | — |
| V10 | human_signoff → published | **you** | **G-H (H5)**; you publish (E6); state recorded after the fact | G-H | rejected → V4 or V1 with your notes |
| V11 | published → performance_review → archived | ANLYT/system | per Phase 3 §8 | — | — |

**Engine bindings:** the `hyperframes` binding pins SK-C1 (+ vendored upstream set) at V4/V6; the `remotion` binding pins SK-C2. Nothing else differs — same gates, same validators, same rubric (Phase 4 §7.3), so routing decisions accumulate comparable evidence. A **hybrid** work order runs two build lanes (V4–V7 per segment) merging at V8; a **human-editor** route exits the machine at V3 with the storyboard + asset package as the deliverable and re-enters at V7 with the returned cut.

---

## 6. Handoff architecture

### 6.1 Three parts, not one flat object (D-042)

The master prompt's §4.3 sketches ~29 fields in one object. Implemented flat, it mixes three lifetimes: task context (immutable for the run), per-hop metadata (changes every transition), and stage evidence (typed, grows). Mixing them means every agent re-validates everything and inline-copied context drifts from its source — the exact failure D1 exists to prevent. So:

**Work order** (`runs/<id>/workorder.yaml`, written at intake, immutable except `state` and appended human feedback):

```yaml
task_id: T-2026-0710-004        # the request; survives re-runs
run_id: 2026-07-10-ben-drop-001
parent_run: null                 # set for campaign children / adaptations
project_id: benowitz-wealth
cross_project: null              # Phase 3 §3.4 block when authorized
deliverable: {type: script, format: reel-90s, platform: instagram-reels, spec: "..."}
objective: webinar-registration
audience_ref: audience.md#frs-50plus     # reference, not copy
funnel_stage: awareness
voice_profile_version: brand-voice.md@1.2.0   # pin for audit; text never copied
required_fact_ids: [F-BEN-0012, F-BEN-0019]
disclosure_ids: [DISC-BEN-FRS-01]
prohibited_notes: []             # task-specific additions; standing rules live in compliance.md
asset_manifest_ref: null
constraints: {length_words: [170, 200], deadline: null}
model_tier_escalation: none
state: fact_check                # ORCH-written after each passed transition
```

**Handoff envelope** (`runs/<id>/handoffs/<seq>.yaml`, one per transition):

```yaml
run_id: 2026-07-10-ben-drop-001
seq: 7
stage: {from: voice_edit, to: fact_delta}
agents: {from: VOICE, to: FACT}
artifacts:                        # D1: paths + checksums, never inline content
  - {path: voice/drop-reel-v3.md, sha256: "...", version: 3}
  - {path: voice/change-log.md, sha256: "..."}
  - {path: voice/claim-diff.yaml, sha256: "..."}
skills_used: [{id: SK-B9, version: 1.0.0}, {id: SK-B2, version: 1.0.0}]   # D-034 gate input
gate_results: [{gate: G-V:claim-diff-present, pass: true}]
concerns: ["beat 3 runs long read aloud; cut marked, not made"]
confidence: {value: high, basis: "profile match; zero disclosure touches"}
approvals: []                     # human entries appear only at G-H gates
feedback_ref: null                # path to your notes when present
escalations: []                   # E3 memo refs if any
```

**Stage payloads** — the typed evidence each stage produces, referenced from envelopes: packet (`RP-*`), ledger, compliance report, scorecard, storyboard, render manifest. Already schema'd in Phases 3–4.

### 6.2 Master-prompt field mapping — every §4.3 field, its home, and why

| §4.3 field | Home | Why there |
|---|---|---|
| Task ID / Run ID / Project ID | work order | Immutable run identity; loader key; re-run lineage |
| Content type / Requested deliverable / Formatting constraints / Length / Deadline | work order `deliverable` + `constraints` | Fixed at intake; validators read one place |
| Business objective / Audience / Platform / Funnel stage | work order | Brief and QA rubric both consume them; single source |
| Brand voice | **reference only**: `voice_profile_version` | Copying voice text into handoffs creates a drifting second copy; the packet provides the live profile, the pin provides audit |
| Required facts / Approved sources / Source dates | `required_fact_ids` + packet ref (dates live *inside* fact/source records) | Phase 3 single-source-of-truth; duplicated dates are the ones that rot |
| Claims requiring verification | the ledger (statuses) + envelope blocking summary | The ledger *is* this field, with history — a flat list would be a lossy copy |
| Required disclosures / Prohibited claims | `disclosure_ids` + compliance.md (standing) + `prohibited_notes` (task-specific) | Standing rules stay governed in one file; only task-specific additions travel |
| Assets | `asset_manifest_ref` | Manifest is generated; rights fields mandatory (Phase 2) |
| Current workflow stage | SQLite (authoritative) + work order `state` + envelope `stage` | Machine-readable in three consistent places, one writer (ORCH) |
| Previous / Next agent | envelope `agents` | Per-hop by nature |
| Changes made | envelope artifact ref to change-log file | D1: the log is an artifact, not envelope prose |
| Unresolved concerns / Confidence level | envelope `concerns` / `confidence` | Per-hop judgment that the next agent must see first |
| Approval status / Human feedback | envelope `approvals` / `feedback_ref` | Gate outcomes are per-transition events |
| Version number | envelope `artifacts[].version` + sha256 | Version without checksum can't detect tampering or stale reads; both or neither |
| *(added)* skills_used / gate_results / escalations / parent_run / cross_project | as shown | Required by D-034, D-045, E3, D-047, D-026 respectively |

---
## 7. Gate registry

### 7.1 Gate taxonomy
**G-V** — validator gates: deterministic scripts, hook-invoked at the transition, blocking. **G-R** — reviewer gates: a governance agent's verdict (FACT, COMPL, QA, VDIR at V5), resolvable only by revision or escalation (E1). **G-M** — manager gates: ORCH completeness/consistency checks (never content judgment). **G-H** — human gates.

### 7.2 The human gates (complete registry — if it isn't here, it isn't a human gate)

| ID | Where | What you're deciding |
|---|---|---|
| H1 | campaign `strategy_review` | Activate this campaign strategy |
| H2 | trunk `human_review` (T14) | Approve this external-facing content — the D-005 gate, no v1 exceptions |
| H3 | video V3 (when routing flagged close) | Engine choice override |
| H4 | campaign `launch_ready` | Launch checklist; you execute publish/spend (E6) |
| H5 | video V10 | Final render sign-off; you publish |
| H6 | memory ratification (Phase 3 §6) | Merge staging → main |
| H7 | E4 events (any state) | Confirm or decline an instruction-vs-rule override |

Design intent: **few gates, total coverage.** Every external consequence passes H2/H4/H5; every rule change passes H6/H7; nothing else interrupts you. If v1 operation shows a gate being rubber-stamped, that's evidence for a *proposal* to change its scope — not permission to skip it.

---

## 8. Error recovery and resumability (closes Phase 1 risk 4)

**8.1 Resume protocol.** State is persisted after every passed transition (§1). On session start against an in-flight run, ORCH: reads SQLite state → verifies the last envelope's artifact checksums against disk → if intact, resumes at the current state; if a checksum fails, rolls back one state with audit event `integrity-rollback` and re-executes that stage. No stage's output depends on conversational memory of a prior session — everything needed is in the work order, packet, ledger, and envelopes by construction.

**8.2 Failure taxonomy and retry policy.**

| Class | Examples | Policy |
|---|---|---|
| Transient | tool error, timeout, fetch failure | auto-retry ×2 with backoff; then escalate |
| Substantive | validator fail, reviewer non-pass | → `revision` (the designed path; not an error) |
| Structural | handoff schema violation, checksum mismatch, namespace assertion failure | halt the transition; ORCH may not "fix and proceed" — these mean the machinery itself misbehaved |
| Poison run | 3 crashes at the same stage | halt run; human notification with state dump |

**8.3 Audit events.** Every transition writes one SQLite row — `{run, seq, from, to, initiator, gate_results, artifact_hashes, ts}` — and appends the human-readable line to `runs/<id>/logs/run.log`. Event verbs: `transition`, `revision`, `rollback`, `integrity-rollback`, `escalation`, `halt`, `resume`, `human-decision`. Together with envelopes and the Phase 3 commit conventions, this is the complete answer to master prompt §4.5's audit questions — each maps to a query, not an investigation.

**8.4 Stage timeouts.** Per-stage wall-clock budgets in the profile (defaults: research 20m, draft 15m, reviews 10m, builds 45m); expiry = transient-class failure. Budgets are telemetry-tuned via proposals, not hardcoded forever.

---

## 9. Escalation wiring (E1–E6 → machinery)

| Rule | Mechanical form |
|---|---|
| E1 material flags block | G-R gates T7/T10/T11/T12/V5/V8 have no ORCH bypass path — the transition table simply contains none |
| E2 one revision cycle | `revision` counter per stage in SQLite; T8 checks `< 2`; at 2 → `escalated` with both positions preserved (the findings file and the response file are already on disk) |
| E3 disagreement memo | `escalated` substate requires the memo artifact (schema'd); exit only via H-gate decision or logged ORCH rule application → DEC record |
| E4 instruction-vs-rule | any agent may raise; ORCH freezes the transition, presents H7; outcome → DEC record; standing change → lesson path |
| E5 loop breaker | same counter, run-level: >2 cycles at one stage → halt + summary (also V4's 2-diagnosis-cycle rule) |
| E6 external actions | H2/H4/H5 exist precisely because no tool exists — the gates are where *you* act |

---

## 10. Stage-pinned Skills (closes Phase 4 §10)

| Stage | Pinned Skills (versions recorded in `skills_used`) |
|---|---|
| intake / context_loaded | SK-A1, SK-A2 |
| brief | SK-B3 (or SK-B10 in campaign parent) |
| research | SK-B1, SK-A2 (+SK-C4 when project=TRD) |
| draft | SK-B3 \| SK-B4 \| SK-B5 \| SK-B6 \| SK-B7 \| SK-B8 per deliverable + SK-B2(declare) + SK-B15 + SK-A2 |
| fact_check / fact_delta | SK-B2 (adjudicate \| delta) |
| voice_edit | SK-B9, SK-B2(diff), SK-A2 |
| compliance | SK-B14, SK-B15 |
| qa | SK-B18 + validator suite |
| manager_review | SK-A2, SK-A3 |
| campaign stages | SK-B10–B13 per stage |
| storyboard / engine_routing | SK-B16, SK-B15, SK-B17, SK-C3 |
| build/render (binding) | SK-C1 \| SK-C2 (+SK-C3) |
| visual_brief (social statics) | SK-B16-lite, SK-B15 |
| all stages | SK-A3 available for proposals |

---

## 11. Decision log — Phase 5 proposed

| ID | Decision |
|---|---|
| D-040 | Three machines (content trunk, video machine, campaign parent) with profiles/bindings — replaces six bespoke workflows |
| D-041 | Trunk states §2.1 and transition table §2.2; initiator restrictions hook-enforced; authoritative state in SQLite + work order |
| D-042 | Handoff architecture: work order / envelope / typed payloads; envelopes carry paths + sha256, never inline content |
| D-043 | §4.3 field mapping per §6.2, incl. reference-not-copy resolutions (brand voice, source dates, claims) |
| D-044 | Gate taxonomy G-V/G-R/G-M/G-H; human-gate registry H1–H7 is closed and complete |
| D-045 | Resume protocol, failure taxonomy, retry policy, poison-run halt, audit-event schema, stage timeouts |
| D-046 | Memory curation decoupled from the content critical path (async batch at T15) |
| D-047 | Adaptations/repurposing as child runs with delta-scope fact-check and full downstream gates |
| D-048 | Rollback rules: pre-approval one-state rollback with reason; approved artifacts never patched — new version re-enters at T6 |
| D-049 | Stage-pinned Skills table §10; `skills_used` gate-checked per D-034 |
| D-050 | Video machine V1–V11 with identical gates across engine bindings; hybrid and human-editor routes defined |

## 12. Open items carried forward

- Rubric content behind G-R gates (`RUB-*`) and the regression/eval suites that patrol them — Phase 6.
- SQLite DDL, hook implementations for transition enforcement and checksum verification, timeout mechanics — Phase 7.
- Campaign assembly validator (ledger-ID subset comparison) implementation — Phase 7.
- Dashboard information architecture consumes §8.3 events — Phase 7 per master prompt §20.
