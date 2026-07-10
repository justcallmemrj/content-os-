---
name: vo-voice-application
description: "Apply the active project's full voice profile to a structurally-approved draft: register, cadence-aloud, phrase discipline. Emits the clean version + change log + claim diff (SK-B2 delta duty). Also owns spoken-word editing and proofreading. Pinned at the voice_edit stage."
skill_id: SK-B9
version: 1.0.0
tier: B
owner: wes
approval_status: draft
supported_agents: [VOICE]
required_inputs: [draft_path, "brand-voice.md (full)", claim_list]
optional_inputs: [voice_exemplars, prior_edit_pairs]
prerequisites: ["fact_check passed (T7) — voice never precedes verification"]
requires: [SK-B2, SK-A2]
reads: ["projects/<active>/brand-voice.md (full)", "projects/<active>/voice/exemplars/", "projects/<active>/voice/edits/"]
schemas: [claim-ledger]
evaluation_rubric: RUB-VOICE-1
---

# vo-voice-application (SK-B9)

## Process

1. Read the profile AND the exemplars — including the rejected ones; "not
   this" is half the fingerprint.
2. Edit for register and cadence: read it aloud; if you run out of breath,
   cut. Fragments are fine. Short sentences. The banned/avoided lists are
   hard, not stylistic suggestions.
3. Run `scripts/voice_fingerprint.py` — the deterministic half (lengths,
   openings, phrases, readability). Resemblance-to-exemplars is the judgment
   half; never report the first as the second (D-030).
4. Emit: clean version + change log (every edit, one line) + **claim diff**
   via SK-B2 delta duty. Every diff hit maps to a CL-id; suppressing a hit is
   prohibited — cosmetic-vs-semantic is FACT's call.
5. Rule candidates you notice ("this phrase keeps getting cut") become
   proposals via SK-A3 (`voice-phrase`, `edit-pair`) — the standing job.

## Prohibited behavior

Changing factual content, qualifications, or disclosure text (a voice edit
that touches a claim goes through the delta, and disclosure wording is never
"smoothed"); adding claims; suppressing diff hits; imposing another brand's
cadence (composed-Ducat weight in a Benowitz colleague-voice piece is
contamination, not style range).

## Tests

`scripts/test_skills.py`: clean fixture passes fingerprint; fixture with
"unlock your financial journey" + banned opening fails with named violations;
delta-emission duty covered by SK-B2's delta fixture.
