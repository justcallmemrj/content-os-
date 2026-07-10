#!/usr/bin/env python3
"""duration_check.py — spoken word count vs. format band (SK-B3).

190 words ≈ 90 seconds for to-camera financial content (NOT 140-wpm podcast
pace — the speaker pauses after claims and the viewer needs the pause).
Counts only spoken words: delivery markers, [TEXT ON SCREEN] strings, headers,
and blockquotes are excluded.

Usage: python duration_check.py <draft.md> [--format reel-90s]
Exit 0 in band · 1 outside
"""
import re
import sys
from pathlib import Path

BANDS = {                     # words (min, max) per format
    "reel-90s": (170, 200),
    "reel-60s": (110, 135),
    "reel-30s": (55, 70),
}
MARKER_LINE = re.compile(r"^\s*(\[|>|#|\||-{3,})")
INLINE_MARKER = re.compile(r"\[(TO CAMERA|VO / B-ROLL:[^\]]*|TEXT ON SCREEN:[^\]]*)\]", re.I)


def spoken_words(text: str) -> int:
    count = 0
    for line in text.splitlines():
        clean = INLINE_MARKER.sub("", line)   # strip delivery markers first —
        if MARKER_LINE.match(clean):          # spoken lines START with [TO CAMERA]
            continue                          # what remains bracketed is structure
        count += len(clean.split())
    return count


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    path = Path(sys.argv[1])
    fmt = sys.argv[sys.argv.index("--format") + 1] if "--format" in sys.argv else "reel-90s"
    lo, hi = BANDS[fmt]
    n = spoken_words(path.read_text(encoding="utf-8"))
    est = round(n / 190 * 90)
    ok = lo <= n <= hi
    print(f"{'PASS' if ok else 'FAIL'}: {n} spoken words (band {lo}-{hi} for {fmt}; ~{est}s est)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
