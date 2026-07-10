#!/usr/bin/env python3
"""SK-B2 tests: property (extraction recall), counterexample (verified-without-
evidence rejected; on_screen byte-match), delta (semantic vs cosmetic)."""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))
import claim_diff            # noqa: E402
import extract_claims        # noqa: E402
import ledger_validate       # noqa: E402

# ---- property fixture: 12 seeded claims (all should be candidates; all high-risk) ----
SEEDED = """Your DROP window is capped at 96 calendar months for most members.
To receive your DROP money, you must terminate all FRS-covered employment.
The DROP lump sum is taxed as ordinary income if you take it in cash.
A distribution paid to you carries mandatory 20% federal withholding.
A direct rollover keeps the money tax-deferred until you withdraw it.
DROP is available only to Pension Plan members.
Members enrolled on or after July 1, 2011 receive no COLA on their pension.
The Social Security Fairness Act repealed WEP and GPO in January 2025.
Special Risk members accrue benefits at 3 percent per year of service.
Your pension is calculated from your average final compensation over 8 years.
You are vested in the Pension Plan after 8 years of service.
Medicare Part B late enrollment adds a 10% penalty for each missed year.

I think planning early feels better than planning late.
Here's the part nobody mentions: paperwork is easier with coffee.
"""
NON_CLAIM_COUNT = 2  # the last two sentences are texture


def test_extraction_property() -> list[str]:
    errors = []
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "draft.md"
        p.write_text(SEEDED, encoding="utf-8")
        cands = extract_claims.extract(p.read_text(encoding="utf-8"))
    texts = [c["text"] for c in cands]
    seeded_lines = [l.strip() for l in SEEDED.strip().splitlines() if l.strip()][:12]
    found = sum(1 for s in seeded_lines if any(s in t or t in s for t in texts))
    if found < 11:
        errors.append(f"extraction recall {found}/12 < 11/12")
    high = [c for c in cands if c["risk"] == "high"
            and any(s in c["text"] or c["text"] in s for s in seeded_lines)]
    if len(high) < 12:
        errors.append(f"high-risk recall {len(high)}/12")
    print(f"  extraction: {found}/12 recall, {len(high)}/12 high-risk")
    return errors


# ---- counterexample: planted wrong figure, plausible blog source ----
def _ledger(status_block: str) -> str:
    return f"""run: 2026-07-10-ben-test-001
deliverable: drafts/test.md
version: 1
passes:
  - {{type: full, by: FACT, at: "2026-07-10T12:00"}}
claims:
  - id: CL-01
    text: "The 2026 contribution limit is $24,000."
    location: {{file: drafts/test.md, anchor: beat-2}}
    risk: high
    declared_by: WRITE
{status_block}
    on_screen: false
    history:
      - {{at: "2026-07-10T11:00", event: declared, by: WRITE}}
blocking_summary: {{high_risk_non_verified: 0}}
"""


def test_counterexamples() -> list[str]:
    errors = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        # WRONG path: verified by citation-trust, no evidence ref -> must be REJECTED
        wrong = td / "wrong.yaml"
        wrong.write_text(_ledger("    status: verified"), encoding="utf-8")
        v = ledger_validate.validate(wrong, None)
        if not any("without an evidence ref" in e for e in v):
            errors.append("counterexample FAILED: verified-without-evidence was accepted")
        else:
            print("  counterexample: verified-from-memory rejected ✓")
        # RIGHT path: incorrect status citing the controlling source -> accepted
        right = td / "right.yaml"
        right.write_text(_ledger(
            "    status: incorrect\n    evidence: S-BEN-0002\n"
            "    suggested_correction: \"route the figure to the official limit page\""
        ).replace("high_risk_non_verified: 0", "high_risk_non_verified: 1"), encoding="utf-8")
        v = ledger_validate.validate(right, None)
        if v:
            errors.append(f"right-path ledger rejected: {v}")
        else:
            print("  counterexample: incorrect-with-evidence accepted ✓")
        # on_screen byte-match (D-016)
        deliv = td / "d.md"
        deliv.write_text("The card says: DROP has a hard exit date.", encoding="utf-8")
        led = td / "os.yaml"
        led.write_text(_ledger(
            "    status: verified\n    evidence: F-BEN-0003"
        ).replace('text: "The 2026 contribution limit is $24,000."',
                  'text: "DROP has a hard exit deadline."')
         .replace("on_screen: false", "on_screen: true")
         .replace("high_risk_non_verified: 0", "high_risk_non_verified: 0"), encoding="utf-8")
        v = ledger_validate.validate(led, deliv)
        if not any("byte-present" in e for e in v):
            errors.append("on_screen mismatch not caught")
        else:
            print("  counterexample: on_screen byte-mismatch caught ✓")
    return errors


# ---- delta fixture: 3 semantic among 14 cosmetic ----
OLD = """You can access your pension earlier than age 62.
DROP participation is capped at 96 months.
The lump sum is taxed as ordinary income.
Planning ahead of a known date is a position of strength.
Your paycheck keeps coming while the bucket fills.
Mark the date on your calendar.
The pension is the pension.
Nobody explains this at the exit interview.
Retirement is a transition, not an event.
A checklist beats a maze.
Read your statement once a year.
The decision deserves a slow afternoon.
Coffee helps with paperwork.
Your family should know where the documents live.
The bucket earns interest quietly.
Ask questions before you sign anything.
Take a breath.
"""
NEW = """Many Special Risk members can access their pension earlier than age 62.
DROP participation is capped at 60 months.
The lump sum is taxed as capital gains.
Planning ahead of a known date is a position of strength!
Your paycheck keeps coming while the bucket fills;
mark the date on your calendar.
The pension is the pension.
Nobody explains this at the exit interview...
Retirement is a transition — not an event.
A checklist beats a maze.
Read your statement once a year,
the decision deserves a slow afternoon.
Coffee helps with the paperwork.
Your family should know where the documents live.
The bucket earns interest quietly.
Ask questions before you sign anything.
Take a breath.
"""
SEMANTIC_MARKERS = ["Special Risk", "60 months", "capital gains"]


def test_delta() -> list[str]:
    errors = []
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        (td / "old.md").write_text(OLD, encoding="utf-8")
        (td / "new.md").write_text(NEW, encoding="utf-8")
        hits = claim_diff.diff(td / "old.md", td / "new.md")
    flagged_texts = " | ".join((h["new"] or h["old"] or "") for h in hits)
    missed = [m for m in SEMANTIC_MARKERS if m not in flagged_texts]
    if missed:
        errors.append(f"delta MISSED semantic edits: {missed}")
    semantic_hits = sum(1 for m in SEMANTIC_MARKERS if m in flagged_texts)
    false_pos = len(hits) - semantic_hits
    if false_pos > 1:
        errors.append(f"delta false positives {false_pos} > 1: {hits}")
    print(f"  delta: {semantic_hits}/3 semantic flagged, {false_pos} false positive(s)")
    return errors


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    failures = []
    for name, fn in [("property", test_extraction_property),
                     ("counterexamples", test_counterexamples),
                     ("delta", test_delta)]:
        print(f"SK-B2 {name}:")
        failures += fn()
    print(f"\nSK-B2: {'PASS' if not failures else 'FAIL'} ({len(failures)} failure(s))")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
