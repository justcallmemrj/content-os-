#!/usr/bin/env python3
"""load_context.py — deterministic context loader (Phase 3 §3, Phase 7 §3.2).

Reads runs/<run-id>/workorder.yaml, loads L0 (global/) + EXACTLY ONE project's
records via generated indexes, asserts namespaces, and emits the packet
manifest the run cites. Refuses to run on a missing, unknown, or ambiguous
project_id — ambiguity escalates to the human; there is no guess mode.

Usage: python scripts/load_context.py --run <run-id> [--dry-run]
Exit codes: 0 assembled · 1 refused (reason on stderr)
"""
import argparse
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = {"benowitz-wealth": "BEN", "ducat-private-wealth": "DUC",
            "trading-research": "TRD", "founder-brand": "FDR"}
L0_FILES = ["owner-profile.md", "general-voice.md", "workflow-preferences.md", "approval-rules.md"]
PROFILE_FILES = ["project-profile.md", "audience.md", "brand-voice.md", "compliance.md", "disclosures.md"]
ID_RE = re.compile(r"^\s*id:\s*([A-Z]+-)([A-Z]{3})-", re.M)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def refuse(msg: str) -> int:
    print(f"REFUSED: {msg}", file=sys.stderr)
    return 1


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    wo_path = ROOT / "runs" / args.run / "workorder.yaml"
    if not wo_path.exists():
        return refuse(f"no work order at {wo_path} — the loader does not run on a missing work order")
    wo = yaml.safe_load(wo_path.read_text(encoding="utf-8"))

    project = wo.get("project_id")
    if project is None or project == "":
        return refuse("work order has no project_id — escalate to human (no guess mode)")
    if isinstance(project, list) or (isinstance(project, str) and "," in project):
        return refuse(f"ambiguous project_id {project!r} — exactly one project loads per run; escalate to human")
    if project not in PROJECTS:
        return refuse(f"unknown project_id {project!r} — not in the ID registry (Phase 3 §4.1)")
    code = PROJECTS[project]

    manifest = {
        "run": args.run,
        "assembled_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "project": project,
        "project_code": code,
        "work_order_sha256": sha256(wo_path),
        "l0": [],
        "project_records": [],
        "indexes": [],
        "cross_project": [],
        "namespace_assertions": {"checked": 0, "violations": []},
    }

    for name in L0_FILES:
        p = ROOT / "global" / name
        if p.exists():
            manifest["l0"].append({"path": f"global/{name}", "sha256": sha256(p)})

    proj_dir = ROOT / "projects" / project
    if not proj_dir.exists():
        return refuse(f"project directory missing: {proj_dir}")

    for name in PROFILE_FILES:
        p = proj_dir / name
        if p.exists():
            manifest["project_records"].append({"path": f"projects/{project}/{name}", "sha256": sha256(p)})

    # Records load via generated indexes, not corpora (D-066). Index absence is
    # legal pre-seeding; each present index is pinned by hash.
    for idx in ["approved-facts/_index.yaml", "approved-facts/_claim-keys.yaml", "sources/_index.yaml"]:
        p = proj_dir / idx
        if p.exists():
            manifest["indexes"].append({"path": f"projects/{project}/{idx}", "sha256": sha256(p)})

    # Namespace assertion (Phase 3 §3.2): every record ID in the loaded project
    # must embed this project's code. A stray ID is a hard failure, not a warning.
    for sub in ["approved-facts", "sources", "decisions", "lessons"]:
        for rec in sorted((proj_dir / sub).glob("*.md")):
            for m in ID_RE.finditer(rec.read_text(encoding="utf-8")):
                manifest["namespace_assertions"]["checked"] += 1
                if m.group(2) != code:
                    manifest["namespace_assertions"]["violations"].append(
                        {"file": f"projects/{project}/{sub}/{rec.name}", "found": m.group(2), "expected": code})
    if manifest["namespace_assertions"]["violations"]:
        print(yaml.safe_dump(manifest["namespace_assertions"]["violations"]), file=sys.stderr)
        return refuse("namespace assertion failed — record(s) from another project inside the loaded project")

    # Cross-project material only via the explicit work-order block (Phase 3 §3.4),
    # and only the NAMED records — never a blanket second-project load.
    xp = wo.get("cross_project")
    if xp:
        for rec_id in xp.get("records_permitted", []):
            manifest["cross_project"].append({"record": rec_id, "second_project": xp.get("second_project"),
                                              "authorized_by": xp.get("authorized_by")})

    # The shared compliance envelope arrives only by explicit include (§3.5);
    # the loader pins it when the project's compliance.md exists to include it.
    shared = ROOT / "projects" / "_shared" / "ria-compliance-envelope.md"
    if shared.exists() and (proj_dir / "compliance.md").exists():
        manifest["project_records"].append(
            {"path": "projects/_shared/ria-compliance-envelope.md", "sha256": sha256(shared),
             "via": "explicit include from compliance.md"})

    out = ROOT / "runs" / args.run / "packet-manifest.yaml"
    if not args.dry_run:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    print(f"OK: packet assembled for {project} ({code}); "
          f"{len(manifest['l0'])} L0 + {len(manifest['project_records'])} project records, "
          f"{manifest['namespace_assertions']['checked']} namespace checks clean"
          + ("" if args.dry_run else f"; manifest at {out.relative_to(ROOT)}"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
