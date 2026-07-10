#!/usr/bin/env python3
"""generate_indexes.py — derives what no one hand-maintains (Phase 3 §5.1, D-066).

Per project: approved-facts/_index.yaml, approved-facts/_claim-keys.yaml,
sources/_index.yaml (including generated cited_by). Two ACTIVE facts sharing a
claim_key is a mechanically-detected conflict -> exit 1 with the collision list.

cited_by is written into sources/_index.yaml, not into the protected S-*.md
files (index regeneration is auto-commit class 3; editing protected records is not).

Usage: python scripts/generate_indexes.py [--project <id>] [--check]
"""
import argparse
import hashlib
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ["benowitz-wealth", "ducat-private-wealth", "trading-research", "founder-brand"]


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return yaml.safe_load(text[3:end])


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(project: str, check: bool) -> list[str]:
    errors = []
    pdir = ROOT / "projects" / project
    facts_dir, sources_dir = pdir / "approved-facts", pdir / "sources"

    facts, claim_keys, cited_by = [], {}, {}
    for f in sorted(facts_dir.glob("F-*.md")):
        fm = frontmatter(f)
        if not fm:
            errors.append(f"{f}: no frontmatter")
            continue
        facts.append({"id": fm["id"], "claim_key": fm.get("claim_key"), "status": fm.get("status"),
                      "review_by": str(fm.get("review_by")), "file": f.name, "sha256": sha256(f)})
        claim_keys.setdefault(fm.get("claim_key"), []).append({"id": fm["id"], "status": fm.get("status")})
        for sid in fm.get("source_ids", []):
            cited_by.setdefault(sid, []).append(fm["id"])

    for key, entries in claim_keys.items():
        active = [e["id"] for e in entries if e["status"] == "active"]
        if len(active) > 1:
            errors.append(f"{project}: claim_key conflict '{key}': {active} all active (Phase 3 §7 case 1)")

    sources = []
    for s in sorted(sources_dir.glob("S-*.md")):
        fm = frontmatter(s)
        if not fm:
            errors.append(f"{s}: no frontmatter")
            continue
        sources.append({"id": fm["id"], "type": fm.get("type"), "tier": fm.get("tier"),
                        "status": fm.get("status"), "stability": fm.get("stability"),
                        "cited_by": sorted(cited_by.get(fm["id"], [])), "file": s.name, "sha256": sha256(s)})

    if not check and not errors:
        (facts_dir / "_index.yaml").write_text(
            yaml.safe_dump({"generated": True, "project": project, "facts": facts}, sort_keys=False),
            encoding="utf-8")
        (facts_dir / "_claim-keys.yaml").write_text(
            yaml.safe_dump({"generated": True, "project": project,
                            "claim_keys": {k: [e["id"] for e in v] for k, v in claim_keys.items() if k}},
                           sort_keys=False), encoding="utf-8")
        (sources_dir / "_index.yaml").write_text(
            yaml.safe_dump({"generated": True, "project": project, "sources": sources}, sort_keys=False),
            encoding="utf-8")
    return errors


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", choices=PROJECTS)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    all_errors = []
    for project in ([args.project] if args.project else PROJECTS):
        all_errors += build(project, args.check)
    if all_errors:
        for e in all_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print("OK: indexes " + ("verified" if args.check else "regenerated"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
