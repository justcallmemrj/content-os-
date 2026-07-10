---
name: ev-claim-ledger
description: "Claim-ledger discipline for content runs: declare mode (WRITE enumerates every claim while drafting), adjudicate mode (FACT extracts independently and assigns one of seven statuses against opened evidence), delta mode (VOICE emits a claim diff; FACT re-adjudicates only touched claims). Pinned at draft, fact_check, and voice_edit stages; use ad-hoc whenever handling text with verifiable claims."
skill_id: SK-B2
version: 1.0.0
tier: B
owner: wes
approval_status: draft            # activates with the vertical slice
supported_agents: [WRITE, FACT, VOICE]
read_only_reference: [VDIR, QA, COMPL]
required_inputs: [deliverable_path, "source packet and/or approved-fact set", ledger_schema, "mode: declare|adjudicate|delta"]
optional_inputs: [prior_ledger_versions, risk_threshold_overrides]
prerequisites: ["context packet loaded (SK-A1)", "packet exists OR work order authorizes approved-facts-only drafting"]
requires: [SK-A2]
reads: ["projects/<active>/approved-facts/", "projects/<active>/approved-facts/_claim-keys.yaml", "schemas/research-packet.schema.json"]
schemas: [claim-ledger]
evaluation_rubric: RUB-LEDGER-1
---

# ev-claim-ledger (SK-B2)

**Purpose:** one procedure, three seats — a factual claim carries one ID and one
auditable history from first draft to on-screen text (D-012, D3).

## Process

**declare (WRITE):** enumerate every claim while drafting — stated, implied,
numeric, visual, comparative (`references/claim-taxonomy.md`). Each gets a
CL-id, text, location, risk (`references/risk-classification.md`), and either
`evidence:` (a packet claim id or F-id) or `[UNVERIFIED]`. Before handoff, run
`scripts/extract_claims.py` on your own draft and reconcile every miss — the
script is your self-audit, not the boundary.

**adjudicate (FACT):** run extraction independently; merge with the declared
list, marking discoveries `declared_by: FOUND`. For each claim, open the cited
source and verify the *evidence*, not the citation. Assign exactly one of the
seven statuses (`references/status-protocol.md`) with qualification text where
needed. Write the blocking summary; `scripts/ledger_validate.py` recomputes it
and rejects drift.

**delta (VOICE → FACT):** VOICE runs `scripts/claim_diff.py` old-vs-new and
maps every flagged sentence to its CL-id with the nature of the touch. A
non-empty diff routes to FACT in delta mode, which re-adjudicates only the
touched claims (`references/delta-protocol.md`).

Project TRD evidence tags map on entry: `[ESTABLISHED]`→verified,
`[PLAUSIBLE]`→verified-with-qualification, `[SPECULATIVE]`→unverified.

## Prohibited behavior

- Assigning `verified` from model memory — `ledger_validate.py` rejects any
  verified status without an evidence ref, structurally.
- Softening `unverified` into hedged prose (D8): the status is categorical.
- FACT editing the deliverable (D4 — findings, never rewrites).
- VOICE suppressing a diff hit ("it's just cadence" is FACT's call, not VOICE's).
- Deleting a claim from the ledger — claims are withdrawn by status, never removed.

## Error handling

- Packet missing → declare mode proceeds with all material claims
  `[UNVERIFIED]` and the ⚠️ unsourced header before the content (verbatim
  convention, D-008); the header stays until claims check against the arrived
  source — *especially* if the copy looks finished.
- Extraction script failure → hard stop and escalate; never hand-count as a
  silent fallback (log any fallback).
- Cited URL dead in adjudicate → status `unverified` + RSRCH refresh proposal.

## Tests

`tests/test_sk_b2.py` — property: seeded 12-claim fixture, extraction recall
≥11/12, high-risk recall 12/12 (deterministic scripts, so stable across runs);
counterexample: planted wrong figure with plausible-blog sourcing must fail
validation on the verified-without-evidence path; delta fixture: 3 semantic
edits among 14 cosmetic — all 3 flagged, ≤1 false positive.
