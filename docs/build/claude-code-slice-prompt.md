# Vertical Slice Prompt — Milestone 1 (Steps 0–6)

The master prompt is in effect; this narrows scope. **Deliver the vertical slice and nothing beyond it**: one Benowitz 90-second reel script traveling the full content trunk — intake → context load → research → draft → fact-check → voice → delta → compliance → QA → manager review → Wes's approval — with the enforcement layer live underneath it and the acceptance tests proving the system fails safely, not just succeeds politely.

## Scope

Build sequence steps 0–6 only (package §4). Explicitly out of scope: social profile, adaptation runs, the video machine, both engines, campaigns, analytics, reports beyond the build log. If a task tempts you toward "while I'm here" work on those, it's out of scope — note it in LOG.md and move on.

## The slice deliverable

Live run: *"Turn the DROP chapter material into a 90-second Benowitz reel script"* — using a real source asset Wes provides, through every trunk gate, ending at H2 with the full package (script, claim ledger, compliance report, scorecard, interventions, change history).

## What Wes provides (ask for these at the start of step 3, not before)

1. Back-catalog source material for seeding: the DROP/FRS book chapter(s) or webinar deck to draft from, plus whatever else he wants in the first facts PR.
2. 10–20 approved pieces per brand (Benowitz and Ducat) for voice exemplars — Ducat's are seeded now even though its workflows activate later, because the contamination fixtures need a real second brand to contaminate *from*.
3. About an hour for the first H6 staging-PR review, and his H2 decision on the live run.
4. Confirmation of the GitHub repo URL and that branch protection is on.

## Step-by-step exit criteria (condensed from package §4; evidence required at each)

- **Step 0 [WES]** — environment report + doc re-verification note (subagents, hooks, memory, Skills surfaces; HyperFrames pin *recorded but not built against*; Remotion license check deferred to step 9 and noted as such). Stop for acknowledgment.
- **Step 1 [WES]** — tree scaffolded; all slice-relevant JSON Schemas (work order, envelope, packet, ledger, proposal, fact, source, decision, lesson, scorecard) validating fixtures; CLAUDE.md constitution ≤200 lines presented for review; auto memory disabled and *demonstrated* disabled.
- **Step 2 [WES watches the demo]** — HK1–HK9 registered; each hook has a deny fixture and an allow fixture, green; live demonstration: attempt to edit `projects/benowitz-wealth/compliance.md` → denied; attempt WRITE-agent web fetch → denied; loader refuses an ambiguous project; `transition.py` writes state, direct write blocked.
- **Step 3 [WES: inputs + first merge]** — four project profiles + `_shared/` envelope scaffolded; `benowitz-ducat-social` decomposition executed per the Phase 4 §8 table (original Skill retired with a decision record); seeded facts/disclosures/exemplars filed as **proposals**, staged, digest written; Wes merges the first PR; indexes regenerate on merge.
- **Step 4** — SK-B2 and SK-B3 implemented from their full Phase 4 §7 specs; SK-A1, SK-A2, SK-A3, SK-B1, SK-B9, SK-B14, SK-B15 authored to template; all property + counterexample tests green (including: the testimonial-request fixture produces refusal + compliant alternative; the missing-packet fixture produces the ⚠ header path).
- **Step 5** — 13 agent definition files live; slice agents' instruction-adherence fixtures green; `model:` pins per D-071.
- **Step 6 [WES: acceptance]** — fixtures authored (contamination, injected-failure, missing-source, minimal compliance seeds); the live run executed; then the acceptance battery.

## Acceptance battery (package §5 — all ten, evidence attached)

Run and document, in this order: (1) the clean live run through H2 · (2) the injected-failure request — *"make a reel about how this move could save teachers thousands"* — confirmed to arrive at Wes as a flagged intervention with a compliant alternative, with the FACT and COMPL findings attached · (3) the delta path shown in ledger history · (4) the contamination fixture refused · (5) the missing-source path · (6) the crash-resume test (kill mid-`fact_check`, restart, verify checksums, complete) · (7) the protected-path denial log · (8) the H6 PR flow (already exercised at step 3; cite it) · (9) the rollback rehearsal — activate one genuinely low-tier lesson (e.g., a Benowitz avoided-phrase addition Wes actually wants), then revert it, dependents green, drill timed · (10) golden #1 ratified from the approved run; Wes's edit distance recorded as the north-star baseline; secret-scan clean.

## Acceptance report format

One document, `docs/build/slice-acceptance.md`: a row per criterion — what was run, where the evidence lives (paths, SQLite queries, PR links, commit hashes), pass/fail, and any caveat in the required honesty phrasing ("implemented and tested" / "implemented, untested" / "not implemented"). End with open questions and the recommendation for step 7. Tag `v1.0-slice` only after Wes signs.

## Reminders that bite hardest in this milestone

The slice is accepted for *blocking well*, not just producing well — criteria 2, 4, 6, 7, and 9 are the point. Seeded content is proposals until merged (D-079). The Ducat exemplars exist to be contaminated *from*, not to activate Ducat. And if any test only passes because a hook was loosened or a fixture was softened, that is a failed test wearing a green badge — report it as the failure it is.
