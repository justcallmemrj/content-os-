#!/usr/bin/env python3
"""Schema lint + fixture validation (build step 1 exit criterion).

For every schemas/*.schema.json:
  1. Lint: the schema itself must be a valid Draft 2020-12 schema.
  2. Every fixture in schemas/fixtures/<name>.yaml `valid:` must validate.
  3. Every fixture in `invalid:` must be rejected.
Exit 0 only if all three hold for all schemas. A schema with no fixture file fails.
"""
import datetime
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
FIXTURE_DIR = SCHEMA_DIR / "fixtures"


def normalize(obj):
    """YAML parses bare dates/timestamps into date objects; records treat them as strings."""
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    failures = []
    checks = 0
    schema_paths = sorted(SCHEMA_DIR.glob("*.schema.json"))
    if not schema_paths:
        print("FAIL: no schemas found")
        return 1

    for schema_path in schema_paths:
        name = schema_path.name.removesuffix(".schema.json")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        try:
            Draft202012Validator.check_schema(schema)
            print(f"LINT  ok    {schema_path.name}")
        except SchemaError as e:
            failures.append(f"{schema_path.name}: schema lint failed: {e.message}")
            print(f"LINT  FAIL  {schema_path.name}: {e.message}")
            continue
        checks += 1
        validator = Draft202012Validator(schema)

        fixture_path = FIXTURE_DIR / f"{name}.yaml"
        if not fixture_path.exists():
            failures.append(f"{name}: no fixture file at {fixture_path}")
            print(f"FIXT  FAIL  {name}: fixture file missing")
            continue
        fixtures = yaml.safe_load(fixture_path.read_text(encoding="utf-8"))

        for case in fixtures.get("valid", []):
            record = normalize(case["record"])
            errors = list(validator.iter_errors(record))
            checks += 1
            if errors:
                failures.append(f"{name} valid[{case['why']}]: {errors[0].json_path}: {errors[0].message}")
                print(f"VALID FAIL  {name}: {case['why']} -> {errors[0].message}")
            else:
                print(f"VALID ok    {name}: {case['why']}")

        for case in fixtures.get("invalid", []):
            record = normalize(case["record"])
            errors = list(validator.iter_errors(record))
            checks += 1
            if errors:
                print(f"INVAL ok    {name}: {case['why']} (rejected: {errors[0].message[:70]})")
            else:
                failures.append(f"{name} invalid[{case['why']}]: was ACCEPTED but must be rejected")
                print(f"INVAL FAIL  {name}: {case['why']} -> accepted, should reject")

    print(f"\n{checks} checks, {len(failures)} failures")
    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"  - {f}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
