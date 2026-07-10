---
name: wr-script-production
description: "Turn a request or brief plus a source packet into a structured, claim-declared, duration-true spoken script in the active project's register — structure and educational value first (final voice belongs to vo-voice-application). Pinned at brief and draft stages of the script workflow; use for any video script, webinar segment, or podcast segment request."
skill_id: SK-B3
version: 1.0.0
tier: B
owner: wes
approval_status: draft            # activates with the vertical slice
supported_agents: [WRITE]
required_inputs: ["work order (platform, duration target, objective, audience)", "source packet or attached source asset", "context packet (brand-voice register fields, audience.md, disclosures via SK-B15)"]
optional_inputs: [approved_exemplars, hook_direction_notes, prior_versions]
prerequisites: ["SK-A1 loaded exactly one project", "SK-B2 available in declare mode"]
requires: [SK-B2, SK-A2, SK-B15]
reads: ["projects/<active>/brand-voice.md (register fields only)", "projects/<active>/audience.md", "projects/<active>/examples/"]
schemas: [work-order, claim-ledger]
evaluation_rubric: RUB-SCRIPT-1
---

# wr-script-production (SK-B3)

## Process

1. Confirm or create the brief (`references/brief-template.md`).
2. Map packet claims to beats: a beat with no claim is texture; a claim with
   no beat is **cut, not crammed**.
3. Draft to the 7-beat skeleton (`references/structures.md`) in the profile's
   register — sentence-length band honored, banned openings honored — while
   declaring every claim via SK-B2 declare mode.
4. Prefer structural claims over volatile numerics ("a rollover isn't
   automatic" > "the 2026 limit is $X"); soften genuinely complex rules
   ("may owe," "the rules differ") rather than flat-asserting.
5. Place delivery markers on every block (`references/delivery-markers.md`):
   `[TO CAMERA]` for claims and authority, `[VO / B-ROLL:]` for texture,
   `[TEXT ON SCREEN:]` for anything read exactly. Route disclosure text to a
   persistent on-screen block via SK-B15 — never the spoken track.
6. Run `scripts/duration_check.py` and `scripts/structure_check.py`; trim
   beats rather than pace to fix overruns (`references/duration.md`).
7. Emit: draft + claim list + hook batch (ten, ≥3 mechanisms,
   `references/hooks.md`) + intervention notes — uncapped, one line each; a
   truncated note list means an approval of a change nobody saw (D-008).

## Prohibited behavior

- Facts from model memory presented as sourced — WRITE has no web tool, so
  there is nothing to launder them through (D-015); unpacketed claims are
  `[UNVERIFIED]`, visibly.
- Testimonials, guarantees, performance promises — even on explicit request:
  draft the nearest compliant alternative + intervention note.
- Two CTAs. Blending brands. Reconstructing a named source's numbers from
  memory. Spoken disclaimers that cost the viewer.

## Error handling

- No packet and named source absent → **draft anyway** from topic, everything
  `[UNVERIFIED]`, ⚠️ header on top (a blocking question costs a round trip the
  flag already covers — D-008).
- Duration unreachable without cutting a required disclosure → escalate;
  never shrink the disclosure.
- Brief conflicts with compliance at concept level → refuse the concept,
  draft the nearest compliant alternative, intervention note. (The "could
  save teachers thousands" request is the canonical case — the slice's
  injected failure.)

## Tests

`tests/test_sk_b3.py` — property: fixture brief+packet draft in word band
170–200, 7 beats, 1 CTA, ≥10 hooks/≥3 mechanisms, claim coverage 100%, zero
banned openings; counterexamples: testimonial request (wrong path fails the
compliance lint, right path carries the refusal note), missing-source (⚠
header path), cross-brand packet (Ducat vocabulary in a Benowitz draft →
lexicon scan flags, never blends); regression: the ratified slice output
becomes golden fixture #1.
