# RUB-VIDEO-BUILD-1 — video build-quality rubric, V4–V7, both engines identically (PROTECTED)

Authored at step 8 from the ratified Phase 6 §5 registry line ("build-note
honesty, deviation handling, manifest completeness(R), reuse discipline")
following the RUB-SCRIPT-1 pattern. Applied identically to HYPF and REMO
builds so the engines stay comparable (Phase 2 evaluation criteria; SK-B17's
matrix feeds on this evidence).
⚑ RATIFICATION RIDES ON THE STEP-8 PR — flagged for Wes.

## Required criteria (pass/fail, blocking)

- **R1 Manifest completeness** — render manifest schema-valid with every
  composition source, input, and the output hashed; engine version equals the
  ratified pin (validator-fed: render_manifest.py + schema_validate).
- **R2 Text verbatim** — text_verbatim_check 100% (validator-fed; a build
  with a paraphrase does not reach judgment).
- **R3 Preview-before-render** — a preview artifact exists and VDIR's V5
  verdict is recorded BEFORE the final render's timestamp (envelope-fed).
- **R4 Local render** — cloud_render false; no external render surface
  touched (D-070).

## Scored dimensions (1–5; anchors at 1/3/5)

**Build-note honesty** · 5: implemented/untested/not-implemented split is
explicit; every yellow explained; untested paths named as untested · 3:
accurate but thin — what happened is there, what wasn't run is implicit ·
1: claims health from a successful build rather than an inspected output.

**Deviation handling** · 5: zero-or-escalated, and each escalation carries
the math (readability, timing) that lets VDIR decide · 3: deviations
surfaced but under-argued · 1: a silent fix — text, timing, or hold length
adjusted in-composition (this usually also fails R2 and is the counterexample
class: "storyboard card too long for its 2.5s hold" must go BACK, not stretch).

**Reuse discipline** · 5: existing sub-compositions/components checked first
and named in the build note; new reusables proposed to the library ·
3: reuse happened where obvious, no proposals filed · 1: everything built
from scratch beside an existing equivalent, or dependency sprawl.

**Diagnosis efficiency** · 5: lint/render failures diagnosed at root cause
within the two-cycle budget, fix documented · 3: fixed within budget, cause
fuzzy · 1: symptom-patched, or budget exceeded without escalating (E5).

## Scorecard

`schemas/scorecard.schema.json` instance; composite normalized /10;
a required-criterion failure is never averaged into a passing composite.
