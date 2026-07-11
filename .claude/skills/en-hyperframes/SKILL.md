---
name: en-hyperframes
description: "Our constraint layer over the official HyperFrames skills: brand tokens, safe areas, the disclosure-block pattern, ledger-verbatim text, and our lint → preview → render → QC loop — so HYPF builds with the vendor's current best practice AND our governance, without maintaining a fork of their knowledge. Pinned at the video-production build stage (V4–V6) when VDIR's routing (SK-B17) selects HyperFrames."
skill_id: SK-C1
version: 1.0.0
tier: C
owner: wes
approval_status: draft            # activates with the first video workflow (step 8)
upstream_pin: 6152437d2a5c2c05e51b43d53f0f6cb6acdd9a79   # heygen-com/hyperframes = v0.7.49 (D-036/D-037)
engine_version: 0.7.49            # the CLI version that runs is the version Wes approved
supported_agents: [HYPF]
required_inputs: ["storyboard (schema-valid: scenes, ID-mapped on-screen strings, asset refs with rights fields)", "brand tokens", "platform export spec"]
optional_inputs: [reusable_sub_compositions, prior_production_notes]
prerequisites: ["upstream skill set vendored at the pinned commit in vendor/ (byte-verified)", "assets manifest resolved (no GAPs unless the work order accepts placeholders)"]
requires: [SK-B16, SK-C3]
reads: ["projects/<active>/visual identity / brand tokens (via storyboard handoff)", "runs/<id>/storyboard/**"]
schemas: [storyboard, render-manifest]
evaluation_rubric: RUB-VIDEO-BUILD-1
---

# en-hyperframes (SK-C1)

## Purpose

Wrap — never fork — the vendored upstream HyperFrames skill set
(`vendor/`, pinned at `6152437d` = v0.7.49) with our governance: token
application, safe-area margins per aspect ratio, the persistent
disclosure-block spec, and the text-verbatim rule. HYPF builds with the
vendor's best practice plus our constraints.

## Process

1. Load the storyboard and brand tokens; verify the storyboard's
   `script_ref.sha256` equals the parent run's locked hash (D5).
2. Consult `references/upstream-map.md` for the composition pattern in play;
   read the mapped vendored skill(s) on demand — never a live fetch (D-036).
3. Build or extend under `video/hyperframes/<project>/<piece>/` with content
   values injected from the storyboard file, **never retyped**: every rendered
   text element carries `data-text-id` and its string is copied
   programmatically or verbatim from the storyboard.
4. Apply tokens and safe areas per `references/wrapper-rules.md`; place the
   disclosure block persistent and inside the safe area.
5. **Lint → preview** with the pinned CLI (`npx hyperframes@0.7.49 …`) — VDIR
   reviews the preview (V5) before any final render.
6. Local render with the approved preset (cloud render OFF, D-070).
7. Run the three scripts: `scripts/text_verbatim_check.py`,
   `scripts/safe_area_check.py`, `scripts/render_manifest.py`.
8. Write the manifest + production notes
   (`references/production-notes-template.md`); hand to QA/validators via ORCH.

## Deterministic checks

Upstream lint (`npx hyperframes@0.7.49 lint`); the three wrapper scripts;
export-spec validators (resolution / fps / duration / aspect ratio via the
render manifest + ffprobe).

## Prohibited behavior

- Deviating from storyboard text or timing beyond tolerance — **escalate to
  VDIR**, never silently adjust.
- Render-without-preview.
- Enabling cloud render or any MCP call (D-019/D-070 — off until the Phase 7
  config decision).
- Pulling upstream updates or new runtime adapters at run time (D-036).
- Overwriting an approved render — version, never replace.

## Error handling

Lint failures → fix or document exceptions in the build note, never suppress.
Render nondeterminism or 2-cycle unresolved errors → escalate (E5-adjacent).
Upstream behavior deviating from the pinned map → **halt** and file a
platform-churn observation; never live-update mid-run.
