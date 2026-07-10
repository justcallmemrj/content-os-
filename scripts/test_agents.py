#!/usr/bin/env python3
"""Step-5 checks: 13 agent definitions well-formed with ratified model pins
(D-071), Tier-1 tool surfaces per Phase 2 §4.2, and adherence-fixture coverage
for every slice agent's reject lines (Phase 6 §7).

The fixtures' live-model exercise happens in the step-6 acceptance battery;
this suite verifies the definitions and the fixtures' deterministic shadows
exist and are themselves tested.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
AGENTS = ROOT / ".claude" / "agents"

EXPECTED = {
    # file: (model pin, forbidden-tool markers, required-tool markers)
    "orchestrator.md":        ("claude-opus-4-8",  ["WebFetch", "WebSearch"], ["Bash"]),
    "researcher.md":          ("claude-opus-4-8",  ["Bash"], ["WebSearch", "WebFetch"]),
    "fact-checker.md":        ("claude-sonnet-4-6", ["Bash", "WebSearch"], ["WebFetch"]),
    "compliance-reviewer.md": ("claude-sonnet-4-6", ["Bash", "WebFetch", "WebSearch"], []),
    "qa-evaluator.md":        ("claude-sonnet-4-6", ["WebFetch", "WebSearch"], ["Bash"]),
    "memory-curator.md":      ("claude-sonnet-4-6", ["WebFetch", "WebSearch"], ["Bash"]),
    "analyst.md":             ("claude-sonnet-4-6", ["WebFetch", "WebSearch"], ["Bash"]),
    "strategist.md":          ("claude-opus-4-8",  ["Bash", "WebFetch", "WebSearch"], []),
    "writer.md":              ("claude-sonnet-4-6", ["Bash", "WebFetch", "WebSearch"], []),
    "voice-editor.md":        ("claude-sonnet-4-6", ["Bash", "WebFetch", "WebSearch"], []),
    "video-director.md":      ("claude-sonnet-4-6", ["Bash", "WebFetch", "WebSearch"], []),
    "remotion-builder.md":    ("claude-sonnet-4-6", ["WebSearch"], ["Bash", "WebFetch"]),
    "hyperframes-builder.md": ("claude-sonnet-4-6", ["WebSearch"], ["Bash", "WebFetch"]),
}
SLICE_AGENTS = ["ORCH", "RSRCH", "FACT", "COMPL", "QA", "MEMC", "WRITE", "VOICE"]
failures = []


def check(label, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + label + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(f"{label}: {detail}")


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    end = text.find("\n---", 3)
    return yaml.safe_load(text[3:end])


# ---- definitions ----
files = sorted(p.name for p in AGENTS.glob("*.md"))
check("13 agent definition files present", len(files) == 13, f"found {len(files)}: {files}")

for fname, (model, forbidden, required) in EXPECTED.items():
    p = AGENTS / fname
    if not p.exists():
        check(f"{fname} exists", False)
        continue
    fm = frontmatter(p)
    check(f"{fname}: frontmatter has name+description",
          bool(fm.get("name")) and bool(fm.get("description")))
    check(f"{fname}: model pin {model} (D-071)", fm.get("model") == model,
          f"got {fm.get('model')}")
    tools = str(fm.get("tools", ""))
    for t in forbidden:
        check(f"{fname}: tool surface excludes {t}", t not in tools, tools)
    for t in required:
        check(f"{fname}: tool surface includes {t}", t in tools, tools)

# ---- adherence fixtures ----
fixtures = yaml.safe_load(
    (ROOT / "evaluations" / "fixtures" / "adherence" / "slice-agents.yaml")
    .read_text(encoding="utf-8"))
for agent in SLICE_AGENTS:
    entries = fixtures.get(agent, [])
    check(f"adherence fixtures exist for {agent} (>=4 reject lines covered)",
          len(entries) >= 4, f"{len(entries)}")
    for e in entries:
        ok = all(k in e for k in ("reject", "invitation", "required", "shadow"))
        if not ok:
            check(f"{agent} fixture complete: {e.get('reject', '?')[:40]}", False, str(e))
    # every fixture names a shadow; shadows referencing scripts must exist
    for e in entries:
        for hint, path in [("ledger_validate", ".claude/skills/ev-claim-ledger/scripts/ledger_validate.py"),
                           ("lexicon_scan", "validators/lexicon_scan.py"),
                           ("compliance_lint", "validators/compliance_lint.py"),
                           ("claim_diff", ".claude/skills/ev-claim-ledger/scripts/claim_diff.py"),
                           ("disclosure_check", ".claude/skills/co-disclosure-management/scripts/disclosure_check.py"),
                           ("transition", "scripts/transition.py"),
                           ("HK1", ".claude/hooks/protect_paths.py"),
                           ("HK4", ".claude/hooks/web_policy.py"),
                           ("HK6", ".claude/hooks/schema_gate.py")]:
            if hint in e["shadow"]:
                check(f"{agent} shadow artifact exists: {hint}", (ROOT / path).exists())
                break

print(f"\nAGENTS: {'ALL GREEN' if not failures else 'FAILURES'} ({len(failures)})")
for f in failures:
    print(f"  - {f}")
sys.exit(1 if failures else 0)
