#!/usr/bin/env python3
"""SK-B16 storyboard validator — the V2 gate (Phase 5 §5), deterministic.

Checks, beyond schema validity (schema_validate covers that):
  - scene durations sum to platform_spec.duration_s ± tolerance_s
  - scenes are contiguous from 0 (no gaps/overlaps in start_s)
  - 100% on-screen text ID-mapped (schema) AND caption/claim/disclosure IDs
    unique per text
  - every asset ref resolves to the literal GAP or a manifest-style ref, with
    a rights field (schema enforces presence; this enforces non-empty)
  - every GAP is mirrored in asset_gaps[] and vice versa
  - script_ref.sha256 matches --locked-hash when provided (D5)

Usage: python storyboard_check.py <storyboard.yaml> [--locked-hash <sha256>]
Exit 0 = pass; exit 2 = violations (back to storyboard).
"""
import argparse
import sys
from pathlib import Path

import yaml


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard")
    ap.add_argument("--locked-hash")
    args = ap.parse_args()
    sb = yaml.safe_load(Path(args.storyboard).read_text(encoding="utf-8"))
    v = []

    spec = sb["platform_spec"]
    scenes = sb["scenes"]

    total = sum(s["duration_s"] for s in scenes)
    if abs(total - spec["duration_s"]) > spec["tolerance_s"]:
        v.append(f"durations sum to {total}s; spec {spec['duration_s']}±{spec['tolerance_s']}s")

    cursor = 0.0
    for s in sorted(scenes, key=lambda x: x["start_s"]):
        if abs(s["start_s"] - cursor) > 1e-6:
            v.append(f"{s['id']}: starts at {s['start_s']}, expected {cursor} (gap/overlap)")
        cursor = s["start_s"] + s["duration_s"]

    seen = {}
    for s in scenes:
        for t in s.get("on_screen_text", []):
            tid, text = t["text_id"], t["text"]
            if tid in seen and seen[tid] != text:
                v.append(f"{tid}: same ID carries two different strings")
            seen[tid] = text

    gap_scenes = {s["id"] for s in scenes for a in s.get("assets", []) if a["ref"] == "GAP"}
    listed = {g["scene_id"] for g in sb.get("asset_gaps", [])}
    for sc in gap_scenes - listed:
        v.append(f"{sc}: GAP asset not mirrored in asset_gaps[]")
    for sc in listed - gap_scenes:
        v.append(f"asset_gaps lists {sc} but no GAP asset in that scene")
    for s in scenes:
        for a in s.get("assets", []):
            if not a["rights"].strip():
                v.append(f"{s['id']}: empty rights field")

    if args.locked_hash and sb["script_ref"]["sha256"] != args.locked_hash:
        v.append(f"script_ref hash {sb['script_ref']['sha256'][:12]}… != locked {args.locked_hash[:12]}… (D5 HALT)")

    print(f"storyboard-check: {len(scenes)} scenes, {len(seen)} text IDs, {len(v)} violation(s)")
    for x in v:
        print(f"  - {x}")
    return 2 if v else 0


if __name__ == "__main__":
    sys.exit(main())
