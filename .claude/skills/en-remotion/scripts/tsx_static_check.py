#!/usr/bin/env python3
"""SK-C2 static composition check — the Remotion twin of SK-C1's safe_area_check
plus the no-literal-text rule.

Enforces on every .jsx/.tsx under the composition dir:
  1. NO literal visible text in JSX positions — rendered words may only arrive
     via props expressions. Detected: a JSX text node (between > and <) with
     3+ consecutive letters. (Deterministic approximation; attribute strings,
     comments, and code outside JSX returns are not flagged. Documented
     limitation: it is a lexical scan, not a full parser — gaming it is a D7
     violation, not a pass.)
  2. Every element carrying data-text-id sits lexically inside a <SafeArea>
     element in the same file.
  3. tokens.js/tokens.ts defines the exact ratified safe-area values for the
     declared aspect ratio (same px table as SK-C1 wrapper-rules §2).

Usage: python tsx_static_check.py <composition_dir> --ar 9:16
Exit 0 = pass; exit 2 = violations.
"""
import argparse
import re
import sys
from pathlib import Path

SAFE = {
    "9:16": {"safeTop": 220, "safeBottom": 320, "safeX": 64},
    "4:5":  {"safeTop": 120, "safeBottom": 180, "safeX": 60},
    "1:1":  {"safeTop": 60,  "safeBottom": 60,  "safeX": 60},
    "16:9": {"safeTop": 54,  "safeBottom": 54,  "safeX": 96},
}

# a JSX text node: between a tag close '>' and the next '<', containing words
LITERAL_TEXT = re.compile(r">\s*([^<>{}\n]*[A-Za-z]{3,}[^<>{}\n]*)\s*<")
# prose shape: only letters/digits/spaces/basic punctuation AND >=2 real words —
# excludes code slivers the lexical scan can bite off (e.g. `= c.startS && t`)
PROSE = re.compile(r"[A-Za-z0-9 .,'’\"!?;:—\-()%$]+")


def is_prose(text: str) -> bool:
    return bool(PROSE.fullmatch(text)) and len(re.findall(r"[A-Za-z]{3,}", text)) >= 2


def strip_noise(src: str) -> str:
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)          # block comments
    src = re.sub(r"^\s*//[^\n]*$", "", src, flags=re.M)      # line comments
    src = re.sub(r"^\s*import[^\n]*$", "", src, flags=re.M)  # imports
    return src


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("composition_dir")
    ap.add_argument("--ar", required=True, choices=sorted(SAFE))
    args = ap.parse_args()
    comp_dir = Path(args.composition_dir)
    v = []

    files = [p for p in list(comp_dir.rglob("*.jsx")) + list(comp_dir.rglob("*.tsx"))
             if "node_modules" not in p.parts and "renders" not in p.parts]
    if not files:
        v.append(f"no .jsx/.tsx under {comp_dir}")

    for f in files:
        src = strip_noise(f.read_text(encoding="utf-8"))
        for m in LITERAL_TEXT.finditer(src):
            text = m.group(1).strip()
            if text and is_prose(text):
                v.append(f"{f.name}: literal JSX text {text[:60]!r} — rendered words must come from props")
        # containment: data-text-id occurrences must be inside <SafeArea>...</SafeArea>
        depth = 0
        for tok in re.finditer(r"<SafeArea\b|</SafeArea>|data-text-id", src):
            t = tok.group(0)
            if t == "data-text-id" and depth <= 0:
                v.append(f"{f.name}: data-text-id element outside <SafeArea> (offset {tok.start()})")
            elif t.startswith("<SafeArea"):
                depth += 1
            elif t == "</SafeArea>":
                depth -= 1

    token_files = [p for p in list(comp_dir.rglob("tokens.js")) + list(comp_dir.rglob("tokens.ts"))
                   if "node_modules" not in p.parts]
    if not token_files:
        v.append("no tokens.js/tokens.ts found")
    else:
        tokens_src = "\n".join(p.read_text(encoding="utf-8") for p in token_files)
        for name, want in SAFE[args.ar].items():
            m = re.search(rf"\b{name}\s*:\s*(\d+)", tokens_src)
            if not m:
                v.append(f"tokens: {name} not defined")
            elif int(m.group(1)) != want:
                v.append(f"tokens: {name} = {m.group(1)}, ratified value for {args.ar} is {want}")

    print(f"tsx-static ({args.ar}): {len(files)} files scanned, {len(v)} violation(s)")
    for x in v:
        print(f"  - {x}")
    return 2 if v else 0


if __name__ == "__main__":
    sys.exit(main())
