#!/usr/bin/env python3
"""SK-C2 props generator — storyboard/captions -> props.json (the ONLY text source).

Deterministic: sorted keys, canonical text passthrough (no rewriting — the
strings are copied byte-for-byte from the YAMLs).

Usage: python gen_props.py <storyboard.yaml> <captions.yaml> <out_props.json>
"""
import json
import sys
from pathlib import Path

import yaml


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) != 4:
        print(__doc__)
        return 1
    sb = yaml.safe_load(Path(sys.argv[1]).read_text(encoding="utf-8"))
    caps = yaml.safe_load(Path(sys.argv[2]).read_text(encoding="utf-8"))

    texts, seen = [], set()
    for scene in sb["scenes"]:
        for t in scene.get("on_screen_text", []):
            if t["text_id"] not in seen:
                seen.add(t["text_id"])
                texts.append({"id": t["text_id"], "text": t["text"],
                              "persistent": bool(t.get("persistent", False))})

    props = {
        "runId": sb["run_id"],
        "spec": {
            "fps": sb["platform_spec"]["fps"],
            "durationS": sb["platform_spec"]["duration_s"],
            "resolution": sb["platform_spec"]["resolution"],
            "aspectRatio": sb["platform_spec"]["aspect_ratio"],
        },
        "scenes": [{"id": s["id"], "startS": s["start_s"], "durationS": s["duration_s"],
                    "type": s["type"]} for s in sb["scenes"]],
        "texts": texts,
        "captions": [{"id": c["id"], "startS": c["start_s"], "endS": c["end_s"],
                      "text": c["text"]} for c in caps["segments"]],
    }
    out = Path(sys.argv[3])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(props, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(f"OK: props.json — {len(texts)} texts, {len(props['captions'])} captions")
    return 0


if __name__ == "__main__":
    sys.exit(main())
