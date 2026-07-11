# Visual brief — DROP-exit reel (2026-07-10-ben-dropvid-001)

For the HyperFrames builder (HYPF). This brief directs; the storyboard binds.
Every visible string comes from `storyboard.yaml` via `data-text-id` — 28
caption segments (CAP-01…CAP-28, timing in `captions.yaml`) plus the
persistent disclosure (DISC-BEN-FRS-01). **No other text may appear anywhere
in the frame** (wrapper-rules §1; `text_verbatim_check.py` will fail the build
otherwise). Silent render — no audio track by work order; the type IS the
delivery, so treat every caption as the hero element, not a subtitle.

## Ground rules

- Canvas 1080x1920, 30fps, 90.0s. Safe areas per wrapper-rules §2 for 9:16:
  `--safe-top: 220px; --safe-bottom: 320px; --safe-x: 64px` — exact values,
  every text element inside `hf-safe`.
- Brand tokens (wrapper-rules §4, ⚑ DERIVED not ratified — consume ONLY via
  `tokens.css` custom properties, never hard-coded):
  - Navy `#0E2A47` / dark `#081A2D` / soft `#1B3A5F` / ink `#0B1E33`
  - Gold `#C8A35C` / soft `#DDC18A` / deep `#A78443`
  - Paper `#FBF7EE` / warm `#F7F1E6` / cream `#F1E9D7` / muted `#7A6E55`
  - Cormorant (display serif) · Manrope (UI sans) · JetBrains Mono (numeric —
    unused in this piece: there are no on-screen numerals)
- Caption contrast >= 4.5:1 against its real backdrop; scrim token if the
  backdrop is busy. Motion on caption text stays subtle — readability beats
  spectacle (SK-C3).

## Placeholder-slate doctrine (honest, but designed)

Nothing is filmed (DEM-01) and there is no VO (DEM-05). The work order accepts
placeholders, and both conditions surface at H5. Do NOT fake footage, stock
people, or a synthetic presenter. Instead the to-camera blocks become an
intentional editorial-typography piece: full-bleed navy/paper fields,
oversized Cormorant caption cards, one gold accent per beat. The result must
stand alone as a finished-looking typographic reel — "placeholder" describes
its governance status, not its craft. If footage is later filmed, the caption
system survives as the lower-register layer over video.

## Caption system (all scenes)

- One segment on screen at a time, center-stage; Cormorant for sentence
  cards, Manrope 600 for the roll-call address (CAP-04) and disclosure band.
- Enter: 150ms fade/rise (8px). Exit: 100ms fade. No bounces, no per-word
  karaoke — this is a wealth brand, not a hype channel.
- Line breaks are pre-authored in the storyboard strings (max 2 lines / 42
  chars); render them as given.
- **Timing flow (flag, already recorded in both YAML headers):** the caption
  track flows continuously across scene cuts where the script's marker
  windows under-allocate reading time at CPS<=17 — HOOK text runs to 8.2s,
  STAKES text to 20.3s, TURN text starts 69.7s, CTA text starts 79.4s. Scene
  *backgrounds* cut exactly on the markers (0/5/15/35/55/75/85s); captions
  ride over the cuts (an L-cut, in type). Build backgrounds and captions as
  independent tracks so this is trivial.

## Scene-by-scene

**SC-01 · HOOK · 0–5s · navy field.** `--brand-navy` field with a barely
visible paper-grain vignette. CAP-01/02/03 as full-frame serif cards; gold
hairline underlines "as a single check." line (styling, not new words). Hard
cuts between caption cards on their timing beats. No disclosure yet.

**SC-02 · STAKES · 5–15s · dark navy.** Field deepens to `--brand-navy-dark`
on the 5s cut. CAP-04 sets as a stacked roll-call (Manrope caps, equal
weight per line). CAP-05 must follow it immediately at full contrast — the
"if you're in DROP" conditional is the compliance scoping of the address
(CL-16); never let it read as skippable fine print. CAP-06 ("The rule is
hard.") gets a lone, centered, oversized beat. Disclosure band enters at
exactly 5.0s and persists to 90.0s (see below).

**SC-03 · BEAT ONE · 15–35s · the envelope.** The piece's one drawn motion
graphic: flat vector envelope in gold line-work drifts down and lands on a
paper-tone table plane (landing ~17s, after the cut settles). Then a quiet
split: a steady pulsing line animates on by itself (the pension, "turns on
by itself") while a second shape holds motionless (the lump sum, "waits").
Abstract geometry only — no dollar signs, no numerals, no labels; the mapped
captions carry all meaning. Captions sit in the upper-center zone here so the
graphic owns the middle third. Track re-syncs to the scene grid by ~35s.

**SC-04 · BEAT TWO · 35–55s · the stack.** Neutral cream/warm blocks stack
one atop another as CAP-14/15 run — income stacking as pure shape. On CAP-16
(the 20%-withholding sentence, ledger CL-08) the top block shears away in
gold. No percentage figure is ever drawn; the fact exists only as the
verbatim words of CAP-16. Motion slow and weighted; captions center-stage
over a calmed zone.

**SC-05 · BEAT THREE · 55–75s · the route.** One unbroken gold line travels
left-to-right between two navy vessels — trustee to trustee. Nothing leaks
from the line (the "nothing withheld" visual), but do not add any invented
account labels, institution marks, or figures. CAP-20 ("The timing becomes
yours.") is ledger-qualified (CL-11: deferral, not unlimited control) — style
it quiet and matter-of-fact, no triumphant flourish. From ~69.7s the TURN
captions begin over this scene's tail; keep the backdrop calm there.

**SC-06 · TURN · 75–85s · the inversion.** The single pattern interrupt:
palette inverts to `--paper` field with navy type — the only light-field
moment in the piece. CAP-24 and CAP-25 land as two separate full-frame beats;
gold accent on the word "runway." only (emphasis is an editorial act — V8
judges it; keep it to color, no scale games). CTA captions begin at 79.4s
over this scene's tail.

**SC-07 · CTA · 85–90s · end-card.** Warm paper continues. Benowitz wordmark
treatment set in Cormorant from tokens (there is NO logo asset in the
manifest — typography only, don't source one). CAP-27's register ask holds
center; CAP-28 (the consult-a-tax-professional sentence — spoken script text,
the DISC-BEN-TAX-01 rider riding in the CTA) sets smaller and quieter, above
the disclosure band, clearly a different register from the ask. CAP-28 ends
exactly at 90.0s.

## Disclosure block (DISC-BEN-FRS-01)

- Text exactly: `Educational only. Not advice. Not affiliated with FRS. Full
  disclosures in profile.` — the short-format fallback; the
  full-disclosure-in-profile condition is a recorded publish rider (CL-15).
- Persistent 5.0s → 90.0s without interruption, across all backdrop changes.
- Pinned in the lower `hf-safe` region (above the 320px bottom margin),
  >= 26px at 1080-wide, Manrope, `--muted`-toned on navy scenes / navy-ink on
  paper scenes, contrast >= 4.5:1 — use the scrim token over the SC-06/07
  paper field if needed. Wrap as two stacked lines ("Educational only. Not
  advice. Not affiliated with FRS." / "Full disclosures in profile.") —
  whitespace-collapse canonicalization keeps byte-match intact (wrapper §1).
- Nothing may ever occlude it — captions live above its band by layout.

## Pacing summary

5 / 10 / 20 / 20 / 20 / 10 / 5 — a symmetric arc: fast hook, hard stakes,
three long teaching beats, sharp turn, clean ask. Backgrounds cut on the
marker grid; type flows at reading pace (~15–16 CPS design, 17 hard cap).
Transitions: hard cuts except the gold-rule wipe into SC-02, the match-cut
into SC-03 (gold rule becomes the envelope edge), and the navy→paper
inversion into SC-06.
