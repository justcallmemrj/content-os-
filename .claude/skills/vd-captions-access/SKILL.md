---
name: vd-captions-access
description: "Caption generation (content side), caption QC (the judgment half), and accessibility judgment — shared by VDIR (planning), HYPF/REMO (implementation), and QA (V8 judgment). Caption text is script text: segments carry CAP-* IDs and byte-match applies (D-016). The deterministic half (CPS, line length, timing) is scripts/caption_check.py, run at V7."
skill_id: SK-C3
version: 1.0.0
tier: C
owner: wes
approval_status: draft            # activates with build step 8
supported_agents: [VDIR, HYPF, REMO, QA]
required_inputs: ["locked script with delivery markers", "storyboard scene timings", "platform spec"]
optional_inputs: [prior_caption_tracks]
prerequisites: ["storyboard passed V2 (caption segments ID-mapped)"]
requires: []
reads: ["runs/<parent>/voice/** (locked script)", "runs/<id>/storyboard/**"]
schemas: [storyboard]
evaluation_rubric: RUB-VIDEO-1
---

# vd-captions-access (SK-C3)

## Content rules

1. Caption segments are **verbatim script text**, segmented for reading —
   segmentation may split sentences at natural clause boundaries; it may
   never rewrite, compress, or "tighten" (that's a paraphrase → escalate).
2. Each segment gets a `CAP-NN` ID in the storyboard; the composition
   consumes segments from the storyboard file (SK-C1 rule 3).
3. Segment at meaning boundaries; keep a spoken phrase and its caption
   on-screen together (sync tolerance ±0.25s against the delivery timing).

## Deterministic limits (scripts/caption_check.py, the V7 caption validator)

⚑ ASSUMPTION — thresholds authored at step 8 from broadcast/platform norms;
ratification rides the step-8 PR:

- CPS (chars/sec, whitespace included) ≤ 17
- ≤ 2 lines per segment; ≤ 42 chars per line
- on-screen ≥ 0.8s and ≤ 7s per segment
- no overlapping segments; no segment outside the video duration

## Judgment half (V8, QA with VDIR input)

Placement never occludes the disclosure block or platform UI (safe areas are
V7-deterministic; *aesthetic* placement is judged here); reading rhythm
matches delivery pace; emphasis styling never distorts meaning (an
all-caps or color-pop word is an editorial act — judge it).

## Accessibility judgment

Contrast ≥ 4.5:1 against real backdrop (scrim if busy); no information
carried by color alone; motion on caption text stays subtle (readability
beats spectacle); disclosure block readable at target device size.

## Prohibited behavior

Rewriting script text for caption fit (escalate with the readability math);
dropping segments to fix pacing; caption text without a CAP-* ID; treating
the deterministic limits as style advice — they gate V7.
