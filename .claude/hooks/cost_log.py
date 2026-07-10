#!/usr/bin/env python3
"""HK8 — PostToolUse on Agent calls: per-subagent cost telemetry → costs table (D-072).

Best-effort and silent: telemetry must never break a run. Reads whatever usage
fields the harness provides on the completed Agent tool call.
"""
import datetime
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import ROOT, read_input

DB = ROOT / "state" / "workflow.sqlite"
DDL = ROOT / "state" / "ddl.sql"


def dig(obj, *keys):
    for k in keys:
        if isinstance(obj, dict) and k in obj:
            obj = obj[k]
        else:
            return None
    return obj


def main() -> None:
    try:
        data = read_input()
        resp = data.get("tool_response") or {}
        usage = resp.get("usage") or dig(resp, "meta", "usage") or {}
        tool_input = data.get("tool_input") or {}
        conn = sqlite3.connect(DB)
        conn.executescript(DDL.read_text(encoding="utf-8"))
        conn.execute(
            "INSERT INTO costs(run_id,stage,agent,model,input_tokens,output_tokens,usd,ts)"
            " VALUES(?,?,?,?,?,?,?,?)",
            (dig(resp, "run_id") or "",
             "",
             tool_input.get("subagent_type") or data.get("agent_type") or "",
             tool_input.get("model") or "",
             usage.get("input_tokens") or usage.get("inputTokens"),
             usage.get("output_tokens") or usage.get("outputTokens")
                or usage.get("subagent_tokens"),
             None,
             datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")))
        conn.commit()
    except Exception:
        pass  # telemetry never blocks
    sys.exit(0)


if __name__ == "__main__":
    main()
