#!/usr/bin/env python3
"""HK4 — PreToolUse WebFetch|WebSearch: per-agent web policy (D-010, D-015).

RSRCH: full web (the single entry point for evidence, D2).
FACT: fetch only URLs already present in the current run's packet/ledger files
      (verification of cited sources, never new sourcing).
REMO/HYPF: official-docs domain allowlist.
Everyone else: deny — WRITE/COMPL/ORCH deliberately have no web (Phase 2 §4.2).
Main session: allowed during build mode (doc re-verification is a build duty).
"""
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent))
from _common import ROOT, allow, build_mode, deny, read_input

ENGINE_DOMAINS = {
    "REMO": ("remotion.dev", "www.remotion.dev", "github.com/remotion-dev"),
    "HYPF": ("github.com/heygen-com", "hyperframes.heygen.com", "docs.heygen.com"),
}


def url_cited_in_run_files(url: str) -> bool:
    """Deterministic check: the URL (host+path) appears in a packet or ledger."""
    parsed = urlparse(url)
    needle = (parsed.netloc + parsed.path).rstrip("/")
    if not needle:
        return False
    runs = ROOT / "runs"
    if not runs.exists():
        return False
    for pattern in ("*/research/*.yaml", "*/research/*.yml", "*/factcheck/*.yaml", "*/factcheck/*.yml"):
        for f in runs.glob(pattern):
            try:
                if needle in f.read_text(encoding="utf-8", errors="ignore"):
                    return True
            except OSError:
                continue
    return False


def main() -> None:
    data = read_input()
    tool_input = data.get("tool_input", {})
    url = tool_input.get("url", "") or ""
    agent = (data.get("agent_id") or data.get("agent_type") or "").upper()

    if not agent:
        if build_mode():
            allow("HK4: main session, build mode — doc re-verification traffic (DEC-BUILD-005)")
        deny("HK4: ORCH has no web — it delegates; a manager that researches becomes "
             "a bottleneck and a contamination vector (Phase 2 §4.2)")

    if agent == "RSRCH":
        allow("HK4: RSRCH is the single evidence entry point (D2)")

    if agent == "FACT":
        if data.get("tool_name") == "WebSearch":
            deny("HK4: FACT verifies cited URLs only — searching for new sources is RSRCH's job")
        if url and url_cited_in_run_files(url):
            allow("HK4: URL present in current packet/ledger — verification fetch")
        deny(f"HK4: FACT may fetch only URLs already cited in a packet or ledger; "
             f"'{url}' is not — new sourcing belongs to RSRCH")

    if agent in ENGINE_DOMAINS:
        host_path = (urlparse(url).netloc + urlparse(url).path) if url else ""
        if any(host_path == d or host_path.startswith(d + "/") for d in ENGINE_DOMAINS[agent]):
            allow(f"HK4: {agent} official-docs domain")
        deny(f"HK4: {agent} web access is domain-allowlisted to official docs "
             f"{ENGINE_DOMAINS[agent]}; extending the list is a proposal, not a fetch")

    deny(f"HK4: agent {agent} has no web access (Phase 2 §4.2 — evidence enters through RSRCH)")


if __name__ == "__main__":
    main()
