#!/usr/bin/env python3
"""transition.py — the ONLY writer of workflow state (D-041, HK2).

Validates a requested transition against workflows/machines/content-trunk.yaml
(state exists, edge allowed, initiator matches), then atomically:
  1. inserts a row into state/workflow.sqlite `transitions`
  2. updates `runs.state` (creating the run row on the first transition)
  3. rewrites the work order's `state:` field

Usage:
  python scripts/transition.py --run <run-id> --to <state> --initiator <party>
      [--event <name>] [--gate-results '<json>'] [--artifact-hashes '<json>']
      [--task-id T-...] [--project <id>] [--profile script]   (first transition only)
  python scripts/transition.py --run <run-id> --rollback --reason "<why>" --initiator ORCH
  python scripts/transition.py --run <run-id> --status
"""
import argparse
import datetime
import json
import sqlite3
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "state" / "workflow.sqlite"
DDL = ROOT / "state" / "ddl.sql"
MACHINE = ROOT / "workflows" / "machines" / "content-trunk.yaml"

PRE_APPROVAL = ["requested", "intake", "context_loaded", "brief", "research", "draft",
                "fact_check", "revision", "voice_edit", "fact_delta", "compliance",
                "qa", "manager_review", "human_review"]


def now() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def open_db() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB)
    conn.executescript(DDL.read_text(encoding="utf-8"))
    return conn


def load_machine() -> dict:
    return yaml.safe_load(MACHINE.read_text(encoding="utf-8"))


def workorder_path(run_id: str) -> Path:
    return ROOT / "runs" / run_id / "workorder.yaml"


def rewrite_workorder_state(run_id: str, new_state: str) -> None:
    """Rewrite only the state: line; the work order is otherwise immutable."""
    path = workorder_path(run_id)
    if not path.exists():
        return  # first transitions may precede the work order (requested->intake writes it)
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out, replaced = [], False
    for line in lines:
        if line.startswith("state:") and not replaced:
            out.append(f"state: {new_state}\n")
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(f"state: {new_state}\n")
    path.write_text("".join(out), encoding="utf-8")


def current_state(conn: sqlite3.Connection, run_id: str):
    row = conn.execute("SELECT state FROM runs WHERE run_id=?", (run_id,)).fetchone()
    return row[0] if row else None


def next_seq(conn: sqlite3.Connection, run_id: str) -> int:
    row = conn.execute("SELECT COALESCE(MAX(seq),0)+1 FROM transitions WHERE run_id=?", (run_id,)).fetchone()
    return row[0]


def record(conn, run_id, from_state, to_state, initiator, event, gate_results, artifact_hashes,
           task_id=None, project=None, profile=None, parent_run=None):
    ts = now()
    seq = next_seq(conn, run_id)
    conn.execute(
        "INSERT INTO transitions(run_id,seq,from_state,to_state,initiator,event,gate_results,artifact_hashes,ts)"
        " VALUES(?,?,?,?,?,?,?,?,?)",
        (run_id, seq, from_state, to_state, initiator, event,
         json.dumps(gate_results), json.dumps(artifact_hashes), ts))
    if current_state(conn, run_id) is None:
        conn.execute(
            "INSERT INTO runs(run_id,task_id,project,profile,parent_run,state,created_at,updated_at)"
            " VALUES(?,?,?,?,?,?,?,?)",
            (run_id, task_id, project, profile, parent_run, to_state, ts, ts))
    else:
        conn.execute("UPDATE runs SET state=?, updated_at=? WHERE run_id=?", (to_state, ts, run_id))
    conn.commit()
    rewrite_workorder_state(run_id, to_state)
    return seq


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--to")
    ap.add_argument("--initiator")
    ap.add_argument("--event", default="transition")
    ap.add_argument("--gate-results", default="[]")
    ap.add_argument("--artifact-hashes", default="[]")
    ap.add_argument("--task-id")
    ap.add_argument("--project")
    ap.add_argument("--profile")
    ap.add_argument("--parent-run")
    ap.add_argument("--rollback", action="store_true")
    ap.add_argument("--reason")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    conn = open_db()
    machine = load_machine()
    state = current_state(conn, args.run)

    if args.status:
        print(json.dumps({"run": args.run, "state": state}))
        return 0

    if args.rollback:
        if not args.reason or not args.initiator:
            print("DENY: rollback requires --reason and --initiator", file=sys.stderr)
            return 1
        if state not in PRE_APPROVAL:
            print(f"DENY: '{state}' is not a pre-approval state; approved never silently rolls back (D-5/D-048)",
                  file=sys.stderr)
            return 1
        prev = conn.execute(
            "SELECT from_state FROM transitions WHERE run_id=? ORDER BY seq DESC LIMIT 1",
            (args.run,)).fetchone()
        if not prev:
            print("DENY: no transition history to roll back", file=sys.stderr)
            return 1
        seq = record(conn, args.run, state, prev[0], args.initiator, "rollback",
                     [{"reason": args.reason}], [])
        print(f"OK: rollback {state} -> {prev[0]} (seq {seq}, reason logged)")
        return 0

    if not args.to or not args.initiator:
        print("DENY: --to and --initiator are required", file=sys.stderr)
        return 1

    if state is None:
        # First transition of a run must be the machine's entry.
        if args.to != "requested":
            print(f"DENY: run '{args.run}' has no state; first transition must be to 'requested'",
                  file=sys.stderr)
            return 1
        if not (args.task_id and args.project):
            print("DENY: first transition requires --task-id and --project", file=sys.stderr)
            return 1
        seq = record(conn, args.run, None, "requested", args.initiator, args.event,
                     json.loads(args.gate_results), json.loads(args.artifact_hashes),
                     args.task_id, args.project, args.profile, args.parent_run)
        print(f"OK: {args.run} -> requested (seq {seq})")
        return 0

    edge = next((t for t in machine["transitions"] if t["from"] == state and args.to in t["to"]), None)
    if edge is None and args.to == "escalated":
        # escalated is a substate any state can enter (E3)
        seq = record(conn, args.run, state, "escalated", args.initiator, args.event or "escalation",
                     json.loads(args.gate_results), json.loads(args.artifact_hashes))
        print(f"OK: {args.run} {state} -> escalated (seq {seq})")
        return 0
    if edge is None:
        print(f"DENY: no transition {state} -> {args.to} in the ratified machine", file=sys.stderr)
        return 1
    if edge["initiator"] != args.initiator:
        print(f"DENY: {edge['id']} may only be initiated by {edge['initiator']}, not {args.initiator}",
              file=sys.stderr)
        return 1

    seq = record(conn, args.run, state, args.to, args.initiator, args.event,
                 json.loads(args.gate_results), json.loads(args.artifact_hashes))
    print(f"OK: {args.run} {state} -> {args.to} ({edge['id']}, seq {seq})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
