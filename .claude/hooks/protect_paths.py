#!/usr/bin/env python3
"""HK1 — PreToolUse Write|Edit|MultiEdit|NotebookEdit: protected paths (D-011, D-024).

Deny writes to Phase 2 §4.4 protected paths; deny memory-staging/** for every
agent except MEMC. docs/architecture/** is denied in every mode (D-078).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import (ALWAYS_DENIED_GLOBS, PROTECTED_GLOBS, allow, build_mode,
                     deny, matches, read_input, rel_path)


def main() -> None:
    data = read_input()
    tool_input = data.get("tool_input", {})
    raw = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not raw:
        allow()
    rel = rel_path(data, raw)
    agent = data.get("agent_id") or data.get("agent_type")  # absent in the main session

    if matches(rel, ALWAYS_DENIED_GLOBS):
        deny(f"HK1: '{rel}' is a ratified specification (D-078) — read-only to the build and the system, every mode")

    if rel.startswith("memory-staging/") and (agent or "").upper() != "MEMC":
        deny(f"HK1: memory-staging/** is writable only by MEMC, not {agent or 'the main session'}")

    if matches(rel, PROTECTED_GLOBS):
        if agent:
            deny(f"HK1: '{rel}' is a protected path (Phase 2 §4.4) — human-commit only; "
                 f"agent {agent} must file a proposal instead")
        if not build_mode():
            deny(f"HK1: '{rel}' is a protected path (Phase 2 §4.4) — human-commit only; "
                 "runtime mode active (no state/BUILD-MODE)")
        allow(f"HK1: build-mode write to protected path '{rel}' (DEC-BUILD-005; ends at slice acceptance)")

    allow()


if __name__ == "__main__":
    main()
