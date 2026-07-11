# Voice pass change log — drafts/drop-carousel-v1.md + drafts/caption.md -> voice/drop-carousel-v2.md + voice/caption-v2.md

Run 2026-07-10-ben-carous-001 · VOICE · SK-B9 · profile brand-voice.md@1.0.0 ·
register scored against VX-BEN-0001 (carousel plain-English definition target)
and VX-BEN-0002 (caption register target: checkable fact, implication without
fear). Per-claim accounting lives in voice/claim-diff.yaml.

## Changes

1. Carousel: ZERO slide-text edits. Every slide string is on_screen ledger
   text (CL-01..CL-16 cover all eight slides and the final disclosure line
   wall-to-wall) — any slide edit is a semantic-delta candidate by default,
   and none was needed: the slide copy is already the approved drop-001
   claim text placed at brand cadence.
2. Carousel title/provenance lines — "carousel v1" -> "carousel v2 (voice)"
   plus a revises-note appended to the provenance line — metadata marker
   lines, not on-image copy, outside differ and validator word-count scope.
3. Caption: one whitespace-only beat break — blank line inserted after
   "…The lump sum waits for your instruction." splitting the four-line body
   block into rule/fork couplet + tax-routes couplet. Read aloud, the fork ran
   straight into the tax cost; the parent voice pass (drop-001 changes 1-3)
   established pause-before-the-tax-claim as this asset's spoken cadence, and
   Instagram preserves line spacing. Sentence bytes untouched; differ sees no
   re-segmentation (0 hits).

## Deliberate non-changes

- Caption sentence text untouched end to end: every sentence in caption.md is
  ledger text (CL-17..CL-27). Cadence work was confined to whitespace.
- Slide 7's "Choose the rollover, and the timing becomes yours." (CL-13) and
  caption L4's "…the timing becomes yours." (CL-23) left exactly in place
  directly after the rollover mechanics — both carry the parent CL-11
  qualification (deferral-until-withdrawal, not unconditional control) whose
  placement condition depends on that adjacency. The caption beat break was
  placed BEFORE the cash/rollover couplet, keeping CL-23 in the same line
  block as its deferral-mechanics clause.
- Disclosure strings byte-identical and never smoothed: Slide-8 final line
  (CL-16: DISC-BEN-SHORT-01 + DISC-BEN-TAX-01 + profile pointer), caption
  tax referral (CL-26: DISC-BEN-TAX-01) and caption disclosure line (CL-27).
- Single CTA kept (webinar registration, per work order objective and brand
  one-CTA canon); no hashtags introduced (none defined in profile).
- caption-v2.md still carries no metadata header — the caption validator
  treats the first non-empty line as the hook (WRITE interventions #7);
  hook line stays "Your DROP payout arrives as a single check — and it comes
  with a decision attached." (16 words, under the 20-word fold rule).

## Verification on v2 outputs

- claim_diff.py drafts/drop-carousel-v1.md -> voice/drop-carousel-v2.md
  --json: `[]` — 0 hits.
- claim_diff.py drafts/caption.md -> voice/caption-v2.md --json: `[]` —
  0 hits.
- Tool-sight CONTROLS (a zero is verified, never assumed — drop-001 lesson;
  note the carousel's "**Slide N:**" lines do NOT start with the differ's
  marker characters, so slides are parsed): planted semantic changes
  ("twenty percent"->"thirty percent" in a scratch carousel copy; "that
  year's"->"next year's" in a scratch caption copy) each produce exactly
  1 hit. Both zeros are real.
- Byte-presence audit: all 27 literal ledger claim texts confirmed present in
  their file (CL-01..CL-16 in carousel-v2, CL-17..CL-27 in caption-v2;
  whitespace-normalized only for YAML-folded ledger entries). CL-28 is the
  FOUND implied comparative claim carried by the Slides 5-7 structure — that
  structure (slide order and fork framing) is unchanged.
- voice_fingerprint.py caption-v2 --project benowitz-wealth (deterministic
  half only, D-030): PASS — median 8.0w · p90 14w · grade 7.5 (bands: median
  target 11 / p90 max 22 / grade 6-9; short-of-median is doctrine). Judgment
  resemblance, separately: caption sits on VX-BEN-0002's register — checkable
  second-person facts, consequence stated without fear, one ask; not claimed
  as the deterministic score.
- social_format_check.py: carousel-v2 --format carousel PASS 0 findings
  (8 slides numbered, body slides one idea <=25 words, final slide carries
  CTA + disclosure); caption-v2 --format caption PASS 0 findings (hook under
  fold, disclosure present).
- compliance_lint.py --project benowitz-wealth: carousel-v2 0 findings;
  caption-v2 0 findings.

## Proposal candidates noticed (SK-A3, standing job)

- None new this pass.
