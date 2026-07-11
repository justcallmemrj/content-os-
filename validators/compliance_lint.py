#!/usr/bin/env python3
"""compliance_lint.py — the deterministic tier of two-tier compliance (D-002).

Runs on every transition (cheap, always); COMPL's model judgment layers on top
at the gate; the human always follows. Checks a deliverable against the
envelope's hard lines + brand rules that have deterministic shadows.

Usage: python validators/compliance_lint.py <deliverable> --project <id> [--tax] [--json]
Exit: 0 clean · 1 findings (listed on stdout/stderr)
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Envelope hard line 1 — performance claims / guarantees / projections
PERFORMANCE = [
    re.compile(r"(?i)\b(could|can|will|would)\s+save\s+(you|your)\b"),
    re.compile(r"(?i)\bsave\s+(you\s+)?(thousands|\$)"),
    re.compile(r"(?i)\bguarantee[ds]?\b"),
    re.compile(r"(?i)\bmaximize\s+your\s+(payout|pension|benefit|return)"),
    re.compile(r"(?i)\bgrow\s+your\s+money\s+by\b"),
    re.compile(r"(?i)\bget\s+more\s+from\s+your\s+pension\b"),
    re.compile(r"(?i)\bleav(e|ing)\s+money\s+on\s+the\s+table\b"),
]
# Hard line 2 — testimonials/endorsements
TESTIMONIAL = [
    re.compile(r"(?i)\b(a|one of my|our)\s+clients?\s+(said|told|shared|wrote)"),
    re.compile(r"(?i)\bjoin\s+(the\s+)?hundreds\s+of\b"),
    re.compile(r"(?i)\btestimonial\b"),
]
# Hard line 3 — individualized advice
ADVICE = [
    re.compile(r"(?i)\byou\s+should\s+(take|roll|buy|sell|move|invest|claim)\b"),
    re.compile(r"(?i)\btake\s+the\s+lump\s+sum\s+and\s+roll\b"),
]
# Standing rules
# FEE_ONLY rule RETIRED by DEC-BEN-0002 (hold lifted 2026-07-11, ADV-verified);
# the pattern lives in git history should a future decision re-impose it.
URGENCY = [
    re.compile(r"(?i)\b(act|call|book)\s+now\b"),
    re.compile(r"(?i)\bbefore\s+it'?s\s+too\s+late\b"),
    re.compile(r"(?i)\bdon'?t\s+wait\b"),
]
SOLVENCY_FEAR = [
    re.compile(r"(?i)pension\s+(is\s+)?(going\s+)?(broke|insolvent|collapsing|running\s+out)"),
]

DISCLOSURE_SNIPPETS = {
    "benowitz-wealth": ["not affiliated with", "Educational"],
    "ducat-private-wealth": ["not affiliated with", "Educational"],
    "trading-research": ["Educational research only"],
}
TAX_LINE = re.compile(r"(?i)consult\s+a\s+qualified\s+tax\s+professional")
TAX_TOPIC = re.compile(r"(?i)\b(tax(es|able|ed)?|withholding|IRS|bracket|ordinary income)\b")


def lint(text: str, project: str, tax: bool | None = None) -> list[dict]:
    findings = []

    def hit(rules, rule_id, severity, why):
        for pat in rules:
            m = pat.search(text)
            if m:
                findings.append({"rule": rule_id, "severity": severity,
                                 "match": m.group(0), "why": why})

    hit(PERFORMANCE, "ENV-1-performance", "major",
        "performance claim/guarantee/projection (envelope hard line 1)")
    hit(TESTIMONIAL, "ENV-2-testimonial", "major",
        "testimonial/endorsement pattern (envelope hard line 2)")
    hit(ADVICE, "ENV-3-individualized", "major",
        "individualized-advice framing (envelope hard line 3)")
    hit(URGENCY, "VOICE-urgency", "minor", "manufactured urgency (urgency slider is 1 by design)")
    if project == "benowitz-wealth":
        hit(SOLVENCY_FEAR, "BEN-C2-solvency-fear", "major", "pension-solvency fear as persuasion")

    snippets = DISCLOSURE_SNIPPETS.get(project, [])
    if snippets and not all(s.lower() in text.lower() for s in snippets):
        findings.append({"rule": "ENV-4-disclosure", "severity": "major",
                         "match": "(absent)", "why": "required disclosure text not found (non-affiliation is an implied claim when silent)"})

    tax_touches = TAX_TOPIC.search(text) is not None if tax is None else tax
    if tax_touches and project in ("benowitz-wealth", "ducat-private-wealth") and not TAX_LINE.search(text):
        findings.append({"rule": "TAX-referral", "severity": "major",
                         "match": "(absent)", "why": "tax content requires the qualified-tax-professional referral line"})
    return findings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("deliverable")
    ap.add_argument("--project", required=True)
    ap.add_argument("--tax", action="store_true", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    text = Path(args.deliverable).read_text(encoding="utf-8")
    findings = lint(text, args.project, args.tax)
    if args.json:
        print(json.dumps(findings, indent=1))
    else:
        for f in findings:
            print(f"[{f['severity']}] {f['rule']}: {f['why']} ({f['match']!r})")
        print(f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    main() and sys.exit(1)
