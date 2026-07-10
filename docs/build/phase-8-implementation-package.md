# Implementation Package — Phase 8 (Final Assembly)

| | |
|---|---|
| Status | FINAL — pending owner approval |
| Version | 1.0.0-rc |
| Date | 2026-07-10 |
| Compiles | Phases 1–7 (D-001–D-073, ratified) into the master prompt §21 handoff |
| Ships with | `claude-code-master-prompt.md` · `claude-code-slice-prompt.md` · the seven phase specifications |

---

## 1. Executive summary

This package implements a **project-isolated content operating system** run through Claude Code: four brand workspaces (Benowitz Wealth Management, Ducat Private Wealth, Trading Research, Founder Brand) served by **13 agents** (7 production, 6 independent-review), **25 brand-agnostic Skills**, and **3 workflow machines** (content trunk, video machine with two engine bindings, campaign parent) — governed by **7 human gates**, **9 enforcement hooks**, schema-validated handoffs, a claim-ledger audit spine, and a git-based memory system where every permanent change is a commit you approve. Learning is a lifecycle, not a leak: observations become lessons only through evidence thresholds, evaluations, and your merge — and every activation is a one-command-revertible diff.

The design's spine, in one sentence per layer: *evidence enters through one door (the Researcher), claims carry IDs for life (draft → fact-check → voice → on-screen text, byte-matched), reviewers flag but never rewrite, the manager cannot waive material flags, nothing external-facing ships without you, and the system cannot edit its own rules.*

First milestone: the **vertical slice** — a Benowitz 90-second reel script through every gate, accepted only when the system *correctly blocks* an injected non-compliant request, survives a mid-run crash, refuses a cross-brand contamination fixture, and completes a timed lesson-rollback rehearsal.

## 2. §21 component map — all 33, with locations

| # | Component | Location |
|---|---|---|
| 1 | Executive summary | §1 above |
| 2 | Approved system architecture | Phase 1 (system map + decisions) as ratified through Phase 7 |
| 3 | Architecture diagram | §3 below (in-repo ASCII) + Phase 1/Phase 5 rendered diagrams |
| 4 | Agent roster | Phase 2 §2 |
| 5 | Complete agent definition files | Phase 2 §6 (13 cards → `.claude/agents/` per Phase 7 §3.2 mapping; build step 5) |
| 6 | Skills catalog | Phase 4 §2 |
| 7 | Initial Skill files | Phase 4 §7 (SK-B2, SK-B3, SK-C1 fully authored); remainder per template at build |
| 8 | Memory architecture | Phase 3 (entire) |
| 9 | Data schemas | Phase 3 §4 + `schemas/` JSON Schemas (build step 1) |
| 10 | Handoff schemas | Phase 5 §6 |
| 11 | Workflow state machines | Phase 5 §2–§5 |
| 12 | Project structure | Phase 7 §3.1 (final tree) |
| 13 | Security model | Phase 7 §8 (+ Phase 3 §9, Phase 2 §4) |
| 14 | Permission model | Phase 2 §4 + Phase 7 §5 (hooks) |
| 15 | Testing strategy | Phase 4 §5 + Phase 6 §8–§9 |
| 16 | Evaluation strategy | Phase 6 (entire) |
| 17 | Observability plan | Phase 7 §9 |
| 18 | Deployment options | Phase 7 §2 + §6 (Claude Code-native; SDK graduation) |
| 19 | Local development requirements | Phase 7 §7 (Node 22+, FFmpeg, Python 3.11+, git+LFS, SQLite) |
| 20 | External service requirements | Phase 7 §7 |
| 21 | Cost considerations | Phase 7 §10 |
| 22 | Implementation phases | §4 below |
| 23 | Acceptance criteria | §5 below |
| 24 | Rollback plan | §6 below (+ Phase 6 §10) |
| 25 | Documentation requirements | §7 below |
| 26 | Sample project configuration | §8.1 below |
| 27 | Sample workflow | §8.2 below |
| 28 | Sample agent handoff | Phase 5 §6.1 (the seq-7 envelope is a filled instance) |
| 29 | Sample memory proposal | Phase 3 §4.8 (P-2026-0710-014 is a filled instance) |
| 30 | Sample evaluation report | §8.3 below |
| 31 | Sample HyperFrames workflow | §8.4 below |
| 32 | Sample Remotion workflow | §8.5 below |
| 33 | Migration and expansion plan | §9 below |

## 3. Architecture at a glance (travels with the repo)

```
 WES ── requests ─────────────────────────► ORCH (main session, constitution-bound)
  ▲  ◄── H1 strategy · H2 content · H3 route │
  │      H4 launch · H5 render · H6 memory   │ spawns (only ORCH may)
  │      H7 overrides                        ▼
  │            PRODUCTION: STRAT  WRITE  VOICE  VDIR ──► HYPF | REMO
  │            REVIEW:     RSRCH  FACT  COMPL  QA  MEMC  ANLYT   (flag, never rewrite)
  │                                          │
  │              transition.py ⇄ state/workflow.sqlite    HK1–HK9 guard every tool call
  │                                          ▼
  └── staging PRs (H6) ◄── git repo: global/ · projects/{BEN,DUC,TRD,FDR}/ · _shared/
                            skills/ · schemas/ · workflows/ · evaluations/ · runs/ · video/
```

Counts: 13 agents · 25 Skills · 3 machines · 16 trunk states + 11 video states · 7 human gates · 9 hooks · ~80 ratified decisions.

## 4. Build sequence (component 22) — steps, exit criteria, gates

**[WES]** marks steps that end at your gate. Every step: implement → tests green → build-log entry → next.

| Step | Scope | Exit criteria |
|---|---|---|
| 0 | **Environment & re-verification** (D-062): inspect machine deps; init repo + private remote + branch protection; re-verify subagent/hooks/memory/skills doc surfaces; pin HyperFrames upstream commit; Remotion license-eligibility check | Verification build-note filed as a decision record; deps installed **[WES: review note]** |
| 1 | **Scaffold**: Phase 7 §3.1 tree; all JSON Schemas; CLAUDE.md constitution (≤200 lines); `.claude/settings.json`; `.gitignore`/`.gitattributes`; auto-memory disabled (D-065) | Tree matches spec; schemas lint; constitution reviewed **[WES]** |
| 2 | **Enforcement layer**: HK1–HK9 + per-hook deny/allow fixtures; `load_context.py`, `transition.py`, index generators, `schema_validate.py`; SQLite DDL init | Every hook fixture green; a scripted protected-path write is *demonstrably denied* **[WES: watch the denial demo]** |
| 3 | **Memory seeding** (D-079): scaffold 4 project profiles + `_shared/` envelope; execute the D-038 decomposition of `benowitz-ducat-social`; draft initial facts *as proposals* from the back catalog; select 10–20 voice exemplars/brand; first staging PR | First H6 PR merged by you; foreign_terms populated; DISC-* records live **[WES: inputs + merge]** |
| 4 | **Slice Skills**: implement SK-B2/B3 from Phase 4 §7; author SK-A1–A3, SK-B1, SK-B9, SK-B14, SK-B15 to template | All Skill tests + counterexample tests green |
| 5 | **Agent definitions**: 13 runtime files from Phase 2 cards; instruction-adherence fixtures for slice agents | `/agents` lists all 13; adherence fixtures green |
| 6 | **Slice run & acceptance**: fixtures (contamination, injected failure, missing-source); live DROP-reel run through H2; §5 checklist; tag `v1.0-slice` | **All ten §5 criteria pass [WES: acceptance sign-off]** |
| 7 | Social profile + adaptation child runs + calendar linkage | Adaptation delta-inheritance fixture green; one social run through H2 **[WES]** |
| 8 | **Video — HyperFrames binding**: manifest script, VDIR + SK-B16/B17/C3/C1, byte-match/safe-area validators; first render through H5 | V1–V11 walked; text byte-match 100% **[WES: H5]** |
| 9 | **Video — Remotion binding**: license gate, SK-C2; comparability eval vs. step 8 | Same fixtures green on both engines |
| 10 | Campaign parent + STRAT/ANLYT + reports (`report_*.py`) + weekly digest | Assembly-consistency validator green on a fixture campaign **[WES: H1/H4 on first real campaign]** |
| 11 | **Ducat activation** (proves multi-project); TRD/FDR scaffolds confirmed | Contamination suite green across both live brands **[WES]** |

## 5. Vertical-slice acceptance criteria (component 23; extends D-006/D-060)

The slice passes only when **all ten** hold, with evidence attached:

1. Full trunk walk on the DROP-reel request — every transition in SQLite, every envelope schema-valid, every gate result recorded.
2. **Injected failure blocked**: the "could save teachers thousands" request reaches you as a flagged intervention with the compliant alternative — never as polished copy.
3. **Delta path proven**: a VOICE semantic edit produces a claim diff; FACT re-adjudicates *only* touched claims (ledger history shows it).
4. **Contamination refused**: the Ducat-packet-against-Benowitz-profile fixture flags; no blended output exists.
5. **Missing-source path**: a packet-less request yields the ⚠ unsourced header + complete `[UNVERIFIED]` listing.
6. **Resume proven**: session killed mid-`fact_check`; restart verifies checksums and completes the run.
7. **Hook denial proven**: a scripted attempt to edit `compliance.md` is denied and logged (HK1).
8. **H6 flow proven**: ≥1 staging PR with curation digest, merged by you, indexes regenerated post-merge.
9. **Rollback rehearsal**: one low-tier lesson activated then reverted, dependents re-tested green, drill timed (D-060).
10. **Baselines recorded**: slice output ratified as golden #1; your edit-distance on it logged as the north-star baseline; secret-scan clean; step docs written.

## 6. Rollback plan (component 24)

Two levels, both revert-by-construction. **Build-level:** every build step is its own commit series behind a tag; a failed step is `git revert`ed, its build-log entry marked, and the step re-planned — never patched forward silently. **Operational:** the Phase 6 §10 drill (lesson `implements_diff` revert → dependent fixtures → status update → post-mortem), rehearsed at slice acceptance. Published-content escapes follow Phase 6 §10's H-level notification with the affected-artifact query.
## 7. Documentation requirements (component 25) — what Claude Code writes as it builds

Per area: a README (what lives here, how to run its tests); `docs/runbook.md` (operating the system: starting a run, answering gates, reviewing PRs, running reports, the rollback drill); `docs/build/PLAN.md` + `docs/build/LOG.md` (the living build log — every session appends: done, tested, deviations, open questions); a decision record for **every** build-time choice the specs left open (dependency picks, pin commits, threshold tunings) filed as D-/DEC- records; and the seven phase specifications copied to `docs/architecture/` and added to protected paths (D-078) — the implementation may not edit its own requirements.

## 8. Samples (components 26–32)

### 8.1 Sample project configuration — `projects/benowitz-wealth/project-profile.md` frontmatter

```yaml
project_id: benowitz-wealth
code: BEN
status: active
audience_summary: Florida Retirement System members — teachers, deputies, firefighters, state staff
source_hierarchy: [statute, agency-publication (FRS/DMS/SSA/IRS/CMS), regulator-guidance,
                   peer-reviewed, practitioner, press]
foreign_terms: [NIL, signing bonus, jock tax, backtest, drawdown, contract year]   # contamination scan
compliance_includes: [projects/_shared/ria-compliance-envelope.md]
voice_profile: brand-voice.md@1.0.0
default_disclosures: [DISC-BEN-FRS-01]
review_cadence: {facts_sweep: weekly, profile_review: quarterly}
```

### 8.2 Sample workflow — the DROP-reel run traced (the spine every spec example shares)

| Stage | Agent | Artifact | Gate result |
|---|---|---|---|
| intake → context_loaded | ORCH + loader | workorder.yaml (BEN, reel-90s) | G-V pass |
| research | RSRCH | RP-…-03: 14 claims, 2 conflicts escalated | G-V pass |
| draft | WRITE | 188-word script · 11-claim list · 10 hooks · 2 interventions | G-V pass |
| fact_check | FACT | ledger: 9 verified, 2 unverified → revision | **G-R blocks** |
| revision → fact_check | WRITE | sources added / claims reframed structural | G-R pass |
| voice_edit | VOICE | clean v3 · change log · diff touches CL-07 | G-V pass |
| fact_delta | FACT | CL-07 verified-with-qualification | G-R pass |
| compliance | COMPL | pass · required-language table complete | G-R pass |
| qa | QA | scorecard §8.3 | G-R pass |
| manager_review → human_review | ORCH → **Wes** | full package | **H2: approved** |
| approved | system | text locked (hash) · proposals filed | → video machine |

### 8.3 Sample evaluation report — RUB-SCRIPT-1 scorecard instance

```yaml
run: 2026-07-10-ben-drop-001   rubric: RUB-SCRIPT-1   target: voice/drop-reel-v3.md
required: {R1_facts: pass, R2_compliance: pass, R3_duration: pass(88s est),
           R4_disclosure: pass, R5_structure: pass, R6_contamination: pass}
scores: {hook: 5, clarity: 5, flow: 4, educational: 5, voice: 4, cadence: 5,
         platform_fit: 5, cta: 4, source_quality: 4}
composite: 9.1/10
golden_comparison: "nearest: none yet (this becomes golden #1); n/a"
observations: ["hook lands 0:06; watch vs. future goldens"]
verdict: pass
```

### 8.4 Sample HyperFrames workflow (video machine, `hyperframes` binding)

V1 storyboard (11 scenes, 3 ledger-mapped text cards, disclosure block persistent) → V2 validators pass → V3 SK-B17 recommends HyperFrames (one-off, caption-heavy; factors logged; no H3 flag) → V4 SK-C1 build: 3 sub-compositions, lint clean → V5 VDIR preview approval → V6 local render, manifest HF-…-01 → V7 validators: byte-match 100%, safe-area pass, 1080×1920/88.1s to spec → V8 QA judgment pass (RUB-VIDEO-1) → V9 package → **V10 H5: Wes signs, publishes** → V11 archive. Cloud render untouched (D-070).

### 8.5 Sample Remotion workflow

Identical machine, `remotion` binding: V3 routes to Remotion when the matrix favors parameterized reuse (e.g., a monthly data-driven series) — license eligibility confirmed at step 9's gate → V4 SK-C2: `DropReel.tsx` composing library `CaptionTrack` + `DisclosureBlock`, props populated from the storyboard file → V5–V11 as above, same validators, same rubric — by design, so engine evidence stays comparable (D-050).

## 9. Migration and expansion plan (component 33)

**New-project onboarding checklist** (adding project #5 is procedure, not architecture): register code in the ID registry (consequential) → scaffold profile set (§8.1 pattern) → populate `foreign_terms` *and add this project's terms to the other projects' lists* → define source hierarchy + disclosures → seed 10–20 voice exemplars via staging → author contamination fixtures → activation decision record. **Activation order:** Ducat (step 11) → Trading Research (SK-C4 is already its core; its guardrails seed `compliance.md`) → Founder Brand. **Growth levers, all pre-decided:** agent fission triggers (Phase 2 §7) · SDK graduation triggers (Phase 7 §2/§6; first candidates MEMC batch + weekly digest) · dashboard build trigger (when generated reports feel insufficient — the IA is ready, Phase 7 §9) · Remotion person-#4 licensing tripwire (D-070) · vector-retrieval trigger at ~500 facts/project (D-004).

## 10. Getting started (the five steps)

1. Create a private GitHub repo (`content-os`), enable branch protection on `main`, clone locally.
2. Copy the seven phase specifications into `docs/architecture/`, and this package + both prompts into `docs/build/`.
3. Install deps: Node 22+, FFmpeg, Python 3.11+, git-lfs; run `git lfs install`.
4. Open Claude Code in the repo and paste **`claude-code-master-prompt.md`** as your first message — it binds the session to the specs and the operating rules.
5. Then paste **`claude-code-slice-prompt.md`** — it scopes work to steps 0–6 and ends at your acceptance sign-off. Have ready: the back-catalog files (books, webinar decks, the 60-post package), 10–20 approved pieces per brand for voice exemplars, and an hour for the seeding PR review.

## 11. Decision log — Phase 8 proposed (final design decisions)

| ID | Decision |
|---|---|
| D-074 | Package structure: this document + master prompt + slice prompt; §2 component map is the §21 compliance record |
| D-075 | Build sequence steps 0–11 with named Wes gates |
| D-076 | Slice acceptance = the ten criteria of §5, evidence-attached |
| D-077 | Master prompt and slice prompt approved as authored |
| D-078 | The seven specifications become protected paths in-repo (`docs/architecture/**`) — the implementation cannot edit its requirements |
| D-079 | Seeding is proposals-first and H6-ratified; no back-catalog fact enters approved memory without your merge |
| D-080 | Expansion procedures §9 adopted as standing guidance |

**Closing note:** with D-074–D-080, all eight design phases of the master prompt §22 are complete. What remains is execution — in Claude Code, against these documents, at your pace, with every consequential step still ending at you. That was the requirement on page one, and it held to the last page.
