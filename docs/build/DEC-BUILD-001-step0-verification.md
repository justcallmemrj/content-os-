# DEC-BUILD-001 — Step 0 verification build-note

| | |
|---|---|
| Status | PRESENTED — awaiting Wes acknowledgment (step-0 [WES] gate) |
| Date | 2026-07-10 |
| Covers | Package §4 step 0: environment inspection + documentation re-verification (D-062) |
| Author | Claude Code (implementation engineer) |

## 1. Environment inspection (master prompt §2.1)

| Dependency | Required (package §2 #19) | Found | Verdict |
|---|---|---|---|
| OS | — | Windows 11 Pro 10.0.26200 | noted |
| Node | 22+ | v24.16.0 | PASS |
| Python | 3.11+ | 3.14.5 | PASS |
| SQLite | required | 3.50.4 (via Python stdlib `sqlite3`) | PASS |
| FFmpeg | required | 8.1.1-full_build (gyan.dev) | PASS |
| git | required | 2.54.0.windows.1 | PASS |
| git-lfs | required | 3.7.1 — binary present, but global filters were **not** registered; `git lfs install` run this session | PASS (fixed) |
| Disk | — | ~75.7 GB free on C: | adequate for slice; video renders (step 8+) will need monitoring |
| GitHub CLI (`gh`) | not named in specs; needed for H6 PR flow from this environment | **NOT INSTALLED** | proposal below |

Repo: local `C:\Users\Mrder\content-os` initialized on `main`, LFS enabled. **No private remote / branch protection yet** — package §10.1 assigns repo creation to Wes; awaiting URL + confirmation.

## 2. Documentation re-verification (D-062) — verified against live docs 2026-07-10

Index: code.claude.com/docs/en/claude_code_docs_map.md. All four surfaces confirmed current; key facts relevant to steps 1–5:

**Subagents** (…/subagents.md): project files at `.claude/agents/*.md`; frontmatter supports `name`, `description` (both required), `tools`, `disallowedTools`, `model` (alias/full-ID/`inherit` — supports the D-071 model pins), `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `effort`, `isolation`, `color`. Note: subagents now run **background by default** (v2.1.198) — step-5 agent cards must account for this when the orchestrator expects synchronous handoffs.

**Hooks** (…/hooks.md, …/hooks-guide.md): 30 events currently supported, including `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `Stop`, `SubagentStart/Stop`, `SessionStart/End`, `PreCompact`, plus newer ones (`PermissionRequest`, `PostToolUseFailure`, `ConfigChange`, `FileChanged`, `InstructionsLoaded`). Path-denial mechanism for HK1-style protected paths CONFIRMED: `PreToolUse` matcher + JSON stdout `{"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": "…"}}`; exit code 2 = block with stderr fed back. `updatedInput` rewriting also available. This is sufficient surface for HK1–HK9 as designed.

**Memory/CLAUDE.md** (…/memory.md): loading order = managed policy → `~/.claude/CLAUDE.md` → `./CLAUDE.md` → `./CLAUDE.local.md` → `.claude/rules/*.md` (lazy, path-scoped). Imports via `@path`, max 4 hops. **Auto memory can be disabled** via `"autoMemoryEnabled": false` in settings or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` — this is the D-065 implementation vehicle at step 1, and it is demonstrable (slice-prompt step-1 exit criterion).

**Skills** (…/skills.md): `SKILL.md` + optional `references/`/`scripts/`/`examples/`; frontmatter includes `name`, `description`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `context: fork` + `agent`, `paths`, `hooks`, `model`, `effort`. Project skills at `.claude/skills/<name>/SKILL.md`. ⚠ One gap: docs publish **no SKILL.md size limit** — if a Phase 4 spec cites one, treat the spec's number as the binding constraint (it is stricter, no conflict).

**HyperFrames pin** (step-0 requirement): upstream `heygen-com/hyperframes` pinned at commit `6152437d2a5c2c05e51b43d53f0f6cb6acdd9a79` = release **v0.7.49** (2026-07-10). Recorded only — NOT built against until step 8, per slice prompt.

**Remotion license eligibility**: DEFERRED to step 9 per slice prompt; explicitly noted as unperformed. No Remotion facts asserted.

## 3. DEVIATION MEMO — missing binding sources (blocking)

**What conflicts:** The package header says it "ships with … the seven phase specifications," and §10.2 instructs copying them into `docs/architecture/`. `agents.zip` contained only three files (this package + two prompts). The Phase 1–7 specifications are binding source #3 (master prompt §1) and are cited by every build step's exit criteria (tree = Phase 7 §3.1; schemas = Phase 3 §4; hooks = Phase 7 §5; Skills = Phase 4 §7; agent cards = Phase 2 §6; evals = Phase 6).

**Both readings:** (a) the specs were meant to be in the zip and were omitted by accident; (b) they are delivered separately and I should wait. Either way the action is the same.

**Recommendation:** Wes provides the seven specification documents; I copy them to `docs/architecture/`, register them as protected paths (D-078), and only then start step 1. **I have made no structural assumptions in their absence** — improvising the tree, schemas, or hook semantics from the package's summaries would be redesign, which the master prompt forbids.

**What it affects:** everything from step 1 onward. Step 0 is unaffected and is complete except for this gate.

## 4. Proposals requiring Wes's decision (dependency memos, per never-list)

1. **Install GitHub CLI (`gh`)** — needed to open/inspect the H6 staging PRs from the build environment (step 3+). Alternative: I push branches and Wes opens PRs in the browser. Recommendation: install via `winget install GitHub.cli` (free, official).
2. **Confirm repo location** `C:\Users\Mrder\content-os` (ASSUMPTION: name matches package §10.1's `content-os`).
3. **GitHub private remote + branch protection on `main`** — Wes's account action (package §10.1); provide the URL.
4. **Commit-message conventions** live in Phase 3 §6 (missing). ASSUMPTION: conventional-commits style for step-0 commits; will reconcile when the spec arrives.

## 5. Honest status (master prompt §2.14)

- Implemented and tested: environment inspection; `git lfs install`; repo init; doc re-verification against live docs (14 of 15 items confirmed; 1 flagged gap noted above).
- Implemented, untested: none.
- Not implemented: everything from step 1 onward — correctly, per the gate structure and the missing-specs blocker.
