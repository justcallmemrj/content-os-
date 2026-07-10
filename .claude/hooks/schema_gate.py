#!/usr/bin/env python3
"""HK6 — PostToolUse Write|Edit on record paths: schema-on-write + queue screens.

Delegates to scripts/schema_validate.py (routing, validation, Phase 3 §9.1
screens). On violation, emits {"decision": "block"} so the writing agent sees
the exact failure and must fix it — a schema violation is a structural failure,
never patched around (master prompt §2.9).
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import ROOT, post_block, post_ok, read_input, rel_path

ROUTED_PREFIXES = ("runs/", "proposals/", "projects/", "docs/decisions/")


def main() -> None:
    data = read_input()
    tool_input = data.get("tool_input", {})
    raw = tool_input.get("file_path") or ""
    if not raw:
        post_ok()
    rel = rel_path(data, raw)
    if not rel.startswith(ROUTED_PREFIXES):
        post_ok()
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "schema_validate.py"), rel],
        capture_output=True, text=True, cwd=ROOT)
    if proc.returncode == 1:
        post_block(f"HK6: schema/screen violation — fix the record, never the gate.\n{proc.stderr.strip()}")
    post_ok()


if __name__ == "__main__":
    main()
