#!/usr/bin/env python3
"""HK7 — SessionStart: resume protocol (D-045, Phase 5 §8.1).

If in-flight runs exist: verify the last envelope's artifact checksums against
disk and inject a state summary as additionalContext. Never blocks a session —
it informs; integrity failures instruct ORCH to run the integrity-rollback via
transition.py.
"""
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import ROOT

DB = ROOT / "state" / "workflow.sqlite"

try:
    import yaml
except ImportError:
    yaml = None


def check_run(run_id: str) -> dict:
    result = {"run": run_id, "checksums": "no-envelopes"}
    handoffs = sorted((ROOT / "runs" / run_id / "handoffs").glob("*.yaml")) if yaml else []
    if not handoffs:
        return result
    env = yaml.safe_load(handoffs[-1].read_text(encoding="utf-8"))
    bad = []
    for art in env.get("artifacts", []):
        p = ROOT / "runs" / run_id / art["path"]
        if not p.exists():
            bad.append(f"{art['path']}: missing")
        elif hashlib.sha256(p.read_bytes()).hexdigest() != art.get("sha256"):
            bad.append(f"{art['path']}: checksum mismatch")
    result["checksums"] = "intact" if not bad else bad
    result["last_envelope"] = handoffs[-1].name
    return result


def main() -> None:
    if not DB.exists():
        sys.exit(0)
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT run_id, state, updated_at FROM runs WHERE state NOT IN ('done','archived')").fetchall()
    if not rows:
        sys.exit(0)
    summary = []
    for run_id, state, updated in rows:
        entry = {"run": run_id, "state": state, "updated_at": updated}
        entry.update(check_run(run_id))
        summary.append(entry)
    context = ("HK7 resume check — in-flight runs found. Resume at the recorded state; "
               "if any checksum is not 'intact', roll back one state via transition.py "
               "with event integrity-rollback and re-execute that stage (Phase 5 §8.1). "
               + json.dumps(summary))
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "SessionStart", "additionalContext": context}}))
    sys.exit(0)


if __name__ == "__main__":
    main()
