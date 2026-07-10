#!/usr/bin/env python3
"""new_proposal.py — generate a schema-valid memory proposal (SK-A3).

Validates against schemas/memory-proposal.schema.json AND the Phase 3 §9.1
queue screens (via scripts/schema_validate.py) before writing to
proposals/queue/.

Usage: python new_proposal.py --origin VOICE --type voice-phrase \
    --target "projects/.../brand-voice.md#avoided_phrases" \
    --payload '{"add": "..."}' --rationale "..." [--run <id>] [--source S-...]
"""
import argparse
import datetime
import json
import subprocess
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "schemas").is_dir())


def next_id() -> str:
    today = datetime.date.today().strftime("%Y-%m%d")
    existing = sorted((ROOT / "proposals" / "queue").glob(f"P-{today}-*.yaml"))
    seq = len(existing) + 1
    return f"P-{today}-{seq:03d}"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--origin", required=True)
    ap.add_argument("--type", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--payload", required=True, help="JSON")
    ap.add_argument("--rationale", required=True)
    ap.add_argument("--run")
    ap.add_argument("--source", action="append", default=[])
    ap.add_argument("--sensitivity", default="S1")
    ap.add_argument("--consequence", default="consequential")
    args = ap.parse_args()

    record = {
        "id": next_id(), "run": args.run, "origin_agent": args.origin,
        "type": args.type, "target": args.target,
        "payload": json.loads(args.payload), "rationale": args.rationale,
        "consequence_class": args.consequence, "sources": args.source,
        "sensitivity": args.sensitivity, "status": "queued",
        "memc": {"triaged_at": None, "notes": None, "staged_in": None, "resolved_by": None},
    }
    out = ROOT / "proposals" / "queue" / f"{record['id']}.yaml"
    out.write_text(yaml.safe_dump(record, sort_keys=False, allow_unicode=True), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "schema_validate.py"),
                           str(out.relative_to(ROOT))], capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        out.unlink()          # a proposal that fails the screens never enters the queue
        print(proc.stderr.strip(), file=sys.stderr)
        print("REJECTED: proposal failed validation/screens; not queued")
        return 1
    print(f"OK: queued {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
