# Runbook — operating the Content OS

<!-- Grows with each build step (package §7). Sections marked (step N) land then. -->

## Current operations (as of step 1)

**Verify the specs:** `cd docs/architecture && sha256sum -c CHECKSUMS.sha256`
(PowerShell: compare `Get-FileHash` output against the file).

**Run schema tests:** `python scripts/test_schemas.py` — 0 failures required.

**Answering build gates:** every step marked [WES] in `docs/build/PLAN.md` ends
with evidence presented in-session; your acknowledgment (or merge, where the
gate is a PR) is what un-blocks the next step.

## Pending sections

- Starting a run / answering H-gates (step 2/6)
- Reviewing H6 staging PRs (step 3)
- Running reports (step 10)
- The rollback drill (step 6, rehearsed at acceptance)
- Kill/resume a run mid-flight (step 2, HK7)

## Lesson activation / rollback (drilled 2026-07-10, criterion 9)

Activation = a SCOPED commit: `git add <lesson-file> <changed-artifact>` ONLY —
never `add -A`, never on a dirty tree (the drill proved a revert then destroys
unrelated work). Sequence: staging branch -> scoped activation commit
(message: `activate(lesson): L-X -> artifact@version`) -> dependent fixtures
green -> H6 PR -> Wes merges. Rollback: `git revert <activation-commit>` ->
re-run dependent fixtures -> update lesson status; post-mortem note.
