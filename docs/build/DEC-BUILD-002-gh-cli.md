# DEC-BUILD-002 — Dependency: GitHub CLI (`gh`)

| | |
|---|---|
| Status | APPROVED by Wes 2026-07-10 (live instruction at the step-0 gate) |
| Type | Build-environment dependency (master prompt §3 dependency-memo rule) |

**What:** GitHub CLI, installed via `winget install GitHub.cli` (official Microsoft-managed package source, GitHub-published).

**Why:** The H6 staging-PR flow (step 3+) and PR-required branch protection on `main` mean the build environment must open, inspect, and reference PRs. `gh` is the supported CLI surface; the alternative (push branches, Wes opens PRs in the browser) adds friction at every H6 cycle.

**Constraints set by Wes:** install only; **authentication is Wes's action** (`gh auth login` run by him at the keyboard). No token is stored by the build; no secret enters the repo (master prompt §2.8).

**Version policy:** winget-latest at install time; version recorded in LOG.md at install. Not pinned — it is build tooling, not a runtime dependency of the system (pinning rule D-036/D-037 applies to runtime/skill dependencies).
