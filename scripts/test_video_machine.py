#!/usr/bin/env python3
"""Video-machine transition tests (build step 8; Phase 5 §5).

Exercises transition.py against video-machine.yaml in-process with a temp DB:
happy path V1->V9, denial cases (missing parent, wrong initiator, illegal skip,
wes-only V10), pipe-alternative initiators, escalated substate, and a trunk
regression (default machine still enters at `requested`).
"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import transition


def call(*argv):
    """Run transition.main() with argv; returns (exit_code, stdout+stderr)."""
    class _Buf(io.StringIO):
        def reconfigure(self, **kwargs):   # transition.main() reconfigures stdout
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
    transition.DB = tmp / "workflow.sqlite"   # isolate: never touch the real state DB

    checks, failures = [], []

    def expect(name, want_code, code, log, needle=None):
        ok = code == want_code and (needle is None or needle in log)
        checks.append(name)
        if not ok:
            failures.append(f"{name}: exit={code} (want {want_code}); log: {log.strip()[:200]}")

    VID = "test-vid-001"
    common = ["--run", VID, "--initiator", "ORCH"]

    # 1. video run without parent is denied
    code, log = call("--run", VID, "--to", "storyboard", "--initiator", "ORCH",
                     "--task-id", "T-1", "--project", "benowitz-wealth", "--profile", "video")
    expect("V1 without --parent-run denied", 1, code, log, "--parent-run required")

    # 2. video run must enter at storyboard
    code, log = call("--run", VID, "--to", "requested", "--initiator", "ORCH",
                     "--task-id", "T-1", "--project", "benowitz-wealth", "--profile", "video",
                     "--parent-run", "parent-1")
    expect("video entry must be storyboard", 1, code, log, "must be to 'storyboard'")

    # 3. happy path V1..V9
    code, log = call("--run", VID, "--to", "storyboard", "--initiator", "ORCH",
                     "--task-id", "T-1", "--project", "benowitz-wealth", "--profile", "video",
                     "--parent-run", "parent-1")
    expect("V1 approved->storyboard", 0, code, log, "-> storyboard")
    code, log = call(*common, "--to", "engine_routing")
    expect("V2 storyboard->engine_routing", 0, code, log, "V2")

    # 4. illegal skip engine_routing->render denied
    code, log = call(*common, "--to", "render")
    expect("illegal skip denied", 1, code, log, "no transition")

    code, log = call(*common, "--to", "build")
    expect("V3 engine_routing->build", 0, code, log, "V3")

    # 5. wrong initiator: ORCH may not initiate V4 (HYPF|REMO)
    code, log = call(*common, "--to", "preview_review")
    expect("V4 by ORCH denied", 1, code, log, "may only be initiated by")
    code, log = call("--run", VID, "--to", "preview_review", "--initiator", "HYPF")
    expect("V4 by HYPF (pipe alternative)", 0, code, log, "V4")

    # 6. V5 is VDIR's reviewer verdict, not ORCH's
    code, log = call(*common, "--to", "render")
    expect("V5 by ORCH denied", 1, code, log, "may only be initiated by")
    code, log = call("--run", VID, "--to", "render", "--initiator", "VDIR")
    expect("V5 preview_review->render (VDIR)", 0, code, log, "V5")

    code, log = call("--run", VID, "--to", "technical_qc", "--initiator", "REMO")
    expect("V6 by REMO (pipe alternative)", 0, code, log, "V6")
    code, log = call(*common, "--to", "judgment_qc")
    expect("V7 technical_qc->judgment_qc", 0, code, log, "V7")

    # 7. V8 failure route: QA may send judgment_qc back to build
    code, log = call("--run", VID, "--to", "build", "--initiator", "QA")
    expect("V8f judgment_qc->build (QA)", 0, code, log, "V8f")
    code, log = call("--run", VID, "--to", "preview_review", "--initiator", "HYPF")
    expect("V4 again after V8f", 0, code, log, "V4")
    code, log = call("--run", VID, "--to", "render", "--initiator", "VDIR")
    expect("V5 again", 0, code, log, "V5")
    code, log = call("--run", VID, "--to", "technical_qc", "--initiator", "HYPF")
    expect("V6 again", 0, code, log, "V6")
    code, log = call(*common, "--to", "judgment_qc")
    expect("V7 again", 0, code, log, "V7")
    code, log = call("--run", VID, "--to", "delivery_ready", "--initiator", "QA")
    expect("V8 judgment_qc->delivery_ready (QA)", 0, code, log, "V8")
    code, log = call(*common, "--to", "human_signoff")
    expect("V9 delivery_ready->human_signoff", 0, code, log, "V9")

    # 8. V10 is Wes's alone (H5)
    code, log = call(*common, "--to", "published")
    expect("V10 by ORCH denied (H5 is Wes's)", 1, code, log, "may only be initiated by")

    # 9. escalated substate enterable from a video state
    code, log = call(*common, "--to", "escalated")
    expect("escalated from human_signoff", 0, code, log, "escalated")

    # 10. trunk regression: default machine still enters at requested
    code, log = call("--run", "test-trunk-001", "--to", "requested", "--initiator", "ORCH",
                     "--task-id", "T-2", "--project", "benowitz-wealth", "--profile", "script")
    expect("trunk entry unchanged", 0, code, log, "-> requested")
    code, log = call("--run", "test-trunk-001", "--to", "storyboard", "--initiator", "ORCH")
    expect("trunk cannot enter video states", 1, code, log, "no transition")

    print(f"{len(checks)} checks, {len(failures)} failures")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
