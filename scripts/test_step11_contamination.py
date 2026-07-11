#!/usr/bin/env python3
"""Step-11 exit criterion (package §4 row 11): contamination suite green across
BOTH live brands, TRD/FDR scaffolds confirmed.

Four layers:
  1. Synthetic cross-brand fixtures: a DUC-context text carrying BEN vocabulary
     (and vice versa) is CAUGHT by lexicon_scan; clean texts pass.
  2. REAL-CORPUS sweep: every vendored DUC caption scanned with DUC's
     foreign_terms; the locked BEN reel + BEN exemplars scanned with BEN's —
     all clean (the both-live-brands proof).
  3. Loader isolation: a DUC packet contains zero benowitz-wealth records and
     vice versa (namespace assertions + manifest path check), via --dry-run
     fixture runs cleaned up afterward.
  4. TRD/FDR scaffolds: profiles parse with foreign_terms; required subdirs
     exist (FDR has no compliance.md BY DESIGN — scaffold only; TRD's exists).
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
SCAN = ROOT / "validators/lexicon_scan.py"


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

    with tempfile.TemporaryDirectory() as td:
        # 1. synthetic cross-brand fixtures
        dirty_duc = Path(td) / "dirty-duc.md"
        dirty_duc.write_text("Your NIL deal is one thing, but your DROP payout from FRS is another.",
                             encoding="utf-8")
        code, log = run(SCAN, dirty_duc, "--project", "ducat-private-wealth")
        expect("BEN vocab in DUC context CAUGHT", code == 1 and "DROP" in log, log)

        dirty_ben = Path(td) / "dirty-ben.md"
        dirty_ben.write_text("Before your DROP window closes, think about your NIL income and contract year.",
                             encoding="utf-8")
        code, log = run(SCAN, dirty_ben, "--project", "benowitz-wealth")
        expect("DUC vocab in BEN context CAUGHT", code == 1 and "NIL" in log, log)

        clean_duc = Path(td) / "clean-duc.md"
        clean_duc.write_text("Quarterly estimated taxes are how self-employment income stays paid up.",
                             encoding="utf-8")
        code, log = run(SCAN, clean_duc, "--project", "ducat-private-wealth")
        expect("clean DUC text passes", code == 0, log)

    # 2. real-corpus sweep — both live brands
    duc_captions = sorted((ROOT / "projects/ducat-private-wealth/assets/social-captions").glob("*.txt"))
    expect("DUC corpus present (36 captions)", len(duc_captions) == 36, f"found {len(duc_captions)}")
    dirty = []
    for cap in duc_captions:
        code, log = run(SCAN, cap, "--project", "ducat-private-wealth")
        if code != 0:
            dirty.append(f"{cap.name}: {log.strip()[:80]}")
    expect("all 36 DUC captions clean of BEN/TRD vocabulary", not dirty, "; ".join(dirty))

    ben_corpus = [ROOT / "runs/2026-07-10-ben-drop-001/voice/drop-reel-v3.md"]
    ben_corpus += sorted((ROOT / "projects/benowitz-wealth/voice/exemplars").glob("VX-*.md"))
    ben_corpus += sorted((ROOT / "projects/benowitz-wealth/approved-facts").glob("F-*.md"))
    dirty = []
    for piece in ben_corpus:
        code, log = run(SCAN, piece, "--project", "benowitz-wealth")
        if code != 0:
            dirty.append(f"{piece.name}: {log.strip()[:80]}")
    expect(f"BEN corpus clean of DUC/TRD vocabulary ({len(ben_corpus)} pieces)", not dirty, "; ".join(dirty))

    # 3. loader isolation, both directions
    for proj, other in [("ducat-private-wealth", "benowitz-wealth"),
                        ("benowitz-wealth", "ducat-private-wealth")]:
        run_id = f"contam-check-{proj[:3]}"
        run_dir = ROOT / "runs" / run_id
        try:
            run_dir.mkdir(parents=True, exist_ok=True)
            wo = {"task_id": "T-2026-0711-098", "run_id": run_id, "parent_run": None,
                  "project_id": proj, "cross_project": None,
                  "deliverable": {"type": "script", "format": "f", "platform": "p", "spec": "contamination fixture"},
                  "objective": "o", "audience_ref": "a", "funnel_stage": "awareness",
                  "voice_profile_version": "brand-voice.md@1.0.0", "required_fact_ids": [],
                  "disclosure_ids": [], "prohibited_notes": [],
                  "asset_manifest_ref": "none", "constraints": {}, "model_tier_escalation": "none",
                  "state": "requested"}
            (run_dir / "workorder.yaml").write_text(yaml.safe_dump(wo, sort_keys=False), encoding="utf-8")
            code, log = run(ROOT / "scripts/load_context.py", "--run", run_id)
            expect(f"loader assembles {proj}", code == 0, log)
            manifest = yaml.safe_load((run_dir / "packet-manifest.yaml").read_text(encoding="utf-8"))
            paths = json.dumps(manifest)
            expect(f"{proj} packet has ZERO {other} records", f"projects/{other}/" not in paths,
                   f"{other} paths leaked into the packet")
        finally:
            shutil.rmtree(run_dir, ignore_errors=True)

    # 4. TRD/FDR scaffolds confirmed
    for proj in ("trading-research", "founder-brand"):
        profile = ROOT / "projects" / proj / "project-profile.md"
        text = profile.read_text(encoding="utf-8")
        fm = yaml.safe_load(text[3:text.find("\n---", 3)])
        expect(f"{proj} profile parses with foreign_terms", bool(fm.get("foreign_terms")), str(fm)[:100])
        for sub in ("approved-facts", "sources", "voice", "examples", "decisions", "lessons"):
            expect(f"{proj}/{sub} exists", (ROOT / "projects" / proj / sub).is_dir())
    expect("TRD compliance.md exists (guardrail profile)",
           (ROOT / "projects/trading-research/compliance.md").exists())

    print(f"{checks} checks, {len(failures)} failures — "
          f"{'CONTAMINATION SUITE GREEN across both live brands' if not failures else 'CONTAMINATION FOUND'}")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
