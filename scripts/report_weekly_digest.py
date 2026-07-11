#!/usr/bin/env python3
"""Weekly digest — script-assembled from SQLite, the proposal queue, and git log
(Phase 6 §11; sections mirror §16.4 exactly). MEMC/QA annotate; nobody
hand-writes it. Empty sections print as such — insufficient-data is a complete
answer.

Usage: python report_weekly_digest.py [--days 7] [--out evaluations/reports/]
"""
import argparse
import datetime
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "state" / "workflow.sqlite"
QUEUE = ROOT / "proposals" / "queue"
HUMAN_GATE_STATES = {"human_review": "H2", "human_signoff": "H5",
                     "strategy_review": "H1", "launch_ready": "H4"}
CHANGE_PATHS = [".claude/skills", ".claude/agents", ".claude/hooks",
                "evaluations", "schemas", "workflows", "validators"]


def git(*args):
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    return r.stdout.strip()


def section(title, lines):
    body = "\n".join(f"- {l}" for l in lines) if lines else "- none this period"
    return f"## {title}\n\n{body}\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out", default="evaluations/reports")
    args = ap.parse_args()
    now = datetime.datetime.now(datetime.timezone.utc)
    since = (now - datetime.timedelta(days=args.days)).isoformat(timespec="seconds")

    conn = sqlite3.connect(DB) if DB.exists() else None

    # queue-derived sections
    observations, candidates, awaiting = [], [], []
    for p in sorted(QUEUE.glob("P-*.yaml")):
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        line = f"{doc['id']} ({doc.get('type','?')}, from {doc.get('run','?')}): {str(doc.get('rationale',''))[:100]}"
        if doc.get("status") == "queued":
            awaiting.append(f"{line} — awaiting MEMC batch → H6")
        if doc.get("type") == "lesson-observation":
            observations.append(line)
        if doc.get("type") in ("exemplar", "profile-gap", "decision-record"):
            candidates.append(line)

    # git-derived sections
    merges = git("log", f"--since={args.days} days ago", "--merges", "--format=%h %s").splitlines()
    approved = [m for m in merges if m]
    changes = git("log", f"--since={args.days} days ago", "--format=%h %s", "--", *CHANGE_PATHS).splitlines()
    changes = [c for c in changes if c]

    # SQLite-derived sections
    perf, rollbacks, gates_open = [], [], []
    if conn:
        rows = conn.execute(
            "SELECT rubric, COUNT(*), AVG(composite), MIN(composite), MAX(composite) "
            "FROM evals WHERE ts >= ? GROUP BY rubric", (since,)).fetchall()
        for rubric, n, avg, lo, hi in rows:
            perf.append(f"{rubric}: n={n}, composite avg {avg:.1f} (min {lo:.1f}, max {hi:.1f})")
        if not rows:
            prev = conn.execute("SELECT rubric, COUNT(*), AVG(composite) FROM evals GROUP BY rubric").fetchall()
            for rubric, n, avg in prev:
                perf.append(f"{rubric}: no new evals this period (all-time n={n}, avg {avg:.1f})")
        for run_id, seq, event, ts in conn.execute(
                "SELECT run_id, seq, event, ts FROM transitions "
                "WHERE ts >= ? AND event IN ('rollback','integrity-rollback')", (since,)).fetchall():
            rollbacks.append(f"{run_id} seq {seq}: {event} at {ts}")
        for run_id, state in conn.execute(
                "SELECT run_id, state FROM runs WHERE state IN (%s)" %
                ",".join("?" * len(HUMAN_GATE_STATES)), tuple(HUMAN_GATE_STATES)).fetchall():
            gates_open.append(f"{run_id} at {state} ({HUMAN_GATE_STATES[state]} — Wes)")

    week = now.isocalendar()
    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"digest-{week.year}-W{week.week:02d}.md"

    doc = "\n".join([
        f"# Weekly digest — {now.date().isoformat()} (last {args.days} days)",
        "",
        "Script-assembled (Phase 6 §11) from SQLite, proposals/queue, and git log.",
        "MEMC/QA annotations go below each section, never replacing generated lines.",
        "",
        section("New observations", observations),
        section("Candidate lessons / records", candidates),
        section("Approved / activated (merges)", approved),
        section("Rejected (with reasons)",
                []),   # populated from resolved proposals with rejection notes when MEMC resolves any
        section("Prompt / Skill / agent / eval changes (commit log)", changes),
        section("Performance changes (ANLYT deltas)", perf),
        section("Regressions and rollbacks", rollbacks),
        section("Decisions awaiting Wes", awaiting + gates_open),
    ])
    out.write_text(doc, encoding="utf-8")
    print(f"OK: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
