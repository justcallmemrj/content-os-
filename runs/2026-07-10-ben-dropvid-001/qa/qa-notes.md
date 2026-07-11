# QA notes — 2026-07-10-ben-dropvid-001 — RUB-VIDEO-1 (V8 judgment QC)

QA, 2026-07-10. Target: `video/hyperframes/benowitz-wealth/drop-reel/renders/v1/drop-reel.mp4`
(sha256 e26f4e39…, manifest HF-2026-0710-01). First run of the video machine; these
notes are written knowing this piece is golden-baseline material — scores are held
to the anchors, not to the novelty of the lane.

Evidence base: RUB-VIDEO-1; storyboard.yaml + visual-brief.md (direction);
BUILD-NOTE.md + PRODUCTION-NOTES.md (build reality, deviations); handoffs 01–05
(gate history); V7 validator results (transition log seq 7, read not re-run, per
rubric); 12 full-res final-render frames read as images
(t2.5/8/20/30/42/48/60/70/78/83/87/89.5). Frames sample every scene and every
declared risk window (post-cut L-cut drift at t8 and t20, shear at t48, TURN
flow-over at t70 and t83, end-card at t87/t89.5).

## Required criteria (validator-fed at V7 — read, not re-derived)

| # | Criterion | Result |
|---|-----------|--------|
| R1 | Script alignment | pass — text_verbatim_check 29/29 IDs, 100% byte-match |
| R2 | Caption accuracy | pass — caption_check 28 segments clean; caption-concat == spoken script, proven twice (VDIR + ORCH independent) |
| R3 | Audio thresholds | **N/A-by-design recorded as pass per the rubric's R3 clause** — zero audio streams; silence is a DECLARED work-order condition (no VO exists, DEM-05 GAP, external TTS OFF); pointer: run work order + storyboard header + BUILD-NOTE "Not implemented" |
| R4 | Technical correctness | pass — 0 blank runs, full-decode 0 errors, 90.000s exact (2700 frames) |
| R5 | Platform specs | pass — 1080x1920, 30fps, 9:16 per instagram-reels spec |
| R6 | Rendering integrity | pass — output + composition hashes match manifest HF-2026-0710-01; engine at ratified pin 0.7.49; cloud_render false (D-070) |
| R7 | Safe areas & disclosure | pass — safe_area_check 0 violations; DISC-BEN-FRS-01 persistent 5.0–90.0s on scrim, measured 8.5–14:1 |

No required failure exists, so the composite is computed normally (D-030
discipline noted: had any of these failed, no composite would rescue it).

Frame corroboration (not re-derivation): t2.5 correctly shows NO disclosure
(declared range starts 5.0s); every frame t8→t89.5 shows the band, byte-identical
text, two-line wrap, inside the bottom safe region. Sampled caption text matches
the storyboard strings verbatim in all 12 frames.

## Scored dimensions (1–5 against RUB-VIDEO-1 anchors)

### Story clarity — 5
The piece is silent-by-design, so the 5-anchor's real test — "the argument lands
with the sound off" — is the entire piece, and it does. The sampled chain reads
as a complete argument with no narration: hook (t2.5 "single check" → t8 "never
hear it called a decision"), hard rule (t20 "must leave FRS-covered work"),
asymmetry (t30 "The lump sum doesn't." over the pension-pulse/still-square
split), tax mechanics (t42 ordinary income → t48 twenty-percent withheld, the
gold block shearing off the stack in sync), the alternative route (t60
trustee-to-trustee vessels), the reframe (t70 "not the real question", t78
"That's not a deadline."), and the ask (t83 webinar). Visuals reinforce and never
assert beyond the mapped words (no numerals, no invented labels — confirmed in
frames). The L-cut caption drift (see Pacing) briefly puts stakes text over the
envelope backdrop but never breaks the argument thread, because the captions are
sequential and self-carrying. Delivery order builds; nothing depends on audio.

### Pacing — 4
Reading load is genuinely respected: every sampled card is comfortably readable
in its window (CPS ≤17 validated; ~15–16 by design), the hook snaps through
three cards in 8.2s, CAP-06-style full-frame beats breathe, and the single
pattern interrupt (navy→paper inversion) lands exactly at the 75s attention-sag
point (t78). What keeps it from 5: the recorded pacing flag is real on screen —
the caption track runs up to ~5.6s behind the scene grid, so at t20 STAKES text
("You must leave FRS-covered work…") plays over BEAT ONE's envelope graphic, a
transient semantic desync a sound-off viewer can notice; and the tail spends its
final ~3s holding on the compliance rider (t87 = t89.5, static) after the
register ask has exited — the piece ends on its quietest beat. This is the
correct resolution of a CPS impossibility without touching locked text (D5), and
it was flagged, not hidden — but judged against the anchor it reads as "even,
competent" with one stretch (the tail) slightly flat: 4.

### Visual quality — 4
Across all 12 frames the type, spacing, and composition read as designed:
consistent scale system (sentence cards / 84px full-frame beats / quiet 33px
rider at t87), generous negative space, precise centering, disciplined accent
budget (one gold accent per beat — underline at t2.5, shear block at t48,
arrival dot at t70). The motion graphics are clean flat vector work in brand
line-weight. Two things hold it at 4: the VDIR-logged transient envelope/caption
overlap at 15.4–17.0s (not visible at my sampled t20, but recorded by the
reviewer who saw those frames — an accidental-looking instant in an otherwise
deliberate piece), and the end-card (t87/t89.5), which with the adjudicated
wordmark omission is a lone hairline + rider + disclosure — honest, but visibly
sparser than "designed" and the thinnest composition in the piece.

### Brand consistency — 3
This is the anchor-3 description almost verbatim: "on-palette with drift in
weight/spacing." The derived token palette (navy/gold/paper) is applied with
total internal consistency in every frame, and the treatments (hairline rules,
line-work envelope, scrim band) are coherent with the Benowitz webinar-kit
lineage. But: (a) the brand faces are NOT in the render — Cormorant/Manrope fell
back to Palatino Linotype/Georgia + Segoe UI (documented; visible in frames —
the serif reads Palatino, the band/rider read Segoe), which is a visible seam
against the approved back catalog; (b) no wordmark or brand name appears
anywhere in the 90s (SC-07 omission adjudicated at V5, riding to H5) — the piece
cannot self-identify; (c) the tokens themselves are derived, not ratified
(wrapper-rules §4 flag). None of this is a craft failure by HYPF — it is the
declared placeholder reality — but the dimension judges the rendered artifact
against the brand, and the rendered artifact drifts. 3, with a clear upgrade
path (install fonts via ratified proposal + ID-mapped wordmark string →
re-render would plausibly re-score 5).

### Caption placement judgment — 4
Placement discipline is excellent: captions never touch the disclosure band in
any frame (layout separation held even in the busiest frame, t48, and in the
double-text-register end-card t87 where CAP-28 sits clearly above the band as a
distinct element); the caption stage moves per scene exactly as directed
(upper-center in HOOK, upper zone over the envelope, center over calmed zones);
the captions that cross the 75s inversion swap to ink correctly (t78, t83).
Emphasis styling clarifies without editorializing: the gold underline on "as a
single check." adds no words; CAP-20/CAP-24 render plain and matter-of-fact as
the ledger qualification demanded (t78). Held at 4 by the same SC-03 transient:
during 15.4–17.0s the descending envelope's path intrudes on the caption zone
(VDIR: readability preserved, polish note) — for that window the caption and
graphic briefly fight the frame — and by rhythm that is systematic (fixed
150ms/100ms fades) rather than delivery-shaped, which is appropriate for this
brand but mechanical by anchor.

### Audio quality, judgment half — 5
The 5-anchor explicitly includes "silence is deliberate," and this is the rare
piece where that clause is the whole story: silence is a declared work-order
condition (R3 N/A-by-design), and the design commits to it rather than merely
tolerating it — type is treated as the delivery (oversized serif cards, beat
timing on reading pace), so nothing on screen implies missing sound. No
threshold half exists to contradict the ear. Scored on what the dimension can
see: the silent mix is coherent and intentional. (Whether a silent reel is the
right platform call for Instagram is an H5/platform judgment, recorded below as
an observation, not averaged into this dimension.)

### Motion quality — 4
Every documented motion is motivated by the words on screen: the envelope lands
on the marker beat; the pension line pulses ("turns on by itself") while the
lump-sum square holds still ("waits") — visible as a state difference between
t20 and t30; the stack builds under the income-stacking sentences and the gold
top block shears exactly on CAP-16 (caught mid-shear at t48 — the single best
frame in the piece); the route line draws trustee-to-trustee (t60 mid-draw, t70
complete with arrival dot) and calms to 35% under the TURN captions. Nothing
moves without a reason; determinism rules followed (finite repeats, no
clocks/random; seek-safe fromTo-at-clip-start). Held at 4: full-speed motion
feel (settle weight, pulse cadence, shear pacing) is verified only from static
frames and the low-res preview — VDIR logged the same medium-confidence residue
— and the one known motion-planning blemish is the envelope's descent path
crossing the caption zone (the SC-03 overlap). I am confident in the
choreography's correctness from frames + notes (this is not a low-confidence
score), but "nothing accidental" cannot be fully certified without full-speed
viewing, which H5 provides.

### Accessibility — 4
Contrast is verified, not assumed: validate reported 0 WCAG failures; the
disclosure band measures 8.5–14:1 across backdrops (frames confirm the ink
scrim under the band on both navy and paper fields); caption cream-on-navy and
ink-on-paper both read far above 4.5:1 in every sampled frame. Captions are
complete and verbatim (R2), which for a deaf viewer makes the piece 100%
accessible — nothing is audio-only. Disclosure holds ≥26px (27px built) with a
two-line wrap and never gets occluded. Held at 4 by the anchor-3 clause "minor
color-only accents": the "runway." emphasis is color-only (deep gold chosen for
≥3:1 large-text contrast — a considered choice, but still color as the only
channel), and at real device size the 27px band is at the legal-but-small end
of readable. No viewer-blocking failure exists; a clean 5 would want the
emphasis accents to carry a second channel (the SC-01 underline already does).

## Composite and verdict

Scores: 5, 4, 4, 3, 4, 5, 4, 4 → mean 4.125 → **composite 8.3 / 10**
(same mean×2 convention as the prior run's card). All required criteria pass;
no low-confidence exclusions (all eight scored at usable confidence; the
motion-feel residue is noted inside its score, and H5 covers full-speed
viewing). **Verdict: pass** — the render proceeds to manager_review /
human_review (H5 render sign-off), carrying its riders.

Nothing here re-litigates FACT/COMPL or VDIR's adjudications (wordmark,
disclosure tone): their reports were read as context per the chain of trust.

## Golden comparison

No video goldens exist — evaluations/goldens/ has no video-profile entries;
this is the video machine's first run, so no nearest-golden citation or delta
narrative is possible. This piece is video golden-candidate #1: if it clears
H5, QA proposes it via proposals/queue/ WITH ITS CONDITIONS ATTACHED — it is a
placeholder-slate, fallback-font, silent, derived-token golden. Future pieces
that have real footage, installed brand faces, or audio must NOT be regressed
against these conditions as if they were targets; the golden's value is the
caption system, disclosure band, safe-area discipline, and motion grammar.

## Observations (tagged for MEMC — separated from the verdict)

1. **MEMC/golden-conditioning:** golden-candidate #1 carries four explicit
   conditions (placeholder slate, system-font fallback, silent, derived
   tokens). Record them ON the golden if ratified, or the video lane's first
   baseline will quietly normalize placeholder craft as the target.
2. **MEMC/brand-gap (highest-leverage fix):** installing Cormorant/Manrope
   locally (ratified vendored-font proposal) + adding one ID-mapped wordmark
   string to the storyboard schema path are the two cheapest changes that
   would move brand consistency 3→5 with zero locked-text impact; the piece
   currently contains no brand identification anywhere in 90s.
3. **MEMC/storyboard-pattern:** the L-cut caption flow rescued a CPS
   impossibility, but the root cause is upstream — marker windows were timed
   for speech, not reading. For future silent/caption-led pieces, the script
   stage should budget spoken-word counts per beat against CPS≤17 at the
   beat's own duration (a structure_check-style validator could catch this at
   T-stage instead of V2), so caption and backdrop stay in semantic sync.
4. **MEMC/end-card-pattern:** with one-segment-at-a-time captions, placing
   the compliance rider (CAP-28) last means the final held frame is compliance
   text, not the ask — the register CTA is off-screen for the last ~3s
   (t87/t89.5). Future CTA storyboards should either persist the ask as a
   second register (like the disclosure band pattern) or order the rider
   before the ask.
5. **MEMC/polish + platform (H5 items, restated):** SC-03 envelope drift
   start ≥16.2s in any rebuild clears the caption-zone overlap (VDIR's own
   number); and silent-by-design on Instagram Reels is a distribution risk
   (platform auto-plays with sound expectation) — H5 owns that call; if BGM
   is ever added it re-enters the machine as a new render, R3 goes live, and
   this scorecard's audio dimension does not transfer.
