#!/usr/bin/env python3
"""HK3 — PreToolUse Bash: per-agent command policy (D-010, Phase 7 §5).

Global deny-patterns bind everyone in every mode. Agent scoping (Phase 2 §4.2):
REMO/HYPF jailed to their engine dir + command allowlist; ORCH/QA/ANLYT/MEMC
limited to scripts/ + validators/; all other agents have no Bash at all.
Main session: global deny-patterns only while build mode lasts (DEC-BUILD-005).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import allow, build_mode, deny, read_input

GLOBAL_DENY = [
    (re.compile(r"(?i)\brm\s+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r)\b"), "recursive force delete"),
    (re.compile(r"(?i)\b(rd|rmdir)\s+/s\b"), "recursive directory delete"),
    (re.compile(r"(?i)\bdel\s+.*/s\b"), "recursive delete"),
    (re.compile(r"(?i)\bformat\s+[a-z]:"), "disk format"),
    (re.compile(r"(?i)git\s+push\s+.*--force"), "force push (master prompt §2.6)"),
    (re.compile(r"(?i)git\s+.*--no-verify"), "hook bypass"),
    (re.compile(r"(?i)(cat|type|more|less|copy|cp|move|mv)\s+[^|;&]*\.env"), ".env access (D-069)"),
    (re.compile(r"(?i)\.env\s*(>|>>)"), ".env write"),
    (re.compile(r"(?i)\b(curl|wget|invoke-webrequest|iwr)\b.*\.env"), ".env exfiltration"),
]

SCRIPT_AGENTS = {"ORCH", "QA", "ANLYT", "MEMC"}
ENGINE = {
    "REMO": {"dir": "video/remotion", "cmds": ("npm", "npx", "node", "ffprobe")},
    "HYPF": {"dir": "video/hyperframes", "cmds": ("npx", "hyperframes", "ffprobe", "node", "npm")},
}


def main() -> None:
    data = read_input()
    cmd = (data.get("tool_input") or {}).get("command", "") or ""
    agent = (data.get("agent_id") or data.get("agent_type") or "").upper()

    for pat, why in GLOBAL_DENY:
        if pat.search(cmd):
            deny(f"HK3: denied for everyone — {why}")

    if not agent:
        if build_mode():
            allow("HK3: main session, build mode — global deny-patterns only (DEC-BUILD-005)")
        # Runtime: the main session is ORCH (Phase 7 §3.2) — script-scoped.
        agent = "ORCH"

    if agent in SCRIPT_AGENTS:
        first = cmd.strip().split()[0].lower() if cmd.strip() else ""
        if first in ("python", "python3", "py") and re.search(r"(scripts|validators)[/\\]", cmd):
            allow()
        deny(f"HK3: {agent} may only run python scripts/ or validators/ entries (Phase 2 §4.2)")

    if agent in ENGINE:
        spec = ENGINE[agent]
        first = cmd.strip().split()[0].lower() if cmd.strip() else ""
        if first not in spec["cmds"]:
            deny(f"HK3: {agent} command allowlist is {spec['cmds']} (Phase 7 §5)")
        forbidden_dirs = [v["dir"] for k, v in ENGINE.items() if k != agent]
        if any(d in cmd.replace("\\", "/") for d in forbidden_dirs):
            deny(f"HK3: {agent} is jailed to {spec['dir']} — cross-engine access denied")
        allow()

    deny(f"HK3: agent {agent} has no Bash tool at all (Phase 2 §4.2 — the absence is the control)")


if __name__ == "__main__":
    main()
