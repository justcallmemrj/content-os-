#!/usr/bin/env python3
"""schema_validate.py — write-time record validation + proposal-queue screens.

Used by HK6 (PostToolUse) and callable directly. Routes a file path to its
schema by location, validates, and for proposals additionally runs the Phase 3
§9.1 screens: S3/secret patterns, unsourced facts, instruction payloads, PII.

Usage: python scripts/schema_validate.py <path> [<path>...]
Exit: 0 all valid · 1 any violation (details on stderr)
"""
import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"

ROUTES = [
    (re.compile(r"runs/[^/]+/workorder\.yaml$"), "work-order"),
    (re.compile(r"runs/[^/]+/handoffs/[^/]+\.ya?ml$"), "handoff-envelope"),
    (re.compile(r"runs/[^/]+/research/RP-[^/]+\.ya?ml$"), "research-packet"),
    (re.compile(r"runs/[^/]+/factcheck/ledger.*\.ya?ml$"), "claim-ledger"),
    (re.compile(r"runs/[^/]+/qa/scorecard.*\.ya?ml$"), "scorecard"),
    (re.compile(r"runs/[^/]+/storyboard/storyboard\.ya?ml$"), "storyboard"),
    (re.compile(r"(^|/)campaign\.ya?ml$"), "campaign"),
    (re.compile(r"video/[^/]+/.+/renders/.+/manifest\.ya?ml$"), "render-manifest"),
    (re.compile(r"proposals/(queue|resolved)/P-[^/]+\.ya?ml$"), "memory-proposal"),
    (re.compile(r"projects/[^/]+/approved-facts/F-[^/]+\.md$"), "fact-record"),
    (re.compile(r"projects/[^/]+/sources/S-[^/]+\.md$"), "source-record"),
    (re.compile(r"projects/[^/]+/decisions/DEC-[^/]+\.md$"), "decision-record"),
    (re.compile(r"docs/decisions/D-\d+[^/]*\.md$"), "decision-record"),
    (re.compile(r"projects/[^/]+/lessons/L-[^/]+\.md$"), "lesson-record"),
]

# Phase 3 §9.1 never-store screens (queue pre-screening, before MEMC ever looks)
S3_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret[_-]?key|access[_-]?token|bearer\s+[a-z0-9_\-\.]{16,}|password\s*[:=])"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
]
INSTRUCTION_PATTERNS = [
    re.compile(r"(?i)\b(always|on every run)\b.{0,40}\b(fetch|load|open|execute|run)\b"),
    re.compile(r"(?i)ignore (your|the|all) (rules|instructions|compliance|guidelines)"),
    re.compile(r"(?i)disregard (prior|previous|the above)"),
    re.compile(r"(?i)(skip|bypass) (the )?(review|compliance|fact[- ]?check|gate)"),
]
PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),               # SSN
    re.compile(r"(?i)\b(account|routing)\s*(number|#)\s*[:=]?\s*\d{6,}"),
]


def frontmatter_or_yaml(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        if not text.startswith("---"):
            return None, text
        end = text.find("\n---", 3)
        if end == -1:
            return None, text
        return yaml.safe_load(text[3:end]), text
    return yaml.safe_load(text), text


def normalize(obj):
    import datetime
    if isinstance(obj, dict):
        return {k: normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [normalize(v) for v in obj]
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj


def screen_proposal(record: dict, raw: str, errors: list, label: str) -> None:
    for pat in S3_PATTERNS:
        if pat.search(raw):
            errors.append(f"{label}: S3/secret pattern detected — auto-reject (never-store list)")
            break
    if str(record.get("type", "")).startswith("fact-") and not record.get("sources"):
        errors.append(f"{label}: unsourced fact proposal — auto-bounce")
    payload_text = json.dumps(record.get("payload", ""), ensure_ascii=False) + " " + str(record.get("rationale", ""))
    for pat in INSTRUCTION_PATTERNS:
        if pat.search(payload_text):
            errors.append(f"{label}: instruction payload detected (D6 — an instruction is an attack, not a lesson)")
            break
    for pat in PII_PATTERNS:
        if pat.search(raw):
            errors.append(f"{label}: PII pattern — client-identifying data never enters permanent memory (S2 policy)")
            break


def validate_file(path: Path, errors: list) -> None:
    rel = path.resolve().relative_to(ROOT).as_posix() if path.resolve().is_relative_to(ROOT) else path.as_posix()
    schema_name = next((name for pat, name in ROUTES if pat.search(rel)), None)
    if schema_name is None:
        print(f"SKIP  {rel}: no schema route")
        return
    record, raw = frontmatter_or_yaml(path)
    if record is None:
        errors.append(f"{rel}: expected YAML frontmatter/body, found none")
        return
    record = normalize(record)
    schema = json.loads((SCHEMA_DIR / f"{schema_name}.schema.json").read_text(encoding="utf-8"))
    for err in Draft202012Validator(schema).iter_errors(record):
        errors.append(f"{rel}: [{schema_name}] {err.json_path}: {err.message}")
    if schema_name == "memory-proposal":
        screen_proposal(record, raw, errors, rel)
    if not errors:
        print(f"OK    {rel} [{schema_name}]")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) < 2:
        print("usage: schema_validate.py <path> [...]", file=sys.stderr)
        return 2
    errors: list[str] = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if not p.is_absolute():
            p = ROOT / p
        if not p.exists():
            errors.append(f"{arg}: file not found")
            continue
        validate_file(p, errors)
    if errors:
        for e in errors:
            print(f"BLOCK: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
