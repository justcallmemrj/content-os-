---
name: st-campaign-briefs
description: "Campaign brief creation for STRAT (Phase 5 §4): objective, audience, message, offer (verbatim-locked), conversion event, measurement plan, stop criteria — the seven fields H1 judges. Nothing spawns before Wes approves the brief. Pinned at the campaign machine's strategy_brief stage (C1→C2)."
skill_id: SK-B10
version: 1.0.0
tier: B
owner: wes
approval_status: draft            # activates with build step 10
supported_agents: [STRAT]
required_inputs: ["campaign request (objective sketch)", "context packet (audience.md, offers in project memory, back-catalog inventory)"]
optional_inputs: [prior_campaign_outcomes, ANLYT_baselines]
prerequisites: ["SK-A1 loaded exactly one project"]
requires: [SK-B11, SK-B12]
reads: ["projects/<active>/audience.md", "projects/<active>/campaigns/", "projects/<active>/decisions/"]
schemas: [campaign]
evaluation_rubric: RUB-MKTG-1
---

# st-campaign-briefs (SK-B10)

## Process

1. One campaign, one **message** — the sentence every deliverable must agree
   with. If the request contains two messages, that's two campaigns
   (escalate the split, don't blend).
2. **Offer language is written once and locked verbatim** (`offer.verbatim:
   true`) — the assembly gate compares the exact string across every child.
   Offer design itself is SK-B11's procedure.
3. **Conversion event** is one observable action, not a sentiment.
4. **Measurement plan**: metrics tied to the conversion event; a review date;
   an experiment block ONLY if arms are pre-registered with SK-B13's
   guardrails (n ≥ 20/arm, success criteria written before launch).
5. **Stop criteria are concrete** — a date, a count, a spend ceiling. A
   campaign without reachable stop criteria never closes (the schema blocks
   an empty list; this rule blocks a vacuous one like "when it feels done").
6. Emit the schema-valid campaign record; ORCH presents at H1. **Nothing
   spawns before H1** — no child work orders, no drafts, no research runs.

## Prohibited behavior

Spawning or drafting anything pre-H1; offers that promise outcomes
(compliance envelope binds campaign copy too); measurement plans without a
review date; stop criteria that can't be evaluated mechanically; writing
deliverable content (a brief is planning — SK-B12's calendar rule applies).
