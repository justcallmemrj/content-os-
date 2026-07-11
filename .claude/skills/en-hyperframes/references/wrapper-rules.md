# Wrapper rules — what our layer adds/overrides on top of upstream (SK-C1)

## 1. Text-verbatim rule (D-016 / D5, mechanical form)

Every rendered text element carries `data-text-id="<ID>"` where `<ID>` is a
claim-ledger ID (`CL-*`), an approved disclosure ID (`DISC-*`), or a
caption-segment ID (`CAP-*`) declared in the storyboard. The element's text
must **byte-match** the storyboard string under the canonical form
`C(s) = NFC(html-unescape(s))` with internal whitespace runs collapsed to a
single space and trimmed (HTML whitespace semantics make raw-byte comparison
of markup meaningless; the canonical form is still fully deterministic).
`scripts/text_verbatim_check.py` enforces:

- every storyboard text ID present in the composition,
- no `data-text-id` in the composition that the storyboard doesn't declare,
- no visible text node outside a `data-text-id` element,
- 100% canonical byte-match.

A string that doesn't fit its card is a **flag to VDIR with the readability
math** — never a paraphrase, never a silent hold-extension.

## 2. Safe areas per aspect ratio (⚑ ASSUMPTION — margin values authored at
## step 8 from platform-UI conventions; ratification rides the step-8 PR)

Every text element sits inside a container with class `hf-safe`. The
composition's `tokens.css` must define these variables **exactly**:

| Aspect ratio | Canvas | `--safe-top` | `--safe-bottom` | `--safe-x` | Rationale |
|---|---|---|---|---|---|
| 9:16 | 1080x1920 | 220px | 320px | 64px | Reels/Shorts UI: username top, CTA/caption+nav bottom, like-rail right |
| 4:5 | 1080x1350 | 120px | 180px | 60px | Feed UI chrome |
| 1:1 | 1080x1080 | 60px | 60px | 60px | Minimal chrome |
| 16:9 | 1920x1080 | 54px | 54px | 96px | 5% title-safe |

`scripts/safe_area_check.py` enforces: exact variable values for the declared
AR, `hf-safe` containment for every `data-text-id` element, and no negative
inline offsets on text elements.

## 3. Persistent disclosure block (imported from SK-B15's placement rules)

- The disclosure rides **on-screen, never the spoken track** (SK-B15).
- Persistent for its declared scene range (for BEN reels: the full body+CTA
  range the storyboard declares; the H2 publish rider requires persistence —
  final call at H5).
- Inside the safe area; minimum rendered size 26px at 1080-wide canvas;
  contrast ≥ 4.5:1 against its backdrop (use the scrim token if the
  background is busy).
- Text verbatim from the `DISC-*` record — it is a `data-text-id` element
  like everything else and byte-match applies.

## 4. Brand tokens (⚑ DERIVED, not ratified — proposal filed; same class as
## the DUC tone-sliders precedent)

Benowitz visual identity has no ratified record in project memory yet. The
step-8 token set is derived from the owner-approved `benowitz-drop-exit`
webinar kit (46 final renders accepted 2026-07-10 — approved-by-use):

- Navy family: `#0E2A47` (primary), `#081A2D` (dark), `#1B3A5F` (soft), ink `#0B1E33`
- Gold family: `#C8A35C` (accent), `#DDC18A` (soft), `#A78443` (deep)
- Paper/warm neutrals: `#FBF7EE` (paper), `#F7F1E6` (warm), `#F1E9D7` (cream), muted `#7A6E55`
- Fonts: Cormorant (display serif), Manrope (UI sans), JetBrains Mono (numeric/mono)

Compositions consume these only via `tokens.css` custom properties
(`--brand-navy`, `--brand-gold`, `--paper`, …) — never hard-coded in
sub-compositions — so ratification or revision is a one-file change.
Until Wes merges the proposal these are placeholders-in-governance: flagged
here, in the build note, and at H5.

## 5. Pinned CLI

All CLI work uses `npx hyperframes@0.7.49` explicitly — the machine's floating
`npx hyperframes` resolves newer (0.7.51 observed at step 8) and MUST NOT be
used (D-036: the version that runs is the version Wes approved).

## 6. Versioning

Renders land at `video/hyperframes/<project>/<piece>/renders/v<N>/`; a new
render is always a new `v<N+1>` — an approved render is never overwritten.
