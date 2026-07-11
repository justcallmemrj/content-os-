---
name: vd-engine-routing
description: "The HyperFrames-vs-Remotion decision matrix for VDIR (D-006 HyperFrames-first roadmap): score the ratified factors, log the rationale, surface close calls honestly to the H3 override gate. Pinned at the video machine's engine_routing stage (V3)."
skill_id: SK-B17
version: 1.0.0
tier: B
owner: wes
approval_status: draft            # activates with build step 8
supported_agents: [VDIR]
required_inputs: ["storyboard (schema-valid)", "platform export spec", "reuse-library state (existing components/sub-compositions per engine)"]
optional_inputs: [porting_evaluation_notes_from_builders, prior_routing_records]
prerequisites: ["storyboard passed V2"]
requires: []
reads: ["video/hyperframes/** (reuse inventory)", "video/remotion/** (reuse inventory)"]
schemas: [storyboard]
evaluation_rubric: RUB-VIDEO-BUILD-1
---

# vd-engine-routing (SK-B17)

## The matrix

Score each factor 1–5 **per engine lane** before stating a verdict — deciding
first and scoring after is the named failure mode (Phase 2 §6.11).

| Factor | Favors HyperFrames | Favors Remotion |
|---|---|---|
| Variant structure | one-off piece | data-driven/typed-prop variants, batch personalization |
| Composition type | captioned talking-head package, lower thirds, one-off branded motion | complex programmatic sequencing, reusable typed component libraries |
| Reuse fit | existing HF sub-compositions cover it | existing Remotion components cover it |
| Licensing (D-070) | Apache-2.0, no company-size threshold | free ≤3-person for-profit; Company License at 4+ — **standing watch: hiring person #4** |
| Engine maturity here | first-engine path (D-006), evidence accumulating | Remotion-second roadmap; step-9 binding not yet built |
| Determinism/ops | local headless-Chrome + FFmpeg loop proven | node/npm build chain |

Also available as verdicts: **human/traditional** (exits the machine at V3
with storyboard + asset package; re-enters at V7 with the returned cut) and
**hybrid** (two build lanes V4–V7 per segment, merging at V8).

## Process

1. Score every factor with a one-line note; totals are advisory, the
   pattern is the argument.
2. Declare `close_call: true` whenever lanes are within one point overall or
   any single factor is decisive-but-contested — close calls route V3 through
   **H3 (Wes chooses)**; surfacing them as close is the requirement, not a
   weakness.
3. Record choice + factors + rationale + empty override field in the
   storyboard's engine_recommendation block. Human override is always
   available and always logged.
4. Until step 9 delivers SK-C2, a `remotion` verdict is an **escalation**,
   not a build: the lane exists in the matrix so routing evidence stays
   comparable (Phase 5 §5), but there is no bound builder yet.

## Prohibited behavior

Matrix rationalization (verdict before scores); hiding a close call;
routing to an engine whose binding doesn't exist without escalating;
modifying the matrix itself (that's a spec change — proposal to Wes).
