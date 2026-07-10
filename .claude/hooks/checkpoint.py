#!/usr/bin/env python3
"""HK9 — PreCompact: snapshot the run log before context compaction (D-045).

Dumps runs + transitions for in-flight runs to state/checkpoints/<ts>.json.
Written by a hook process, not a Claude tool call, so HK2 does not apply.
Never blocks compaction.
"""
import datetime
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import ROOT

DB = ROOT / "state" / "workflow.sqlite"


def main() -> None:
    try:
        if not DB.exists():
            sys.exit(0)
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        runs = [dict(r) for r in conn.execute(
            "SELECT * FROM runs WHERE state NOT IN ('done','archived')")]
        if not runs:
            sys.exit(0)
        transitions = [dict(r) for r in conn.execute(
            "SELECT * FROM transitions WHERE run_id IN (SELECT run_id FROM runs "
            "WHERE state NOT IN ('done','archived')) ORDER BY run_id, seq")]
        ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = ROOT / "state" / "checkpoints" / f"{ts}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"runs": runs, "transitions": transitions}, indent=1),
                       encoding="utf-8")
    except Exception:
        pass  # snapshots never block
    sys.exit(0)


if __name__ == "__main__":
    main()
