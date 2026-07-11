# Voice change log — run 2026-07-11-duc-nil-001 — nil-reel-v1.md → voice/nil-reel-v2.md

Pass: SK-B9 vo-voice-application (VOICE), first Ducat voice pass. Profile:
projects/ducat-private-wealth/brand-voice.md@1.0.0 (tone sliders ⚑ PROPOSED —
close slider calls noted for Wes rather than guessed hard; see
slider-calibration notes at the end). Exemplars read: VX-DUC-0001..0010 (no
rejected exemplars exist yet for this project). Cadence verified by
read-aloud pass, beat by beat.

The draft arrived unusually close to profile — short declaratives, hedge
discipline intact, no banned/avoided phrases, no sports-metaphor
contamination. A close draft earns a small edit set (north star: shrink
post-edit distance, not perform editing). Two edits.

## Edits

1. **BEAT THREE (CL-08) — fact-anchored softening per ledger rider**
   - Before: `Nobody withholds for you.`
   - After: `Usually nobody withholds for you.`
   - Rule: ledger CL-08 qualification + FACT finding F-3 — F-DUC-0004 scopes
     no-withholding to 1099 income, "the form behind *most* NIL payments";
     the universal stretched the evidence. One-word softener adopts FACT's
     suggested minimal fix, preserves DUC-C5 hedged-construction discipline
     and the profile's claim-scope honesty ("specific over general").
     Word choice "Usually" over "Generally": "generally" already carries
     CL-07 twenty seconds earlier — repeating it flattens the spoken track;
     "usually" is the plainer spoken register (see calibration note 1).
   - Delta duty: this is a claim-text edit → rides to FACT as fact_delta on
     CL-08 (see voice/claim-diff.yaml, 1 differ hit, mapped).

2. **TURN — throat-clearing opener cut**
   - Before: `So here's the real shift.`
   - After: `Here's the real shift.`
   - Rule: composed register / "fewer words, more weight" — the "So" is
     spoken-filler runway Ducat doesn't need; the exemplar set opens flat
     (VX-DUC-0005 "The test is simple."). Sentence carries no ledger claim
     (CL-12 begins at the next sentence, byte-untouched). Differ-clean:
     changed token is a stopword, no semantic hit.

## Considered and kept (cadence calls that stayed)

- `None of that is what this is.` (BEAT ONE, inside CL-02) — the
  demonstrative stack ("that … this") is a mild delivery risk aloud, but the
  line lands with weight on the right emphasis ("None of that — is what this
  is."). An edit would push CL-02 through fact_delta for a cadence-only
  gain; kept. Delivery note for the video machine: beat before "is what this
  is."
- `Here's the real shift.` — considered cutting "real" (fewer-words purism)
  and did not: the intensifier does contrast work against BEAT ONE's false
  framings, and cutting it is a content-word change that would ride to FACT
  for zero factual gain (calibration note 2).
- CTA pair (`One question… do you know exactly what you're selling?` +
  `Save this for the next deal.`) — reads as two asks; kept as-is because
  the work order mandates both (reflection CTA + save prompt) and the
  profile's reels pattern ("single ask, spoken") is satisfied by the single
  spoken question, with the save prompt as the mechanical close.
- Rhetorical-question budget: exactly one in the piece (the CTA, mandated).
  No pileup.

## Proofread

No spelling, agreement, or punctuation defects found. Em-dash and ellipsis
usage consistent. Timecode markers, [TO CAMERA] / [VO / B-ROLL] delivery
markers, and the production-notes block preserved byte-identical.

## Disclosure check (never smoothed)

`[TEXT ON SCREEN: "Educational only. Not advice. See profile for full
disclosures."]` — byte-identical to v1 and to DISC-DUC-SHORT-01
(disclosures.md@1.0.0). Untouched, as required.

## Duration / band re-verify (post-edit)

Spoken words: 190 (v1: 190 — net zero: +1 "Usually", −1 "So"). Work-order
band 170–200: PASS. At reel narration pace (~125–130 wpm) ≈ 88–91s against
the 90s format — timecodes remain valid; no re-timing needed.

## Deterministic fingerprint (voice_fingerprint.py, project ducat-private-wealth)

`{"median_sentence_length": 7, "p90": 14, "grade": 5.2, "violations": []}` —
**PASS.** p90 14 ≤ 18; grade 5.2 under ceiling (floor informational per the
script — fragments are doctrine); zero banned openings, zero avoided
phrases. Judgment half (resemblance to VX-DUC-0001..0010) scored separately
and NOT reported as the deterministic result (D-030): the piece sits in the
exemplars' register — flat declaratives, unglamorous specifics (compliance
office, withholding, contract underneath), no performed enthusiasm; closest
kin VX-DUC-0002 (1099-vs-paycheck teaching by compression).

## Slider-calibration notes for Wes (sliders are ⚑ PROPOSED)

1. **CL-08 softener register:** chose "Usually" (plain, spoken) over
   "Generally" (more formal, already used at CL-07). At formality 3 "usually"
   wins; at formality 4 "generally" would. Calibrate.
2. **Intensifiers under fewer-words-more-weight:** kept "real" in "Here's the
   real shift." Strict fewer-words would cut it; directness 5 supports the
   contrast word. Decide whether intensifiers must earn a stronger case.
3. **Warmth ceiling:** the STAKES aside "— and the parent reading over their
   shoulder" reads warmth ~3 against the proposed 2. Kept — the pre-money
   audience includes parents. If warmth 2 is strict, the trim is "This is
   for the athlete who just signed."
4. **Directness of the CTA question:** "do you know exactly what you're
   selling?" is a direct challenge to camera; kept at directness 5. The
   softer alternative register is "Ask yourself what you're actually
   selling." Calibrate which Ducat asks.
5. **Sentence-median target:** piece runs median 7 vs proposed target 9. The
   fingerprint treats the floor as informational and the exemplars support
   the shorter cadence — confirm median 9 is ceiling-shaped guidance, not a
   real target to write up to.

## Standing job (SK-A3 rule candidates)

None yet — first Ducat pass, single specimen; "So-opener gets cut" is a
one-sample observation, not a proposal (no single-sample conclusions).
Watch for recurrence.
