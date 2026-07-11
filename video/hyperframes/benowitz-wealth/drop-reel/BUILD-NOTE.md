# BUILD-NOTE — drop-reel V4+V6 (2026-07-10, HYPF)

Run: 2026-07-10-ben-dropvid-001 · engine: hyperframes 0.7.49 pinned (`npx hyperframes@0.7.49`, D-036) ·
scope: video/hyperframes/benowitz-wealth/drop-reel/ · stages: V4 (implement + lint + preview) then V6 (final
local render) after VDIR's V5 verdict RENDER (7/7 scenes pass, zero deviations; wordmark escalation adjudicated:
end-card accepted as-is for v1, no wordmark added, flagged to H5).

## V6 — final render (renders-locally-verified)
- Command: `npx hyperframes@0.7.49 render --quality high --output renders/v1/drop-reel.mp4` (local only, D-070;
  cwd = the piece dir). index.html / tokens.css / scripts untouched since V5's reviewed state — the rendered
  composition is byte-identical to what VDIR previewed.
- Verified locally: ffprobe 1080x1920, 30/1 fps, duration 90.000000s, h264, nb_frames 2700; full decode pass
  (`ffmpeg -f null`) with 0 errors; size 4,351,500 bytes;
  sha256 e26f4e39f13a80a5e6aad4fee60ae57dae44a26ea60f68107f55a199e98b0493.
- Manifest: HF-2026-0710-01 at renders/v1/manifest.yaml (render_manifest.py exit 0; schema_validate.py OK
  [render-manifest], exit 0). Preset reels-local-v1.
- Untested/unclaimed: playback on target devices/platform ingest (Instagram transcode) — not exercised here;
  H5 render sign-off owns the final verdict. HYPF does not final-mark.

## Implemented and tested
- 90.0s monolithic composition (index.html + tokens.css), 1080x1920@30, silent by work order; 7 scene clips
  (track 1) cutting on the marker grid, 28 caption clips (track 2) on captions.yaml timing, persistent disclosure
  clip (track 3, 5.0→90.0s). Single paused GSAP timeline, deterministic (finite repeats, no clocks/random/network
  state; fonts local-only).
- Text injection: scripts/inject_text.py — all 29 strings copied programmatically from storyboard.yaml (timings
  from captions.yaml, canon cross-check between the two YAMLs aborts on mismatch). Verified:
  `text_verbatim_check.py` → **29/29 IDs byte-match, 0 violations, exit 0**;
  `safe_area_check.py --ar 9:16` → **0 violations, exit 0**.
- Pinned-CLI gates: `lint` → 0 errors (3 advisory warnings, below); `validate` → 0 console errors, **0 WCAG
  contrast failures** (disclosure band measured 8.5–14:1 across backdrops); `inspect` → 0 errors, 1 warning
  (below). Snapshot QC at 9 timestamps eyeballed against the brief; two layout collisions found and fixed
  (SC-03 split visuals and SC-04 stack originally intruded on the disclosure band's region — repositioned; and
  the SC-05 arrival dot was rebuilt as an HTML element after GSAP's SVG scale transform relocated it to the
  canvas origin).
- Preview artifact: previews/preview-v1.mp4 — 270x480, 30fps, duration **90.000s** (ffprobe), h264, decode-
  verified all 2700 frames. Produced by pinned-CLI draft render at native 1080x1920 then FFmpeg lanczos downscale
  (the 0.7.49 CLI has no sub-native render size; `--resolution` only supersamples). Cloud render not used (D-070).

## Implemented, untested beyond gates
- Motion feel at full speed (settle bounce weight, pulse cadence, shear pacing) is verified only via static
  snapshots and the low-res preview — that is exactly what V5 review is for.

## Not implemented
- Audio: none, by work order (DEM-05 GAP, external TTS OFF).
- ~~Final render + render manifest (V6 scope)~~ — DONE at V6, see the "V6 — final render" section above.
- `hyperframes feedback` telemetry: skipped — external transmission is not part of SK-C1's loop and our posture
  keeps non-essential external calls off.

## Lint/doctor exceptions (documented, not suppressed)
1. `composition_file_too_large` + 2x `timeline_track_too_dense` (warnings): upstream advises splitting into
   sub-compositions. Rejected deliberately: the text-verbatim checker skips `<template>` contents, so caption
   text inside sub-compositions would be invisible to the D-016 gate; the 28-segment caption track density is the
   storyboard's own design (L-cut captions over scene cuts). Monolithic is the compliant architecture here.
2. `inspect` `content_overlap` at t=15 (warning): CAP-05 and CAP-06 clips share the boundary instant (clip
   windows are end-inclusive). At t=15.0 the outgoing card has completed its 100ms fade (opacity 0) and the
   incoming card starts at opacity 0 — inspect measures rects, not opacity. No readable-frame overlap exists.
   Not silenced with data-layout attributes so future edits keep real-overlap protection.
3. `doctor` ok=false: components are (a) "0.7.51 available" — the pin working as intended (D-036, never
   upgraded), (b) whisper/Kokoro/MusicGen — optional media providers, OFF by policy and unneeded for a silent
   piece, (c) Docker — not required for local render. Node/FFmpeg/FFprobe/Chrome all pass.

## Deviations / escalations
1. **ESCALATION to VDIR — SC-07 wordmark not rendered.** The storyboard direction and visual brief call for a
   "Benowitz wordmark treatment... typography only," but no `text_id` maps any wordmark string, and wrapper-rules
   §1 (enforced by text_verbatim_check.py) forbids any visible text outside a declared `data-text-id`. Rendering
   the name — or disguising it as SVG paths — would violate or game the gate. Built the end-card with the brand
   hairline motif and no wordmark. Resolution options for VDIR: add an ID-mapped wordmark string to the
   storyboard (re-enters governance normally), or accept the typographic end-card as-is.
2. **Disclosure tone (recorded, not escalated):** the brief says "--muted-toned on navy scenes" AND "contrast
   ≥ 4.5:1"; muted-on-navy measures ≈2.9:1, so the two clauses conflict. Chose the brief's own scrim-token
   option with cream text (8.5–14:1 measured, `validate`-clean). VDIR judges the tone at V5.
3. Zero text or timing deviations: 29/29 byte-match; caption windows are captions.yaml's to the millisecond;
   scene cuts on the storyboard markers.

## Flags already riding to H5 (restated from run docs)
Placeholder-slate treatment (DEM-01 unfilmed), silent render (DEM-05), derived-not-ratified brand tokens
(wrapper-rules §4), brand fonts falling back to system faces (Palatino Linotype/Georgia + Segoe UI — install
Cormorant/Manrope locally or ratify a vendored-font proposal before final if fidelity matters).

## Reuse candidates
inject_text.py pattern, the hf-safe zone system, and the disclosure-band component (details in
PRODUCTION-NOTES.md).
