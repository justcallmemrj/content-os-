#!/usr/bin/env python3
"""SK-C1 text-verbatim check (D-016/D5 mechanical form; wrapper-rules §1).

Rendered-composition strings must byte-match storyboard `on_screen` strings
under the canonical form C(s) = NFC(html-unescape(s)), whitespace runs
collapsed, trimmed. Enforces:
  - every storyboard text ID present in the composition
  - no data-text-id the storyboard doesn't declare
  - no visible text node outside a data-text-id element
  - 100% canonical byte-match

Usage: python text_verbatim_check.py <storyboard.yaml> <composition_dir>
Exit 0 = pass; exit 2 = violations (escalate to VDIR — never auto-fix).
"""
import html
import html.parser
import sys
import unicodedata
from pathlib import Path

import yaml

SKIP_TAGS = {"script", "style", "head", "title", "template"}
VOID_TAGS = {"br", "img", "hr", "input", "meta", "link", "source", "track", "wbr", "area", "base", "col", "embed"}


def canon(s: str) -> str:
    return " ".join(unicodedata.normalize("NFC", s).split())


class TextCollector(html.parser.HTMLParser):
    """Collects text per innermost data-text-id element + stray visible text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, text_id_or_None)
        self.collected = {}      # text_id -> [fragments]
        self.stray = []          # fragments outside any data-text-id element

    def _skipping(self):
        return any(t in SKIP_TAGS for t, _ in self.stack)

    def _active_id(self):
        for _, tid in reversed(self.stack):
            if tid is not None:
                return tid
        return None

    def handle_starttag(self, tag, attrs):
        if tag in VOID_TAGS:
            return
        tid = dict(attrs).get("data-text-id")
        self.stack.append((tag, tid))
        if tid is not None:
            self.collected.setdefault(tid, [])

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self._skipping() or not data.strip():
            return
        tid = self._active_id()
        if tid is None:
            self.stray.append(data.strip()[:80])
        else:
            self.collected[tid].append(data)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) != 3:
        print(__doc__)
        return 1
    storyboard = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    comp_dir = Path(sys.argv[2])

    expected = {}
    for scene in storyboard["scenes"]:
        for t in scene.get("on_screen_text", []):
            expected[t["text_id"]] = t["text"]

    found, stray = {}, []
    html_files = [p for p in comp_dir.rglob("*.html")
                  if "renders" not in p.parts and "node_modules" not in p.parts]
    if not html_files:
        print(f"FAIL: no composition html under {comp_dir}")
        return 2
    for f in html_files:
        c = TextCollector()
        c.feed(f.read_text(encoding="utf-8"))
        for tid, frags in c.collected.items():
            found.setdefault(tid, []).append(canon("".join(frags)))
        stray += [(f.name, s) for s in c.stray]

    violations = []
    for tid, text in expected.items():
        if tid not in found:
            violations.append(f"MISSING: {tid} not rendered anywhere")
            continue
        want = canon(text)
        for got in found[tid]:
            if got != want:
                violations.append(f"MISMATCH {tid}:\n    storyboard: {want!r}\n    rendered:   {got!r}")
    for tid in found:
        if tid not in expected:
            violations.append(f"UNMAPPED: data-text-id={tid!r} not declared in the storyboard")
    for fname, s in stray:
        violations.append(f"STRAY TEXT in {fname} (outside any data-text-id element): {s!r}")

    matched = sum(1 for tid in expected if tid in found and all(g == canon(expected[tid]) for g in found[tid]))
    print(f"text-verbatim: {matched}/{len(expected)} IDs byte-match; "
          f"{len(violations)} violation(s)")
    for v in violations:
        print(f"  - {v}")
    if violations:
        print("ESCALATE to VDIR: text deviations are never fixed in-composition (D5).")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
