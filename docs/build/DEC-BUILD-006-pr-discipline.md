# DEC-BUILD-006 — PR discipline after the main-requires-prs ruleset

| | |
|---|---|
| Status | RATIFIED by Wes's slice-acceptance signature 2026-07-10. The build/* self-merge class ENDED with that signature (BUILD-MODE deleted in the acceptance commit — the same commit this ratification ships in, the class's final act). All subsequent merges to main are Wes's. |
| Type | Build decision (consequence of D-068 enforcement going live) |

**Context:** ruleset `main-requires-prs` (id 18790482) is active: nothing
reaches `main` except through a PR; force-pushes and branch deletion blocked.
Verified live — a probe push was rejected with "Changes must be made through a
pull request." This is D-068 restored as ratified. It also means build-journal
commits can no longer push directly.

**Decision — two PR classes, different merge authority:**

1. **`staging/*` PRs (H6 — memory and rules).** Curation digest as body.
   **Only Wes merges.** The merge IS the ratification (D-024/D-068). The build
   never merges these, even though the token could.
2. **`build/*` PRs (journal, scripts, step work).** Opened by the build with
   tests green; **the build may self-merge** — these carry no gate and no
   approved-memory content, and were direct-pushed by design before the ruleset
   existed. This latitude ends at slice acceptance (step 6) together with
   BUILD-MODE (DEC-BUILD-005) — after that, every merge is Wes's.

**Why not require Wes on everything now:** it would put ~daily journal commits
on his desk without adding a control the hooks don't already provide, and the
distinction (content vs. journal) is visible in the branch prefix and the diff.
