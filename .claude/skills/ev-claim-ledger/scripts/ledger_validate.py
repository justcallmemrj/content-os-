#!/usr/bin/env python3
"""ledger_validate.py — ledger completeness beyond the JSON Schema (SK-B2).

Layers on schemas/claim-ledger.schema.json:
  1. schema validation (via scripts/schema_validate.py machinery)
  2. every `on_screen: true` claim's text is byte-present in the deliverable (D-016)
  3. statuses verified/verified-with-qualification REQUIRE an evidence ref —
     'verified from memory' is structurally expressible, so it is structurally
     rejected (D-009 shadow for the model-judgment rule)
  4. verified-with-qualification REQUIRES qualification text
  5. blocking summary recomputed, not trusted: high-risk non-verified count

Usage: python ledger_validate.py <ledger.yaml> [--deliverable <path>]
Exit 0 valid · 1 violations
"""
import datetime
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "schemas").is_dir())
SCHEMA = json.loads((ROOT / "schemas" / "claim-ledger.schema.json").read_text(encoding="utf-8"))
VERIFIED = ("verified", "verified-with-qualification")


def normalize(obj):
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj


def validate(ledger_path: Path, deliverable_path: Path | None) -> list[str]:
    errors = []
    ledger = normalize(yaml.safe_load(ledger_path.read_text(encoding="utf-8")))

    for err in Draft202012Validator(SCHEMA).iter_errors(ledger):
        errors.append(f"schema: {err.json_path}: {err.message}")
    if errors:
        return errors

    deliverable_text = None
    if deliverable_path and deliverable_path.exists():
        deliverable_text = deliverable_path.read_text(encoding="utf-8")

    high_risk_non_verified = 0
    for claim in ledger.get("claims", []):
        cid, status = claim["id"], claim["status"]
        if status in VERIFIED and not claim.get("evidence"):
            errors.append(f"{cid}: status '{status}' without an evidence ref — "
                          "verification from memory is not a verification")
        if status == "verified-with-qualification" and not claim.get("qualification"):
            errors.append(f"{cid}: verified-with-qualification requires qualification text")
        if claim.get("on_screen") and deliverable_text is not None:
            if claim["text"] not in deliverable_text:
                errors.append(f"{cid}: on_screen text not byte-present in deliverable (D-016)")
        if claim["risk"] == "high" and status not in VERIFIED:
            high_risk_non_verified += 1

    bs = ledger.get("blocking_summary")
    if bs is not None and bs.get("high_risk_non_verified") != high_risk_non_verified:
        errors.append(f"blocking_summary says {bs.get('high_risk_non_verified')} but "
                      f"recomputed count is {high_risk_non_verified} — computed, not asserted")
    return errors


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ledger = Path(sys.argv[1])
    deliverable = None
    if "--deliverable" in sys.argv:
        deliverable = Path(sys.argv[sys.argv.index("--deliverable") + 1])
    errors = validate(ledger, deliverable)
    for e in errors:
        print(f"FAIL: {e}", file=sys.stderr)
    print(f"{'INVALID' if errors else 'VALID'}: {ledger.name} ({len(errors)} violation(s))")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
