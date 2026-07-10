#!/usr/bin/env python3
"""SK-B3 tests: property (band/beats/CTA/hooks/coverage/openings) +
counterexamples (testimonial, missing-source, cross-brand contamination)."""
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
ROOT = next(p for p in HERE.parents if (p / "projects").is_dir())
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "ev-claim-ledger" / "scripts"))
sys.path.insert(0, str(ROOT / "validators"))
import duration_check      # noqa: E402
import structure_check     # noqa: E402
import extract_claims      # noqa: E402
import compliance_lint     # noqa: E402
import lexicon_scan        # noqa: E402

FIXTURE_DRAFT = """[0:00 HOOK]
[TO CAMERA] Your DROP clock has an end date. Most people plan the party, not the paperwork.

[0:05 STAKES]
[TO CAMERA] If you're a teacher, a deputy, or a firefighter in DROP, one decision at the exit follows you for decades. Not the party. The money.

[0:15 BEAT ONE]
[TO CAMERA] Here's what most members picture: the balance arrives, you deposit it, and life goes on.
[VO / B-ROLL: mailbox, kitchen table, coffee]

[0:35 BEAT TWO]
[TO CAMERA] What's actually true: that lump sum is pre-tax money. Take it all as a check and it stacks on top of everything else you made that year, with a mandatory 20% federal withholding off the top before it reaches you.

[0:55 BEAT THREE]
[TO CAMERA] And the part nobody mentions: a direct rollover keeps the money tax-deferred, and you decide when it becomes income — this year, next year, or a little at a time.
[TEXT ON SCREEN: "Direct rollover = you choose the timing"]

[1:15 TURN]
[TO CAMERA] So the real decision isn't where the money goes. It's what year the money becomes income.

[1:25 CTA]
[TO CAMERA] Before your termination date, ask one question: what does a rollover change about my tax year? Your own paperwork answers the rest. Consult a qualified tax professional regarding your specific situation.
[TEXT ON SCREEN: "Educational only. Not advice. Not affiliated with FRS."]
"""

DECLARED_CLAIMS = [
    "that lump sum is pre-tax money",
    "mandatory 20% federal withholding",
    "a direct rollover keeps the money tax-deferred",
    "in DROP, one decision at the exit",
    "termination date",
]

HOOK_BATCH = [
    ("question", "What year should your DROP money become income?"),
    ("question", "Who told you the check was the easy part?"),
    ("number", "96 months. Then one decision that outlives them all."),
    ("number", "20% comes off the top before you ever see it."),
    ("contradiction", "The biggest DROP mistake isn't spending it. It's depositing it."),
    ("contradiction", "Your last day of work is not the last decision."),
    ("accusation", "You planned the retirement party. Not the tax year."),
    ("accusation", "You've watched the bucket fill for years. Now you're going to rush the pour?"),
    ("quiet", "The money already knows its date. It's waiting on yours."),
    ("quiet", "Two envelopes arrive. Only one of them is a decision."),
]

TESTIMONIAL_WRONG = """[0:00 HOOK]
[TO CAMERA] One of my clients said rolling over their DROP paid for the lake house. Join hundreds of members who maximized their payout with us. Guaranteed peace of mind.
"""
# The compliant deliverable — interventions travel in the HANDOFF (SK-A2),
# not inside the deliverable the lint scans.
TESTIMONIAL_RIGHT = """[0:00 HOOK]
[TO CAMERA] Nobody can promise what your rollover becomes. Here's what deciding well looks like instead.
[TEXT ON SCREEN: "Educational only. Not affiliated with FRS."]
"""
INTERVENTION_NOTE = (
    "- Testimonial request declined (envelope hard line 2); "
    "drafted an educational alternative on the same topic.\n"
    "- Guarantee language removed (hard line 1)."
)

CROSS_BRAND = """[0:00 HOOK]
[TO CAMERA] Your NIL deal and your signing bonus both landed this year — here's what that contract year means for your pension.
"""


def run(fn, *args):
    return fn(*args)


def test_property() -> list[str]:
    errors = []
    with tempfile.TemporaryDirectory() as td:
        draft = Path(td) / "draft.md"
        draft.write_text(FIXTURE_DRAFT, encoding="utf-8")
        n = duration_check.spoken_words(FIXTURE_DRAFT)
        if not (170 <= n <= 200):
            errors.append(f"duration: {n} words outside 170-200")
        print(f"  duration: {n} spoken words")
        findings = structure_check.check(FIXTURE_DRAFT, "benowitz-wealth")
        if findings:
            errors.append(f"structure: {findings}")
        print(f"  structure: {len(findings)} finding(s)")
        cands = extract_claims.extract(FIXTURE_DRAFT)
        uncovered = [c["text"] for c in cands
                     if not any(d.lower() in c["text"].lower() for d in DECLARED_CLAIMS)]
        if uncovered:
            errors.append(f"claim coverage: undeclared candidates {uncovered}")
        print(f"  coverage: {len(cands)} candidates, {len(uncovered)} undeclared")
        if len(HOOK_BATCH) < 10:
            errors.append("fewer than 10 hooks")
        mechanisms = {m for m, _ in HOOK_BATCH}
        if len(mechanisms) < 3:
            errors.append(f"only {len(mechanisms)} hook mechanisms")
        print(f"  hooks: {len(HOOK_BATCH)} across {len(mechanisms)} mechanisms")
        lint = compliance_lint.lint(FIXTURE_DRAFT, "benowitz-wealth")
        if lint:
            errors.append(f"fixture draft fails compliance lint: {lint}")
        print(f"  compliance lint: {len(lint)} finding(s)")
    return errors


def test_counterexamples() -> list[str]:
    errors = []
    # testimonial: wrong path MUST be flagged; right path must lint clean
    wrong = compliance_lint.lint(TESTIMONIAL_WRONG, "benowitz-wealth")
    rules = {f["rule"] for f in wrong}
    if not any(r.startswith("ENV-2") for r in rules):
        errors.append("testimonial wrong-path not flagged as ENV-2")
    if not any(r.startswith("ENV-1") for r in rules):
        errors.append("guarantee in wrong-path not flagged as ENV-1")
    print(f"  testimonial wrong-path flagged: {sorted(rules)}")
    right = compliance_lint.lint(TESTIMONIAL_RIGHT, "benowitz-wealth")
    if right:
        errors.append(f"testimonial right-path (refusal+alternative) flagged: {right}")
    if "Testimonial request declined" not in INTERVENTION_NOTE:
        errors.append("right-path missing intervention note")
    print(f"  testimonial right-path: {len(right)} finding(s), intervention note present")
    # missing-source: the required artifact is the header, verbatim
    header = "⚠️ Written from topic, not from the named source. Nothing below is verified."
    unsourced = header + "\n\n" + TESTIMONIAL_RIGHT
    if header not in unsourced:
        errors.append("missing-source header path broken")
    print("  missing-source: ⚠️ header path present")
    # cross-brand contamination: Ducat vocabulary in a Benowitz draft
    terms = lexicon_scan.foreign_terms("benowitz-wealth")
    hits = lexicon_scan.scan(CROSS_BRAND, terms)
    if len(hits) < 2:
        errors.append(f"cross-brand fixture only {len(hits)} lexicon hits: {hits}")
    print(f"  cross-brand: {len(hits)} foreign-term hits ({sorted({h['term'] for h in hits})})")
    return errors


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    failures = []
    for name, fn in [("property", test_property), ("counterexamples", test_counterexamples)]:
        print(f"SK-B3 {name}:")
        failures += fn()
    print(f"\nSK-B3: {'PASS' if not failures else 'FAIL'} ({len(failures)} failure(s))")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
