---
name: st-calendar-planning
description: "Content-pillar and calendar planning for STRAT: inventory-first (check the back catalog before inventing topics), a source column on every row, a compliance-touchpoints list closing every calendar. A calendar is planning, not writing — no disclosures, no hooks, no [VERIFY] flags on calendars."
skill_id: SK-B12
version: 1.0.0
tier: B
owner: wes
approval_status: draft          # activates with step 7
supported_agents: [STRAT]
required_inputs: [planning_horizon, project_context, inventory_index]
optional_inputs: [campaign_brief, seasonal_constraints, performance_reports]
prerequisites: ["SK-A1 loaded exactly one project"]
requires: [SK-A2]
reads: ["projects/<active>/assets/manifest.yaml (the inventory)", "projects/<active>/campaigns/", "projects/<active>/decisions/"]
schemas: [work-order]
evaluation_rubric: "inventory-first adherence (calendar 'New' ratio, Phase 2 STRAT card)"
---

# st-calendar-planning (SK-B12)

## The rules (migrated per D-038)

- **A calendar is not writing.** Nothing publishes from a calendar, so a
  calendar gets no disclosures, no hooks, no `[VERIFY]` flags. Those belong on
  the pieces, later.
- **Check inventory FIRST.** The back catalog (webinar scripts, the 30-post
  package, books, decks) is consulted before proposing anything new. A
  calendar that invents thirty topics on top of forty unpublished ones doesn't
  create content, it creates work.
- **Deliver a table:** week · theme · one row per post with channel + working
  title · a **source column** naming the asset each post is cut from. "New" is
  a valid source; a calendar that's mostly "New" is a bad calendar.
- **Fewer posts that get made beats more that don't.** A thin week stays thin.
- **End with compliance touchpoints:** which weeks land on tax content,
  career-ending content, or anything needing a careful hand at copy time.
  These flags MUST carry over to the work orders cut from the calendar (the
  social profile's brief-skip validator checks this).
- A ratified calendar row can BE the brief for a social run (`calendar_ref`
  on the work order, Phase 5 §3.2).

## Deterministic check

`scripts/calendar_check.py <calendar.md>` — every row has a source; a
compliance-touchpoints section exists; flags rows drafted as copy (hooks/
disclosures on a calendar are scope creep).

## Tests

`scripts/test_step7_skills.py`: compliant calendar passes; missing source
column fails; missing touchpoints section fails; calendar containing
disclosure text fails (planning ≠ writing).
