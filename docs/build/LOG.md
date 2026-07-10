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

---

## Session 2026-07-10 (third) — gate follow-ups ratified; remote wired (push pending auth)

**Done (Wes's live instructions):**
- Wes ratified BOTH open assumptions: (1) project slugs `ducat-private-wealth` / `trading-research` / `founder-brand` are now the registered project IDs alongside `benowitz-wealth` — schema enums stand; (2) the SQLite handling proposal (commit DDL as `.sql`, gitignore the live binary, back up via Phase 7 §8 legs) — decision record files at step 2 with the DDL itself.
- Remote `origin` added: `https://github.com/justcallmemrj/content-os-.git` (URL exactly as Wes supplied — note the trailing hyphen in the repo name; unverifiable anonymously since the repo is private; will confirm the name on first authenticated call and correct the remote if it 404s).
- Account `justcallmemrj` confirmed to exist via public API; repo 404s anonymously = consistent with private.

**Blocked / not done:**
- **Push NOT executed:** gh CLI is installed but unauthenticated (`gh auth status`: not logged in). Wes runs `gh auth login` himself (his standing instruction). Pushing before that would trigger an interactive credential prompt this session can't answer. Push of `main` + tag `build-step-0` happens immediately after his auth.
- Branch-protection verification (PRs required on `main`) — needs the authenticated API; queued behind auth.
- `git config user.name` — real value still not supplied (placeholder in Wes's message); remains "Derrick".
- Constitution review: not yet explicitly answered; step 2 does not start until it is (step-1 exit criterion).

---

## Session 2026-07-10 (fourth) — Step 1 gate PASSED; Step 2 built, at gate

**Gate events:** Wes approved the constitution verbatim ("constitution approved") → step-1 exit criteria complete → tag `build-step-1`. Wes said he ran `gh auth login`, but no credentials exist on this machine (no `%APPDATA%\GitHub CLI\hosts.yml`; only user profile is Mrder) — likely a stale-PATH terminal that couldn't find `gh`. Push queued; NOT executed (would hang on interactive credential prompt). Remote `origin` remains set.

**Done (step 2 — enforcement layer):**
- `workflows/machines/content-trunk.yaml`: Phase 5 §2.2 transition table encoded (T1–T15, initiators, gates, rollback rules).
- `state/ddl.sql`: Phase 7 §4 DDL verbatim; live DB + checkpoints gitignored (DEC-BUILD-004, ratified).
- `scripts/transition.py`: sole state writer — machine-validated edges, initiator checks, escalated-substate entry, one-state rollback (pre-approval only, reason logged), first-transition run creation, SQLite + work-order `state:` rewrite. 
- `scripts/load_context.py`: one-project packet assembly via indexes; refuses missing work order / missing/ambiguous/unknown project_id; namespace assertions (stray project code = hard fail); cross-project only via the explicit §3.4 block; `_shared` envelope pinned by explicit-include rule; emits `packet-manifest.yaml`.
- `scripts/generate_indexes.py`: `_index.yaml` + `_claim-keys.yaml` + sources index with generated `cited_by`; active-claim_key collision = exit 1 (Phase 3 §7 case 1). cited_by written to the generated index, NOT into protected S-*.md files (choice documented in script header).
- `scripts/schema_validate.py`: path→schema routing + Phase 3 §9.1 queue screens (S3/secret patterns, unsourced facts, instruction payloads D6, PII).
- **HK1–HK9** in `.claude/hooks/` (+ `_common.py`), registered in `.claude/settings.json`: protect_paths, state_guard, bash_policy, web_policy, secret_guard, schema_gate (HK6→schema_validate), resume_check (HK7 SessionStart+checksums), cost_log (HK8), checkpoint (HK9 PreCompact).
- **DEC-BUILD-005**: build-mode vs runtime-mode phasing — subagents fully enforced always; main session governed by `state/BUILD-MODE` marker (deleted in the step-6 acceptance commit); docs/architecture + secrets denied in every mode. PRESENTED for ratification.

**Tested:** `scripts/test_hooks.py` — **32 cases, 0 failures** (deny + allow per hook, incl. MEMC staging exception, engine jails, FACT cited-URL rule, D6 instruction-payload block). `scripts/test_schemas.py` still 46/0. Live demo captured to `docs/build/step2-denial-demo.txt`: transition allow/deny/initiator-deny, loader refusals + packet manifest, HK1/HK2/HK4 live denials, rollback with audit trail (SQLite rows shown).

**Deviations:** none. DEC-BUILD-005 is a documented decision on a spec tension (build must author protected paths), not a silent workaround — awaiting Wes's ratification.

**Open questions (step-2 gate):**
1. Ratify DEC-BUILD-005 (build-mode phasing) — the one substantive judgment call in this step.
2. gh re-auth: open a NEW terminal (so PATH includes gh), run `gh auth login` → GitHub.com → HTTPS → browser; then I push `main` + tags and verify branch protection.
3. Trailing hyphen in repo name (`content-os-`) — confirm or rename.
4. `git config user.name` still "Derrick" (placeholder never resolved).

---

## Session 2026-07-10 (fifth) — GitHub live; branch-protection gap found

**Done:**
- gh device-flow login completed at Wes's live instruction, using his signed-in Chrome (account `justcallmemrj`); GitHub's sudo-mode email verification was completed with a code that appeared via his browser/himself — the build never read or entered a credential. Token scopes: gist, read:org, repo (keyring-stored).
- Repo name CONFIRMED `content-os-` (trailing hyphen is real), private, was empty.
- `gh auth setup-git`; **pushed `main` (5 commits) + tags `build-step-0`, `build-step-1` to origin.** Remote backup leg is live.

**Deviation memo — D-068 enforcement gap (escalated at gate):**
GitHub returns 403 "Upgrade to GitHub Pro or make this repository public" for
both branch protection and rulesets on this repo: **the Free plan does not
enforce branch protection on private repos.** D-068's premise ("branch
protection on main makes Tier 2 hosted-enforced") does not currently hold —
"main requires PRs" cannot be enforced hosted-side. Options presented to Wes:
(a) GitHub Pro (~$4/mo) — recommended, restores D-068 as ratified;
(b) make repo public — REJECTED out of hand (S1 brand/compliance content);
(c) proceed with convention-only PRs — H6 still works procedurally (staging
branches + PRs + Wes merges) but nothing hosted blocks a direct push.
Awaiting Wes's decision; will file as a decision record.
