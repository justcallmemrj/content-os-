#!/usr/bin/env python3
"""Step-10 exit criterion (package §4 row 10): assembly-consistency validator
green on a fixture campaign — plus the three counterexample variants failing
for their named reasons, and the fixture campaign records schema-valid.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FX = ROOT / "evaluations/fixtures/campaign-assembly"
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

    for variant in ("good", "bad-claim", "bad-offer", "bad-disc"):
        code, log = run(ROOT / "scripts/schema_validate.py", FX / variant / "campaign.yaml")
        expect(f"{variant}: campaign record schema-valid", code == 0 and "OK" in log and "SKIP" not in log, log)

    code, log = run(ROOT / "validators/assembly_check.py", FX / "good/campaign.yaml")
    expect("GOOD fixture campaign GREEN (the exit criterion)", code == 0, log)
    expect("good checked 2 supported ad claims", "2 supported ad claims" in log, log)

    code, log = run(ROOT / "validators/assembly_check.py", FX / "bad-claim/campaign.yaml")
    expect("unsupported ad claim FAILS", code == 2 and "not supported by any landing child" in log, log)
    code, log = run(ROOT / "validators/assembly_check.py", FX / "bad-offer/campaign.yaml")
    expect("offer drift FAILS", code == 2 and "offer language drifted" in log, log)
    code, log = run(ROOT / "validators/assembly_check.py", FX / "bad-disc/campaign.yaml")
    expect("missing disclosure FAILS", code == 2 and "disclosure coverage incomplete" in log, log)

    print(f"{checks} checks, {len(failures)} failures")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
