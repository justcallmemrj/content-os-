#!/usr/bin/env python3
"""inherit_ledger.py — hash-verified ledger inheritance for adaptations (SK-B5, D-047).

Unchanged claims (byte-identical text present in the child draft) inherit the
parent's status + history with an `inherited` event; changed/new material gets
fresh unverified entries for FACT's delta-scope adjudication. Refuses when the
parent artifact no longer matches its locked hash.

Usage: python inherit_ledger.py --parent-run <id> --parent-artifact <path>
       --parent-artifact-hash <sha256> --child-draft <path> --child-run <id>
       --out <path> [--new-claim "text::risk" ...]
"""
import argparse
import datetime
import hashlib
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "schemas").is_dir())


def now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--parent-run", required=True)
    ap.add_argument("--parent-artifact", required=True)
    ap.add_argument("--parent-artifact-hash", required=True)
    ap.add_argument("--child-draft", required=True)
    ap.add_argument("--child-run", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--new-claim", action="append", default=[],
                    help='"text::risk" for claims the adaptation introduces')
    args = ap.parse_args()

    parent_artifact = Path(args.parent_artifact)
    actual = hashlib.sha256(parent_artifact.read_bytes()).hexdigest()
    if actual != args.parent_artifact_hash:
        print(f"REFUSED: parent artifact hash mismatch — locked "
              f"{args.parent_artifact_hash[:12]}…, found {actual[:12]}…; "
              "the approved parent is not what is on disk (D5)", file=sys.stderr)
        return 1

    parent_ledger = yaml.safe_load(
        (ROOT / "runs" / args.parent_run / "factcheck" / "ledger.yaml")
        .read_text(encoding="utf-8"))
    child_text = Path(args.child_draft).read_text(encoding="utf-8")

    claims, inherited, fresh = [], 0, 0
    for claim in parent_ledger["claims"]:
        if claim["text"] in child_text:                     # byte-identity buys inheritance
            c = dict(claim)
            c["history"] = list(claim["history"]) + [
                {"at": now(), "event": "adjudicated", "by": "FACT",
                 "note": f"inherited from {args.parent_run} (parent hash verified)"}]
            claims.append(c)
            inherited += 1
    for spec in args.new_claim:
        text, _, risk = spec.partition("::")
        fresh += 1
        claims.append({
            "id": f"CL-{len(claims)+1:02d}A",
            "text": text, "location": {"file": Path(args.child_draft).name, "anchor": "adaptation"},
            "risk": risk or "medium", "declared_by": "WRITE", "status": "unverified",
            "on_screen": False,
            "history": [{"at": now(), "event": "declared", "by": "WRITE"}]})

    high_risk_nv = sum(1 for c in claims if c["risk"] == "high"
                       and c["status"] not in ("verified", "verified-with-qualification"))
    child = {
        "run": args.child_run,
        "deliverable": Path(args.child_draft).name,
        "version": 1,
        "passes": [{"type": "delta", "by": "FACT", "at": now(),
                    "trigger": f"adaptation inheritance from {args.parent_run}"}],
        "claims": claims,
        "blocking_summary": {"high_risk_non_verified": high_risk_nv,
                             "notes": f"{inherited} inherited (hash-verified), {fresh} fresh for FACT delta"},
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(child, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"OK: {inherited} inherited, {fresh} fresh, high_risk_non_verified={high_risk_nv} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
