#!/usr/bin/env python3
"""SK-C2 props-verbatim check — props.json byte-matches the storyboard (D-016/D5).

Same canonical form as SK-C1: C(s) = NFC(s), whitespace runs collapsed,
trimmed. Enforces: every storyboard text ID in props with identical text; no
prop texts the storyboard doesn't declare; captions match captions.yaml
exactly (ids, times, text).

Usage: python props_verbatim_check.py <storyboard.yaml> <captions.yaml> <props.json>
Exit 0 = pass; exit 2 = violations (escalate to VDIR — never auto-fix).
"""
import json
import sys
import unicodedata
from pathlib import Path

import yaml


def canon(s: str) -> str:
    return " ".join(unicodedata.normalize("NFC", s).split())


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) != 4:
        print(__doc__)
        return 1
    sb = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    caps = yaml.safe_load(Path(sys.argv[2]).read_text(encoding="utf-8"))
    props = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
    v = []

    expected = {}
    for scene in sb["scenes"]:
        for t in scene.get("on_screen_text", []):
            expected[t["text_id"]] = t["text"]
    got = {t["id"]: t["text"] for t in props.get("texts", [])}

    for tid, text in expected.items():
        if tid not in got:
            v.append(f"MISSING: {tid} not in props.texts")
        elif canon(got[tid]) != canon(text):
            v.append(f"MISMATCH {tid}:\n    storyboard: {canon(text)!r}\n    props:      {canon(got[tid])!r}")
    for tid in got:
        if tid not in expected:
            v.append(f"UNMAPPED: props text id {tid!r} not declared in the storyboard")

    cap_expected = {c["id"]: c for c in caps["segments"]}
    cap_got = {c["id"]: c for c in props.get("captions", [])}
    for cid, c in cap_expected.items():
        g = cap_got.get(cid)
        if g is None:
            v.append(f"MISSING caption {cid} in props")
        elif canon(g["text"]) != canon(c["text"]) or g["startS"] != c["start_s"] or g["endS"] != c["end_s"]:
            v.append(f"CAPTION DRIFT {cid}: text/timing differs from captions.yaml")
    for cid in cap_got:
        if cid not in cap_expected:
            v.append(f"UNMAPPED caption {cid} in props")

    matched = sum(1 for tid in expected if tid in got and canon(got[tid]) == canon(expected[tid]))
    print(f"props-verbatim: {matched}/{len(expected)} text IDs byte-match; "
          f"{len(cap_expected)} captions checked; {len(v)} violation(s)")
    for x in v:
        print(f"  - {x}")
    if v:
        print("ESCALATE to VDIR: text deviations are never fixed in props or code (D5).")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
