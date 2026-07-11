# RUB-MKTG-1 — campaign rubric, `assembly_review` + child QA (PROTECTED)

Authored at step 10 from the ratified Phase 6 §5 registry line ("§17.3:
strategic alignment, audience insight, message consistency(R across children,
validator-fed), offer clarity, claim support(R), funnel continuity,
compliance(R), testability, measurement readiness(R), business relevance")
following the RUB-SCRIPT-1 pattern.
⚑ RATIFICATION RIDES ON THE STEP-10 PR — flagged for Wes.

## Required criteria (pass/fail, blocking)

- **R1 Message consistency across children** — the brief's locked offer
  string appears verbatim in every child; no child contradicts the campaign
  message (validator-fed: assembly_check offer + a QA read of each child
  against `brief.message`).
- **R2 Claim support** — every supported ad claim ⊆ landing claims by
  claim-key/canonical-text set comparison (validator-fed: assembly_check).
- **R3 Compliance** — every child individually passed COMPL at its own trunk
  gate AND campaign-level disclosure coverage is complete (assembly_check).
- **R4 Measurement readiness** — measurement plan complete: metrics tied to
  the conversion event, review date set, experiment (if any) pre-registered
  with SK-B13 guardrails (schema-fed).

## Scored dimensions (1–5; anchors at 1/3/5)

**Strategic alignment** · 5: every child visibly serves the brief's one
objective; nothing rides along "since we're posting anyway" · 3: aligned
with one passenger deliverable · 1: a content batch wearing a campaign name.

**Audience insight** · 5: the campaign meets the named person at the named
moment (the brief's audience_ref is visible in every hook) · 3: right
audience, interchangeable moment · 1: broadcast at everybody.

**Offer clarity** · 5: one offer, plainly stated, honorable exactly as
written; a reader can say what they get and what it costs (nothing) in one
sentence · 3: clear but buried below the fold in some children · 1: the
children imply different offers (this usually also fails R1).

**Funnel continuity** · 5: each child hands to the next step without a seam —
the ad's promise is the landing's headline; the landing's ask is the
conversion event · 3: continuous but with register shifts · 1: a click
lands somewhere that feels like a different company.

**Testability** · 5: the plan can distinguish outcomes — arms isolated,
windows defined, sample floors respected · 3: measurable but only
directionally · 1: no way to know if it worked (or success criteria written
after launch — an SK-B13 prohibited behavior surfacing here).

**Business relevance** · 5: the conversion event traces to the practice's
actual intake path; stop criteria protect Wes's time and spend · 3:
plausible value, soft tracing · 1: vanity metrics.

## Scorecard

`schemas/scorecard.schema.json` instance; composite /10; a required-criterion
failure is never averaged into a passing composite.
