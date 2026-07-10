#!/usr/bin/env python3
"""structure_check.py — 7-beat skeleton, markers, single CTA, banned openings (SK-B3).

Checks: all seven beats present ([HOOK] [STAKES] [BEAT ONE] [BEAT TWO]
[BEAT THREE] [TURN] [CTA]); exactly one CTA; a delivery marker on every spoken
block; zero banned openings from the loaded profile; on-screen disclosure
block present.

Usage: python structure_check.py <draft.md> --project <id>
Exit 0 pass · 1 findings
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "projects").is_dir())

BEATS = ["HOOK", "STAKES", "BEAT ONE", "BEAT TWO", "BEAT THREE", "TURN", "CTA"]
DELIVERY = re.compile(r"\[(TO CAMERA|VO / B-ROLL:|TEXT ON SCREEN:)", re.I)
BEAT_HEADER = re.compile(r"^\s*\[(?:\d:\d\d\s+)?([A-Z ]+?)\]")


def banned_openings(project: str) -> list[str]:
    bv = ROOT / "projects" / project / "brand-voice.md"
    text = bv.read_text(encoding="utf-8")
    fm = yaml.safe_load(text[3:text.find("\n---", 3)])
    return fm.get("banned_openings", [])


def check(text: str, project: str) -> list[str]:
    findings = []
    for beat in BEATS:
        if not re.search(r"\[(?:\d:\d\d\s+)?" + beat + r"\]", text):
            findings.append(f"beat missing: [{beat}]")
    cta_count = len(re.findall(r"\[(?:\d:\d\d\s+)?CTA\]", text))
    if cta_count > 1:
        findings.append(f"{cta_count} CTA blocks — one ask, never two")

    # every spoken block (text between beat headers) must carry a delivery marker
    blocks = re.split(r"^\s*\[(?:\d:\d\d\s+)?[A-Z ]+\]\s*$", text, flags=re.M)
    for i, block in enumerate(blocks[1:], 1):
        if block.strip() and not DELIVERY.search(block):
            findings.append(f"block {i} has spoken text but no delivery marker")

    for opening in banned_openings(project):
        if re.search(r"(?im)^\s*(\[[^\]]+\]\s*)*" + re.escape(opening), text):
            findings.append(f"banned opening: {opening!r}")
        elif opening.lower() in text.lower()[:400]:
            findings.append(f"banned opening pattern near the top: {opening!r}")

    if not re.search(r"\[TEXT ON SCREEN:[^\]]*(educational|not affiliated|disclosure)", text, re.I):
        findings.append("no persistent on-screen disclosure block found "
                        "(spoken disclaimers cost the viewer — SK-B15 placement rule)")
    return findings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("draft")
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    findings = check(Path(args.draft).read_text(encoding="utf-8"), args.project)
    for f in findings:
        print(f"FAIL: {f}")
    print(f"{'PASS' if not findings else 'FAIL'}: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
