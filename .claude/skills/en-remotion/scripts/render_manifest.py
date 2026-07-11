#!/usr/bin/env python3
"""SK-C2 render-manifest writer — the Remotion twin of SK-C1's (RM- prefix).

Same schema (schemas/render-manifest.schema.json), same refusals: engine
version must equal the DEC-BUILD-008 pin; additionally verifies the workspace
package.json still pins exactly (guards a floated install).

Usage: identical flags to SK-C1's render_manifest.py.
"""
import argparse
import datetime
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

PIN_COMMIT = "2e8037fec3cad711a8becf1252ed3af61f09a1fa"   # remotion v4.0.487 (DEC-BUILD-008)
PIN_VERSION = "4.0.487"
ROOT = Path(__file__).resolve().parents[4]
SCHEMA = ROOT / "schemas" / "render-manifest.schema.json"
WORKSPACE_PKG = ROOT / "video" / "remotion" / "package.json"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rel(p: Path) -> str:
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def probe(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=False)
        return out.stdout.strip() or out.stderr.strip()
    except Exception:
        return ""


def next_manifest_id() -> str:
    today = datetime.date.today()
    base = f"RM-{today.year}-{today.month:02d}{today.day:02d}"
    existing = {m.group(0) for p in (ROOT / "video").rglob("manifest.yaml")
                for m in [re.search(re.escape(base) + r"-(\d{2})", p.read_text(encoding="utf-8"))] if m}
    return f"{base}-{len(existing) + 1:02d}"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--storyboard", required=True)
    ap.add_argument("--composition-dir", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--preset", required=True)
    ap.add_argument("--resolution", required=True)
    ap.add_argument("--fps", type=float, required=True)
    ap.add_argument("--aspect-ratio", required=True)
    ap.add_argument("--duration", type=float)
    ap.add_argument("--engine-version", default=PIN_VERSION)
    ap.add_argument("--notes", default="deviations: zero")
    ap.add_argument("--manifest-out", required=True)
    args = ap.parse_args()

    if args.engine_version != PIN_VERSION:
        print(f"REFUSED: engine version {args.engine_version} != ratified pin {PIN_VERSION} (DEC-BUILD-008)")
        return 2
    pkg = json.loads(WORKSPACE_PKG.read_text(encoding="utf-8"))
    for dep in ("remotion", "@remotion/cli"):
        if pkg.get("dependencies", {}).get(dep) != PIN_VERSION:
            print(f"REFUSED: workspace package.json pins {dep}={pkg.get('dependencies', {}).get(dep)!r}, "
                  f"expected exactly {PIN_VERSION!r} (a floated install; DEC-BUILD-008)")
            return 2

    comp_dir = Path(args.composition_dir)
    out_file = Path(args.output)
    if not out_file.exists():
        print(f"REFUSED: output {out_file} does not exist")
        return 2

    duration = args.duration
    if duration is None:
        probed = probe(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(out_file)])
        try:
            duration = float(probed)
        except ValueError:
            print("REFUSED: no --duration and ffprobe could not read the output")
            return 2

    comp_files = sorted(p for p in list(comp_dir.rglob("*.jsx")) + list(comp_dir.rglob("*.tsx"))
                        if "node_modules" not in p.parts and "renders" not in p.parts)
    input_files = sorted(p for p in list(comp_dir.rglob("*.json")) + list(comp_dir.rglob("tokens.js"))
                         + list(comp_dir.rglob("tokens.ts")) + list(comp_dir.rglob("*.css"))
                         if "node_modules" not in p.parts and "renders" not in p.parts)

    node_v = probe(["node", "--version"]).lstrip("v")
    ffm = probe(["ffmpeg", "-version"]).splitlines()
    ffmpeg_v = ffm[0].split()[2] if ffm and len(ffm[0].split()) > 2 else "unknown"

    manifest = {
        "manifest_id": next_manifest_id(),
        "run_id": args.run,
        "engine": "remotion",
        "engine_version": args.engine_version,
        "upstream_pin": PIN_COMMIT,
        "storyboard": {"path": rel(Path(args.storyboard)), "sha256": sha256(Path(args.storyboard))},
        "composition": [{"path": rel(p), "sha256": sha256(p)} for p in comp_files],
        "settings": {"resolution": args.resolution, "fps": args.fps,
                     "duration_s": duration, "aspect_ratio": args.aspect_ratio,
                     "preset": args.preset},
        "inputs": [{"path": rel(p), "sha256": sha256(p)} for p in input_files],
        "output": {"path": rel(out_file), "sha256": sha256(out_file),
                   "duration_s": duration, "size_bytes": out_file.stat().st_size},
        "environment": {"node": node_v or "unknown", "ffmpeg": ffmpeg_v,
                        "os": f"{platform.system()} {platform.release()} {platform.version()}"},
        "rendered_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "cloud_render": False,
        "notes": args.notes,
    }

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: e.json_path)
    if errors:
        print(f"REFUSED: manifest fails its schema ({len(errors)} error(s)):")
        for e in errors[:5]:
            print(f"  - {e.json_path}: {e.message}")
        return 2

    out_path = Path(args.manifest_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"OK: {manifest['manifest_id']} -> {rel(out_path)} (output {manifest['output']['sha256'][:12]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
