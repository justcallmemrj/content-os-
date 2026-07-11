#!/usr/bin/env python3
"""Monthly review — the ANLYT deep pass (Phase 6 §11): hypothesis-log status,
threshold-tuning proposals, cost/latency trends, calibration results.
Script-assembled; where a section has no data yet, it says so —
insufficient-data is a complete answer.

Usage: python report_monthly.py [--out evaluations/reports/]
"""
import argparse
import datetime
import sqlite3
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "state" / "workflow.sqlite"
QUEUE = ROOT / "proposals" / "queue"
HYPO = ROOT / "evaluations" / "hypothesis-log.md"


def section(title, lines):
    body = "\n".join(f"- {l}" for l in lines) if lines else "- insufficient data this period (a complete answer, Phase 6 §7)"
    return f"## {title}\n\n{body}\n"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="evaluations/reports")
    args = ap.parse_args()
    now = datetime.datetime.now(datetime.timezone.utc)
    conn = sqlite3.connect(DB) if DB.exists() else None

    hypo = []
    if HYPO.exists():
        entries = [l for l in HYPO.read_text(encoding="utf-8").splitlines() if l.startswith("- ")]
        hypo = [f"{len(entries)} entries in the hypothesis log; review each for status change"] + entries[:20]

    thresholds = []
    for p in sorted(QUEUE.glob("P-*.yaml")):
        doc = yaml.safe_load(p.read_text(encoding="utf-8"))
        if "threshold" in str(doc.get("rationale", "")).lower():
            thresholds.append(f"{doc['id']}: {str(doc.get('rationale',''))[:120]}")

    costs, calib = [], []
    if conn:
        rows = conn.execute(
            "SELECT strftime('%Y-W%W', ts), COUNT(*), SUM(usd), SUM(input_tokens), SUM(output_tokens) "
            "FROM costs GROUP BY 1 ORDER BY 1 DESC LIMIT 8").fetchall()
        for wk, n, usd, ti, to in rows:
            costs.append(f"{wk}: {n} stage-calls, ${usd or 0:.2f}, {ti or 0} in / {to or 0} out tokens")
        rows = conn.execute(
            "SELECT rubric, COUNT(*), AVG(composite), SUM(required_pass), COUNT(*) - SUM(required_pass) "
            "FROM evals GROUP BY rubric").fetchall()
        for rubric, n, avg, req_pass, req_fail in rows:
            calib.append(f"{rubric}: n={n}, avg composite {avg:.1f}, required pass {req_pass}/{n}"
                         + (f" — {req_fail} required-failures to post-mortem" if req_fail else ""))

    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"monthly-{now.year}-{now.month:02d}.md"
    doc = "\n".join([
        f"# Monthly review — {now.date().isoformat()} (ANLYT deep pass, Phase 6 §11)",
        "",
        section("Hypothesis-log status", hypo),
        section("Threshold-tuning proposals (evidence-backed only)", thresholds),
        section("Cost / latency trends (SQLite costs, by week)", costs),
        section("Calibration (composites vs required outcomes, per rubric)", calib),
        "## Is the system actually getting better?",
        "",
        "ANLYT answers here from the sections above — with SK-B13's language",
        "discipline: causal verbs only for designed experiments.",
    ])
    out.write_text(doc, encoding="utf-8")
    print(f"OK: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
