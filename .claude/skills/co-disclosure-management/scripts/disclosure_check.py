#!/usr/bin/env python3
"""disclosure_check.py — disclosure presence, verbatim-ness, placement (SK-B15).

Given a deliverable + project (+ context flags), asserts the required DISC-*
text is present VERBATIM (never summarized as "[add disclaimer]"), the tax
line rides along when the content touches taxes, and short-format fallbacks
carry their conditions.

Usage: python disclosure_check.py <deliverable> --project <id> [--short-format] [--tax]
Exit 0 · 1 violations
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "projects").is_dir())
TAX_TOPIC = re.compile(r"(?i)\b(tax(es|able|ed)?|withholding|IRS|bracket|ordinary income)\b")


def load_disclosures(project: str) -> dict[str, str]:
    """Parse DISC blocks: '## DISC-ID — label' followed by > quoted lines."""
    path = ROOT / "projects" / project / "disclosures.md"
    if not path.exists():
        return {}
    blocks, current, buf = {}, None, []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+(DISC-[A-Z0-9-]+)", line)
        if m:
            if current and buf:
                blocks[current] = " ".join(buf)
            current, buf = m.group(1), []
        elif current and line.strip().startswith(">"):
            buf.append(line.strip().lstrip("> ").strip())
    if current and buf:
        blocks[current] = " ".join(buf)
    return blocks


def squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def check(text: str, project: str, short_format: bool, tax: bool | None) -> list[str]:
    errors = []
    disc = load_disclosures(project)
    if not disc:
        return [f"no disclosures.md records found for {project}"]
    flat = squash(text)
    standard = next((k for k in disc if k.endswith("-01") and "TAX" not in k and "SHORT" not in k), None)
    short = next((k for k in disc if "SHORT" in k), None)
    tax_id = next((k for k in disc if "TAX" in k), None)

    if short_format:
        if short and squash(disc[short]) not in flat:
            errors.append(f"short-format minimum {short} not present verbatim")
        if not re.search(r"(?i)(profile|first comment|closing slide)", text):
            errors.append("short format must state where the full disclosure lives")
    else:
        if standard and squash(disc[standard]) not in flat:
            errors.append(f"required disclosure {standard} not present verbatim "
                          "(never summarized; if it won't fit the format, the format is wrong)")

    # topic detection must not trigger on the disclosure texts themselves
    # ("...investment, tax, or legal advice" is boilerplate, not tax content)
    content_only = squash(text)
    for d in disc.values():
        content_only = content_only.replace(squash(d), " ")
    touches_tax = TAX_TOPIC.search(content_only) is not None if tax is None else tax
    if touches_tax and tax_id and squash(disc[tax_id]) not in flat:
        errors.append(f"tax content without {tax_id} referral line")
    return errors


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("deliverable")
    ap.add_argument("--project", required=True)
    ap.add_argument("--short-format", action="store_true")
    ap.add_argument("--tax", action="store_true", default=None)
    args = ap.parse_args()
    errors = check(Path(args.deliverable).read_text(encoding="utf-8"),
                   args.project, args.short_format, args.tax)
    for e in errors:
        print(f"FAIL: {e}")
    print(f"{'PASS' if not errors else 'FAIL'}: {len(errors)} violation(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
