---
name: st-experiments
description: "Experiment design and analytics interpretation for STRAT and ANLYT, with the Phase 6 §7 sample-size guardrails baked in: n ≥ 20 per arm, effects must persist across ≥2 non-overlapping windows, every comparison ships the confound checklist, causal verbs only for pre-registered designed experiments, and insufficient-data is a complete answer. Used at campaign measurement planning (C1) and performance review (C8), and for any 'did X work' question."
skill_id: SK-B13
version: 1.0.0
tier: B
owner: wes
approval_status: draft            # activates with build step 10
supported_agents: [STRAT, ANLYT]
required_inputs: ["the question or hypothesis", "the data (SQLite evals/costs, platform metrics as provided by Wes)"]
optional_inputs: [prior_hypothesis_log_entries]
prerequisites: []
requires: []
reads: ["evaluations/hypothesis-log.md (when present)", "state/workflow.sqlite (read-only)"]
schemas: [campaign]
evaluation_rubric: RUB-MKTG-1
---

# st-experiments (SK-B13)

## Designing (STRAT side)

1. Pre-register or it isn't an experiment: hypothesis, arms, `min_n_per_arm`
   (≥ 20 — the schema enforces the floor), and success criteria written
   BEFORE launch, in the campaign brief's experiment block.
2. One variable per experiment; arms differ in exactly the thing the
   hypothesis names.
3. Success criteria are decision rules ("arm A ≥ 30% more registrations
   across both windows"), not aspirations.

## Interpreting (ANLYT side — Phase 6 §7 verbatim)

1. **n ≥ 20 per comparison arm** for any format/hook/topic claim.
2. Effect must **persist across ≥ 2 non-overlapping windows** — one good week
   is an anecdote.
3. Every comparison ships the **confound checklist**: topic mix, posting
   time, platform changes, audience shifts — each marked checked or
   uncontrolled. An uncontrolled confound doesn't kill the observation; it
   caps the language.
4. **Causal verbs are reserved** for pre-registered designed experiments.
   Everything else: "associated with", "observed alongside".
5. Under threshold → report **insufficient-data**. That is a complete
   answer, not a failure — padding it with a hunch is the failure.
6. Performance-sourced lessons enter the log at `observed` regardless of
   effect size; **replication, not magnitude, promotes them.**

## Prohibited behavior

Retro-fitting success criteria; causal language on observational data;
dropping the confound checklist "because it's obvious"; treating
insufficient-data as pressure to lower thresholds (threshold changes are
proposals with evidence, Phase 6 §7).
