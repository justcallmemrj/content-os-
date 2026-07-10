#!/usr/bin/env python3
"""calendar_check.py — calendar hygiene (SK-B12). A calendar is planning:
every row sourced, touchpoints listed, zero copy-artifacts (disclosures/hooks).

Usage: python calendar_check.py <calendar.md>
Exit 0 pass · 1 findings
"""
import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|(?!\s*-)(.+)\|\s*$", re.M)
DISCLOSURE_TEXT = re.compile(r"(?i)(educational content only|not individualized|is a brand of)")
TOUCHPOINTS = re.compile(r"(?i)compliance touchpoints")


def check(text: str) -> list[str]:
    findings = []
    rows = [r for r in ROW.findall(text) if "---" not in r]
    if len(rows) < 2:
        findings.append("no calendar table found")
        return findings
    header = [c.strip().lower() for c in rows[0].split("|")]
    if not any("source" in c for c in header):
        findings.append("no source column — every row names the asset it's cut from")
    else:
        src_idx = next(i for i, c in enumerate(header) if "source" in c)
        for i, row in enumerate(rows[1:], 1):
            cells = [c.strip() for c in row.split("|")]
            if len(cells) > src_idx and not cells[src_idx]:
                findings.append(f"row {i}: empty source cell ('New' is valid; empty is not)")
    if not TOUCHPOINTS.search(text):
        findings.append("no compliance-touchpoints section — which weeks need the careful hand?")
    if DISCLOSURE_TEXT.search(text):
        findings.append("disclosure text on a calendar — calendars are planning, not writing")
    return findings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    findings = check(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for f in findings:
        print(f"FAIL: {f}")
    print(f"{'PASS' if not findings else 'FAIL'}: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
