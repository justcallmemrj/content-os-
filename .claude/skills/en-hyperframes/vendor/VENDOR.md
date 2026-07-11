# Vendored upstream: heygen-com/hyperframes skill set (D-036 / D-037)

**Pin:** commit `6152437d2a5c2c05e51b43d53f0f6cb6acdd9a79` = release tag **v0.7.49**
(verified live at vendoring, 2026-07-10: `git checkout 6152437d…` → "chore: release v0.7.49").
**License:** Apache-2.0 (LICENSE vendored alongside).
**Integrity:** every vendored directory byte-verified (`diff -r`) against the pinned
checkout at copy time — zero differences. `skills-manifest.json` is upstream's own
manifest at the pin, kept whole for reference.

## What is vendored (8 of 21)

The framework-knowledge set SK-C1's upstream-map cites — composition contract,
animation, media, CLI/render:

`hyperframes` · `hyperframes-core` · `hyperframes-animation` · `hyperframes-cli`
· `hyperframes-creative` · `hyperframes-keyframes` · `hyperframes-registry`
· `media-use`

## What is excluded, and why (ASSUMPTION — ratification rides the step-8 PR)

The 13 end-to-end **workflow** skills at the pin (`embedded-captions`,
`faceless-explainer`, `figma`, `general-video`, `motion-graphics`,
`music-to-video`, `pr-to-video`, `product-launch-video`,
`remotion-to-hyperframes`, `slideshow`, `talking-head-recut`,
`website-to-video`) are NOT vendored. Rationale: they are workflow routers —
our ratified video machine (Phase 5 §5, V1–V11) is the workflow layer here, and
importing third-party end-to-end instructions would layer an ungoverned
workflow over our gates (D6 posture). Only framework knowledge is wrapped.
If a later storyboard needs one, it enters by proposal at this same pin.

## Update policy (D-037)

Never live-fetched; never updated at run time. A pin bump is a proposal:
diff the new tag against this set, re-run SK-C1's fixtures (upstream-pin test),
review as third-party content (D6), then Wes ratifies via PR.
