#!/usr/bin/env python3
"""SK-C3 caption validator — the V7 caption gate (CPS / line / timing), deterministic.

Input: a captions YAML (list under `segments:` with id, start_s, end_s, text —
the storyboard-derived caption track the composition consumes), plus the video
duration.

Limits (SK-C3 ⚑ step-8 values): CPS<=17; <=2 lines; <=42 chars/line;
0.8s<=duration<=7s; no overlaps; inside video bounds; ids CAP-NN unique.

Usage: python caption_check.py <captions.yaml> --video-duration <s>
Exit 0 = pass; exit 2 = violations.
"""
import argparse
import sys
from pathlib import Path

import yaml

CPS_MAX = 17.0
LINES_MAX = 2
LINE_CHARS_MAX = 42
DUR_MIN, DUR_MAX = 0.8, 7.0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("captions")
    ap.add_argument("--video-duration", type=float, required=True)
    args = ap.parse_args()
    doc = yaml.safe_load(Path(args.captions).read_text(encoding="utf-8"))
    segs = doc["segments"]
    v = []

    seen = set()
    prev_end, prev_id = -1.0, None
    for s in sorted(segs, key=lambda x: x["start_s"]):
        sid, text = s["id"], s["text"]
        dur = s["end_s"] - s["start_s"]
        if sid in seen:
            v.append(f"{sid}: duplicate id")
        seen.add(sid)
        if dur < DUR_MIN or dur > DUR_MAX:
            v.append(f"{sid}: on-screen {dur:.2f}s (limits {DUR_MIN}-{DUR_MAX}s)")
        if dur > 0 and len(text) / dur > CPS_MAX:
            v.append(f"{sid}: {len(text)/dur:.1f} CPS > {CPS_MAX}")
        lines = text.split("\n")
        if len(lines) > LINES_MAX:
            v.append(f"{sid}: {len(lines)} lines > {LINES_MAX}")
        for ln in lines:
            if len(ln) > LINE_CHARS_MAX:
                v.append(f"{sid}: line {len(ln)} chars > {LINE_CHARS_MAX}: {ln[:50]!r}")
        if s["start_s"] < prev_end - 1e-6:
            v.append(f"{sid}: overlaps {prev_id}")
        if s["start_s"] < 0 or s["end_s"] > args.video_duration + 1e-6:
            v.append(f"{sid}: outside video bounds (0-{args.video_duration}s)")
        prev_end, prev_id = s["end_s"], sid

    print(f"caption-check: {len(segs)} segments, {len(v)} violation(s)")
    for x in v:
        print(f"  - {x}")
    return 2 if v else 0


if __name__ == "__main__":
    sys.exit(main())
