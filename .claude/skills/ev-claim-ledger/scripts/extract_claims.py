#!/usr/bin/env python3
"""extract_claims.py — candidate-claim detection (SK-B2).

Flags sentences likely to contain verifiable claims: numbers, dates, dollar
amounts, percentages, eligibility verbs, and modal-free factual assertions
about rules/programs. Recall-oriented: it is WRITE's self-audit and FACT's
independent sweep, not the boundary — a human-shaped claim it misses is still
FACT's to find.

Usage: python extract_claims.py <deliverable.md> [--json]
Output: one candidate per line: "n. [risk] sentence"
"""
import json
import re
import sys
from pathlib import Path

NUMERIC = re.compile(r"\d")
DOLLAR = re.compile(r"\$\s?\d")
PERCENT = re.compile(r"\d\s?%|\bpercent\b", re.I)
DATE = re.compile(r"\b(19|20)\d{2}\b|\b(january|february|march|april|may|june|july|august|september|october|november|december)\b", re.I)
ELIGIBILITY = re.compile(r"\b(eligible|eligibility|qualify|qualifies|vested|must|required|requirement|only if|available only|entitled)\b", re.I)
RULE_ASSERT = re.compile(r"\b(is|are|means|allows|lets|requires|becomes|receives?|gets?|pays?|earns?|repealed|extended|taxed|withheld|keeps?|remains?|adds?|accrues?|capped|calculated|vested|begins?|starts?)\b", re.I)
TAX_LEGAL = re.compile(r"\b(tax(es|ed|able|ation)?|irs|statute|law|legislation|penalty|penalties|withholding|rmd|medicare|social security)\b", re.I)
HEDGED = re.compile(r"\b(may|might|could|often|sometimes|generally|usually|worth considering|ask)\b", re.I)

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'“])")
MARKER = re.compile(r"^\s*(\[|>|#|\||-{3,})")
DELIVERY_MARKER = re.compile(r"\[(TO CAMERA|VO / B-ROLL:[^\]]*)\]", re.I)
ON_SCREEN = re.compile(r"\[TEXT ON SCREEN:\s*\"?([^\"\]]+)\"?\]", re.I)


def classify_risk(s: str) -> str:
    # spec: numeric, eligibility, legal, tax = high (Phase 4 §7.1 / risk-classification.md)
    if (DOLLAR.search(s) or PERCENT.search(s) or NUMERIC.search(s) or DATE.search(s)
            or ELIGIBILITY.search(s) or TAX_LEGAL.search(s)):
        return "high"
    if RULE_ASSERT.search(s):
        return "medium"
    return "low"


def extract(text: str) -> list[dict]:
    candidates = []
    for raw_line in text.splitlines():
        # on-screen strings are claims too (D-016) — extract before stripping
        for m in ON_SCREEN.finditer(raw_line):
            s = m.group(1).strip()
            if len(s.split()) >= 4 and (NUMERIC.search(s) or RULE_ASSERT.search(s)):
                candidates.append({"text": s, "risk": classify_risk(s),
                                   "hedged": bool(HEDGED.search(s)), "on_screen": True})
        raw_line = ON_SCREEN.sub("", DELIVERY_MARKER.sub("", raw_line))
        if MARKER.match(raw_line):        # what remains bracketed is structure
            continue
        for sentence in SENTENCE_SPLIT.split(raw_line.strip()):
            s = sentence.strip()
            if len(s.split()) < 4:
                continue
            is_claim = bool(
                DOLLAR.search(s) or PERCENT.search(s) or DATE.search(s)
                or (NUMERIC.search(s) and RULE_ASSERT.search(s))
                or (ELIGIBILITY.search(s) and RULE_ASSERT.search(s))
                or (TAX_LEGAL.search(s) and RULE_ASSERT.search(s) and not HEDGED.search(s))
            )
            if is_claim:
                candidates.append({"text": s, "risk": classify_risk(s),
                                   "hedged": bool(HEDGED.search(s))})
    return candidates


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    path = Path(sys.argv[1])
    cands = extract(path.read_text(encoding="utf-8"))
    if "--json" in sys.argv:
        print(json.dumps(cands, indent=1))
    else:
        for i, c in enumerate(cands, 1):
            print(f"{i}. [{c['risk']}] {c['text']}")
        print(f"{len(cands)} candidate claim(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
