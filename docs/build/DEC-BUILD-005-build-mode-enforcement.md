# DEC-BUILD-005 — build-mode vs runtime-mode enforcement phasing

| | |
|---|---|
| Status | IMPLEMENTED at step 2; presented for ratification at the step-2 gate |
| Type | Build decision on a spec-tension point (documented, not silent — §1 rule) |

**The tension:** Phase 2 §4.4 protects `.claude/agents/**`, `.claude/skills/**`,
`schemas/**`, `workflows/**` — but build steps 1–5 *author* exactly those files
from the main session. Enforcing HK1 fully against the main session today would
make the build impossible; not enforcing it at all would ship a system whose
main session can rewrite its own rules.

**Decision (two-phase):**
1. **Subagents are fully enforced from day one** — every HK1–HK4 rule applies
   to any tool call carrying an `agent_id`, in every mode. The 13 runtime agents
   never experience a weaker regime.
2. **The main session is governed by the `state/BUILD-MODE` marker file.** While
   it exists (the build phase), main-session writes to buildable protected paths
   are allowed — each allowed write logs its build-mode basis in the hook output.
   **Deleting the marker is part of the step-6 acceptance commit**, flipping the
   main session to full runtime enforcement the moment the slice is accepted.
3. **No mode weakens:** `docs/architecture/**` (D-078) and all secret patterns
   (HK5) are denied for everyone, in every mode, including the build itself.

**Why a marker file and not a hook edit later:** the flip is a one-line diff in
the acceptance commit — visible, revertible, and it requires no change to hook
code (which is itself protected). Editing hooks at acceptance time would be the
exact "special-case a hook" behavior the never-list forbids.

**Evidence:** `scripts/test_hooks.py` covers both regimes (agent-denied vs
build-mode-allowed on the same path; spec-edit denied in build mode).
