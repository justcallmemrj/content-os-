# Upstream map — which vendored skill covers what (SK-C1)

A *map*, not a copy: our wrapper text never restates upstream content, so a
ratified pin bump doesn't orphan our rules. All paths are under
`.claude/skills/en-hyperframes/vendor/`, pinned at `6152437d` (v0.7.49).

| Need | Vendored skill | Notes |
|---|---|---|
| Composition contract (structure, data attributes, clips, tracks, sub-compositions, variables, deterministic render rules) | `hyperframes-core` | The binding contract for every build |
| Umbrella authoring guidance (timing, media, production workflow) | `hyperframes` | Entry point; routes to the others |
| Animation (atomic motion rules, blueprints, transitions, runtime adapters) | `hyperframes-animation` | GSAP default; single paused timeline, seek-safe |
| Keyframe specifics | `hyperframes-keyframes` | |
| CLI dev loop (init / lint / preview / render / doctor) | `hyperframes-cli` | Always invoked as `npx hyperframes@0.7.49` |
| Creative direction (palettes, typography, beat planning, design spec) | `hyperframes-creative` | Our brand tokens (wrapper-rules §4) override its palette advice |
| Media preprocessing (TTS, BGM, transcription, background removal) | `media-use` | External-service providers OFF by default — any use is a proposal (E6/D-070 posture) |
| Registry blocks/components (`hyperframes add`) | `hyperframes-registry` | Installs are dependency additions → proposals, never mid-run |

## Excluded at the pin (not vendored — see vendor/VENDOR.md)

`embedded-captions`, `faceless-explainer`, `figma`, `general-video`,
`motion-graphics`, `music-to-video`, `pr-to-video`, `product-launch-video`,
`remotion-to-hyperframes`, `slideshow`, `talking-head-recut`,
`website-to-video` — end-to-end workflow routers. Our video machine
(Phase 5 §5) is the workflow layer; importing third-party end-to-end
instructions would layer an ungoverned workflow over our gates (D6 posture).
A storyboard that needs one enters it by proposal at this same pin.
