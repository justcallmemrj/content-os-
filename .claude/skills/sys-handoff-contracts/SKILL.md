---
name: sys-handoff-contracts
description: "Structured handoff creation for every transition: envelope with artifact paths + sha256 checksums (never inline content), skills_used pins, concerns, confidence-with-basis; plus the change-log and intervention-note conventions. Every agent uses this at every handoff; scripts/new_envelope.py generates and validates the envelope."
skill_id: SK-A2
version: 1.0.0
tier: A
owner: wes
approval_status: draft
supported_agents: [ORCH, RSRCH, FACT, COMPL, QA, MEMC, ANLYT, STRAT, WRITE, VOICE, VDIR, REMO, HYPF]
required_inputs: [run_id, stage_from_to, artifact_paths]
optional_inputs: [concerns, escalation_refs, feedback_ref]
prerequisites: ["artifacts written to disk before the envelope references them"]
requires: []
reads: ["schemas/handoff-envelope.schema.json", "schemas/work-order.schema.json"]
schemas: [handoff-envelope, work-order]
evaluation_rubric: "envelope schema pass rate + downstream bounce rate (Phase 6 §7)"
---

# sys-handoff-contracts (SK-A2)

## Process

1. Finish the artifact ON DISK first — the deliverable file is the truth (D1);
   the envelope carries paths, checksums, and metadata, never a paraphrase
   standing in for content.
2. Generate: `python .claude/skills/sys-handoff-contracts/scripts/new_envelope.py
   --run <id> --seq N --from-stage X --to-stage Y --from-agent A --to-agent B
   --artifact <path> --skill SK-XX@V --confidence high:"basis"`.
   Invalid envelopes don't get written — fix the inputs, not the schema.
3. `skills_used` lists every pinned Skill actually loaded, with versions —
   the gate validator checks this (D-034); an empty list at a pinned stage is
   a blocked transition.
4. **Change log** (WRITE/VOICE revisions): findings addressed point-by-point;
   every departure from the literal request is an **intervention note**, one
   line each, uncapped — truncating the list means the human approves a change
   they never saw (D-008).
5. Concerns you hold but can't resolve ride in `concerns:`; material
   disagreements become E3 memos referenced in `escalations:` — never silence.

## Prohibited behavior

Inlining deliverable content into the envelope; referencing artifacts not yet
on disk; version without checksum ("both or neither"); dropping a concern to
keep a handoff clean.

## Tests

`scripts/test_skills.py`: generated envelope validates; envelope with a
missing artifact file fails loudly; inline-content field rejected by schema
(additionalProperties, proven in the step-1 fixtures).
