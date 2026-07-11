# RUB-VIDEO-1 — video judgment-QC rubric, video machine V8 (PROTECTED)

Authored at step 8 from the ratified Phase 6 §5 registry line ("§17.4: script
alignment(R, byte-match), story clarity, pacing, visual quality, brand
consistency, caption accuracy(R)+placement judgment, audio quality(R
thresholds + judgment), motion quality, technical correctness(R), platform
specs(R), rendering integrity(R), accessibility") following the RUB-SCRIPT-1
pattern. QA scores; VDIR provides judgment input (Phase 5 §5 V8).
⚑ RATIFICATION RIDES ON THE STEP-8 PR — flagged for Wes.

## Required criteria (pass/fail, blocking — validator-fed at V7, read here)

- **R1 Script alignment** — text_verbatim_check 100% byte-match against the
  storyboard's ID-mapped strings.
- **R2 Caption accuracy** — caption_check clean (CPS/line/timing) AND caption
  text verbatim from script segments.
- **R3 Audio thresholds** — loudness/clipping validators within spec. Where a
  piece HAS no audio track, the absence must be a declared work-order
  condition, never an unnoticed defect (the check is then recorded N/A-by-
  design with the pointer).
- **R4 Technical correctness** — no blank frames; no decode errors; duration
  within tolerance.
- **R5 Platform specs** — resolution/fps/AR match the export spec.
- **R6 Rendering integrity** — output hash matches the manifest; manifest
  schema-valid at the ratified engine pin.
- **R7 Safe areas & disclosure** — safe_area_check clean; disclosure block
  persistent for its declared range and inside the safe area.

## Scored dimensions (1–5; anchors at 1/3/5)

**Story clarity** · 5: the argument lands with the sound off (text cards +
captions carry it) and with the sound on (delivery order builds) · 3: clear
with audio, muddier muted · 1: scenes in sequence, story absent.

**Pacing** · 5: holds match reading load; the hook window earns the first
seconds; pattern interrupts land where attention sags · 3: even, competent,
slightly flat or slightly rushed in one stretch · 1: crammed to duration or
dead air.

**Visual quality** · 5: type, spacing, and composition read as designed —
nothing accidental on screen · 3: clean but generic · 1: misaligned,
crowded, or accidental-looking frames.

**Brand consistency** · 5: tokens applied everywhere; the piece sits beside
the approved back catalog without a seam · 3: on-palette with drift in
weight/spacing · 1: off-brand color/type, or generic-visual drift that
distorts the message.

**Caption placement judgment** · 5: never occludes disclosure or UI; rhythm
matches delivery; emphasis styling clarifies, never editorializes · 3:
correct placement, mechanical rhythm · 1: captions fight the frame or the
disclosure block.

**Audio quality (judgment half)** · 5: levels sit right against the mix;
transitions are clean; silence is deliberate · 3: within thresholds, rough
edges · 1: within thresholds but distracting (pumping, abrupt cuts) —
thresholds are R3; the ear is scored here.

**Motion quality** · 5: motion serves reading order and emphasis; nothing
moves without a reason; seek-safe and deterministic on re-render · 3:
tasteful defaults · 1: readability sacrificed to spectacle.

**Accessibility** · 5: contrast ≥4.5:1 verified against real backdrops; no
color-only information; captions complete; disclosure readable at device
size · 3: passes contrast, minor color-only accents · 1: fails any of these
in a way a viewer would hit.

## Scorecard

`schemas/scorecard.schema.json` instance; composite /10; required failures
block regardless of composite (the D-030 discipline: judgment is never
averaged over a failed fact).
