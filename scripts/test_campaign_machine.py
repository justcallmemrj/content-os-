#!/usr/bin/env python3
"""Campaign-machine transition tests (build step 10; Phase 5 §4)."""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import transition


def call(*argv):
    class _Buf(io.StringIO):
        def reconfigure(self, **kwargs):
            pass
    out, err = _Buf(), _Buf()
    old = sys.argv
    sys.argv = ["transition.py", *argv]
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = transition.main()
    finally:
        sys.argv = old
    return code, out.getvalue() + err.getvalue()


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    tmp = Path(tempfile.mkdtemp())
    transition.DB = tmp / "workflow.sqlite"

    checks, failures = [], []

    def expect(name, want_code, code, log, needle=None):
        ok = code == want_code and (needle is None or needle in log)
        checks.append(name)
        if not ok:
            failures.append(f"{name}: exit={code} (want {want_code}); log: {log.strip()[:200]}")

    C = "test-cmp-001"
    orch = ["--run", C, "--initiator", "ORCH"]

    code, log = call("--run", C, "--to", "campaign_requested", "--initiator", "ORCH",
                     "--task-id", "T-1", "--project", "benowitz-wealth", "--profile", "campaign")
    expect("entry at campaign_requested", 0, code, log, "-> campaign_requested")
    code, log = call(*orch, "--to", "strategy_brief")
    expect("C1", 0, code, log, "C1")
    code, log = call(*orch, "--to", "strategy_review")
    expect("C2", 0, code, log, "C2")

    # H1 is Wes's alone; nothing spawns before it
    code, log = call(*orch, "--to", "deliverable_planning")
    expect("C3 by ORCH denied (H1 is Wes's)", 1, code, log, "may only be initiated by")
    code, log = call("--run", C, "--to", "strategy_brief", "--initiator", "wes")
    expect("C3 revise route (wes)", 0, code, log, "C3")
    code, log = call(*orch, "--to", "strategy_review")
    expect("C2 again", 0, code, log, "C2")
    code, log = call("--run", C, "--to", "deliverable_planning", "--initiator", "wes")
    expect("C3 approve (wes)", 0, code, log, "C3")

    # cannot skip planning straight to assembly
    code, log = call(*orch, "--to", "assembly_review")
    expect("skip to assembly denied", 1, code, log, "no transition")

    code, log = call(*orch, "--to", "children_active")
    expect("C4", 0, code, log, "C4")
    code, log = call(*orch, "--to", "assembly_review")
    expect("C5", 0, code, log, "C5")
    code, log = call(*orch, "--to", "children_active")
    expect("C5f assembly failure route", 0, code, log, "C5f")
    code, log = call(*orch, "--to", "assembly_review")
    expect("C5 again", 0, code, log, "C5")
    code, log = call(*orch, "--to", "launch_ready")
    expect("C6", 0, code, log, "C6")

    # H4 is Wes's alone
    code, log = call(*orch, "--to", "live")
    expect("C7 by ORCH denied (H4 is Wes's)", 1, code, log, "may only be initiated by")
    code, log = call("--run", C, "--to", "live", "--initiator", "wes")
    expect("C7 (wes)", 0, code, log, "C7")

    code, log = call("--run", C, "--to", "performance_review", "--initiator", "ANLYT")
    expect("C8 (ANLYT)", 0, code, log, "C8")
    code, log = call("--run", C, "--to", "closed", "--initiator", "ANLYT")
    expect("C9 by ANLYT (pipe alt)", 0, code, log, "C9")
    code, log = call(*orch, "--to", "archived")
    expect("C10", 0, code, log, "C10")

    print(f"{len(checks)} checks, {len(failures)} failures")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
