#!/usr/bin/env python3
"""SK-C1 safe-area check (wrapper-rules §2).

Enforces, for the declared aspect ratio:
  - tokens.css defines --safe-top/--safe-bottom/--safe-x with the EXACT
    ratified values
  - every data-text-id element is inside an element with class hf-safe
  - no negative inline offsets on data-text-id elements

Usage: python safe_area_check.py <composition_dir> --ar 9:16
Exit 0 = pass; exit 2 = violations.
"""
import argparse
import html.parser
import re
import sys
from pathlib import Path

SAFE = {   # wrapper-rules §2 (⚑ values assumption-tagged; ratification rides the step-8 PR)
    "9:16": {"--safe-top": "220px", "--safe-bottom": "320px", "--safe-x": "64px"},
    "4:5":  {"--safe-top": "120px", "--safe-bottom": "180px", "--safe-x": "60px"},
    "1:1":  {"--safe-top": "60px",  "--safe-bottom": "60px",  "--safe-x": "60px"},
    "16:9": {"--safe-top": "54px",  "--safe-bottom": "54px",  "--safe-x": "96px"},
}


class SafeChecker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []       # per-element: has hf-safe class?
        self.violations = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        safe = "hf-safe" in (a.get("class") or "").split()
        self.stack.append(safe)
        tid = a.get("data-text-id")
        if tid:
            if not any(self.stack):
                self.violations.append(f"{tid}: not inside an hf-safe container")
            style = a.get("style") or ""
            if re.search(r"(top|bottom|left|right|margin[^:]*)\s*:\s*-", style):
                self.violations.append(f"{tid}: negative inline offset in style={style!r}")

    def handle_endtag(self, tag):
        if self.stack:
            self.stack.pop()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("composition_dir")
    ap.add_argument("--ar", required=True, choices=sorted(SAFE))
    args = ap.parse_args()
    comp_dir = Path(args.composition_dir)

    violations = []

    css_files = [p for p in comp_dir.rglob("*.css") if "renders" not in p.parts]
    css_text = "\n".join(p.read_text(encoding="utf-8") for p in css_files)
    for var, want in SAFE[args.ar].items():
        m = re.search(re.escape(var) + r"\s*:\s*([^;]+);", css_text)
        if not m:
            violations.append(f"{var} not defined in any tokens css")
        elif m.group(1).strip() != want:
            violations.append(f"{var} = {m.group(1).strip()!r}, ratified value for {args.ar} is {want!r}")

    html_files = [p for p in comp_dir.rglob("*.html")
                  if "renders" not in p.parts and "node_modules" not in p.parts]
    if not html_files:
        violations.append(f"no composition html under {comp_dir}")
    for f in html_files:
        c = SafeChecker()
        c.feed(f.read_text(encoding="utf-8"))
        violations += [f"{f.name}: {v}" for v in c.violations]

    print(f"safe-area ({args.ar}): {len(violations)} violation(s)")
    for v in violations:
        print(f"  - {v}")
    return 2 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
