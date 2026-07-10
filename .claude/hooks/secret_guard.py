#!/usr/bin/env python3
"""HK5 — PreToolUse Read|Write|Edit|Bash: secrets never travel (D-069).

Denies access to .env*, key material, and credential-pattern paths/commands —
for everyone, in every mode. There are no legitimate secret reads in v1 by
construction (no publish/send/spend surfaces exist).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import allow, deny, read_input, rel_path

PATH_PATTERNS = [
    re.compile(r"(^|/)\.env($|\.)"),
    re.compile(r"\.(pem|key|pfx|p12)$"),
    re.compile(r"(^|/)id_(rsa|ed25519|ecdsa)"),
    re.compile(r"(?i)(^|/)(credentials?|secrets?)(\.|/|$)"),
    re.compile(r"(?i)hosts\.yml$"),
]
CMD_PATTERNS = [
    re.compile(r"(?i)(^|[\s|;&])\S*\.env\b"),
    re.compile(r"(?i)\b(id_rsa|\.pem\b|\.key\b)"),
    re.compile(r"(?i)gh\s+auth\s+token"),
]


def main() -> None:
    data = read_input()
    tool_input = data.get("tool_input", {})
    tool = data.get("tool_name", "")

    if tool == "Bash":
        cmd = tool_input.get("command", "") or ""
        for pat in CMD_PATTERNS:
            if pat.search(cmd):
                deny("HK5: command touches secret material (.env/keys/credentials) — "
                     "secrets live in the environment/keychain, never in tool reach (D-069)")
        allow()

    raw = tool_input.get("file_path") or ""
    if not raw:
        allow()
    rel = rel_path(data, raw)
    for pat in PATH_PATTERNS:
        if pat.search(rel):
            deny(f"HK5: '{rel}' matches a secret pattern — denied for everyone, every mode (D-069)")
    allow()


if __name__ == "__main__":
    main()
