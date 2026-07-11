# Voice pass change log — drafts/drop-linkedin-v1.md -> voice/drop-linkedin-v2.md

Run 2026-07-10-ben-dropli-001 · VOICE · SK-B9 · profile brand-voice.md@1.0.0
(linkedin platform_overrides applied: written to the professional beside the
client) · register scored against VX-BEN-0001's LinkedIn variant and
VX-BEN-0003. Per-claim accounting lives in voice/claim-diff.yaml.

## Changes

1. DECISION open — "So here is the decision, stated plainly." -> "Here's the
   decision, stated plainly." — drops the throat-clearing "So" and takes the
   brand's contracted "Here's" opener (VX-BEN-0002 "Here's a big one",
   VX-BEN-0003 "Here's the part that matters for accuracy"); non-claim
   sentence; differ classifies the change cosmetic (0 hits).
2. DECISION paragraph split (whitespace only) — the nine-sentence decision
   block now breaks after "It waits for your instruction.": fork setup
   (rule / pension / lump sum) in one paragraph, the two routes (cash tax +
   withholding / rollover mechanics) in the next — LinkedIn scan cadence and
   a breath point between the fork and its consequences; sentence bytes
   untouched, differ sees no re-segmentation.
3. Header line — "draft v1" -> "voice v2" (metadata, not post copy).

## Deliberate non-changes

- All 10 inherited byte-identical sentences (parent CL-04, CL-05, CL-06,
  CL-07, CL-08, CL-09, CL-10, CL-12, CL-13, CL-14 texts) untouched — editing
  any of them breaks inheritance and re-enters fact_check. No cadence edit was
  needed on any of them; WRITE's placement already reads aloud cleanly.
- Fresh claim sentences CL-20, CL-21, CL-22 (hook scene, parking-lot triptych,
  "It's you.") untouched — they are the register high point of the piece and
  they are ledger text; zero-edit was both the safe and the right call.
- CL-27 carrier CTA sentence ("If you work beside teachers, deputies,
  firefighters, or state staff who are close to their DROP date, forward this
  to them.") untouched — the relative clause "who are close to their DROP
  date" is the verified eligibility scoping (F-BEN-0005); any smoothing risks
  widening the address to Investment Plan members.
- Disclosure block byte-identical: DISC-BEN-SHORT-01 three sentences (CL-25),
  first-comment placement sentence (CL-26), DISC-BEN-TAX-01 final line.
  Disclosure wording is never smoothed.
- "That's the difference between a deadline and runway." kept — one concrete
  image doing real planning work, consistent with exemplar range ("quietly
  erodes buying power"); not Ducat weight.
- Dual ask (forward + weigh-in) kept — it is the profile's LinkedIn
  cta_pattern verbatim ("forward this / weigh in — never book-a-call"), not a
  CTA pileup.
- The profile transition "Here's the part nobody mentions:" NOT introduced —
  the parent run adjudicated that secrecy frame misleading (drop-001 CL-19)
  and WRITE deliberately avoided it here (interventions.md #5); voice honors
  the standing adjudication.

## Verification on v2

- claim_diff.py v1 -> v2 --json: `[]` — 0 semantic-delta candidates.
  Tool-sight CONTROL run (this format is plain prose, but per the drop-001
  tool-blindness lesson the zero was verified, not assumed): a scratch copy of
  v2 with "twenty percent" -> "thirty percent" produces exactly 1 hit, so the
  differ demonstrably sees every sentence of this file. The zero is real.
- Byte-presence audit: all 17 literal ledger claim texts (CL-04..CL-14
  inherited, CL-20..CL-26 fresh) confirmed present in v2 (whitespace-
  normalized only for the YAML-folded multi-line entries); CL-27's implied
  carrier sentence byte-identical.
- voice_fingerprint.py --project benowitz-wealth (deterministic half only,
  D-030): PASS — median 9w · p90 18w · grade 7.0 (bands: median target 11 /
  p90 max 22 / grade 6-9; no banned openings, no avoided phrases). Judgment
  resemblance is the separate half: register sits on VX-BEN-0001's LinkedIn
  variant (professional register, same facts, closes on the decision that
  matters) with VX-BEN-0003's accuracy-as-voice posture; second person
  throughout, addressed to the coordinator/rep/HR/CPA per platform override.
  Not claimed as the deterministic score.
- social_format_check.py --format linkedin: PASS, 0 findings (279
  validator-counted words in the 150-300 band; first-comment statement
  present; no link-in-bio; no staccato one-liners).

## Proposal candidates noticed (SK-A3, standing job)

- None new this pass. (The claim_diff inline-marker fix is already queued from
  drop-001; it did not affect this plain-prose format.)
