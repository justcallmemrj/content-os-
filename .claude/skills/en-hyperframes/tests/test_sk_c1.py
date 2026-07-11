#!/usr/bin/env python3
"""SK-C1 tests (Phase 4 §7.3): property, counterexample, upstream-pin, manifest.

property        — fixture storyboard renders to spec: byte-match 100% + safe-area pass
counterexample  — paraphrase temptation FAILS verbatim check (escalation path, exit 2)
counterexample  — text outside hf-safe FAILS safe-area check (exit 2)
upstream-pin    — frontmatter pin == VENDOR.md pin; all 8 vendored sets present
                  with the file counts upstream's own manifest records
manifest        — render_manifest.py writes a schema-valid manifest; refuses
                  a non-pinned engine version
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = SKILL.parents[2]
FX = HERE / "fixtures"
PY = sys.executable

VENDORED = ["hyperframes", "hyperframes-core", "hyperframes-animation",
            "hyperframes-cli", "hyperframes-creative", "hyperframes-keyframes",
            "hyperframes-registry", "media-use"]


def run(script, *args):
    r = subprocess.run([PY, str(SKILL / "scripts" / script), *map(str, args)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    checks, failures = 0, []

    def expect(name, cond, detail=""):
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(f"{name}: {detail[:200]}")

    sb = FX / "storyboard-fixture.yaml"

    # property: good composition passes both deterministic checks
    code, log = run("text_verbatim_check.py", sb, FX / "composition-good")
    expect("verbatim pass on good composition", code == 0, log)
    expect("verbatim reports 2/2", "2/2 IDs byte-match" in log, log)
    code, log = run("safe_area_check.py", FX / "composition-good", "--ar", "9:16")
    expect("safe-area pass on good composition", code == 0, log)

    # counterexample: paraphrase temptation must FAIL with the escalation line
    code, log = run("text_verbatim_check.py", sb, FX / "composition-paraphrase")
    expect("paraphrase FAILS verbatim (exit 2)", code == 2, log)
    expect("paraphrase names the mismatch", "MISMATCH CAP-01" in log, log)
    expect("escalation path stated", "ESCALATE to VDIR" in log, log)

    # counterexample: unsafe placement must FAIL
    code, log = run("safe_area_check.py", FX / "composition-unsafe", "--ar", "9:16")
    expect("unsafe placement FAILS (exit 2)", code == 2, log)
    expect("names the offender", "DISC-BEN-FRS-01" in log, log)
    code, log = run("text_verbatim_check.py", sb, FX / "composition-unsafe")
    expect("unsafe fixture still text-verbatim (isolates the safe-area failure)", code == 0, log)

    # upstream-pin: frontmatter == VENDOR.md; vendored sets complete per upstream manifest
    front = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    pin = re.search(r"upstream_pin:\s*([a-f0-9]{40})", front)
    vendor_doc = (SKILL / "vendor" / "VENDOR.md").read_text(encoding="utf-8")
    expect("pin recorded in frontmatter", pin is not None)
    expect("VENDOR.md records the same pin", pin and pin.group(1) in vendor_doc)
    manifest = json.loads((SKILL / "vendor" / "skills-manifest.json").read_text(encoding="utf-8"))
    for s in VENDORED:
        d = SKILL / "vendor" / s
        expect(f"vendored {s} exists", (d / "SKILL.md").exists())
        want = manifest["skills"].get(s, {}).get("files")
        got = sum(1 for p in d.rglob("*") if p.is_file())
        expect(f"vendored {s} file count matches upstream manifest",
               want == got, f"manifest says {want}, found {got}")

    # manifest: schema-valid write; pin refusal
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "fake.mp4"
        out.write_bytes(b"\x00" * 1024)
        mpath = Path(td) / "manifest.yaml"
        code, log = run("render_manifest.py", "--run", "test-vid-fixture",
                        "--storyboard", sb, "--composition-dir", FX / "composition-good",
                        "--output", out, "--preset", "reels-local-v1",
                        "--resolution", "1080x1920", "--fps", "30",
                        "--aspect-ratio", "9:16", "--duration", "10.0",
                        "--manifest-out", mpath)
        expect("manifest written schema-valid", code == 0 and mpath.exists(), log)
        code, log = run("render_manifest.py", "--run", "x",
                        "--storyboard", sb, "--composition-dir", FX / "composition-good",
                        "--output", out, "--preset", "p", "--resolution", "1080x1920",
                        "--fps", "30", "--aspect-ratio", "9:16", "--duration", "10.0",
                        "--engine-version", "0.7.51", "--manifest-out", Path(td) / "m2.yaml")
        expect("non-pin engine version REFUSED (D-036)", code == 2 and "ratified pin" in log, log)

    print(f"{checks} checks, {len(failures)} failures")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
