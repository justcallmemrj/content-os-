#!/usr/bin/env python3
"""Step-8 skill validator tests: SK-B16 storyboard_check + SK-C3 caption_check.

(SK-C1's own suite lives in .claude/skills/en-hyperframes/tests/test_sk_c1.py.)
"""
import copy
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SB_CHECK = ROOT / ".claude/skills/vd-storyboarding/scripts/storyboard_check.py"
CAP_CHECK = ROOT / ".claude/skills/vd-captions-access/scripts/caption_check.py"
FIXTURE = ROOT / ".claude/skills/en-hyperframes/tests/fixtures/storyboard-fixture.yaml"
PY = sys.executable


def run(script, *args):
    r = subprocess.run([PY, str(script), *map(str, args)], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def with_patch(base, patch_fn):
    doc = copy.deepcopy(base)
    patch_fn(doc)
    f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
    yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True)
    f.close()
    return f.name


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    checks, failures = 0, []

    def expect(name, cond, detail=""):
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(f"{name}: {detail[:200]}")

    base = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))

    # SK-B16 storyboard_check
    code, log = run(SB_CHECK, FIXTURE)
    expect("fixture storyboard passes", code == 0, log)
    code, log = run(SB_CHECK, FIXTURE, "--locked-hash", base["script_ref"]["sha256"])
    expect("locked-hash match passes", code == 0, log)
    code, log = run(SB_CHECK, FIXTURE, "--locked-hash", "b" * 64)
    expect("locked-hash mismatch HALTS (D5)", code == 2 and "D5 HALT" in log, log)

    p = with_patch(base, lambda d: d["scenes"][0].update(duration_s=20))
    code, log = run(SB_CHECK, p)
    expect("duration overrun fails", code == 2 and "durations sum" in log, log)

    def add_gap(d):
        d["scenes"][0]["assets"].append({"ref": "GAP", "rights": "none-recorded"})
    p = with_patch(base, add_gap)
    code, log = run(SB_CHECK, p)
    expect("unmirrored GAP fails", code == 2 and "not mirrored" in log, log)

    def dup_id(d):
        d["scenes"][0]["on_screen_text"].append({"text_id": "CAP-01", "text": "different words"})
    p = with_patch(base, dup_id)
    code, log = run(SB_CHECK, p)
    expect("one ID two strings fails", code == 2 and "two different strings" in log, log)

    # SK-C3 caption_check
    good = {"segments": [
        {"id": "CAP-01", "start_s": 0.0, "end_s": 3.0, "text": "Your DROP payout arrives\nas a single check."},
        {"id": "CAP-02", "start_s": 3.0, "end_s": 6.0, "text": "It comes with a decision attached."},
    ]}
    f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
    yaml.safe_dump(good, f); f.close()
    code, log = run(CAP_CHECK, f.name, "--video-duration", "10")
    expect("good captions pass", code == 0, log)

    bad = {"segments": [
        {"id": "CAP-01", "start_s": 0.0, "end_s": 1.0,
         "text": "This sentence is far too long to read in one second flat."},
        {"id": "CAP-02", "start_s": 0.5, "end_s": 9.0, "text": "overlapping and overlong segment"},
        {"id": "CAP-02", "start_s": 9.0, "end_s": 9.3, "text": "dup id, too brief"},
    ]}
    f = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")
    yaml.safe_dump(bad, f); f.close()
    code, log = run(CAP_CHECK, f.name, "--video-duration", "8")
    expect("bad captions fail", code == 2, log)
    for needle in ["CPS", "overlaps", "duplicate id", "outside video bounds", "on-screen"]:
        expect(f"bad captions name: {needle}", needle in log, log)

    print(f"{checks} checks, {len(failures)} failures")
    for x in failures:
        print(f"  - {x}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
