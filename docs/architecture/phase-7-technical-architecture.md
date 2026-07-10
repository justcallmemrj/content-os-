# Technical Architecture Specification — Phase 7

| | |
|---|---|
| Status | DRAFT — awaiting owner approval |
| Version | 0.7.0 |
| Date | 2026-07-10 |
| Depends on | D-001–D-061 (ratified) |
| Discharges | Master prompt §2.4 (documentation verification), §12 (final structure), §18 (security), §19 (cost), §20 (dashboard IA); all accumulated Phase 2–6 technical open items |

---

## 1. Documentation verification (§2.4) — verified 2026-07-10

Each row states what was confirmed against current sources today, classified per your §2.4 taxonomy. Standing rule: **re-verify at build time** — the Claude Code hook and memory surfaces in particular are expanding quickly enough that even this table has a shelf life.

| Technology | Confirmed current capability | Class |
|---|---|---|
| Claude Code subagents | Markdown + YAML frontmatter definitions in `.claude/agents/` (project) and `~/.claude/agents/` (user); each runs in its own context window with a custom system prompt, specific tool access, and independent permissions; per-agent `model` field; parallel delegation supported | **Confirmed** |
| Claude Code hooks | Deterministic handlers at lifecycle events configured in settings files; PreToolUse can allow, deny, ask, or rewrite tool inputs before execution, and hooks receive `tool_name`/`tool_input` as JSON; exit code 2 blocks; four handler types (command, HTTP, prompt, agent) with async support; when running inside a subagent, hook input includes `agent_id`/`agent_type` fields, and PostToolUse on a completed Agent call carries per-subagent usage telemetry — both directly enabling our per-agent policy and cost hooks. The event set has grown well past the original handful; the official reference is canonical | **Confirmed** (event list itself: verify at build) |
| Claude Code memory | CLAUDE.md hierarchy (managed/user/project, more-specific-wins) loaded at session start as *context, not enforced configuration — blocking requires a PreToolUse hook* (the docs state our D-009 thesis verbatim); `@path` imports; modular `.claude/rules/*.md` with `paths:` frontmatter for path-scoped loading; ~200-line guidance per file; **auto memory**: Claude writes its own notes to `~/.claude/projects/<project>/memory/MEMORY.md`, loaded each session, toggleable via `CLAUDE_CODE_DISABLE_AUTO_MEMORY` | **Confirmed** — auto memory is a governance issue for us; see D-065 |
| Agent Skills | SKILL.md folders with progressive disclosure, usable in Claude Code and via the SDK; Remotion shipped official Agent Skills for Claude Code in Jan 2026 | **Confirmed** |
| Claude Agent SDK | The Claude Code harness as a Python/TS library — same tools, agent loop, permission machinery, and hooks (as in-process callbacks); reads the same filesystem configuration (subagents, skills, CLAUDE.md via `setting_sources=["project"]`); sessions/resume; budget controls; its explicit fit is productized and **unattended** execution | **Confirmed** — our graduation path, §6 |
| Claude Code plugins | Bundle commands, agents, skills, hooks, and MCP servers as a loadable unit (also loadable programmatically in the SDK) | Confirmed; **optional packaging**, not required for v1 |
| MCP | HeyGen HyperFrames MCP connector exists (compose/render/status tools) | Confirmed; **external-paid service surface — OFF in v1** (D-070) |
| HyperFrames | Open source (Apache 2.0), HTML/CSS/JS compositions with deterministic headless-Chrome + FFmpeg rendering; local preview studio, `lint`/`preview`/`render` CLI; ships ~20 official agent skills; requires Node 22+ and FFmpeg; no company-size license threshold | **Confirmed** |
| Remotion | React-based programmatic video, currently v4.x with a 5.0 license revision noted; **free license covers individuals and for-profit teams up to three people, commercial use included**; a Company License is required at four or more people (Creators $25/seat/mo; Automators $100/mo minimum, per-render pricing); licensing telemetry package exists | **Confirmed — licensing is a live constraint**, D-070 |
| git / SQLite / Git LFS / FFmpeg / Node / Python | Stable, boring, exactly why they were chosen (D-004/D-021) | Confirmed |

Nothing this architecture depends on is experimental; the two custom-development items are our own scripts (loader, transition runner, validators, report generators) — by design, since they're where determinism lives.

---

## 2. Implementation options — the comparison (D-003, now formally discharged)

| Dimension | **A: Claude Code-native (chosen)** | B: Agent SDK application | C: Graduation hybrid (adopted as roadmap) |
|---|---|---|---|
| What it is | Interactive sessions drive the trunk; subagents, Skills, hooks, git do the governance | A Python/TS harness program owns orchestration | Start A; wrap specific workflows in SDK drivers when triggers fire |
| Time to working slice | Fastest — zero harness code | Weeks of driver code before first content | = A now |
| Human-gate fit | Natural: you're already in the loop at H-gates | Must build approval surfaces | = A until unattended need |
| Unattended/scheduled runs | Not the fit | The explicit fit | Added per-workflow when needed |
| Auditability | Identical — both read/write the same repo | Identical | Identical |
| Carry-over cost if migrating | — | — | **~Zero for the architecture**: the SDK reads the same subagents, Skills, CLAUDE.md, and hooks from disk; only the driver changes. This is the payoff of the file-based design |

**Decision (D-063):** A, with C as the standing roadmap. Graduation triggers, pre-agreed so it's a config change and not a debate: (1) a genuine need for unattended or scheduled runs (e.g., nightly expiry sweeps + report generation without you at the keyboard), (2) a second human operator, or (3) sustained volume where interactive driving is the bottleneck. First graduation candidates: MEMC batch curation and the weekly report — low-risk, no content judgment, naturally scheduled.

---
## 3. Final repository structure and Claude Code mapping (§12, closed)

### 3.1 The tree (Phase 3 memory tree confirmed; runtime layer added)

```
CLAUDE.md                     # the constitution — ≤200 lines (per current guidance), an index not a wiki:
                              #   identity + doctrines D1–D8 (one line each) + transition protocol
                              #   + "loader before anything" + protected-paths pointer + @imports of
                              #   global/workflow-preferences.md
.claude/
  settings.json               # hooks matrix (§5), permissions; committed
  agents/                     # the 13 runtime definitions (Phase 2 cards → frontmatter+prompt) [PROTECTED]
  skills/                     # SK-A*/B*/C* per Phase 4 anatomy [PROTECTED]
  rules/                      # path-scoped rules: video-remotion.md (paths: video/remotion/**),
                              #   video-hyperframes.md, runs-conventions.md (paths: runs/**)
  hooks/                      # hook scripts (Python, uv single-file style)
global/  projects/  proposals/  runs/  state/  schemas/  docs/  archive/   # Phase 3 §5.1 verbatim
workflows/                    # profiles/*.yaml, machines/*.yaml [PROTECTED]
evaluations/                  # Phase 6 §8 corpus
validators/                   # gate validators not bundled inside Skills
scripts/                      # loader, transition runner, index generators, report generators, sweeps
video/
  remotion/                   # engine workspace (REMO write scope)
  hyperframes/                # engine workspace (HYPF write scope)
.gitattributes                # LFS: assets binaries, renders
.gitignore                    # .env, CLAUDE.local.md, secrets patterns
```

### 3.2 Concept → Claude Code primitive

| Our concept | Runs as |
|---|---|
| ORCH | The main session, constitutionally bound by CLAUDE.md; executes transitions only via `scripts/transition.py` |
| The 12 subordinate agents | `.claude/agents/*.md` — Phase 2 card fields map: Tools→`tools:`, tier→`model:`, purpose+responsibilities+rejections+doctrines→system prompt body |
| Skills | `.claude/skills/` per Phase 4 anatomy; workflow-pinned loads verified via `skills_used` (D-034) |
| Validators & gates | `validators/` + Skill `scripts/`, invoked by the transition runner and by hooks |
| Workflow state | `state/workflow.sqlite` + work-order `state:` — written **only** by the transition runner |
| Memory | Phase 3, unchanged; ratification via GitHub PRs (§7) |
| Context loader | `scripts/load_context.py` — assembles the packet (global overlay + one project via **indexes**, not corpora), asserts namespaces, emits a packet manifest the run cites |

**Auto memory (D-065):** current Claude Code writes its own session notes and loads them automatically — an ungoverned write path that bypasses the proposal queue and would quietly violate D-011's spirit. **Disabled** (`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` in the environment for the main session and subagents). Our governed memory *is* the memory system; convenience notes that earn keeping become proposals like everything else.

## 4. Data storage and retrieval

**SQLite DDL v1** (`state/workflow.sqlite`):

```sql
CREATE TABLE runs(run_id TEXT PRIMARY KEY, task_id TEXT, project TEXT, profile TEXT,
  parent_run TEXT, state TEXT, contains_pii INTEGER DEFAULT 0,
  created_at TEXT, updated_at TEXT);
CREATE TABLE transitions(run_id TEXT, seq INTEGER, from_state TEXT, to_state TEXT,
  initiator TEXT, event TEXT, gate_results TEXT /*json*/, artifact_hashes TEXT /*json*/,
  ts TEXT, PRIMARY KEY(run_id, seq));
CREATE TABLE escalations(id INTEGER PRIMARY KEY, run_id TEXT, stage TEXT, rule TEXT,
  memo_path TEXT, resolved_by TEXT, resolution TEXT, ts TEXT);
CREATE TABLE evals(id INTEGER PRIMARY KEY, run_id TEXT, rubric TEXT, target TEXT,
  scores TEXT /*json*/, required_pass INTEGER, composite REAL, ts TEXT);
CREATE TABLE costs(id INTEGER PRIMARY KEY, run_id TEXT, stage TEXT, agent TEXT,
  model TEXT, input_tokens INTEGER, output_tokens INTEGER, usd REAL, ts TEXT);
```

Costs are fed by the PostToolUse-on-Agent hook (per-subagent usage telemetry, §1). Retrieval stays deterministic (D-004): the loader reads generated `_index.yaml` files and pulls whole records on demand; the packet manifest records exactly which record versions a run saw — reproducibility as a side effect. **Git LFS** tracks `projects/*/assets/**` binaries and `video/**/renders/**`; hosted-LFS quotas are small, so the archive sweep (Phase 3 §8) moves superseded renders out of LFS to the local/offsite archive rather than accreting them in the remote.

## 5. Hooks matrix — Tier 1/2 made concrete (D-067)

All command-type, in `.claude/hooks/`, registered in committed project settings. Hook scripts are code running with your privileges: they are themselves protected paths, reviewed like everything else.

| # | Event · matcher | Script | Enforces |
|---|---|---|---|
| HK1 | PreToolUse · `Write\|Edit\|MultiEdit` | `protect_paths.py` — deny on §4.4 protected paths; deny `memory-staging/**` for all `agent_id` except MEMC | D-011, D-024 |
| HK2 | PreToolUse · `Write\|Edit` | `state_guard.py` — deny direct writes to `state/**` and work-order `state:`; only `transition.py` (via its own guarded Bash invocation) writes state | D-041 |
| HK3 | PreToolUse · `Bash` | `bash_policy.py` — per `agent_id`: REMO/HYPF jailed to their engine dir + command allowlist (npm/npx/hyperframes/ffprobe); ORCH/QA/ANLYT/MEMC limited to `scripts/` + `validators/`; all others deny; global deny-patterns (destructive commands, `.env` access) | D-010 |
| HK4 | PreToolUse · `WebFetch\|WebSearch` | `web_policy.py` — per `agent_id`: RSRCH allow; FACT allow only URLs present in the current ledger/packet; REMO/HYPF official-docs domain allowlist; everyone else deny | D-010, D-015 |
| HK5 | PreToolUse · `Read\|Write\|Edit\|Bash` | `secret_guard.py` — deny on `.env*`, key files, credential patterns in paths/commands | D-069 |
| HK6 | PostToolUse · `Write` on `runs/**/handoffs/*.yaml`, `proposals/queue/*.yaml`, record paths | `schema_validate.py` + queue screens (S3 patterns, unsourced facts, instruction payloads, PII) — block-on-fail via decision output | D-021, D-042, Phase 3 §9.1 |
| HK7 | SessionStart | `resume_check.py` — in-flight run? verify checksums, inject state summary as additionalContext | D-045 |
| HK8 | PostToolUse · Agent | `cost_log.py` — per-subagent tokens/model → `costs` table (async) | D-072 |
| HK9 | PreCompact | `checkpoint.py` — snapshot run log (async) | D-045 |

Residual honesty (D-009 discipline): hooks gate *tool calls*; they cannot make ORCH *want* to call `transition.py` in the right order — that remains constitution + the fact that skipping it leaves no state row, which the next gate and the resume check both detect. Tier 3 with a tripwire, exactly as designed.

## 6. Agent SDK considerations (D-063 mechanics)

When a graduation trigger fires, the migration per workflow is: write a driver that calls `query()` with `setting_sources=["project"]` so it inherits the same agents/skills/CLAUDE.md from disk; re-register HK1–HK9 as SDK hook callbacks (same scripts, in-process invocation); set a per-run budget guard; schedule it. Nothing in `projects/`, `schemas/`, `workflows/`, or `evaluations/` changes. H-gates in unattended contexts become queue items awaiting your action rather than in-session prompts — which the H-gate registry (D-044) already supports since gates are states, not UI.

## 7. External services (complete v1 inventory)

| Service | Role | Decision |
|---|---|---|
| GitHub (private repo) | Remote, backup leg, and **the H6 ratification UI**: MEMC staging branches become PRs; the curation digest is the PR description; your merge — reviewable from your phone — is the ratification. Branch protection on `main` (no direct pushes) makes Tier 2 hosted-enforced too | Adopt (D-068) |
| GitHub LFS | Media versioning | Adopt with archive-out policy (§4) |
| HeyGen cloud render (MCP) | Hosted HyperFrames rendering | **Remains OFF** — local render meets v1 needs; no credential surface, no per-render spend, deterministic local output. Revisit trigger: render volume/duration exceeding local hardware (resolves D-019 → D-070) |
| Remotion licensing | Not a service but a threshold: free ≤3-person for-profit; Company License at 4+ | Eligibility check at build against current LICENSE.md; **standing watch: hiring person #4 triggers licensing review**; the cost asymmetry (HyperFrames Apache-2.0, no threshold) becomes an explicit factor in SK-B17's routing matrix (D-070) |
| Platform APIs (Meta/TikTok/YouTube/LinkedIn) | Performance data | Deferred (D-007); manual exports v1 |
| Local dependencies | Node 22+, FFmpeg (HyperFrames requirements), Python 3.11+, git + git-lfs, SQLite | Install list in the build sequence |

## 8. Security (§18, item-by-item closure)

**Secrets (D-069):** no secrets exist in v1 by construction (no publish/send/spend/API surfaces); when they arrive (SDK graduation, platform APIs), they live in `.env` + OS keychain, never the repo — enforced by `.gitignore` + HK5 + a pre-commit secret-pattern scan. **Backups:** 3-2-1-lite — GitHub remote (continuous), weekly `git bundle` + SQLite + archive snapshot to a second local disk, monthly copy offsite/cloud, restore drill once before go-live (same philosophy as the rollback rehearsal). **Encryption:** private remote + OS full-disk encryption + encrypted offsite copy.

Mapping the rest of §18's checklist: project access & file permissions → Phase 2 §4.2–4.4 + HK1–HK4 · personal/client information → S-classes, PII policy, HK6 screens (Phase 3) · API keys/credentials/social/ad accounts/email/cloud → none exist in v1 (E6); future ones follow the secrets policy with least-privilege scopes · source licensing & asset rights → mandatory rights fields (Phase 2 VDIR, Phase 3 §4.3, D-029) · publishing/email/spend authorization → H2/H4/H5 + tool absence · audit logs → transitions table + envelopes + git history (append-only by convention; branch protection helps) · retention & deletion → Phase 3 §8 · environment variables & secrets management → above · **trading-research firewall** → project isolation + SK-C4's guardrail 12 + no execution tools: research output is structurally incapable of becoming a live trade, which is the §18 requirement stated as architecture.

## 9. Observability and dashboard IA (§20 — specified, not built)

**v1 observability is generated reports, not a UI:** `scripts/report_status.py` (active runs, current stages, pending H-gates), `report_digest.py` (the Phase 6 weekly), `report_costs.py`, `report_expiry.py` — each a SQLite/queue/git query rendered to Markdown, runnable on demand or via the future scheduled driver.

**Dashboard information architecture** (the spec a future UI implements; every §20 item has a home and a source):

| View | Contents (§20 items) | Source |
|---|---|---|
| Needs You | Pending H2/H5 approvals, H6 PRs open, escalations, E4 confirmations, expiry flags, memory proposals staged | `runs.state`, `escalations`, GitHub PRs, queue, expiry sweep |
| Now | Active projects/workflows/agents, current stages, rendering status | `runs`, `transitions`, render manifests |
| Health | Failed runs, regression suite status, calibration drift, cost & latency vs. baselines | `transitions(event=halt)`, suite outputs, `evals`, `costs` |
| Learning | Observations → candidates → active funnel, rejected lessons, Skill/prompt versions, rollbacks | `proposals/`, `lessons/`, git tags/log |
| Library | Projects, campaigns, content calendar, asset status, unverified-claims backlog | project records, CB-*, calendars, manifests, ledgers |

## 10. Cost controls (§19, item-by-item) and model pins (D-071)

**Pins** (from the current model lineup; confirm pricing/limits at build): strong → `claude-opus-4-8` (ORCH, RSRCH, STRAT); mid → `claude-sonnet-4-6` (all others); fast reserve → `claude-haiku-4-5` for extraction/screen sub-tasks if telemetry justifies adding them; optional top-end → Claude Fable 5 for ORCH's E3 conflict memos only, decided at build on pricing. Per-work-order escalation field per D-017.

§19 mapping: smaller models for low-risk tasks → pins + escalation field · caching approved context → the loader's packet manifest is built once per run and reused; approved records are stable files (provider prompt-caching benefits accrue automatically where available) · reuse source packets / approved research → campaign children reference the parent packet; refresh only past `review_by` · avoid repeated fact-checks → delta protocol (D-006) + adaptation inheritance (D-047) · targeted verification → same · focused context → indexes-not-corpora loading; subagent isolation keeps bulk reads out of ORCH · compress completed history → run archival + summaries (Phase 3 §8) · structured summaries → envelopes + run summaries · not every agent loads every file → §4.2 read scopes + loader · deterministic validators where possible → the entire D-002 demotion list · parallelize only independent tasks → campaign children only · track cost by workflow and agent → `costs` table + HK8 + `report_costs.py`. And the standing constraint restated: **quality and compliance gates are never the variable that cost-tuning adjusts** — model tier and caching are.

## 11. Decision log — Phase 7 proposed

| ID | Decision |
|---|---|
| D-062 | §1 verification table adopted; capability classes assigned; re-verify-at-build is a standing build-sequence step |
| D-063 | Option A confirmed; graduation triggers named; MEMC batch + weekly report are first SDK candidates |
| D-064 | Final tree §3.1; concept→primitive mapping §3.2; CLAUDE.md as ≤200-line constitution; path-scoped rules for engine dirs |
| D-065 | **Auto memory disabled** — the governed write path is the only write path |
| D-066 | SQLite DDL v1 §4; deterministic retrieval via generated indexes; packet manifest per run |
| D-067 | Hooks matrix HK1–HK9; hook scripts are protected paths |
| D-068 | GitHub private remote; **staging-branch PRs are the H6 ratification UI**; branch protection on main |
| D-069 | Secrets/backup/encryption policy §8, incl. pre-go-live restore drill |
| D-070 | HeyGen cloud render stays OFF (resolves D-019); Remotion license eligibility check at build + person-#4 licensing tripwire; license economics added to SK-B17 matrix |
| D-071 | Model pins §10 with build-time pricing confirmation |
| D-072 | Dashboard IA adopted as spec-only; v1 observability = four generated reports |
| D-073 | §18 and §19 item-by-item mappings adopted as the compliance record for those sections |

## 12. Open items → Phase 8 (assembly)

All design is now complete. Phase 8 compiles: the §21 handoff package (33 components — sourced from Phases 1–7, nothing new invented), the standalone Claude Code master prompt, the vertical-slice prompt with its acceptance tests (injected failure + rollback rehearsal + contamination fixtures), the build sequence (verification step → scaffold → hooks → loader/transition → slice skills → slice run → acceptance), the test plan consolidation, and implementation step 0: seeding Benowitz/Ducat memory from the back catalog, sized as its own workstream.
