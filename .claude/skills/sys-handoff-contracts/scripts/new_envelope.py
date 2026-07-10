#!/usr/bin/env python3
"""new_envelope.py — generate a schema-valid handoff envelope (SK-A2).

Computes artifact sha256s from disk (D1: paths + checksums, never inline
content) and validates the result against schemas/handoff-envelope.schema.json
before writing.

Usage:
  python new_envelope.py --run <id> --seq N --from-stage X --to-stage Y \
      --from-agent A --to-agent B --artifact <run-relative-path> [...] \
      [--skill SK-B2@1.0.0 ...] [--concern "..."] [--confidence high:basis]
"""
import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "schemas").is_dir())
SCHEMA = json.loads((ROOT / "schemas" / "handoff-envelope.schema.json").read_text(encoding="utf-8"))


def build(run, seq, from_stage, to_stage, from_agent, to_agent,
          artifacts, skills, concerns, confidence) -> dict:
    art_entries = []
    for rel in artifacts:
        p = ROOT / "runs" / run / rel
        art_entries.append({"path": rel,
                            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()})
    skill_entries = []
    for s in skills:
        sid, _, ver = s.partition("@")
        skill_entries.append({"id": sid, "version": ver or "1.0.0"})
    value, _, basis = confidence.partition(":")
    return {
        "run_id": run, "seq": seq,
        "stage": {"from": from_stage, "to": to_stage},
        "agents": {"from": from_agent, "to": to_agent},
        "artifacts": art_entries,
        "skills_used": skill_entries,
        "gate_results": [],
        "concerns": concerns,
        "confidence": {"value": value or "medium", "basis": basis or "unstated"},
        "approvals": [],
        "feedback_ref": None,
        "escalations": [],
    }


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--seq", type=int, required=True)
    ap.add_argument("--from-stage", required=True)
    ap.add_argument("--to-stage", required=True)
    ap.add_argument("--from-agent", required=True)
    ap.add_argument("--to-agent", required=True)
    ap.add_argument("--artifact", action="append", default=[])
    ap.add_argument("--skill", action="append", default=[])
    ap.add_argument("--concern", action="append", default=[])
    ap.add_argument("--confidence", default="medium:unstated")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    env = build(args.run, args.seq, args.from_stage, args.to_stage,
                args.from_agent, args.to_agent, args.artifact, args.skill,
                args.concern, args.confidence)
    errors = [f"{e.json_path}: {e.message}" for e in Draft202012Validator(SCHEMA).iter_errors(env)]
    if errors:
        for e in errors:
            print(f"INVALID: {e}", file=sys.stderr)
        return 1
    out = ROOT / "runs" / args.run / "handoffs" / f"{args.seq:02d}.yaml"
    if not args.dry_run:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml.safe_dump(env, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"OK: {out.relative_to(ROOT)}")
    else:
        print("OK: envelope valid (dry run)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
