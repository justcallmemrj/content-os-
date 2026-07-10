# Discovery & System Map — Phase 1

| | |
|---|---|
| Status | RATIFIED — decisions D-001–D-008 approved 2026-07-10 |
| Version | 1.0.0 |
| Date | 2026-07-10 |
| Provenance | Delivered in-session 2026-07-10 and ratified same day; transcribed to file so the complete decision chain lives in the repository |
| Lineage | Phases 2–7 elaborate this document; where later phases add detail, they govern. The decision log is authoritative throughout |

---

## 1. What is being built

A **project-isolated content operating system**: one governed environment, run through Claude Code, operating four brand workspaces (Benowitz Wealth Management, Ducat Private Wealth, Trading Research, Founder Brand) and moving every deliverable — scripts, social, marketing, video — through a gated pipeline of specialist agents, independent reviewers, deterministic validators, and mandatory human approval. Knowledge is a versioned, curated asset: approved facts carry sources and expiry dates, voice is a measurable per-brand profile, lessons pass a candidate lifecycle before activation, and nothing consequential changes without the owner's signature. The product is not "many agents" — it is *reliability*: the same request produces the same quality bar, the same compliance envelope, and an audit trail, every time.

**The honest-state doctrine** (origin of the sentence quoted throughout later phases): persistence is never assumed. *"The system remembers X" always means "X is a versioned file the context loader injects." "The system learned Y" always means "the owner approved a commit that changed Y."* In Claude Code, persistence is exactly what lives in files: CLAUDE.md and imports load at session start, Skills load on demand, hooks fire deterministically, and each subagent runs in its own context window knowing nothing except what the orchestrator hands it and what it reads from disk.

**Seed assets identified:** the owner's two installed Skills. `benowitz-ducat-social` already contains the compliance envelope, per-brand voice files, the `[VERIFY:]` claim-flagging convention, delivery markers, the intervention Note, and the 90-second ≈ 190-word standard. `institutional-trading-research` contains the `[ESTABLISHED]/[PLAUSIBLE]/[SPECULATIVE]` evidence taxonomy and trading-language discipline. The system absorbs and formalizes these conventions rather than replacing them (D-008).

**Verification performed at delivery:** both installed Skills read in full; Claude Code subagent behavior confirmed against then-current official documentation; HyperFrames researched (open-source Apache 2.0, HTML-native compositions, deterministic rendering, ships its own agent skills). Full documentation re-verification recurred at Phase 7 and is a standing build-time step (D-062).

## 2. Component distinctions

**Agent** — a separately-prompted Claude instance with its own context window, tool allowlist, and model tier. Its value is *independent judgment in a clean context*; its cost is a handoff, latency, and tokens per spawn. **Skill** — a versioned folder of procedural knowledge any agent loads on demand: *how-to*, portable across agents. **Deterministic tool/validator** — plain code with exactly one correct behavior; never spend model judgment on what a script does perfectly. **Workflow** — the state machine of stages, gates, and allowed transitions, living in configuration so no agent can "decide" to skip a gate. **Memory** — persistent, versioned records agents read from and *propose* writes to: storage plus a curation process, not a property agents possess.

The routing heuristic: *judgment in a fresh context → agent; method or knowledge → Skill; one correct answer → validator; sequence and gates → workflow; must survive the session → memory.*

## 3. High-level system map (as ratified; rendered diagram delivered in-session)

```
                        HUMAN OWNER (Wes)
              requests · gate approvals · ratification
                               │   ▲
                               ▼   │
                 ORCHESTRATOR — main session
          routes · enforces gates · loads exactly one project
               │                              │
     PRODUCTION AGENTS                 INDEPENDENT REVIEW
  Strategist · Writer · Voice&Edit   Researcher · Fact-checker
  Video Director → Remotion /        Compliance · QA/Evaluator
                   HyperFrames       Memory Curator · Analyst
               │                              │
               ▼                              ▼
      KNOWLEDGE LAYER — git repo: global/ · projects ×4 ·
      skills/ · schemas/ · runs/  +  validators & hooks
```

Every arrow through the middle is a schema-validated handoff; every upward arrow is a human gate. Agents read approved context from disk and can only *propose* writes back; the git history is the audit log, and a commit awaiting approval is the approval mechanism.

## 4. Consolidated agent roster (13, from the master prompt's ~47)

Consolidation rule: **an agent earns separate existence only if it needs (a) adversarial independence from work it reviews, (b) a genuinely different tool/permission surface, or (c) parallel execution.** Independent review for facts, compliance, and quality was never a merge candidate.

| # | Agent | Dept | Absorbs from master prompt §6–§10 |
|---|---|---|---|
| 1 | Orchestrator | Management | Executive Manager + routing decisions of the Project Router |
| 2 | Researcher | Governance | Script Research, Social Research, Source & Evidence, Market/Audience Research |
| 3 | Fact-checker | Governance | Script Fact-Check, Social Fact-Check |
| 4 | Compliance Reviewer | Governance | Compliance & Risk, Social Compliance |
| 5 | QA / Evaluator | Governance | Quality & Eval + judgment half of Video QC |
| 6 | Memory Curator | Governance | Memory Curator |
| 7 | Writer | Production | Script Brief, Script Writer, Social Copywriter, Ad Copy, Email, Funnel copy |
| 8 | Voice & Edit | Production | Personal Voice, Social Voice, Proofreader |
| 9 | Strategist | Production | CMO, Positioning, Offer, Campaign, Paid Media, Social Strategy, calendar duty |
| 10 | Analyst | Governance | Social Performance Analyst, Marketing Analytics |
| 11 | Video Director | Video | Video Prod Manager, Storyboard, Story/Pacing, B-roll, Creative Brief, engine routing |
| 12 | Remotion Builder | Video | Remotion Production |
| 13 | HyperFrames Builder | Video | HyperFrames Production |

Full definition cards, boundaries, and permissions: Phase 2.

## 5. Roles demoted to Skills, validators, or data (D-002)

Project Router → deterministic context loader + routing Skill (ambiguity → ask the human) with contamination validators · Platform Adaptation & Repurposing → Writer Skills with mandatory claim-diff · Creative Brief → Skill · Duration validation → arithmetic · Caption QC mechanics, audio checks, export & delivery, media intake, transcript alignment → scripts/validators · Disclosure-presence and banned-phrase detection → a deterministic compliance lint on every transition (two-tier compliance: cheap lint always, model judgment at the gate, human always) · HyperFrames-vs-Remotion router → decision-matrix Skill with human override.

## 6. Memory model (as recommended and approved; full architecture in Phase 3)

Git-versioned Markdown/YAML as the single source of truth for approved knowledge, plus SQLite for run telemetry; **no vector database in v1** (small, curated, compliance-sensitive corpus — deterministic retrieval of the *approved* record beats semantic retrieval of a *similar* one). Write path: agents never write approved memory directly — proposals → Memory Curator → staged diff → owner's commit. Conflict hierarchy per master prompt §11.9 with three amendments: (1) a live instruction conflicting with an approved compliance rule triggers pause-and-confirm, never silent obedience; (2) between two approved facts, the later effective date wins with the loser auto-flagged; (3) scope specificity beats generality as a standing tiebreak.

## 7. First vertical slice (D-006)

The script pipeline — request → routing → brief → research → draft → fact-check → voice → proofread → compliance → manager review → human approval — refined three ways: the deliverable is a **90-second Benowitz Reel script** (the tightest compliance profile; if the gates hold there, they hold everywhere); fact-checking after the Voice pass runs as a **delta check** (Voice emits a claim diff; only touched claims re-verify — answering master prompt §7.9); and acceptance includes a **deliberately injected failure** — a performance-adjacent claim that the slice passes only by *blocking*. A pipeline is only trustworthy once it has been watched refusing something.

## 8. Most serious architectural risks (with mitigations, elaborated across Phases 2–7)

1. Cross-project contamination → mandatory project_id, single-project loading, cross-lexicon validators, standing contamination tests. 2. Compliance theater → three tiers (lint → model review with logged rationale → mandatory human sign-off); "passed review" never phrased as clearance. 3. Handoff information decay → schema-validated handoffs; the canonical artifact lives on disk. 4. Orchestration brittleness and cost → persisted state, resumability, per-run cost telemetry, per-agent model tiers. 5. Memory rot → review-by dates, expiry sweeps, stale facts blocked from new content. 6. Uncontrolled learning drift → candidate-lesson lifecycle, versioned activation diffs, regression evals, revert-by-construction. 7. Platform and engine churn → build on durable primitives (files, git, subagents, Skills, hooks); pin vendor versions; re-verify docs at build.

## 9. The ten questions and their approved defaults (all APPROVED 2026-07-10)

1. Substrate → **Claude Code-native**, Agent SDK as the later graduation path. 2. Approvals → **in-session gates for content; git-diff/PR-style for memory and rules**. 3. Storage → **git + Markdown/YAML + SQLite; no vector DB, no Postgres in v1**. 4. Sign-off scope → **100% human approval on all external-facing content, both brands, no exceptions**. 5. Voice corpus → **10–20 approved pieces per brand from the back catalog**, plus ongoing edit capture. 6. Model tiering → **strong for research/strategy/orchestration, mid for production and review, fast reserve for extraction**, set per agent and telemetry-tuned. 7. Video sequencing → **HyperFrames first** (captioned talking-head, one-offs), **Remotion second** (parameterized template library). 8. Project scope → **scaffold all four; activate Benowitz (slice), then Ducat**. 9. Performance data → **manual exports in v1**; APIs deferred. 10. Approvers → **sole approver (Wes)** with a CCO gate field reserved in the approval schema.

## 10. Ratified decisions (the founding block of the log)

| ID | Decision |
|---|---|
| D-001 | Consolidated 13-agent roster; independent review preserved for facts, compliance, quality |
| D-002 | Demotions list: router-as-loader, two-tier compliance lint+judgment, adaptation/repurposing as Skills, media pipeline as validators |
| D-003 | Claude Code-native substrate; in-session content gates; git-diff (PR-style) approvals for memory and rules |
| D-004 | Git+Markdown/YAML+SQLite memory; proposal → curator → human-commit write path; no vector DB in v1; three conflict-hierarchy amendments |
| D-005 | 100% human sign-off on all external-facing content, both brands, no v1 exceptions |
| D-006 | Vertical slice: Benowitz 90-second reel script; delta fact-check after voice; injected-failure acceptance test. HyperFrames first engine, Remotion second for the template library |
| D-007 | Manual performance exports in v1; sole approver with reserved CCO gate field; scaffold four projects, activate Benowitz then Ducat |
| D-008 | Existing Skills (`benowitz-ducat-social`, `institutional-trading-research`) adopted as seed components; their conventions absorbed into system schemas |
