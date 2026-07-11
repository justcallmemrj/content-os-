# Delivery package — 2026-07-10-ben-dropvid-001 (V9 → H5)

First video-machine run: HyperFrames production of the H2-approved DROP-exit
reel script (parent 2026-07-10-ben-drop-001, locked
`8ec534b3c7ef61d4e26d9c75525bdf4ef9f6b4fd8b6da901c5a6b5a3bc1aafd0`,
edit distance 0). Engine binding: SK-C1 at pin `6152437d` / v0.7.49 (D-036).
Local render only (D-070). **Awaiting H5 — Wes's sign-off. Wes publishes (E6).**

## The render

- `video/hyperframes/benowitz-wealth/drop-reel/renders/v1/drop-reel.mp4`
  — 1080x1920, 30fps, 90.000s, 2700 frames, h264, 4,351,500 bytes,
  sha256 `e26f4e39f13a80a5e6aad4fee60ae57dae44a26ea60f68107f55a199e98b0493`
- Manifest: `renders/v1/manifest.yaml` (`HF-2026-0710-01`, schema-valid)
- Preview (VDIR-reviewed at V5): `previews/preview-v1.mp4`
- Thumbnail/cover: not requested in the work order.

## QC results

- V7 deterministic battery (all green): **text byte-match 29/29 = 100%**
  (the step-8 exit criterion); safe-area 0 violations; captions 28 segments
  clean (CPS/line/timing); spec-exact probe; 0 blank runs; full-decode clean;
  hash chain output+composition == manifest; audio: zero streams —
  **silent-by-design, declared** (no VO exists; TTS off).
- V8 judgment (RUB-VIDEO-1): required **7/7**, composite **8.3/10, PASS**.
  Dimensions: story 5 · pacing 4 · visual 4 · brand 3 · caption placement 4 ·
  audio judgment 5 · motion 4 · accessibility 4. Full reasoning:
  `qa/qa-notes.md`; scorecard: `qa/scorecard.yaml`.

## What H5 decides (the flags, complete set)

1. **Placeholder reality** — no presenter footage exists; to-camera blocks are
   an intentional typographic treatment (VDIR brief). Sign-off = accepting a
   caption-led piece, or direct a reshoot path when footage exists.
2. **Silent render** — no VO/BGM by declared design. If audio is ever added,
   R3 goes live and the run re-enters at build.
3. **Derived brand tokens** (⚑ not ratified) — palette/type derived from the
   approved benowitz-drop-exit webinar kit; ratification = P-2026-0710-005.
4. **System-font fallbacks** — brand faces (Cormorant/Manrope) not installed;
   installing is a dependency proposal; render then re-versions to v2.
5. **No wordmark anywhere** (SC-07 escalation, adjudicated) — no text_id class
   maps a brand string; a BRAND-* id class is a schema/wrapper proposal.
6. **Caption L-cut flow** across scene cuts (max ~5.6s offset) — resolves a
   CPS impossibility with zero text changes; strictly scene-locked captions
   would require re-timed markers = D5 re-entry at fact_check.
7. **Disclosure**: DISC-BEN-FRS-01 short-format on-screen 5.0–90.0s (scrim,
   8.5–14:1); the standing publish rider (full disclosure in profile) applies.
8. Polish notes for any rebuild: SC-03 envelope drift start ≥16.2s; final ~3s
   CTA-ask persistence (QA observation 4).

## Gate history

9 transitions V1–V9 (SQLite `state/workflow.sqlite`), 7 schema-valid
envelopes (`handoffs/01–07.yaml`), every gate result recorded. Escalations:
1 (SC-07 wordmark, HYPF → VDIR adjudicated, logged). Untested surfaces,
honestly: platform ingest/device playback; full-speed motion feel (static
frames only — H5's human viewing is the check).
