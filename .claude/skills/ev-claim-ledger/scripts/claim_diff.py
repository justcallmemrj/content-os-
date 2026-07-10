#!/usr/bin/env python3
"""claim_diff.py — sentence-aligned semantic-delta candidates (SK-B2 delta mode).

Compares two versions of a deliverable and flags sentences whose change is
plausibly semantic (words with factual weight changed), separating them from
cosmetic edits (punctuation, casing, filler). Recall-oriented: flagged
sentences go to VOICE to map to CL-ids; suppressing a hit is prohibited —
"it's just cadence" is FACT's call.

Usage: python claim_diff.py <old.md> <new.md> [--json]
"""
import difflib
import json
import re
import sys
from pathlib import Path

SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")
MARKER = re.compile(r"^\s*(\[|>|#|\||-{3,})")
COSMETIC_STRIP = re.compile(r"[^a-z0-9$%]+")
FACTUAL_TOKEN = re.compile(r"\d|%|\$|\b(all|only|must|may|can|cannot|never|always|most|many|some|no|not)\b")
STOPWORDS = {"the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "at",
             "for", "with", "as", "is", "are", "was", "be", "it", "its", "your",
             "you", "that", "this", "so", "up", "out"}


def sentences(path: Path) -> list[str]:
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if MARKER.match(line):
            continue
        out.extend(s.strip() for s in SENTENCE_SPLIT.split(line.strip()) if s.strip())
    return out


def normalize(s: str) -> str:
    return COSMETIC_STRIP.sub(" ", s.lower()).strip()


def semantic_delta(old_text: str, new_text: str) -> bool:
    """True when the changed words carry semantic weight.

    Block-level word comparison so re-segmented sentences (a merged line, a
    swapped period) don't read as edits. Semantic = any changed token that is
    a factual token (number/$/%/quantifier) or a content word (len>3, not a
    stopword). Punctuation, case, and filler churn are cosmetic.
    """
    old_w, new_w = set(normalize(old_text).split()), set(normalize(new_text).split())
    changed = old_w ^ new_w
    return any(FACTUAL_TOKEN.search(w) or (len(w) > 3 and w not in STOPWORDS)
               for w in changed)


def diff(old_path: Path, new_path: Path) -> list[dict]:
    old_s, new_s = sentences(old_path), sentences(new_path)
    sm = difflib.SequenceMatcher(a=[normalize(s) for s in old_s],
                                 b=[normalize(s) for s in new_s])
    hits = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        old_block, new_block = " ".join(old_s[i1:i2]), " ".join(new_s[j1:j2])
        if normalize(old_block) == normalize(new_block):
            continue                               # pure re-segmentation/punctuation
        if not semantic_delta(old_block, new_block):
            continue                               # cosmetic word churn only
        kind = {"replace": "edited", "delete": "removed", "insert": "added"}[tag]
        hits.append({"kind": kind, "old": old_block or None, "new": new_block or None})
    return hits


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    hits = diff(Path(sys.argv[1]), Path(sys.argv[2]))
    if "--json" in sys.argv:
        print(json.dumps(hits, indent=1))
    else:
        for h in hits:
            print(f"[{h['kind']}] old: {h['old']!r} -> new: {h['new']!r}")
        print(f"{len(hits)} semantic-delta candidate(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
