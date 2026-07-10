---
name: wr-social-copy
description: "Social-format drafting for WRITE: captions, carousels, LinkedIn posts, on-image copy, hashtag policy — the format canon migrated from the retired benowitz-ducat-social skill (D-038). Pinned at the social profile's draft stage."
skill_id: SK-B4
version: 1.0.0
tier: B
owner: wes
approval_status: draft          # activates with step 7
supported_agents: [WRITE]
required_inputs: [work_order, "source packet or attached pre-checked asset", context_packet]
optional_inputs: [calendar_ref, approved_exemplars]
prerequisites: ["SK-A1 loaded exactly one project", "SK-B2 declare mode available"]
requires: [SK-B2, SK-A2, SK-B15]
reads: ["projects/<active>/brand-voice.md (register)", "projects/<active>/audience.md", "projects/<active>/disclosures.md"]
schemas: [work-order, claim-ledger]
evaluation_rubric: RUB-SOCIAL-1
---

# wr-social-copy (SK-B4)

## Formats (canon, migrated verbatim-in-substance per D-038)

**Carousel (Instagram/LinkedIn):** Slide 1 is the hook and carries the entire
weight. Slides 2–7 are ONE idea each, under 25 words. Final slide is CTA +
disclosure. Deliver as `**Slide N:**` followed by exact copy — this goes to a
designer, not an interpreter. Every on-image string is a ledger claim with
`on_screen: true` (D-016 applies to statics).

**Static post / caption:** hook line, line break, 3–5 short lines, CTA,
disclosure. Front-load: assume the reader sees two lines before "more."

**LinkedIn:** a different audience, not a different length — the client's
professional neighbors (benefits coordinators, union reps, HR, CPAs; for
Ducat: agents, attorneys, business managers). Write to the professional beside
the client. 150–300 words, real paragraphs, no staccato one-liners. Open with
a specific person in a specific situation, then widen. CTA is *forward this /
weigh in* — never book-a-call. Link goes in the FIRST COMMENT and the post
says so; full disclosure in the first comment, stated in-post (SK-B15).

**Hashtags:** per the brand's hashtag policy in voice/platform notes; never a
substitute for the disclosure.

## Process

Brief (or ratified calendar row AS the brief) → claims declared via SK-B2
while drafting → disclosures via SK-B15 (final slide / caption / first-comment
pattern) → run `scripts/social_format_check.py <file> --format
carousel|caption|linkedin` → hooks in tens when asked → intervention notes,
uncapped.

## Prohibited behavior

Everything WRITE's definition prohibits, plus: on-image text that isn't
ledger-mapped; "link in bio" on LinkedIn (means nothing there); a calendar
row's compliance touchpoints dropped on the way to copy; disclosure-free
"just a hook" pieces.

## Tests

`scripts/test_step7_skills.py`: format fixtures (compliant carousel passes;
8-idea slide fails; 40-word slide fails; LinkedIn under-band fails;
first-comment statement missing fails).
