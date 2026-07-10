#!/usr/bin/env python3
"""HK2 — PreToolUse Write|Edit: state is written only by transition.py (D-041).

Denies, for EVERYONE in EVERY mode:
  - any Write/Edit touching state/workflow.sqlite* (the DB is script-territory)
  - Edit of an existing runs/**/workorder.yaml (immutable except `state:`,
    which only transition.py rewrites; creation of a new work order is allowed)
transition.py itself writes via its own process, not via Claude tools, so this
hook never blocks it.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import ROOT, allow, deny, read_input, rel_path


def main() -> None:
    data = read_input()
    tool_input = data.get("tool_input", {})
    raw = tool_input.get("file_path") or ""
    if not raw:
        allow()
    rel = rel_path(data, raw)

    if re.match(r"^state/.*\.sqlite", rel) or rel == "state/workflow.sqlite":
        deny("HK2: state/workflow.sqlite is written only by scripts/transition.py — "
             "direct state writes are structurally forbidden (D-041)")

    if re.match(r"^runs/[^/]+/workorder\.yaml$", rel):
        exists = (ROOT / rel).exists()
        tool = data.get("tool_name", "")
        if tool in ("Edit", "MultiEdit") or (tool == "Write" and exists):
            deny("HK2: the work order is immutable after intake except its state: field, "
                 "which only transition.py rewrites (D-041); file human feedback via the run's feedback path")

    allow()


if __name__ == "__main__":
    main()
