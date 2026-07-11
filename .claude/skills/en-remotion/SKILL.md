---
name: en-remotion
description: "Our constraint layer for Remotion builds (the second engine, D-006): typed-props content/presentation separation as the text-verbatim mechanism, the same safe-area and disclosure rules as SK-C1, pinned versions, and the same lint → preview → render → QC loop — authored in-house against docs verified at build time. Pinned at the video-production build stage (V4–V6) when VDIR's routing (SK-B17) selects Remotion."
skill_id: SK-C2
version: 1.0.0
tier: C
owner: wes
approval_status: draft            # activates with step 9
upstream_pin: 2e8037fec3cad711a8becf1252ed3af61f09a1fa   # remotion-dev/remotion tag v4.0.487 (DEC-BUILD-008)
engine_version: 4.0.487           # npm pin, exact-saved in video/remotion/package.json
supported_agents: [REMO]
required_inputs: ["storyboard (schema-valid)", "brand tokens", "platform export spec"]
optional_inputs: [existing_components_to_reuse, prior_render_manifests]
prerequisites: ["remotion@4.0.487 installed exact in video/remotion/ (DEC-BUILD-008; license: free tier, <=3 employees attested)", "assets manifest resolved (no GAPs unless the work order accepts placeholders)"]
requires: [SK-B16, SK-C3]
reads: ["projects/<active>/visual identity / brand tokens (via storyboard handoff)", "runs/<id>/storyboard/**"]
schemas: [storyboard, render-manifest]
evaluation_rubric: RUB-VIDEO-BUILD-1
---

# en-remotion (SK-C2)

## Purpose

Bind Remotion as the second engine with the SAME gates, validators, and rubric
as SK-C1 (Phase 5 §5: "nothing else differs"), so routing decisions accumulate
comparable evidence. Doc surfaces verified at build (D-062, 2026-07-11):
composition registration (`<Composition id/durationInFrames/fps/width/height>`
in Root, `registerRoot`), frame model (`useCurrentFrame`), and render-time
props (`npx remotion render <id> <out> --props=./props.json`; input props
override defaultProps).

## The text-verbatim mechanism (props injection)

Remotion compositions are code, so verbatim-ness is enforced at the data
boundary, per the REMO card: **props are populated from the storyboard file,
not retyped.**

1. `scripts/gen_props.py` generates `props.json` from storyboard.yaml +
   captions.yaml — the ONLY source of rendered text.
2. `scripts/props_verbatim_check.py` byte-matches props.json against the
   storyboard (same canonical form as SK-C1).
3. Compositions render text exclusively from props; every text-bearing JSX
   element carries `data-text-id={t.id}` and sits inside `<SafeArea>`.
4. `scripts/tsx_static_check.py` enforces (3) statically: no literal visible
   text in JSX, data-text-id containment in SafeArea, exact safe-area token
   values for the aspect ratio (same px table as SK-C1 wrapper-rules §2).

## Process

1. Verify storyboard hash against the parent lock (D5); read brand tokens
   (`tokens.js` custom values — same DERIVED set and ratification status as
   SK-C1 wrapper-rules §4).
2. Build/extend under `video/remotion/<project>/<piece>/` as parameterized,
   reusable components with typed props; content/presentation separated.
3. gen_props → props_verbatim_check → tsx_static_check (all green before any
   preview).
4. Preview before render (`remotion studio` or a draft render); VDIR reviews
   (V5).
5. Local render at spec with `--props=./props.json`; version outputs (never
   overwrite an approved render); write the RM-* manifest via
   `scripts/render_manifest.py` (refuses any engine version != 4.0.487).
6. Production notes + build note (zero-or-escalated deviations); hand to
   QA/validators via ORCH.

## Prohibited behavior

Text or timing deviations beyond storyboard tolerance (escalate to VDIR);
literal text in JSX (the check blocks it — fix the props flow, never the
words); render-without-preview; skipping QC; marking anything final;
unvetted dependencies (additions are proposals — DEC-BUILD-008 covers exactly
remotion + @remotion/cli at 4.0.487); version bumps at run time.

## Error handling

Render errors: two diagnosis cycles then escalate (E5-adjacent). Doc-vs-
behavior drift at the pin: halt, file a platform-churn observation.
**Standing licensing watch:** hiring person #4 at Joy Financial Group LLC
triggers a Remotion licensing review before the next Remotion render
(DEC-BUILD-008; the Automators tier is the plausible bracket for this
pipeline at 4+ headcount).
