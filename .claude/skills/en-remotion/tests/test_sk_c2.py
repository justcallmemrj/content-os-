#!/usr/bin/env python3
"""SK-C2 tests — mirrors SK-C1's suite so the engines stay comparable.

property        — SAME storyboard fixture as SK-C1 -> gen_props -> props
                  byte-match + tsx static checks green on the fixture comp
counterexample  — paraphrased props FAIL verbatim (escalation, exit 2)
counterexample  — literal JSX text FAILS static check (exit 2)
counterexample  — data-text-id outside SafeArea FAILS static check (exit 2)
pin             — workspace package.json pins exactly 4.0.487; SKILL.md
                  upstream_pin == DEC-BUILD-008 commit; manifest writer
                  REFUSES a floated version
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
SB = ROOT / ".claude/skills/en-hyperframes/tests/fixtures/storyboard-fixture.yaml"  # the SHARED fixture
CAPS = FX / "captions-fixture.yaml"
COMP = ROOT / "video/remotion/fixtures/drop-fixture"
PIN_COMMIT = "2e8037fec3cad711a8becf1252ed3af61f09a1fa"
PIN_VERSION = "4.0.487"
PY = sys.executable


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

    with tempfile.TemporaryDirectory() as td:
        props = Path(td) / "props.json"

        # property: shared fixture -> props -> verbatim + static green
        code, log = run("gen_props.py", SB, CAPS, props)
        expect("gen_props ok", code == 0, log)
        code, log = run("props_verbatim_check.py", SB, CAPS, props)
        expect("props verbatim pass", code == 0, log)
        expect("props verbatim 2/2", "2/2 text IDs byte-match" in log, log)
        code, log = run("tsx_static_check.py", COMP, "--ar", "9:16")
        expect("fixture comp static pass", code == 0, log)

        # counterexample: paraphrase in props
        doc = json.loads(props.read_text(encoding="utf-8"))
        doc["texts"][0]["text"] = doc["texts"][0]["text"].replace("arrives as a single check",
                                                                  "comes as one check")
        bad = Path(td) / "props-bad.json"
        bad.write_text(json.dumps(doc), encoding="utf-8")
        code, log = run("props_verbatim_check.py", SB, CAPS, bad)
        expect("paraphrased props FAIL (exit 2)", code == 2, log)
        expect("paraphrase names mismatch + escalation", "MISMATCH" in log and "ESCALATE to VDIR" in log, log)

        # counterexamples: static check
        code, log = run("tsx_static_check.py", FX / "comp-literal", "--ar", "9:16")
        expect("literal JSX text FAILS (exit 2)", code == 2 and "literal JSX text" in log, log)
        code, log = run("tsx_static_check.py", FX / "comp-unsafe", "--ar", "9:16")
        expect("outside-SafeArea FAILS (exit 2)", code == 2 and "outside <SafeArea>" in log, log)

        # pin tests
        pkg = json.loads((ROOT / "video/remotion/package.json").read_text(encoding="utf-8"))
        expect("remotion pinned exact", pkg["dependencies"].get("remotion") == PIN_VERSION,
               str(pkg["dependencies"]))
        expect("@remotion/cli pinned exact", pkg["dependencies"].get("@remotion/cli") == PIN_VERSION,
               str(pkg["dependencies"]))
        front = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        m = re.search(r"upstream_pin:\s*([a-f0-9]{40})", front)
        expect("SKILL.md pin == DEC-BUILD-008 commit", m and m.group(1) == PIN_COMMIT)
        out = Path(td) / "fake.mp4"
        out.write_bytes(b"\x00" * 1024)
        code, log = run("render_manifest.py", "--run", "x", "--storyboard", SB,
                        "--composition-dir", COMP, "--output", out, "--preset", "p",
                        "--resolution", "1080x1920", "--fps", "30", "--aspect-ratio", "9:16",
                        "--duration", "10.0", "--engine-version", "4.0.488",
                        "--manifest-out", Path(td) / "m.yaml")
        expect("floated engine version REFUSED", code == 2 and "ratified pin" in log, log)

    print(f"{checks} checks, {len(failures)} failures")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
