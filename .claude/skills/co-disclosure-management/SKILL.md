---
name: co-disclosure-management
description: "Disclosure selection and placement per format: which DISC-* records a piece requires (standard / tax addendum / short-format fallback), where they live (video: persistent on-screen block, never spoken; LinkedIn: first comment, stated in-post; statics: closing slide), and verbatim-ness. Used by COMPL, WRITE, and VDIR wherever disclosures ride."
skill_id: SK-B15
version: 1.0.0
tier: B
owner: wes
approval_status: draft
supported_agents: [COMPL, WRITE, VDIR]
required_inputs: [deliverable_or_plan, project_id, format]
optional_inputs: ["context flags (tax, short-format)"]
prerequisites: []
requires: []
reads: ["projects/<active>/disclosures.md"]
schemas: []
evaluation_rubric: "disclosure-presence validator pass rate (R4 of RUB-SCRIPT-1)"
---

# co-disclosure-management (SK-B15)

## Selection

- Every published piece: the brand's standard record (e.g. DISC-BEN-FRS-01) —
  **verbatim, written out**, never "[add disclaimer here]".
- Content touching taxes: append the tax referral record.
- Genuinely space-constrained formats (Story frame, Reel cover): the SHORT
  fallback, AND the full text must live in the profile/first comment, AND the
  deliverable says so explicitly. Never ship with no disclosure "because it's
  just a hook."

## Placement (per format)

| Format | Placement |
|---|---|
| Video/reel | Persistent `[TEXT ON SCREEN:]` block, in-safe-area — never the spoken track |
| Carousel/static | Final slide + caption |
| LinkedIn | Full disclosure in the FIRST COMMENT; the post states it's there |
| Webinar | Read aloud early (a compliance moment, not a throwaway) + on-slide |

If the disclosure won't fit the format, **the format is wrong** — escalate;
the disclosure never shrinks (SK-B3 error-handling rule).

## Deterministic check

`python .claude/skills/co-disclosure-management/scripts/disclosure_check.py
<deliverable> --project <id> [--short-format] [--tax]`

## Prohibited behavior

Summarizing or paraphrasing disclosure text; moving it to the spoken track to
save screen space; skipping the tax line because the mention was brief.

## Tests

`scripts/test_skills.py`: correct-disclosure fixture passes; missing → fail;
summarized ("disclosures apply") → fail; tax content without referral → fail;
short-format with location statement → pass.
