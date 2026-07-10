#!/usr/bin/env python3
"""lexicon_scan.py — cross-lexicon contamination validator (Phase 3 §3.3).

Scans a deliverable for the active project's `foreign_terms` (vocabulary that
signals another project's material). Deterministic and tunable; false
positives are cheap (a flag you dismiss), true positives are the Phase 1 top
risk caught.

Usage: python validators/lexicon_scan.py <deliverable> --project <id>
Exit: 0 clean · 1 foreign terms found
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def foreign_terms(project: str) -> list[str]:
    profile = ROOT / "projects" / project / "project-profile.md"
    text = profile.read_text(encoding="utf-8")
    end = text.find("\n---", 3)
    fm = yaml.safe_load(text[3:end])
    return fm.get("foreign_terms", [])


def scan(text: str, terms: list[str]) -> list[dict]:
    findings = []
    for term in terms:
        pat = re.compile(r"\b" + re.escape(term) + r"\b", re.IGNORECASE)
        for m in pat.finditer(text):
            line_no = text[:m.start()].count("\n") + 1
            findings.append({"term": term, "line": line_no})
    return findings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("deliverable")
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    findings = scan(Path(args.deliverable).read_text(encoding="utf-8"),
                    foreign_terms(args.project))
    for f in findings:
        print(f"CONTAMINATION: foreign term '{f['term']}' at line {f['line']} "
              f"(not {args.project} vocabulary)")
    print(f"{len(findings)} foreign-term hit(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
