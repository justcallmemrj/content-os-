#!/usr/bin/env python3
"""Step-9 exit criterion (package §4 row 9): SAME fixtures green on BOTH engines.

Runs the shared storyboard fixture through each engine's full deterministic
lane and asserts both come back green, plus both engines' paraphrase
counterexamples both FAIL (the gates are equally strict):

  HyperFrames (SK-C1): text_verbatim_check + safe_area_check on the HTML fixture
  Remotion    (SK-C2): gen_props -> props_verbatim_check + tsx_static_check
                       on the JSX fixture twin

Both rubric-gated identically by RUB-VIDEO-BUILD-1 (Phase 5 §5: "nothing else
differs").
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
C1 = ROOT / ".claude/skills/en-hyperframes"
C2 = ROOT / ".claude/skills/en-remotion"
SB = C1 / "tests/fixtures/storyboard-fixture.yaml"          # THE shared fixture
CAPS = C2 / "tests/fixtures/captions-fixture.yaml"
PY = sys.executable


def run(*cmd):
    r = subprocess.run([PY, *map(str, cmd)], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    checks, failures = 0, []

    def expect(name, cond, detail=""):
        nonlocal checks
        checks += 1
        if not cond:
            failures.append(f"{name}: {detail[:200]}")

    # Lane 1 — HyperFrames
    code, log = run(C1 / "scripts/text_verbatim_check.py", SB, C1 / "tests/fixtures/composition-good")
    expect("HF: verbatim green on shared fixture", code == 0, log)
    code, log = run(C1 / "scripts/safe_area_check.py", C1 / "tests/fixtures/composition-good", "--ar", "9:16")
    expect("HF: safe-area green", code == 0, log)
    code, log = run(C1 / "scripts/text_verbatim_check.py", SB, C1 / "tests/fixtures/composition-paraphrase")
    expect("HF: paraphrase counterexample fails", code == 2, log)

    # Lane 2 — Remotion
    with tempfile.TemporaryDirectory() as td:
        props = Path(td) / "props.json"
        code, log = run(C2 / "scripts/gen_props.py", SB, CAPS, props)
        expect("RM: gen_props green", code == 0, log)
        code, log = run(C2 / "scripts/props_verbatim_check.py", SB, CAPS, props)
        expect("RM: verbatim green on shared fixture", code == 0, log)
    code, log = run(C2 / "scripts/tsx_static_check.py", ROOT / "video/remotion/fixtures/drop-fixture", "--ar", "9:16")
    expect("RM: static checks green", code == 0, log)
    code, log = run(C2 / "scripts/tsx_static_check.py", C2 / "tests/fixtures/comp-literal", "--ar", "9:16")
    expect("RM: paraphrase/literal counterexample fails", code == 2, log)

    print(f"{checks} checks, {len(failures)} failures — "
          f"{'BOTH ENGINES GREEN on the shared fixture' if not failures else 'ENGINES DIVERGE'}")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
