# Build Log — append-only session journal

Format per session: done / tested / deviations / open questions. Newest entry last.

---

## Session 2026-07-10 — Step 0 (environment & re-verification)

**Done:**
- Received `agents.zip` (package + master prompt + slice prompt). Extracted; copied to `docs/build/`.
- Environment inspection complete (results in `docs/build/DEC-BUILD-001-step0-verification.md`).
- `git lfs install` run (global filters were not previously registered).
- Local repo `C:\Users\Mrder\content-os` initialized on `main`; `docs/build/` + `docs/architecture/` (empty, awaiting specs) created.
- HyperFrames upstream pin recorded: commit `6152437d2a5c2c05e51b43d53f0f6cb6acdd9a79` (release v0.7.49, 2026-07-10) — recorded, NOT built against (slice-prompt step-0 rule).
- Documentation re-verification (D-062) executed against live official docs for: subagent frontmatter, hook events + JSON contracts, memory/CLAUDE.md loading, Skills packaging. Findings in the step-0 decision record.
- Remotion license-eligibility check: DEFERRED to step 9 per slice prompt; noted, not performed.

**Tested:** n/a (no code exists yet; environment checks are the evidence).

**Deviations:**
- **DEVIATION MEMO (blocking): the seven phase specifications (Phases 1–7) were not in `agents.zip` and are not on this machine.** Package §header and §10.2 say they ship with the package; they are binding source #3. Searched Downloads (incl. all zips), Documents, home directory. Without them, steps 1–11 cannot be implemented faithfully. Halted at the step-0 gate; specs requested from Wes. No structural assumptions were made in their absence.
- GitHub private remote + branch protection (package §10.1) not created — requires Wes's account. `gh` CLI not installed; install proposed (dependency memo in the decision record).

**Open questions (for Wes at the step-0 gate):**
1. Provide the seven phase specification documents (→ `docs/architecture/`, then protected per D-078).
2. Repo location `C:\Users\Mrder\content-os` — confirm or redirect. ASSUMPTION: local path chosen to match the `content-os` repo name in package §10.1.
3. GitHub repo URL + branch protection confirmation (slice prompt "What Wes provides" #4).
4. Approve installing GitHub CLI (`gh`) — needed for the H6 staging-PR flow from the build environment.
5. Commit-message conventions are defined in Phase 3 §6 (missing). ASSUMPTION: conventional-commits style used for step-0 commits until the spec arrives; will re-verify against Phase 3 §6 on receipt.

---

## Session 2026-07-10 (second) — Step 0 closed; Step 1 built, presented at gate

**Done:**
- Specs received (`content-os-design-bundle.zip` v1.0.1): all seven verified full-SHA-256 against Wes's prefixes AND bundle CHECKSUMS — 0 mismatches; installed to `docs/architecture/`; DEC-BUILD-001 closed with resolution. Master prompt updated to v1.0.1 (one-paragraph delta: Phase 1 added to binding list).
- Phase 3 §6 commit conventions now readable: they govern *memory/ratification* commits (`approve(fact):`, `activate(lesson):`, `auto(summary):`). Build commits keep conventional style; ratification commits will use §6 verbatim from step 3 on. Step-0 assumption resolved.
- gh CLI 2.96.0 installed **user-scope** (system MSI needs a UAC prompt this session can't answer; user-scope needs none). NOT authenticated — reserved to Wes (DEC-BUILD-002).
- `jsonschema` 4.26.0 installed + pinned in `requirements.txt` (DEC-BUILD-003; pyyaml 6.0.3 pre-existing, pinned).
- **Step 1 scaffold:** Phase 7 §3.1 tree (95 dirs incl. Phase 3 §5.1 memory tree ×4 projects); `.gitignore` (secrets, CLAUDE.local.md); `.gitattributes` (LFS for assets/renders; `docs/architecture/** -text` so spec bytes stay checksum-stable).
- **Ten slice JSON Schemas** authored from spec field definitions; fixtures use the ratified spec examples verbatim as valid cases. `scripts/test_schemas.py`: **46 checks, 0 failures** (lint + valid + invalid-rejected).
- **CLAUDE.md constitution v1.0.0** (98 lines ≤ 200): identity/ORCH binding, D1–D8, loader-first, transition protocol + gate registry, protected-paths list, memory rules, `@global/workflow-preferences.md` import. PRESENTED FOR REVIEW at the step-1 gate.
- `.claude/settings.json`: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` (D-065) + deny rules for `docs/architecture/**` writes (D-078) and `.env*` access. Hooks matrix intentionally absent until step 2 (scripts don't exist yet).
- **Auto-memory disabled AND demonstrated:** headless `claude -p` session run inside the repo; transcript created, `memory/MEMORY.md` NOT created. Implemented and tested.
- `global/approval-rules.md` scaffolded with the Phase 3 §2.1 closed auto-commit list (spec-verbatim); other L0 files are deliberately-empty scaffolds pending step-3 H6 seeding (D-079).
- `.claude/rules/` path-scoped stubs (runs, both engines); READMEs (schemas, scripts, projects); `docs/runbook.md` skeleton.
- Tag `build-step-0` placed on the step-0 close commit.

**Tested:** schema suite 46/0 (command in schemas/README.md); auto-memory demonstration as above; spec-integrity full-hash verification 7/7.

**Deviations:** none. One doc-vs-spec note (not a conflict): current docs also offer `autoMemoryEnabled: false` in settings; the spec's named mechanism (`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`) is used and demonstrated to work.

**Open questions (for Wes at the step-1 gate):**
1. Review the CLAUDE.md constitution (the step-1 [WES] exit criterion).
2. Ratify DEC-BUILD-003 (jsonschema 4.26.0 install) and the user-scope gh install.
3. The repo URL and `git config user.name` from your last message contained literal placeholders (`<MY-USERNAME>`, `<MY NAME>`) — send the real values; origin not added, user.name still "Derrick".
4. ASSUMPTION (low-risk, please confirm): project directory slugs `ducat-private-wealth`, `trading-research`, `founder-brand` normalized from the brand names; only `benowitz-wealth` appears verbatim in the specs.
5. `state/workflow.sqlite`: commit to git or ignore? Spec is silent (telemetry vs. repo-as-backup both argued). Proposal at step 2: commit the DDL as `.sql`, gitignore the live `.sqlite`, rely on the Phase 7 §8 backup legs for the binary. Will file as a decision record with your answer.
