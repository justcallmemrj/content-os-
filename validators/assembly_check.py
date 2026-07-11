#!/usr/bin/env python3
"""Assembly-consistency validator — the campaign gate (Phase 5 §4, C6 G-V).

Individually compliant pieces can still disagree with each other. Checks:
  1. AD ⊆ LANDING: every claim in an ad-role child's ledger must appear in at
     least one landing-role child's ledger — matched by claim_key when both
     carry one, else by canonical text — and the landing copy must hold a
     supporting status (verified / verified-with-qualification). The ad may
     not promise what the page doesn't support.
  2. OFFER IDENTICAL: the brief's offer.text appears verbatim (canonical
     whitespace form) in every child's offer_text_path file.
  3. DISCLOSURE COVERAGE: every child's final text carries at least one
     DISC-* id reference or the project's short-format disclosure text.

Usage: python assembly_check.py <runs/<campaign-id>/campaign.yaml>
Exit 0 = green; exit 2 = violations (C5f: offending children revise).
"""
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SUPPORTING = {"verified", "verified-with-qualification"}


def canon(s: str) -> str:
    return " ".join(unicodedata.normalize("NFC", s).split())


def load_claims(ledger_path: Path):
    doc = yaml.safe_load(ledger_path.read_text(encoding="utf-8"))
    out = []
    for c in doc.get("claims", []):
        out.append({"id": c.get("id"), "key": c.get("claim_key"),
                    "text": canon(c.get("text", "")), "status": c.get("status")})
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    cmp_path = Path(sys.argv[1])
    cmp_doc = yaml.safe_load(cmp_path.read_text(encoding="utf-8"))
    base = ROOT
    v = []

    children = cmp_doc["children"]
    ads = [c for c in children if c["role"] == "ad"]
    landings = [c for c in children if c["role"] == "landing"]

    landing_claims = []
    for lc in landings:
        p = base / lc["ledger"]
        if not p.exists():
            v.append(f"{lc['run_id']}: landing ledger missing ({lc['ledger']})")
            continue
        landing_claims += [c for c in load_claims(p) if c["status"] in SUPPORTING]

    def supported(claim):
        for l in landing_claims:
            if claim["key"] and l["key"]:
                if claim["key"] == l["key"]:
                    return True
            elif claim["text"] == l["text"]:
                return True
        return False

    for ad in ads:
        p = base / ad["ledger"]
        if not p.exists():
            v.append(f"{ad['run_id']}: ad ledger missing ({ad['ledger']})")
            continue
        for claim in load_claims(p):
            if claim["status"] in SUPPORTING and not supported(claim):
                v.append(f"{ad['run_id']}: ad claim {claim['id']} ({claim['text'][:60]!r}) "
                         f"not supported by any landing child — the ad promises what the page doesn't hold")

    offer = canon(cmp_doc["brief"]["offer"]["text"])
    for c in children:
        fp = c.get("offer_text_path")
        if not fp:
            v.append(f"{c['run_id']}: no offer_text_path declared")
            continue
        p = base / fp
        if not p.exists():
            v.append(f"{c['run_id']}: offer file missing ({fp})")
            continue
        body = canon(p.read_text(encoding="utf-8"))
        if offer not in body:
            v.append(f"{c['run_id']}: offer language drifted — brief's offer text not found verbatim")
        if "DISC-" not in p.read_text(encoding="utf-8"):
            v.append(f"{c['run_id']}: no DISC-* reference in final text — disclosure coverage incomplete")

    n_ad_claims = sum(1 for ad in ads if (base / ad["ledger"]).exists()
                      for c in load_claims(base / ad["ledger"]) if c["status"] in SUPPORTING)
    print(f"assembly-check: {len(children)} children ({len(ads)} ad, {len(landings)} landing), "
          f"{n_ad_claims} supported ad claims checked, {len(v)} violation(s)")
    for x in v:
        print(f"  - {x}")
    return 2 if v else 0


if __name__ == "__main__":
    sys.exit(main())
