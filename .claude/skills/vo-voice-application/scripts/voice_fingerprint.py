#!/usr/bin/env python3
"""voice_fingerprint.py — the deterministic half of the voice fingerprint (D-030).

Measures: sentence-length median and p90 vs. profile bands; banned-opening
hits; avoided-phrase hits; approximate readability grade vs. band. Judgment
resemblance ("does this sound like Wes") is scored separately against
exemplars — we never pretend the second is the first.

Usage: python voice_fingerprint.py <text.md> --project <id> [--json]
Exit 0 pass · 1 fingerprint violations
"""
import argparse
import json
import re
import statistics
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve()
ROOT = next(p for p in HERE.parents if (p / "projects").is_dir())
MARKER_LINE = re.compile(r"^\s*(\[|>|#|\||-{3,})")
INLINE_MARKER = re.compile(r"\[(TO CAMERA|VO / B-ROLL:[^\]]*|TEXT ON SCREEN:[^\]]*)\]", re.I)
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
VOWELS = re.compile(r"[aeiouy]+")


def profile(project: str) -> dict:
    bv = ROOT / "projects" / project / "brand-voice.md"
    text = bv.read_text(encoding="utf-8")
    return yaml.safe_load(text[3:text.find("\n---", 3)])


def spoken_sentences(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        clean = INLINE_MARKER.sub("", line)
        if MARKER_LINE.match(clean):
            continue
        out.extend(s.strip() for s in SENTENCE_SPLIT.split(clean.strip()) if s.strip())
    return out


def syllables(word: str) -> int:
    return max(1, len(VOWELS.findall(word.lower())))


def fk_grade(sents: list[str]) -> float:
    words = [w for s in sents for w in re.findall(r"[A-Za-z']+", s)]
    if not words or not sents:
        return 0.0
    return round(0.39 * (len(words) / len(sents))
                 + 11.8 * (sum(syllables(w) for w in words) / len(words)) - 15.59, 1)


def fingerprint(text: str, project: str) -> dict:
    prof = profile(project)
    sents = spoken_sentences(text)
    lengths = sorted(len(s.split()) for s in sents) or [0]
    median = statistics.median(lengths)
    p90 = lengths[min(len(lengths) - 1, int(0.9 * len(lengths)))]
    grade = fk_grade(sents)

    violations = []
    sl = prof.get("sentence_length", {})
    if sl.get("p90_max") and p90 > sl["p90_max"]:
        violations.append(f"p90 sentence length {p90} > {sl['p90_max']}")
    rb = prof.get("readability_band", {})
    # The ceiling blocks (too complex = not this brand). The floor is
    # informational only: "short sentences, fragments are fine" is doctrine,
    # so simpler-than-band never fails the fingerprint.
    if rb and grade > rb["grade_max"] + 2:
        violations.append(f"readability grade {grade} above ceiling {rb['grade_max']}")
    lowered = text.lower()
    for opening in prof.get("banned_openings", []):
        if lowered.strip().startswith(opening.lower()) or f"\n{opening.lower()}" in lowered:
            violations.append(f"banned opening: {opening!r}")
    for phrase in prof.get("avoided_phrases", []):
        if re.search(r"(?i)\b" + re.escape(phrase) + r"\b", text):
            violations.append(f"avoided phrase: {phrase!r}")

    return {"median_sentence_length": median, "p90": p90, "grade": grade,
            "violations": violations}


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("text")
    ap.add_argument("--project", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    fp = fingerprint(Path(args.text).read_text(encoding="utf-8"), args.project)
    if args.json:
        print(json.dumps(fp, indent=1))
    else:
        print(f"median {fp['median_sentence_length']}w · p90 {fp['p90']}w · grade {fp['grade']}")
        for v in fp["violations"]:
            print(f"FAIL: {v}")
        print(f"{'PASS' if not fp['violations'] else 'FAIL'}")
    return 1 if fp["violations"] else 0


if __name__ == "__main__":
    sys.exit(main())
