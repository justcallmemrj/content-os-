#!/usr/bin/env python3
"""social_format_check.py — deterministic social-format validators (SK-B4).

Modes: carousel (Slide-N blocks; slides 2..N-1 one idea <=25 words; final
slide carries CTA+disclosure) · caption (hook line, <=6 body lines, disclosure
present) · linkedin (150-300 words; first-comment disclosure STATED in-post;
no link-in-bio).

Usage: python social_format_check.py <file> --format carousel|caption|linkedin
Exit 0 pass · 1 findings
"""
import argparse
import re
import sys
from pathlib import Path

SLIDE = re.compile(r"^\*\*Slide (\d+):\*\*\s*(.*)$", re.M)
DISCLOSURE_HINT = re.compile(r"(?i)(educational only|not affiliated|full disclosures?)")
FIRST_COMMENT_STATED = re.compile(r"(?i)(first comment|in the comments)")
LINK_IN_BIO = re.compile(r"(?i)link in bio")


def check_carousel(text: str) -> list[str]:
    findings = []
    slides = SLIDE.findall(text)
    if len(slides) < 3:
        return [f"carousel needs >=3 slides, found {len(slides)}"]
    nums = [int(n) for n, _ in slides]
    if nums != list(range(1, len(nums) + 1)):
        findings.append(f"slide numbering broken: {nums}")
    # body slides: one idea each, under 25 words (slide text = the line after the marker
    # up to the next slide marker)
    blocks = re.split(r"^\*\*Slide \d+:\*\*\s*", text, flags=re.M)[1:]
    for i, block in enumerate(blocks[1:-1], start=2):     # slides 2..N-1
        words = len(block.split())
        if words > 25:
            findings.append(f"slide {i}: {words} words > 25 (one idea per slide)")
        if len([s for s in re.split(r"[.!?]", block) if len(s.split()) > 3]) > 2:
            findings.append(f"slide {i}: reads as multiple ideas")
    final = blocks[-1]
    if not DISCLOSURE_HINT.search(final):
        findings.append("final slide missing the disclosure")
    return findings


def check_caption(text: str) -> list[str]:
    findings = []
    lines = [l for l in text.splitlines() if l.strip()]
    if not lines:
        return ["empty caption"]
    if len(lines[0].split()) > 20:
        findings.append("hook line too long to survive the fold")
    if not DISCLOSURE_HINT.search(text):
        findings.append("caption missing the disclosure")
    return findings


def check_linkedin(text: str) -> list[str]:
    findings = []
    body = re.sub(r"(?im)^disclosure.*$", "", text)
    words = len(body.split())
    if not (150 <= words <= 300):
        findings.append(f"LinkedIn body {words} words outside 150-300")
    if LINK_IN_BIO.search(text):
        findings.append("'link in bio' means nothing on LinkedIn — link goes in the first comment")
    if not FIRST_COMMENT_STATED.search(text):
        findings.append("post must STATE that link/full disclosure lives in the first comment")
    one_liners = sum(1 for l in text.splitlines() if 0 < len(l.split()) <= 4)
    if one_liners > 4:
        findings.append("staccato one-liners — reads as a Reel caption in the wrong box")
    return findings


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--format", required=True, choices=["carousel", "caption", "linkedin"])
    args = ap.parse_args()
    text = Path(args.file).read_text(encoding="utf-8")
    findings = {"carousel": check_carousel, "caption": check_caption,
                "linkedin": check_linkedin}[args.format](text)
    for f in findings:
        print(f"FAIL: {f}")
    print(f"{'PASS' if not findings else 'FAIL'}: {len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
