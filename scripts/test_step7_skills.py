#!/usr/bin/env python3
"""Step-7 skill tests: SK-B4 social formats, SK-B5 delta inheritance (against
the REAL approved parent run), SK-B12 calendar hygiene."""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".claude" / "skills"
sys.path.insert(0, str(SKILLS / "wr-social-copy/scripts"))
sys.path.insert(0, str(SKILLS / "st-calendar-planning/scripts"))
import social_format_check as sfc   # noqa: E402
import calendar_check as cal        # noqa: E402

failures = []


def check(label, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + label)
    if not cond:
        failures.append(f"{label}: {detail}")


# ---- SK-B4: carousel ----
GOOD_CAROUSEL = """**Slide 1:** Your DROP exit has one big decision hiding inside it.
**Slide 2:** The monthly pension turns on by itself.
**Slide 3:** The lump sum waits for your instruction.
**Slide 4:** Cash is taxed as that year's ordinary income.
**Slide 5:** A direct rollover stays tax-deferred.
**Slide 6:** The timing becomes yours.
**Slide 7:** Save this for your exit year.
**Slide 8:** Free DROP Exit webinar — link in profile. Educational only. Not affiliated with FRS. Full disclosures in profile.
"""
BAD_CAROUSEL = GOOD_CAROUSEL.replace(
    "**Slide 4:** Cash is taxed as that year's ordinary income.",
    "**Slide 4:** Cash is taxed as that year's ordinary income, stacked on top of everything else you earn, with a mandatory twenty percent federal withholding taken right off the top before the money ever reaches your account.")
NO_DISC_CAROUSEL = GOOD_CAROUSEL.replace(
    " Educational only. Not affiliated with FRS. Full disclosures in profile.", "")

check("SK-B4 compliant carousel passes", not sfc.check_carousel(GOOD_CAROUSEL))
check("SK-B4 40-word slide fails", any("words > 25" in f for f in sfc.check_carousel(BAD_CAROUSEL)))
check("SK-B4 disclosure-free final slide fails",
      any("disclosure" in f for f in sfc.check_carousel(NO_DISC_CAROUSEL)))

# ---- SK-B4: linkedin ----
GOOD_LI = ("A district benefits coordinator asked me last week what happens to a member's DROP balance "
           "the month after separation, and it is the right question at the right altitude. "
           + "The mechanics matter to the people who advise members every day. " * 12 +
           "If this is useful, forward it to the person who fields these questions in your building. "
           "Full disclosures and the registration link are in the first comment.")
BAD_LI_SHORT = "Quick DROP tip. Link in bio. Educational only."

check("SK-B4 LinkedIn in-band with first-comment statement passes",
      not sfc.check_linkedin(GOOD_LI), str(sfc.check_linkedin(GOOD_LI)))
li_bad = sfc.check_linkedin(BAD_LI_SHORT)
check("SK-B4 LinkedIn short + link-in-bio fails on both",
      any("outside 150-300" in f for f in li_bad) and any("first comment" in f for f in li_bad)
      and any("bio" in f for f in li_bad), str(li_bad))

# ---- SK-B5: delta inheritance against the REAL approved parent ----
PARENT_RUN = "2026-07-10-ben-drop-001"
PARENT_ARTIFACT = ROOT / "runs" / PARENT_RUN / "voice" / "drop-reel-v3.md"
LOCKED_HASH = "8ec534b3c7ef61d4e26d9c75525bdf4ef9f6b4fd8b6da901c5a6b5a3bc1aafd0"
import yaml  # noqa: E402
parent_ledger = yaml.safe_load((ROOT / "runs" / PARENT_RUN / "factcheck" / "ledger.yaml").read_text(encoding="utf-8"))
verified_texts = [c["text"] for c in parent_ledger["claims"]
                  if c["status"] in ("verified", "verified-with-qualification")][:2]
assert len(verified_texts) == 2, "need two verified parent claims for the fixture"

with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    child = td / "linkedin-adaptation.md"
    child.write_text(
        "LinkedIn adaptation fixture.\n\n"
        + verified_texts[0] + "\n\n" + verified_texts[1] + "\n\n"
        "New adaptation-only sentence: coordinators field these questions every spring.\n",
        encoding="utf-8")
    out = td / "child-ledger.yaml"
    proc = subprocess.run(
        [sys.executable, str(SKILLS / "wr-adaptation/scripts/inherit_ledger.py"),
         "--parent-run", PARENT_RUN, "--parent-artifact", str(PARENT_ARTIFACT),
         "--parent-artifact-hash", LOCKED_HASH, "--child-draft", str(child),
         "--child-run", "2026-07-10-ben-adapt-fixture", "--out", str(out),
         "--new-claim", "coordinators field these questions every spring::low"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    check("SK-B5 inheritance run succeeds", proc.returncode == 0, proc.stderr)
    if proc.returncode == 0:
        child_ledger = yaml.safe_load(out.read_text(encoding="utf-8"))
        inh = [c for c in child_ledger["claims"]
               if any("inherited from" in h.get("note", "") for h in c["history"])]
        fresh = [c for c in child_ledger["claims"] if c["status"] == "unverified"
                 and c["id"].endswith("A")]
        check("SK-B5 exactly 2 claims inherited with history events", len(inh) == 2, str(len(inh)))
        check("SK-B5 inherited claims keep parent statuses",
              all(c["status"] in ("verified", "verified-with-qualification") for c in inh))
        check("SK-B5 1 fresh claim awaits FACT delta", len(fresh) == 1, str(len(fresh)))
    # tamper case: wrong parent hash must REFUSE
    proc2 = subprocess.run(
        [sys.executable, str(SKILLS / "wr-adaptation/scripts/inherit_ledger.py"),
         "--parent-run", PARENT_RUN, "--parent-artifact", str(PARENT_ARTIFACT),
         "--parent-artifact-hash", "0" * 64, "--child-draft", str(child),
         "--child-run", "x", "--out", str(td / "no.yaml")],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=ROOT)
    check("SK-B5 tampered parent hash REFUSED", proc2.returncode == 1 and "REFUSED" in proc2.stderr,
          proc2.stderr[:120])

# ---- SK-B12: calendar ----
GOOD_CAL = """# Q3 calendar (fixture)
| Week | Channel | Working title | Source |
|---|---|---|---|
| 1 | Reels | DROP exit: the one decision | assets/webinar-scripts/01 |
| 2 | LinkedIn | What coordinators ask about DROP | New |

## Compliance touchpoints
- Week 1 lands on tax content — careful hand at copy time.
"""
NO_SRC_CAL = GOOD_CAL.replace("| Source |", "| Notes |").replace("| assets/webinar-scripts/01 |", "| |").replace("| New |", "| |")
COPY_CAL = GOOD_CAL + "\nDisclosure: Educational content only. Benowitz Wealth Management is a brand of Joy Financial Group LLC.\n"

check("SK-B12 compliant calendar passes", not cal.check(GOOD_CAL), str(cal.check(GOOD_CAL)))
check("SK-B12 missing source column fails", any("source column" in f for f in cal.check(NO_SRC_CAL)))
check("SK-B12 disclosure-on-calendar fails", any("planning, not writing" in f for f in cal.check(COPY_CAL)))

print(f"\nSTEP-7 SKILLS: {'ALL GREEN' if not failures else 'FAILURES'} ({len(failures)})")
for f in failures:
    print(f"  - {f}")
sys.exit(1 if failures else 0)
