---
name: vd-storyboarding
description: "Script-to-storyboard for VDIR: time-coded scene planning, b-roll mapping, motion-graphics planning, creative brief generation. Converts a LOCKED, human-approved script into a schema-valid storyboard — pacing for the platform, every visual mapped to the asset manifest or marked GAP (never invented), every on-screen text element ID-mapped verbatim (D-016). Pinned at the video machine's storyboard stage (V1→V2)."
skill_id: SK-B16
version: 1.0.0
tier: B
owner: wes
approval_status: draft            # activates with build step 8
supported_agents: [VDIR]
required_inputs: ["human-approved script + claim ledger (locked hash verified)", "asset manifest", "brand visual identity", "platform spec", "disclosure placement rules (SK-B15 outputs)"]
optional_inputs: [reference_videos_from_approved_examples, b_roll_library_index]
prerequisites: ["parent run at approved with text locked (T15 record)", "asset manifest generated"]
requires: [SK-C3]
reads: ["runs/<parent>/voice/** (locked script)", "runs/<parent>/factcheck/ledger.yaml", "projects/<active>/assets/manifest.yaml", "projects/<active>/disclosures.md"]
schemas: [storyboard]
evaluation_rubric: RUB-VIDEO-BUILD-1
---

# vd-storyboarding (SK-B16)

## Process

1. Verify the script hash against the parent's T15 lock (D5) — a mismatch is
   a halt, not a warning.
2. Honor the script's delivery markers: `[TO CAMERA]` → to-camera scene,
   `[VO / B-ROLL:]` → b-roll scene, `[TEXT ON SCREEN:]` → text card. The
   script's text is immutable; the storyboard arranges, never rewrites.
3. Time-code scenes to the platform spec; durations must sum to the target
   ± tolerance. Pace for the platform (hook placement, pattern interrupts,
   jump-cut restraint) — never cram pacing to hit duration; flag instead.
4. Map every visual to the asset manifest or mark it `GAP` with an
   acquisition suggestion — **never invent that an asset exists**; rights
   fields are mandatory (unknown = GAP-equivalent).
5. ID-map 100% of on-screen text: claims → `CL-*` (ledger), disclosures →
   `DISC-*`, caption segments → `CAP-*` carrying script text verbatim.
   A visual implying a claim the ledger can't support is an escalation.
6. Place the disclosure block persistent per SK-B15/SK-C1 wrapper rules.
7. Score the engine recommendation via SK-B17; record factors, rationale,
   close_call honestly (deciding first and scoring after is a failure mode).
8. Run `scripts/storyboard_check.py` (the V2 validator); emit the schema-valid
   storyboard + asset-gap list + visual creative brief.

## Prohibited behavior

Altering script text (D5 — changes re-enter at fact_check); writing
composition code or rendering; inventing assets or rights; approving its own
storyboard as final; on-screen text without a ledger/disclosure/caption ID.

## Error handling

Material asset gaps, matrix ambiguity, unsupported-claim visuals, missing
rights metadata → escalate to Wes via ORCH; one revision cycle per flag set
(E2); the storyboard returns to this stage on V2 failure with the validator
report attached.
