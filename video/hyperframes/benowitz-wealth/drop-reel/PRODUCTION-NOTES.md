# drop-reel — production notes

## STORYBOARD
- source: runs/2026-07-10-ben-dropvid-001/storyboard/storyboard.yaml (sha256 0ad0d26d2331e56a…)
- script: parent run 2026-07-10-ben-drop-001, locked hash 8ec534b3c7ef61d4e26d9c75525bdf4ef9f6b4fd8b6da901c5a6b5a3bc1aafd0
  (drop-reel-v3.md — script text immutable, D5; storyboard `script_ref.sha256` carries the lock)
- scenes: 7; duration 90.0s; platform instagram-reels 9:16 1080x1920 30fps, silent by work order (no VO, DEM-05 GAP)
- caption track: 28 segments (captions.yaml), flows continuously across scene cuts per the recorded PACING FLAG
  (HOOK to 8.2s, STAKES to 20.3s, TURN from 69.7s, CTA from 79.4s); scene backgrounds cut on the marker grid
  (0/5/15/35/55/75/85s) — built as independent tracks (backgrounds track 1, captions track 2, disclosure track 3)

## DESIGN
- tokens: tokens.css @ sha256 319f905bd0b413b2… (⚑ DERIVED from the benowitz-drop-exit webinar kit, NOT ratified —
  wrapper-rules §4; proposal rides the step-8 PR; consumed only as CSS custom properties)
- fonts: brand faces (Cormorant / Manrope / JetBrains Mono) are NOT installed on this machine and external font
  fetching at render is banned (determinism). Stacks resolve to documented local fallbacks: display serif →
  Palatino Linotype/Georgia; UI sans → Segoe UI; mono unused. Same stacks pick up the brand faces with no markup
  change if they are ever installed locally. Surfaces at H5 with the other placeholder conditions.
- safe areas: 9:16 row of wrapper-rules §2 — `--safe-top: 220px; --safe-bottom: 320px; --safe-x: 64px` (exact);
  every text element inside an `hf-safe` container (checker-enforced)
- disclosure block: DISC-BEN-FRS-01, persistent 5.0s → 90.0s (scenes SC-02 through SC-07), pinned at the bottom of
  hf-safe (above the 320px bottom margin), 27px Manrope on the ink scrim token (measured contrast 8.5–14:1 across
  all backdrops), two stacked lines per the visual brief (whitespace-only wrap, canon-safe). NOTE: the brief's
  "--muted-toned on navy scenes" reading fails its own ≥4.5:1 floor (muted-on-navy ≈ 2.9:1); the scrim + cream
  treatment satisfies the hard rule — see BUILD-NOTE deviations.
- type scale: sentence cards Cormorant-stack 46px/1.3 cream (ink on paper scenes); roll-call CAP-04 Manrope 600
  caps 40px; full-frame beats (CAP-06/24/25) 84px/600; CTA rider CAP-28 Manrope 400 33px ink (distinct register
  from the serif ask, above the disclosure band); accents: gold hairline underline on "as a single check."
  (CAP-01), deep-gold color-only accent on "runway." (CAP-25 — deep gold for ≥3:1 large-text contrast on paper)
- caption motion: enter 150ms fade/rise (8px), exit 100ms fade, one segment on screen at a time, no per-word
  effects; captions that cross the 75s navy→paper inversion swap to ink at the cut (timeline `set`)

## BUILD
- architecture: MONOLITHIC single index.html (deliberate): the text-verbatim checker parses static HTML and skips
  `<template>` contents, so sub-composition scenes would hide caption text from the verbatim gate; the L-cut
  caption structure also wants captions and backgrounds as sibling tracks in one timeline. Upstream lint's two
  "split into sub-compositions" advisory warnings are accepted on these grounds (documented, not suppressed).
- sub-compositions: none (see above)
- upstream patterns used: hyperframes-core minimal-composition (standalone root, sized box, single paused GSAP
  timeline at `window.__timelines["drop-reel"]`), tracks-and-clips (track 1 scenes / track 2 captions / track 3
  disclosure; boundary-touching sequential clips), determinism-rules (finite repeat pulse — `repeat: 12`, no
  clocks/random/network; GSAP 3.14.2 via the skeleton's pinned CDN URL), animation: svg-path-draw (route line
  stroke-dashoffset), fromTo-at-clip-start for all later-scene state (no load-time `gsap.set`)
- text injection: scripts/inject_text.py reads storyboard.yaml (canonical strings) + captions.yaml (timings),
  cross-checks them (canon mismatch aborts = escalation), and regenerates the caption/disclosure DOM plus the
  timing JSON between `HF-INJECT` sentinels in index.html. Storyboard `\n` line breaks render via
  `white-space: pre-line` (no `<br>`). Accent spans wrap exact slices of the original string (bytes preserved).
  Every text element carries `data-text-id` and sits inside `hf-safe`. Never edit between sentinels — rerun the script.
- variables: none declared (single-variant piece); re-versioning = storyboard/caption YAML change + rerun
  inject_text.py + relint/preview
- scene treatments:
  - SC-01 HOOK (0–5): navy field, paper-grain vignette, upper-zone serif cards, gold underline accent
  - SC-02 STAKES (5–15): dark navy, 300ms gold-rule vertical wipe in at 5.0s; roll-call stack; exit gold rule
    (748px) fades in 14.6s as the match-cut seed
  - SC-03 BEAT ONE (15–35): gold line-work envelope (top edge aligns with SC-02's rule) drifts down 15.4–17.0s,
    lands on the paper-tone table plane with a small settle; pension = gold pulse line (left, finite 13-cycle
    pulse 18.0–33.6s), lump sum = still navy-soft square with gold border (right); captions upper-low zone
  - SC-04 BEAT TWO (35–55): five blocks (cream/warm alternating, gold top) stack bottom-up 38.6–46.1s between the
    caption zone and the disclosure band; gold top block shears away (x/rotation/fade) 46.8–49.0s on CAP-16
  - SC-05 BEAT THREE (55–75): two navy-soft vessels, one unbroken gold line draws trustee-to-trustee 58.2–64.2s,
    still gold point lands 64.2s; line calms to 35% opacity from 73.5s under the TURN captions
  - SC-06 TURN (75–85): the single inversion — paper field, navy ink type, deadline/runway full-frame beats
  - SC-07 CTA (85–90): warm paper end-card, deep-gold hairline; CTA ask + quieter tax-professional rider +
    disclosure band; **no wordmark rendered** (un-mapped text — escalated, see BUILD-NOTE)

## RENDERS
- previews/preview-v1.mp4: 2026-07-10 · 270x480 30fps 90.000s h264 (draft-quality 1080x1920 render via
  `npx hyperframes@0.7.49 render --quality draft`, lanczos-downscaled to 270x480 with the local FFmpeg — the
  pinned CLI has no sub-native output size; `--resolution` only supersamples) · sha256 d6469a4eb2498d6a… ·
  V5 review artifact for VDIR · decode-verified (2700/2700 frames)
- renders/v1/drop-reel.mp4: 2026-07-10 · manifest HF-2026-0710-01 (renders/v1/manifest.yaml, schema-valid) ·
  V6 final local render after VDIR's V5 verdict RENDER (7/7 scenes pass; wordmark escalation adjudicated:
  end-card accepted as-is for v1, no wordmark, flagged to H5) · `npx hyperframes@0.7.49 render --quality high`
  from the composition byte-identical to V5's reviewed state · 1080x1920 30fps h264, duration 90.000s,
  2700 frames, full-decode verified (0 errors), 4,351,500 bytes,
  sha256 e26f4e39f13a80a5e6aad4fee60ae57dae44a26ea60f68107f55a199e98b0493 · KEPT (v1; any re-render is v2+,
  never an overwrite) · not final-marked by HYPF — H5 render sign-off owns that verdict

## DEVIATIONS
- see BUILD-NOTE.md (wordmark omission escalated to VDIR; disclosure tone choice inside the brief's own
  contrast floor; all else zero)

## REUSE CANDIDATES
- the caption-injection pattern (inject_text.py: YAML → sentinel-bounded DOM + timing JSON, canon cross-check) —
  generalizes to every future caption-led piece; proposal to lift into a shared script once a second piece needs it
- hf-safe zone system (zone-upper / zone-upperlow / zone-center / zone-lower + disclosure band) as the standing
  9:16 caption stage
- disclosure-band component (scrim token, 27px, bottom-of-safe pinning) — every BEN reel will need it verbatim
