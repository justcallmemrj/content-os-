---
name: sys-context-loading
description: "Loader companion for ORCH: resolve the request to exactly one project (confidence >= 0.8 or ask the human), run scripts/load_context.py to assemble the packet, and cite the packet manifest in everything downstream. Pinned at intake and context_loaded stages; no content work starts before the manifest exists."
skill_id: SK-A1
version: 1.0.0
tier: A
owner: wes
approval_status: draft
supported_agents: [ORCH]
required_inputs: [request_text, task_id]
optional_inputs: [cross_project_authorization]
prerequisites: ["work order written at runs/<id>/workorder.yaml"]
requires: []
reads: ["project registry (schemas + Phase 3 §4.1 codes)", "projects/<resolved>/project-profile.md"]
schemas: [work-order]
evaluation_rubric: "intake-audit sample (Phase 6 §7 task-routing accuracy)"
---

# sys-context-loading (SK-A1)

## Process

1. **Resolve the project.** Brand/topic vocabulary usually decides it (DROP,
   FRS, Special Risk → BEN; NIL, contracts, signing bonus → DUC; backtest,
   drawdown → TRD). Confidence < 0.8 → ask the human ONCE; never guess and
   never write for two brands unless the work order carries a `cross_project`
   block (Phase 3 §3.4).
2. Write the work order (schema-valid) and run
   `python scripts/load_context.py --run <run-id>`.
3. The loader refuses on: missing work order, missing/ambiguous/unknown
   project_id, namespace violations. **A refusal is escalated, not retried
   with a guess** — the loader has no guess mode and neither do you.
4. Cite `runs/<id>/packet-manifest.yaml` in the first handoff; work not
   traceable to a manifest is invalid (constitution).

## Prohibited behavior

Loading a second project without the authorization block; proceeding past a
namespace violation; hand-assembling context that bypasses the loader.

## Tests

`scripts/load_context.py` behavior is covered by the step-2 fixtures (missing
work order refused; blank project refused; valid order assembles + manifest).
`scripts/test_skills.py` re-runs the refusal cases under this Skill's id.
