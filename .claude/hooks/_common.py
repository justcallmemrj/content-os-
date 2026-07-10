"""Shared plumbing for HK1–HK9 (Phase 7 §5). Hook scripts are protected paths.

Contract (re-verified 2026-07-10, code.claude.com/docs/en/hooks):
  stdin: JSON with hook_event_name, tool_name, tool_input, cwd, and agent_id/
         agent_type when running inside a subagent.
  stdout JSON for PreToolUse: hookSpecificOutput.permissionDecision allow|deny|ask.
  PostToolUse feedback: {"decision": "block", "reason": ...}.
  Exit 0 = decision in JSON; exit 2 = hard block with stderr fed to Claude.

Build-mode phasing (DEC-BUILD-005): main-session (no agent_id) writes to most
protected paths are permitted while state/BUILD-MODE exists — the build must
author agents/skills/schemas. docs/architecture/** and secrets are denied in
every mode for everyone. Subagents are always fully enforced.
"""
import fnmatch
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
BUILD_MODE_MARKER = ROOT / "state" / "BUILD-MODE"

# Phase 2 §4.4 protected paths (repo-relative, forward slashes)
PROTECTED_GLOBS = [
    "docs/decisions/*",
    "schemas/*", "schemas/**/*",
    ".claude/agents/*", ".claude/agents/**/*",
    ".claude/skills/*", ".claude/skills/**/*",
    ".claude/hooks/*",
    ".claude/settings.json",
    "workflows/*", "workflows/**/*",
    "evaluations/rubrics/*",
    "global/approval-rules.md",
    "projects/_shared/*",
    "projects/*/project-profile.md",
    "projects/*/brand-voice.md",
    "projects/*/compliance.md",
    "projects/*/disclosures.md",
    "projects/*/approved-facts/*",
    "projects/*/sources/*", "projects/*/sources/**/*",
    "projects/*/decisions/*",
    "projects/*/lessons/*",
]
# Denied in EVERY mode, for everyone (D-078; the build may not edit its requirements)
ALWAYS_DENIED_GLOBS = ["docs/architecture/*", "docs/architecture/**/*"]


def read_input() -> dict:
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def rel_path(data: dict, raw: str) -> str:
    """Normalize a tool path to repo-relative forward slashes."""
    p = Path(raw)
    if not p.is_absolute():
        base = Path(data.get("cwd") or ROOT)
        p = base / p
    try:
        return p.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return p.resolve().as_posix()


def matches(rel: str, globs) -> bool:
    return any(fnmatch.fnmatch(rel, g) for g in globs)


def build_mode() -> bool:
    return BUILD_MODE_MARKER.exists()


def deny(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason}}))
    sys.exit(0)


def allow(reason: str = "") -> None:
    out = {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}
    if reason:
        out["hookSpecificOutput"]["permissionDecisionReason"] = reason
    print(json.dumps(out))
    sys.exit(0)


def post_block(reason: str) -> None:
    print(json.dumps({"decision": "block", "reason": reason}))
    sys.exit(0)


def post_ok() -> None:
    sys.exit(0)
