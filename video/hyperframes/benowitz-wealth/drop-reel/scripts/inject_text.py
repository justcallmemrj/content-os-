#!/usr/bin/env python3
"""inject_text.py — text injection for the drop-reel composition (HYPF, V4).

Reads the run's storyboard.yaml (canonical on-screen strings, D-016/D5) and
captions.yaml (segment timings) and regenerates two blocks in index.html
between sentinel comments:

  HF-INJECT:CAPTIONS — 28 caption clips (track 2) + the persistent
                       disclosure clip (track 3), every text element carrying
                       data-text-id and sitting inside an hf-safe container.
  HF-INJECT:TIMING   — the caption timing JSON the composition's timeline
                       script consumes.

Text is NEVER retyped here: every rendered string is copied programmatically
from the storyboard YAML. Presentation (zone/class/accent-span) is config;
accent spans wrap a slice of the ORIGINAL storyboard string located by exact
match — if the slice is not found, the wrap is skipped, the text unchanged.
The disclosure's two-line wrap replaces one inter-sentence space with a
newline, which is identity under the wrapper-rules §1 canonical form
(whitespace runs collapse).

Usage (from anywhere):
    python scripts/inject_text.py
Exit 0 = injected; exit 1 = configuration/consistency error (escalate).
"""
import html as html_mod
import json
import re
import sys
import unicodedata
from pathlib import Path

import yaml

PIECE = Path(__file__).resolve().parents[1]
REPO = PIECE.parents[3]  # .../content-os
STORYBOARD = REPO / "runs/2026-07-10-ben-dropvid-001/storyboard/storyboard.yaml"
CAPTIONS = REPO / "runs/2026-07-10-ben-dropvid-001/storyboard/captions.yaml"
INDEX = PIECE / "index.html"

DISC_ID = "DISC-BEN-FRS-01"
DISC_START, DISC_END = 5.0, 90.0
# two-line wrap point per visual-brief (whitespace-only change, canon-safe)
DISC_WRAP_AFTER = "Not affiliated with FRS."

# ---- presentation config (classes only — never text) ----------------------
ZONE = {}
for i in (1, 2, 3):
    ZONE[f"CAP-{i:02d}"] = "zone-upper"       # SC-01 hook: upper-center
for i in range(8, 13):
    ZONE[f"CAP-{i:02d}"] = "zone-upperlow"    # SC-03: lower third of upper zone
ZONE["CAP-28"] = "zone-lower"                 # CTA rider: above disclosure band
# all others default to zone-center

CARD_CLASS = {
    "CAP-04": "rollcall",                     # occupational roll-call, Manrope caps
    "CAP-06": "beat-xl",                      # "The rule is hard." full-frame beat
    "CAP-23": "ink",                          # paper-field scenes: navy ink type
    "CAP-24": "beat-xl ink",                  # "That's not a deadline."
    "CAP-25": "beat-xl ink",                  # "That's runway."
    "CAP-26": "ink",
    "CAP-27": "ink",
    "CAP-28": "rider",                        # consult-a-tax-professional register
}

# accent spans: (cap_id) -> (exact substring of the storyboard text, class)
SPAN_WRAP = {
    "CAP-01": ("as a single check.", "u-gold"),   # gold hairline underline
    "CAP-25": ("runway.", "au-gold"),             # gold accent, color only
}

SENT_CAP = re.compile(
    r"(<!-- HF-INJECT:CAPTIONS:BEGIN -->)(.*?)(<!-- HF-INJECT:CAPTIONS:END -->)",
    re.DOTALL,
)
SENT_TIM = re.compile(
    r"(<!-- HF-INJECT:TIMING:BEGIN -->)(.*?)(<!-- HF-INJECT:TIMING:END -->)",
    re.DOTALL,
)


def canon(s: str) -> str:
    """wrapper-rules §1 canonical form (mirror of text_verbatim_check.py)."""
    return " ".join(unicodedata.normalize("NFC", s).split())


def esc(s: str) -> str:
    return html_mod.escape(s, quote=False)


def num(v: float) -> str:
    return f"{v:g}"


def render_text(cap_id: str, text: str) -> str:
    """Escape the storyboard string; optionally wrap an exact slice of the
    ORIGINAL string in an accent span (styling only, bytes preserved)."""
    wrap = SPAN_WRAP.get(cap_id)
    if wrap:
        sub, cls = wrap
        i = text.find(sub)
        if i >= 0:
            pre, mid, post = text[:i], text[i : i + len(sub)], text[i + len(sub) :]
            return f'{esc(pre)}<span class="{cls}">{esc(mid)}</span>{esc(post)}'
        print(f"  note: accent substring not found in {cap_id}; wrap skipped")
    return esc(text)


def main() -> int:
    storyboard = yaml.safe_load(STORYBOARD.read_text(encoding="utf-8"))
    captions = yaml.safe_load(CAPTIONS.read_text(encoding="utf-8"))

    # canonical strings from the STORYBOARD (source of truth for verbatim)
    sb_text = {}
    for scene in storyboard["scenes"]:
        for t in scene.get("on_screen_text", []):
            tid, txt = t["text_id"], t["text"]
            if tid in sb_text and sb_text[tid] != txt:
                print(f"ERROR: {tid} declared twice with different text")
                return 1
            sb_text[tid] = txt

    segs = captions["segments"]

    # consistency: captions.yaml text must canon-match the storyboard string
    for s in segs:
        if s["id"] not in sb_text:
            print(f"ERROR: {s['id']} in captions.yaml but not in storyboard")
            return 1
        if canon(s["text"]) != canon(sb_text[s["id"]]):
            print(f"ERROR: {s['id']} text differs between captions.yaml and "
                  f"storyboard.yaml — escalate to VDIR, do not build")
            return 1
    if DISC_ID not in sb_text:
        print(f"ERROR: {DISC_ID} not declared in storyboard")
        return 1

    # ---- caption clips (track 2) ------------------------------------------
    parts = []
    for s in segs:
        cid, start, end = s["id"], float(s["start_s"]), float(s["end_s"])
        text = sb_text[cid]  # storyboard string, not the captions copy
        zone = ZONE.get(cid, "zone-center")
        card = ("cap-card " + CARD_CLASS[cid]) if cid in CARD_CLASS else "cap-card"
        parts.append(
            f'      <div id="clip-{cid}" class="clip cap" data-start="{num(start)}" '
            f'data-duration="{num(end - start)}" data-track-index="2">\n'
            f'        <div class="hf-safe {zone}">\n'
            f'          <div id="card-{cid}" class="{card}" data-text-id="{cid}">'
            f"{render_text(cid, text)}</div>\n"
            f"        </div>\n"
            f"      </div>"
        )

    # ---- disclosure clip (track 3), persistent 5.0 -> 90.0 ----------------
    disc = sb_text[DISC_ID]
    j = disc.find(DISC_WRAP_AFTER)
    if j >= 0:
        k = j + len(DISC_WRAP_AFTER)
        if k < len(disc) and disc[k] == " ":
            disc = disc[:k] + "\n" + disc[k + 1 :]
    parts.append(
        f'      <div id="clip-disc" class="clip disc" data-start="{num(DISC_START)}" '
        f'data-duration="{num(DISC_END - DISC_START)}" data-track-index="3">\n'
        f'        <div class="hf-safe">\n'
        f'          <div id="disc-band" class="disc-band" data-text-id="{DISC_ID}">'
        f"{esc(disc)}</div>\n"
        f"        </div>\n"
        f"      </div>"
    )

    captions_block = "\n" + "\n".join(parts) + "\n      "

    # ---- timing JSON -------------------------------------------------------
    timing = [
        {"id": s["id"], "start": float(s["start_s"]), "end": float(s["end_s"])}
        for s in segs
    ]
    timing_block = (
        '\n    <script type="application/json" id="hf-cap-timing">\n'
        + json.dumps(timing, indent=2)
        + "\n    </script>\n    "
    )

    src = INDEX.read_text(encoding="utf-8")
    if not SENT_CAP.search(src) or not SENT_TIM.search(src):
        print("ERROR: sentinel comments missing from index.html")
        return 1
    src = SENT_CAP.sub(lambda m: m.group(1) + captions_block + m.group(3), src)
    src = SENT_TIM.sub(lambda m: m.group(1) + timing_block + m.group(3), src)
    INDEX.write_text(src, encoding="utf-8", newline="\n")

    print(f"injected: {len(segs)} caption segments + {DISC_ID} "
          f"(persistent {DISC_START:g}s->{DISC_END:g}s) into {INDEX.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
